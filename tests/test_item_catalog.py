import unittest

from data.items import completion_labels, resolve_item


class ItemCatalogTests(unittest.TestCase):
    def test_resolves_prefab_case_insensitively(self):
        item = resolve_item("arrowwood")
        self.assertIsNotNone(item)
        self.assertEqual(item.prefab, "ArrowWood")
        self.assertEqual(item.max_stack, 100)

    def test_resolves_human_readable_name(self):
        item = resolve_item("Bronze Sword")
        self.assertIsNotNone(item)
        self.assertEqual(item.prefab, "SwordBronze")
        self.assertEqual(item.max_quality, 4)

    def test_resolves_completion_label(self):
        label = "Megingjord — BeltStrength"
        item = resolve_item(label)
        self.assertIsNotNone(item)
        self.assertEqual(item.prefab, "BeltStrength")

    def test_unknown_or_modded_prefab_is_not_coerced(self):
        self.assertIsNone(resolve_item("MyModdedLegendaryHammer"))

    def test_completion_labels_are_search_friendly(self):
        labels = completion_labels()
        self.assertIn("Wood Arrow — ArrowWood", labels)
        self.assertIn("Bronze Sword — SwordBronze", labels)


if __name__ == "__main__":
    unittest.main()
