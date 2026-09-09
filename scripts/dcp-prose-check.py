#!/usr/bin/env python3
"""Bounded no-context prose checks for dcp-pre-push-hook.sh; no writes."""
from __future__ import annotations

import fnmatch
import json
import os
from pathlib import Path
import re
import subprocess
import sys


CONFIG = "Projects/Ora/Reference — Documentation-Code Parity Configuration.md"
MANIFEST = "Projects/Ora/Reference — Vault Ora Framework Pair Manifest.md"
SETUP = "Projects/Ora/Working — Ora Setup and Refinement.md"
OVERVIEW = "Projects/Ora/Registry — Ora Overview and Document Registry.md"
PROSE = {"README.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md",
         "SUPPORT.md", "GOVERNANCE.md"}
CONTROLS = {
    SETUP: (r"G1\.25 — .+",),
    OVERVIEW: (
        "How This Registry Stays Current",
        "Framework — Documentation-Code Parity.md",
        "Reference — Documentation-Code Parity Configuration.md",
        "Reference — Vault Ora Framework Pair Manifest.md",
    ),
}


def git(root: str, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", root, *args], check=True, capture_output=True,
        encoding="utf-8", timeout=20,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    ).stdout


def default_base(root: str, destination: str, head: str) -> str:
    if not destination:
        raise ValueError("Git's push destination is unavailable")
    advertised = git(root, "ls-remote", "--symref", "--exit-code", "--",
                     destination, "HEAD").splitlines()
    refs = [line.split("\t")[0][5:] for line in advertised
            if line.startswith("ref: ") and line.endswith("\tHEAD")]
    heads = [line.split("\t")[0] for line in advertised
             if re.fullmatch(r"[0-9a-f]{40}\tHEAD", line)]
    if len(refs) != 1 or not refs[0].startswith("refs/heads/") or len(heads) != 1:
        raise ValueError("destination has no unambiguous advertised default branch")
    for commit in (head, heads[0]):
        if git(root, "rev-parse", "--verify", f"{commit}^{{commit}}").strip() != commit:
            raise ValueError("destination ancestry is not available locally")
    bases = git(root, "merge-base", "--all", heads[0], head).splitlines()
    if len(bases) != 1:
        raise ValueError("destination ancestry has no unique merge-base")
    return bases[0]


def blob(root: str, revision: str, path: str) -> str | None:
    entry = git(root, "ls-tree", "-z", revision, "--", f":(literal){path}")
    if not entry:
        return None
    mode, kind, rest = entry.split(" ", 2)
    oid, name = rest.split("\t", 1)
    if mode != "100644" or kind != "blob" or name != path + "\0":
        raise ValueError(f"not a plain, nonexecutable prose file: {path}")
    return git(root, "cat-file", "blob", oid)


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate control-data key")
        result[key] = value
    return result


def control_json(content: str | None, name: str) -> dict:
    begin, end = f"<!-- BEGIN DCP {name} JSON -->", f"<!-- END DCP {name} JSON -->"
    if content is None or content.count(begin) != 1 or content.count(end) != 1:
        raise ValueError("required vault control data is absent or ambiguous")
    block = content.split(begin, 1)[1].split(end, 1)[0].strip()
    match = re.fullmatch(r"```json\s*\n(.*?)\n```", block, re.DOTALL)
    if not match:
        raise ValueError("invalid vault control-data block")
    result = json.loads(match[1], object_pairs_hook=unique_object)
    if not isinstance(result, dict):
        raise ValueError("invalid vault control-data object")
    return result


def protected_paths(root: str, revision: str) -> set[str]:
    """Use the existing registrations, including their pre-change versions."""
    registry = control_json(blob(root, revision, CONFIG), "DOCUMENTATION OWNERSHIP")
    if (registry["schema_version"] != 1
            or registry["registry_id"] != "ora/documentation-integrity-ownership@1"):
        raise ValueError("unsupported vault ownership registry")
    protected = {CONFIG, MANIFEST}
    for surface in registry["surfaces"]:
        protected.add(surface["canonical"]["path"])
        for owner in surface["owners"]:
            if owner["repository"] == "vault" and owner["pattern"] != "**":
                # These two existing mixed files have a section boundary below.
                if not (surface["surface_id"] == "dcp.coordinated-enforcement"
                        and owner["pattern"] in CONTROLS):
                    protected.add(owner["pattern"])
        propagation = surface["propagation"]
        if propagation.get("repository") == "vault":
            protected.add(propagation["path"])
        for reference in surface["references"]:
            if reference.get("repository") == "vault" and "path" in reference:
                protected.add(reference["path"])
    for sources in registry["discovery"].values():
        for source in sources:
            if source["repository"] == "vault":
                protected.add(source.get("glob") or source["path"])
    manifest = control_json(blob(root, revision, MANIFEST), "FRAMEWORK PAIR MANIFEST")
    for entry in manifest["entries"]:
        protected.add(entry["canonical_path"])
    return protected


def passive_metadata(content: str) -> bool:
    """Recognize plain Working metadata, never PED/workflow/runtime declarations."""
    if not content.startswith("---\n"):
        return True
    pieces = content.split("\n---", 1)
    if len(pieces) != 2:
        return False
    field = ""
    for line in pieces[0].splitlines()[1:]:
        if not line.strip():
            continue
        match = re.fullmatch(r"([a-z ]+):\s*(.*)", line)
        if match:
            field, value = match.groups()
            if field not in {"type", "tags", "nexus", "date created", "date modified"}:
                return False
            if field == "type" and value not in {"working", "registry"}:
                return False
            if field == "tags" and value:
                return False  # ambiguous/inline metadata uses coordinated review
        elif not (field in {"nexus", "tags"}
                  and re.fullmatch(r"  - [\w-]+", line)):
            return False
        if field == "tags" and line.strip().startswith("- "):
            if line.strip()[2:] not in {"working", "reference", "book", "plan",
                                        "specification", "registry", "overview", "navigation",
                                        "tracker", "ora-setup"}:
                return False
    return True


def control_sections(content: str, patterns: tuple[str, ...]) -> list[str]:
    # Same heading-level boundary used by the focused verifier. Requiring one
    # exact match also refuses deleting, renaming, or duplicating a control.
    headings = list(re.finditer(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", content, re.MULTILINE))
    sections = []
    for pattern in patterns:
        matches = [i for i, h in enumerate(headings) if re.fullmatch(pattern, h[2])]
        if len(matches) != 1:
            raise ValueError("missing or ambiguous mixed-document control section")
        index = matches[0]
        heading = headings[index]
        finish = next((h.start() for h in headings[index + 1:]
                       if len(h[1]) <= len(heading[1])), len(content))
        sections.append(content[heading.start():finish].rstrip())
    return sections


def prose(sentinel: str, repository: str, root: str, changed_file: str,
          *revisions: str) -> bool:
    paths = Path(changed_file).read_text(encoding="utf-8").splitlines()
    if not paths or paths[-1] != sentinel or len(revisions) % 2:
        raise ValueError("incomplete changed-path capture")
    paths = set(paths[:-1])
    for path in paths:
        if path in PROSE:
            continue
        if repository != "vault" or not (path in CONTROLS or re.fullmatch(
                r"Projects/[^/]+/Working — [^/\n\r]+\.md", path)):
            return False
    for base, head in zip(revisions[::2], revisions[1::2]):
        protected = set()
        if repository == "vault" and paths - PROSE:
            protected = protected_paths(root, base) | protected_paths(root, head)
        for path in paths:
            if any(fnmatch.fnmatchcase(path, pattern) for pattern in protected):
                return False
            before, after = blob(root, base, path), blob(root, head, path)
            if path in PROSE:
                continue
            if any(not passive_metadata(c) for c in (before, after) if c is not None):
                return False
            if path in CONTROLS:
                if before is None or after is None:
                    return False
                if control_sections(before, CONTROLS[path]) != control_sections(after, CONTROLS[path]):
                    return False
    return True


if __name__ == "__main__":
    try:
        if sys.argv[1] == "base":
            print(default_base(*sys.argv[2:]))
        elif not prose(*sys.argv[2:]):
            sys.exit(1)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(f"DCP prose classification unavailable: {error}", file=sys.stderr)
        sys.exit(1)
