import unittest

from ui.branding import (
    APP_NAME,
    APP_SUBTITLE,
    APP_AUTHOR,
    BANNER_RELATIVE_PATH,
    banner_path,
)


class BrandingTests(unittest.TestCase):
    def test_product_identity_is_wulfpack_forge(self):
        self.assertEqual(APP_NAME, "Wulfpack Forge")
        self.assertEqual(APP_SUBTITLE, "Character Editor for Valheim")
        self.assertEqual(APP_AUTHOR, "Frostwulf")

    def test_approved_banner_is_a_runtime_resource(self):
        self.assertEqual(BANNER_RELATIVE_PATH, "assets/wulfpack-forge-banner.jpg")
        path = banner_path()
        self.assertTrue(path.is_file())
        self.assertGreater(path.stat().st_size, 50_000)


if __name__ == "__main__":
    unittest.main()
