from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import workspace_paths as paths


class WorkspacePathTests(unittest.TestCase):
    def test_stage_shortcut_follows_selection_and_rejects_escaping_or_missing_folders(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ('first', 'second'):
                (root / name / 'mod/event').mkdir(parents=True)
            with mock.patch.object(paths.vdb, 'selected_source', return_value=root / 'first') as selected:
                self.assertEqual(paths.stage_folder(root, {}, 'main', 'event'), root / 'first/mod/event')
                selected.return_value = root / 'second'
                self.assertEqual(paths.stage_folder(root, {}, 'main', 'event'), root / 'second/mod/event')
                with self.assertRaises(ValueError):
                    paths.stage_folder(root, {}, 'main', '../outside')
                with self.assertRaisesRegex(ValueError, 'missing'):
                    paths.stage_folder(root, {}, 'main', 'absent')
                selected.return_value = None
                with self.assertRaisesRegex(ValueError, 'No verified'):
                    paths.stage_folder(root, {}, 'main', 'event')

    def test_stage_drift_is_not_hidden_by_opening_an_old_folder(self):
        with mock.patch.object(paths.vdb, 'selected_source', side_effect=ValueError('stage differs')):
            with self.assertRaisesRegex(ValueError, 'stage differs'):
                paths.stage_folder(Path.cwd(), {}, 'main', 'event')
