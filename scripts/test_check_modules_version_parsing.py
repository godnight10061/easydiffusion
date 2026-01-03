import importlib.util
import pathlib
import unittest


def _load_check_modules():
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    module_path = repo_root / "scripts" / "check_modules.py"

    spec = importlib.util.spec_from_file_location("check_modules", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec for {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestCheckModulesVersionParsing(unittest.TestCase):
    def test_parse_version_handles_prerelease_suffix(self):
        check_modules = _load_check_modules()

        v_rc = check_modules.parse_version("1.2.3rc1")
        v_final = check_modules.parse_version("1.2.3")

        self.assertLess(v_rc, v_final)
        self.assertNotEqual(v_rc, v_final)


if __name__ == "__main__":
    unittest.main()

