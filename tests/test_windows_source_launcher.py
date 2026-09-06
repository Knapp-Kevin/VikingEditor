import pathlib
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
LAUNCHER = REPO_ROOT / "run-wulfpack-forge.cmd"


class WindowsSourceLauncherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = LAUNCHER.read_text(encoding="utf-8")

    def test_launcher_is_present_and_uses_its_own_directory(self):
        self.assertTrue(LAUNCHER.is_file())
        self.assertIn('cd /d "%~dp0"', self.script)

    def test_launcher_uses_a_private_environment(self):
        self.assertIn('set "VENV_DIR=.wulfpack-forge-venv"', self.script)
        self.assertIn('"%VENV_PYTHON%" -m pip install', self.script)
        self.assertNotIn('python -m pip install -r "requirements.txt"', self.script)

    def test_launcher_installs_requirements_and_starts_the_app(self):
        self.assertIn('-r "requirements.txt"', self.script)
        self.assertIn('"%VENV_PYTHON%" "main.py" %*', self.script)

    def test_launcher_checks_supported_python_versions(self):
        for version in ("3.10", "3.11", "3.12", "3.13", "3.14"):
            self.assertIn(version, self.script)
        self.assertIn(":python_missing", self.script)


if __name__ == "__main__":
    unittest.main()
