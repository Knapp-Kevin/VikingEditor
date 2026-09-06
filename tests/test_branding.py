import unittest

from ui.branding import (
    APP_NAME,
    APP_SUBTITLE,
    APP_AUTHOR,
    BANNER_RELATIVE_PATH,
    MIN_BANNER_WIDTH,
    MIN_BANNER_HEIGHT,
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
        self.assertGreaterEqual(MIN_BANNER_WIDTH, 1000)
        self.assertGreaterEqual(MIN_BANNER_HEIGHT, 300)
        self.assertTrue(banner_path().is_file())
        self.assertTrue(banner_is_usable())


if __name__ == "__main__":
    unittest.main()
