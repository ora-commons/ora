"""The icon set must contain every icon the UI asks for by name.

The builder only scans ``config/toolbars`` and ``config/packs`` JSON, so an
icon referenced solely from JavaScript is silently tree-shaken out and its
button renders the fallback "?" glyph at runtime. That is exactly what happened
to all four Manage Projects lifecycle buttons — Pause, Archive, Reactivate and
Restore were visually identical question marks.

The runtime artifact is generated on startup and is not committed. These tests
seed a stale artifact in a temporary directory, exercise the real self-healing
builder, and inspect the rebuilt output. A normal test run therefore proves the
startup path without writing into the checkout.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from orchestrator import icon_set_builder as isb  # noqa: E402

_SIDEBAR_JS = Path(_REPO) / "server" / "static" / "js" / "sidebar.js"
_NODE_SHAKE = Path(_REPO) / "scripts" / "lucide-tree-shake.js"

class IconSetUiNamesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmpdir = tempfile.mkdtemp(prefix="ora-icon-set-")
        cls.runtime_path = Path(cls._tmpdir) / "icon-set.json"
        cls.stale = {
            "version": "stale-test-fixture",
            "generated_at": "2000-01-01T00:00:00Z",
            "source": "test fixture",
            "mode": "tree-shaken",
            "referenced_from": [],
            "referenced_names": [],
            "icon_count": 0,
            "icons": {},
        }
        cls.runtime_path.write_text(json.dumps(cls.stale), encoding="utf-8")
        with mock.patch.object(isb, "OUT_PATH", cls.runtime_path):
            cls.build_result = isb.rebuild_if_stale()
        cls.built = json.loads(cls.runtime_path.read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._tmpdir, ignore_errors=True)

    def test_declared_ui_icons_are_built(self):
        """Every icon declared for the UI survives the runtime build."""
        icons = self.built.get("icons") or {}
        missing = sorted(n for n in isb._UI_ICON_NAMES if n not in icons)
        self.assertEqual(
            missing, [],
            f"UI-referenced icons absent from the runtime set: {missing}. "
            "Every button using one renders the fallback glyph.",
        )

    def test_shipped_icon_set_is_not_stale(self):
        """A stale runtime artifact is detected and rebuilt in place."""
        self.assertTrue(self.build_result.get("rebuilt"), self.build_result)
        self.assertEqual(
            self.build_result.get("reason"), "referenced-names changed")
        self.assertNotEqual(self.built, self.stale)
        self.assertEqual(
            self.built.get("referenced_names"),
            sorted(set(self.built.get("icons") or {})
                   | set(self.build_result.get("unknown_names", []))
                   | set(self.build_result.get("missing_svgs", []))),
        )

    def test_every_icon_the_sidebar_requests_is_declared(self):
        """resolveProjectActionIcon('name') calls must be covered.

        Catches the failure at its source: adding a new lifecycle button
        without declaring its icon fails here rather than shipping a "?" box.
        """
        js = _SIDEBAR_JS.read_text(encoding="utf-8")
        requested = set(re.findall(r"resolveProjectActionIcon\(\s*'([a-z0-9-]+)'", js))
        self.assertTrue(requested, "expected to find icon requests in sidebar.js")
        undeclared = sorted(requested - set(isb._UI_ICON_NAMES))
        self.assertEqual(
            undeclared, [],
            f"sidebar.js requests {undeclared} but they are not in "
            "icon_set_builder._UI_ICON_NAMES, so the build will drop them.",
        )

    def test_node_and_python_builders_declare_the_same_names(self):
        """The Node script is the canonical manual rebuild path.

        If it disagrees, a manual `node lucide-tree-shake.js` silently
        reintroduces the missing-icon bug the Python builder just fixed.
        """
        js = _NODE_SHAKE.read_text(encoding="utf-8")
        m = re.search(r"var UI_ICON_NAMES = \[(.*?)\];", js, re.S)
        self.assertIsNotNone(m, "UI_ICON_NAMES not found in lucide-tree-shake.js")
        node_names = set(re.findall(r"'([a-z0-9-]+)'", m.group(1)))
        self.assertEqual(node_names, set(isb._UI_ICON_NAMES))

    def test_builder_reports_no_unknown_or_missing(self):
        """From the tempdir build in setUpClass — no second write anywhere."""
        self.assertEqual(self.build_result.get("unknown_names", []), [])
        self.assertEqual(self.build_result.get("missing_svgs", []), [])


if __name__ == "__main__":
    unittest.main()
