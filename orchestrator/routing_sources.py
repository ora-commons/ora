"""Compile the maintained Markdown routing source set, without runtime effects.

The existing process loader owns the lifetime of the returned records. This
module has no cache, model calls, environment defaults, or writes. Generated
catalogues are views of these records and are never read as routing authority.
"""
from __future__ import annotations

from pathlib import Path
import re

import yaml


class RoutingSourceError(ValueError):
    """An authored source or reference cannot be represented truthfully."""


class _SourceLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise RoutingSourceError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_SourceLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)

# These are mechanical bindings to existing detectors, not authored synonyms or
# destinations. A new condition must acquire a real consumer before admission.
PREDICATE_BINDINGS = frozenset({
    "enum_hypotheses", "enum_options", "enum_parties", "enum_frames",
    "enum_scenarios", "pasted_argument", "decision_with_options",
    "failure_description", "conflict_description", "spatial_description",
    "attached_image", "attached_document", "red_team_subject_missing",
    "mechanism_subject_missing", "passion_subject_missing",
})
ACTION_BINDINGS = frozenset({
    "ask-for-subject", "bypass", "direct-response", "keep-selection",
    "select-depth", "sequential-selection",
})
FALLBACK_BINDINGS = frozenset({"route-by-intent"})


def _yaml(text: str, source: str) -> dict:
    try:
        value = yaml.load(text, Loader=_SourceLoader)
    except yaml.YAMLError as exc:
        raise RoutingSourceError(f"{source}: invalid YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise RoutingSourceError(f"{source}: expected a YAML mapping")
    return value


def _sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## ([^\n]+)\n", text, re.M))
    return {match[1].upper(): text[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)].strip()
            for i, match in enumerate(matches)}


def _fences(text: str):
    return re.finditer(r"^```yaml\s*\n(.*?)^```\s*$", text, re.M | re.S)


def compile_routing_sources(ora_home: Path | str) -> dict:
    """Read and validate the entire public collection before returning records.

    ``ora_home`` is explicit: a worktree compiler never falls back to live data.
    Mode declarations, adjacent selection records, territory/cross-mode
    questions, lens metadata, and named molecular companions form the closure.
    """
    root = Path(ora_home).resolve()
    modes, lenses, companions, documents = {}, {}, {}, {}
    questions, territory_questions, cross_questions, defaults = {}, {}, {}, {}
    utility_territories = {}
    depth_signals = {}
    signals, deferred_signals, data_shapes, deferred_shapes, conflicts = [], [], {}, [], []
    sources = []
    declared_predicates, declared_actions, declared_fallbacks = set(), set(), set()

    def read(path: Path) -> str:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RoutingSourceError(f"cannot read routing source {path}: {exc}") from exc
        relative = path.relative_to(root).as_posix()
        if relative not in sources:
            sources.append(relative)
        return text

    def add_question(question: dict, source: str):
        if not isinstance(question, dict) or not isinstance(question.get("id"), str):
            raise RoutingSourceError(f"{source}: question requires a stable id")
        qid = question["id"]
        if qid in questions:
            raise RoutingSourceError(f"{source}: duplicate question {qid}")
        if not question.get("text") or "default" not in question:
            raise RoutingSourceError(f"{source}: {qid} needs text and explicit default")
        question = dict(question)
        question["source"] = source
        questions[qid] = question

    def global_records(record: dict, source: str):
        for question in record.get("routing_questions", []):
            add_question(question, source)
        for dest, key in ((territory_questions, "territory_questions"),
                          (cross_questions, "cross_territory_questions"),
                          (defaults, "territory_defaults")):
            for name, value in record.get(key, {}).items():
                if key == "cross_territory_questions":
                    name = "|".join(sorted(name.split("|")))
                if name in dest:
                    raise RoutingSourceError(f"{source}: duplicate {key} entry {name}")
                dest[name] = value
        declared_predicates.update(record.get("routing_predicates", []))
        declared_actions.update(record.get("routing_actions", []))
        declared_fallbacks.update(record.get("routing_fallbacks", []))
        deferred_signals.extend(record.get("deferred_signals", []))
        deferred_shapes.extend(record.get("deferred_data_shapes", []))
        conflicts.extend(record.get("routing_conflicts", []))
        utility_territories.update(record.get("routing_utility_territories", {}))
        depth_signals.update(record.get("routing_depth_cues", {}))

    for filename in ("territories", "within-territory-trees", "cross-territory-adjacency", "disambiguation-style-guide"):
        path = root / "architecture" / f"{filename}.md"
        text = read(path)
        documents[filename] = text
        for block in _fences(text):
            if re.search(r"^(?:routing_|territory_|cross_territory_|deferred_)[a-z_]+:", block[1], re.M):
                global_records(_yaml(block[1], str(path)), str(path))
    for filename in ("pre-routing-pipeline", "mode-template", "lens-library-specification"):
        documents[filename] = read(root / "architecture" / f"{filename}.md")
    territories = {match[1]: {"id": match[1], "name": match[2]}
                   for match in re.finditer(r"^### (T\d+)\. ([^\n]+)", documents["territories"], re.M)}
    # These utility destinations are declared by mode sources outside T1–T21.
    deferred = set(re.findall(r"^- `([^`]+)` — gap-deferred\.", documents["territories"], re.M))
    if not territories or not deferred:
        raise RoutingSourceError("territory source has no complete territory/deferred collection")
    if declared_predicates - PREDICATE_BINDINGS:
        raise RoutingSourceError(f"unbound predicates: {sorted(declared_predicates - PREDICATE_BINDINGS)}")
    if declared_actions - ACTION_BINDINGS or declared_fallbacks - FALLBACK_BINDINGS:
        raise RoutingSourceError("unbound routing action or fallback")

    for path in sorted((root / "modes").glob("*.md")):
        if path.name == "INDEX.md":
            continue
        text = read(path)
        blocks = list(_fences(text))
        if not blocks:
            raise RoutingSourceError(f"{path}: missing mode declaration")
        metadata = _yaml(blocks[0][1], str(path))
        mid = metadata.get("mode_id")
        if mid != path.stem or mid in modes:
            raise RoutingSourceError(f"{path}: mode identity differs from filename or is duplicated")
        selection = None
        for block in blocks[1:]:
            if re.search(r"^selection:", block[1], re.M):
                record = _yaml(block[1], str(path))
                if selection is not None:
                    raise RoutingSourceError(f"{path}: multiple selection authorities")
                selection = record["selection"]
                global_records(record, str(path))
        sections = _sections(text)
        description = sections.get("DISPLAY DESCRIPTION")
        if not isinstance(selection, dict) or not description:
            raise RoutingSourceError(f"{path}: mode needs display description and adjacent selection guidance")
        gear = re.search(r"\bGear\s+([1-4])\b", sections.get("DEFAULT GEAR", ""), re.I)
        if not gear:
            raise RoutingSourceError(f"{path}: no valid Default Gear")
        territory = metadata.get("territory")
        if not isinstance(territory, str):
            raise RoutingSourceError(f"{path}: missing territory")
        territory_id = territory.split("-")[0]
        if territory_id not in territories and territory not in {"T-bypass", "T0-default-judgment"}:
            raise RoutingSourceError(f"{path}: unknown territory {territory}")
        identity_aliases = list(dict.fromkeys([mid, mid.replace("-", " "), metadata["canonical_name"], metadata.get("educational_name", "")] + metadata.get("expert_aliases", []) + selection.get("aliases", [])))
        identity_aliases = [alias for alias in identity_aliases if alias]
        dependencies = metadata.get("lens_dependencies", {})
        lens_groups, lens_qualifications = {}, {}
        for group, entries in dependencies.items():
            if not isinstance(entries, list):
                raise RoutingSourceError(f"{mid}: malformed lens dependency group {group}")
            lens_groups[group] = []
            for entry in entries:
                lid = entry.get("lens_id") if isinstance(entry, dict) else entry
                if not isinstance(lid, str):
                    raise RoutingSourceError(f"{mid}: malformed lens reference")
                lens_groups[group].append(lid)
                if isinstance(entry, dict):
                    lens_qualifications[lid] = entry.get("qualification", "")
        lens_ids = list(dict.fromkeys(lens for group in lens_groups.values() for lens in group))
        record = {"metadata": metadata, "text": text, "sections": sections,
                  "default_gear": int(gear[1]), "description": description,
                  "educational_name": metadata.get("educational_name", metadata["canonical_name"]),
                  "input_contract": metadata.get("input_contract", {}),
                  "aliases": identity_aliases, "lenses": lens_ids,
                  "lens_dependencies": lens_groups, "lens_qualifications": lens_qualifications,
                  "selection": selection, "lighter_siblings": [], "path": str(path)}
        modes[mid] = record
        for alias in identity_aliases:
            signals.append({"signal": alias, "territory": territory, "mode": mid,
                            "disambiguation_answer": "—", "confidence_weight": "strong",
                            "evidence": "mode-name reference"})
        for signal in selection.get("signals", []):
            signals.append({**signal, "mode": mid})
        for phrase, canonical in selection.get("phrase_aliases", {}).items():
            canonical_records = [signal for signal in signals if signal["mode"] == mid and signal["signal"].casefold() == canonical.casefold()]
            if not canonical_records:
                raise RoutingSourceError(f"{mid}: phrase alias has no canonical signal {canonical!r}")
            for signal in canonical_records:
                signals.append({**signal, "signal": phrase, "canonical_phrase": canonical})
        for shape in selection.get("data_shapes", []):
            data_shapes.setdefault(shape["predicate"], []).append({**shape, "mode": mid})

    if not modes:
        raise RoutingSourceError("no mode collection")
    if set(modes) & deferred:
        raise RoutingSourceError("an active mode is also declared deferred")

    for path in sorted((root / "lenses").glob("*.md")):
        if path.name == "INDEX.md":
            continue
        text = read(path)
        frontmatter = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not frontmatter:
            raise RoutingSourceError(f"{path}: no lens declaration")
        metadata = _yaml(frontmatter[1], str(path))
        lid = metadata.get("lens_id")
        if lid != path.stem or lid in lenses:
            raise RoutingSourceError(f"{path}: lens identity differs from filename or is duplicated")
        # Older lens declarations include subject areas as well as actual mode
        # names. Keep every declared area, but never pretend it is a route.
        applicability = metadata.get("applicability", []) or []
        lenses[lid] = {"metadata": metadata, "text": text, "path": str(path),
                       "applicable_modes": [mid for mid in applicability if mid in modes],
                       "applicability_topics": [name for name in applicability if name not in modes]}

    def target(record, source):
        if record is None:
            return
        if not isinstance(record, dict) or set(record) - {"kind", "id"}:
            raise RoutingSourceError(f"{source}: malformed typed target {record!r}")
        kind, name = record.get("kind"), record.get("id")
        destinations = {"active": modes, "deferred": deferred, "territory": territories,
                        "fallback": declared_fallbacks, "action": declared_actions}
        if kind not in destinations or name not in destinations[kind]:
            raise RoutingSourceError(f"{source}: unresolved {kind} target {name!r}")

    def closure(value, source):
        if isinstance(value, list):
            for child in value:
                closure(child, source)
        elif isinstance(value, dict):
            for key, child in value.items():
                if key == "targets":
                    if not isinstance(child, list):
                        raise RoutingSourceError(f"{source}: targets must be a list")
                    for item in child:
                        target(item, source)
                elif key in {"target", "lighter_targets"}:
                    for item in (child if isinstance(child, list) else [child]):
                        target(item, source)
                elif key in {"predicate", "question_predicate"}:
                    if child not in declared_predicates:
                        raise RoutingSourceError(f"{source}: unbound operative condition {child!r}")
                elif key in {"mode_id", "target_mode_id"} and child is not None:
                    if child not in modes and child not in deferred:
                        raise RoutingSourceError(f"{source}: unbound mode reference {child!r}")
                elif key == "territory" and isinstance(child, str):
                    code = child.split("-")[0]
                    if code not in territories and child not in {"T-bypass", "T0-default-judgment"}:
                        raise RoutingSourceError(f"{source}: unbound territory reference {child!r}")
                closure(child, source)

    for mid, record in modes.items():
        metadata, selection = record["metadata"], record["selection"]
        closure(metadata, mid)
        closure(selection, mid)
        missing = set(record["lenses"]) - set(lenses)
        if missing:
            raise RoutingSourceError(f"{mid}: unresolved lens dependencies {sorted(missing)}")
        downward = metadata.get("escalation_signals", {}).get("downward", {})
        sibling = downward.get("target") if isinstance(downward, dict) else None
        if sibling and sibling["kind"] == "active":
            record["lighter_siblings"].append(sibling["id"])
        alternatives = record["input_contract"].get("graceful_degradation", {}).get("lighter_targets", [])
        for alternative in alternatives:
            if alternative["kind"] == "active" and alternative["id"] not in record["lighter_siblings"]:
                record["lighter_siblings"].append(alternative["id"])
        record["lighter_qualification"] = downward.get("when", "") if isinstance(downward, dict) else ""
        for lid in record["lenses"]:
            if mid not in lenses[lid]["applicable_modes"]:
                lenses[lid]["applicable_modes"].append(mid)
        molecular = metadata.get("molecular_spec")
        if molecular:
            companion = molecular.get("companion_source")
            if not isinstance(companion, str) or not re.fullmatch(r"frameworks/book/[a-z-]+\.md", companion):
                raise RoutingSourceError(f"{mid}: invalid molecular companion source")
            if companion not in companions:
                companions[companion] = read(root / companion)
            references = set()
            for component in molecular.get("components", []):
                if component["mode_id"] not in modes:
                    raise RoutingSourceError(f"{mid}: executable molecular component is not active")
                runs = component.get("runs")
                if runs not in {"full", "fragment"}:
                    raise RoutingSourceError(f"{mid}: component must specify full or fragment")
                if runs == "fragment" and not component.get("fragment_spec"):
                    raise RoutingSourceError(f"{mid}: fragment has no meaning")
                references.add(component.get("reference_id", component["mode_id"] + ("-fragment" if runs == "fragment" else "")))
            for stage in molecular.get("synthesis_stages", []):
                if not set(stage.get("input", [])) <= references:
                    raise RoutingSourceError(f"{mid}: unresolved molecular stage input {stage['name']}")
                if stage["name"] in references:
                    raise RoutingSourceError(f"{mid}: duplicate molecular stage name {stage['name']}")
                references.add(stage["name"])

    for qid, question in questions.items():
        closure(question, qid)
        for branch in [*question.get("answers", []), question["default"]]:
            if not isinstance(branch, dict) or not ("targets" in branch or "question" in branch):
                raise RoutingSourceError(f"{qid}: answer/default has no destination")
            if branch.get("question") and branch["question"] not in questions:
                raise RoutingSourceError(f"{qid}: unresolved next question {branch['question']}")
            if "territory_order" in branch:
                order = branch["territory_order"]
                if not isinstance(order, list) or len(set(order)) != len(order) or not set(order) <= set(territories):
                    raise RoutingSourceError(f"{qid}: invalid ordered territory selection")
        for branch in question.get("answers", []):
            if not isinstance(branch.get("phrases"), list) or not branch["phrases"]:
                raise RoutingSourceError(f"{qid}: answer has no authored phrase")
        for next_question in question.get("optional_questions", []):
            if next_question not in questions:
                raise RoutingSourceError(f"{qid}: unresolved optional question {next_question}")
        for territory in question.get("territories", []):
            if territory not in territories:
                raise RoutingSourceError(f"{qid}: unknown question territory {territory}")
    def question_closure(qid, visiting, done):
        if qid in visiting:
            raise RoutingSourceError(f"cyclic canonical question: {qid}")
        if qid in done:
            return
        record = questions[qid]
        edges = list(record.get("optional_questions", []))
        edges.extend(branch["question"] for branch in [*record.get("answers", []), record["default"]] if branch.get("question"))
        for edge in edges:
            question_closure(edge, visiting | {qid}, done)
        done.add(qid)
    visited_questions = set()
    for qid in questions:
        question_closure(qid, set(), visited_questions)
    for territory, qid in territory_questions.items():
        if territory not in territories or qid not in questions:
            raise RoutingSourceError(f"unresolved territory question {territory}/{qid}")
    for key, qid in cross_questions.items():
        if any(t not in territories for t in key.split("|")) or qid not in questions:
            raise RoutingSourceError(f"unresolved cross-territory question {key}/{qid}")
    for territory, destination in defaults.items():
        if territory not in territories:
            raise RoutingSourceError(f"unknown default territory {territory}")
        target(destination, territory)
    for mid, record in modes.items():
        qid = record["selection"].get("question")
        if qid and qid not in questions:
            raise RoutingSourceError(f"{mid}: unresolved selection question {qid}")
    for conflict in conflicts:
        if conflict.get("question") not in questions:
            raise RoutingSourceError("unresolved conflict question")

    signals.extend(deferred_signals)
    unique_signals, seen = [], set()
    for signal in signals:
        signal = dict(signal)
        signal.setdefault("disambiguation_answer", "—")
        signal.setdefault("evidence", signal.get("evidence_for_mapping", "authored selection guidance"))
        if signal.get("confidence_weight") not in {"strong", "weak"} or not signal.get("signal"):
            raise RoutingSourceError("signal requires an authored phrase and strong/weak weight")
        target({"kind": "active" if signal["mode"] in modes else "deferred", "id": signal["mode"]}, "signal")
        territory = signal.get("territory", "").split("-")[0]
        if territory not in territories and signal.get("territory") not in {"T-bypass", "T0-default-judgment"}:
            raise RoutingSourceError(f"signal has unknown territory {signal.get('territory')}")
        closure(signal, "signal")
        # Only wholly equivalent records coalesce. The same phrase pointing to
        # causal AND structural systems dynamics remains two valid destinations.
        key = tuple(sorted((name, repr(value.casefold() if name == "signal" else value)) for name, value in signal.items()))
        if key not in seen:
            unique_signals.append(signal)
            seen.add(key)
    for shape in deferred_shapes:
        target({"kind": "deferred", "id": shape["mode"]}, "data shape")
        data_shapes.setdefault(shape["predicate"], []).append(shape)
    for shape, records in data_shapes.items():
        if shape not in declared_predicates:
            raise RoutingSourceError(f"unbound data-shape predicate {shape}")
        records.sort(key=lambda record: (record.get("priority", 0), record["mode"]))
    return {"modes": modes, "lenses": lenses, "companions": companions,
            "signals": unique_signals, "questions": questions,
            "territories": territories, "deferred": deferred,
            "territory_metadata": {**{tid: {"name": record["name"], "order": int(tid[1:])} for tid, record in territories.items()},
                                   **utility_territories},
            "territory_questions": territory_questions,
            "cross_territory_questions": cross_questions, "defaults": defaults,
            "mode_selection": {mid: record["selection"] for mid, record in modes.items()},
            "data_shapes": {shape: [(record["mode"], record["territory"]) for record in records] for shape, records in data_shapes.items()},
            "data_shape_records": data_shapes, "conflicts": conflicts,
            "depth_signals": depth_signals,
            "predicates": declared_predicates, "actions": declared_actions,
            "sources": sources, "root": str(root)}


def render_routing_views(compiled: dict) -> dict[str, str]:
    """Return current body-only Markdown views; callers choose where to write.

    The returned mode registry body is the Vault catalogue. INDEX and signal
    registry bodies are mirrored through their existing canonical pairs.
    """
    modes, territories = compiled["modes"], compiled["territories"]
    note = ("Generated from mode-owned Display Description and Selection/Activation "
            "Guidance, with shared territory/question and lens declarations. Edit "
            "the owning source and regenerate; this view is not routing authority.\n\n")
    index = "# Modes — Index\n\n" + note
    registry = "# Registry — Mode Registry\n\n" + note
    registry += ("The complete library includes analytical modes and utility/bypass modes. "
                 "Input contracts, default Gear, analytical sections, lens declarations, and "
                 "molecular composition remain in each mode. The seven molecular companion "
                 "sources preserve their authored meaning; this catalogue makes no claim "
                 "that the compiler executes their composition.\n\n")
    order = sorted(territories, key=lambda name: int(name[1:])) + ["utility"]
    for territory in order:
        members = [(mid, record) for mid, record in modes.items()
                   if (record["metadata"]["territory"].split("-")[0] == territory if territory != "utility"
                       else record["metadata"]["territory"].split("-")[0] not in territories)]
        title = (territory + " — " + territories[territory]["name"]
                 if territory != "utility" else "Runtime utility / bypass modes")
        index += f"## {title}\n\n"
        registry += f"## {title}\n\n"
        for mid, record in members:
            index += f"- **`{mid}.md`** — {record['description']}\n"
            metadata = record["metadata"]
            registry += (f"- **`{mid}`** · {metadata['canonical_name']} · "
                         f"Gear {record['default_gear']} · {metadata.get('composition', 'atomic')} · "
                         f"{record['description']}\n")
        index += "\n"
        registry += "\n"
    registry += "## Deferred Candidates (CR-6)\n\n"
    for mid in sorted(compiled["deferred"]):
        registry += f"- `{mid}` — declared deferred in Analytical Territories; cannot execute.\n"
    registry += "\n## Lens-to-mode relationships\n\n"
    registry += ("Generated union of mode-owned dependencies and actual mode IDs in "
                 "lens-owned applicability. Application-area topics remain in the lens "
                 "declaration and are not executable modes.\n\n")
    registry += "| Lens | Applicable modes |\n|---|---|\n"
    for lid, lens in sorted(compiled["lenses"].items()):
        registry += f"| `{lid}` | " + ", ".join(f"`{mid}`" for mid in sorted(lens["applicable_modes"])) + " |\n"
    registry += ("\n## Source references\n\n- `Modes/<mode_id>.md` — identity, display and selection guidance, "
                 "input contract, Gear, analytical sections and molecular references.\n"
                 "- `Reference — Analytical Territories.md` — territory identity, boundaries, deferred candidates and finite bindings.\n"
                 "- `Reference — Within-Territory Disambiguation Trees.md` and `Reference — Cross-Territory Adjacency.md` — canonical questions, answers and defaults.\n"
                 "- `Reference — Pre-Routing Pipeline Architecture.md`, `Reference — Mode Specification Template.md`, "
                 "and `Reference — Lens Library Specification.md` — active source/consumer contracts.\n")
    signal_view = "# Registry — Signal Vocabulary Registry\n\n" + note
    for territory in order:
        title = territory if territory != "utility" else "Runtime utility / bypass modes"
        records = [signal for signal in compiled["signals"]
                   if (signal["territory"].split("-")[0] == territory if territory != "utility"
                       else signal["territory"].split("-")[0] not in territories)]
        signal_view += f"## {title}\n\n| signal | territory | mode | disambiguation_answer | confidence_weight | evidence_for_mapping |\n|---|---|---|---|---|---|\n"
        for signal in records:
            signal_view += "| " + " | ".join(str(signal.get(field, "—")).replace("|", "\\|") for field in ("signal", "territory", "mode", "disambiguation_answer", "confidence_weight", "evidence")) + " |\n"
        signal_view += "\n"
    runtime_index = ("# Modes Directory Index\n\n"
                     "*Generated from the compiled canonical routing sources — do not edit manually.*\n\n"
                     "| Mode | File | Default Gear | Trigger Summary |\n|---|---|---|---|\n")
    for mid, mode in sorted(modes.items()):
        runtime_index += "| " + " | ".join(str(value).replace("|", "\\|") for value in (
            mode["metadata"]["canonical_name"], mid + ".md",
            "Gear " + str(mode["default_gear"]), mode["description"])) + " |\n"
    return {"modes/INDEX.md": index,
            "config/modes-index.md": runtime_index,
            "architecture/signal-vocabulary-registry.md": signal_view.rstrip() + "\n",
            "mode_registry": registry}
