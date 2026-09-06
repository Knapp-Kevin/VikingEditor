import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ui.branding import (
    APP_NAME,
    APP_SUBTITLE,
    APP_AUTHOR,
    BANNER_RELATIVE_PATH,
    MIN_BANNER_BYTES,
    banner_is_usable,
    banner_path,
)


class BrandingTests(unittest.TestCase):
    def test_product_identity_is_wulfpack_forge(self):
        self.assertEqual(APP_NAME, "Wulfpack Forge")
        self.assertEqual(APP_SUBTITLE, "Character Editor for Valheim")
        self.assertEqual(APP_AUTHOR, "Frostwulf")

    def test_approved_banner_is_a_runtime_resource(self):
        self.assertEqual(BANNER_RELATIVE_PATH, "assets/wulfpack-forge-banner.jpg")
        self.assertGreaterEqual(MIN_BANNER_BYTES, 12_000)
        self.assertTrue(banner_path().is_file())
        self.assertGreaterEqual(banner_path().stat().st_size, MIN_BANNER_BYTES)
        self.assertTrue(banner_is_usable())

    def test_app_icon_resources_are_usable(self):
        from PySide6.QtGui import QImageReader
        from ui.branding import APP_ICO_RELATIVE_PATH, app_icon, app_icon_path, resource_path

        self.assertTrue(app_icon_path().is_file())
        ico = resource_path(APP_ICO_RELATIVE_PATH)
        self.assertTrue(ico.is_file())
        self.assertTrue(QImageReader(str(ico)).canRead())
        self.assertFalse(app_icon().isNull())

    def test_missing_app_icon_yields_null_icon_without_raising(self):
        from ui.branding import app_icon

        with TemporaryDirectory() as temp_dir:
            with patch("ui.branding.app_icon_path", return_value=Path(temp_dir) / "missing.png"):
                self.assertTrue(app_icon().isNull())

    def test_non_image_bytes_do_not_pass_runtime_asset_validation(self):
        with TemporaryDirectory() as temp_dir:
            invalid_banner = Path(temp_dir) / "banner.jpg"
            invalid_banner.write_bytes(b"not-a-jpeg" * 2_000)

            with patch("ui.branding.banner_path", return_value=invalid_banner):
                self.assertFalse(banner_is_usable())


if __name__ == "__main__":
    unittest.main()
