import unittest

from data.items import (
    CATALOG_GAME_VERSION,
    CATALOG_ITEM_COUNT,
    CATALOG_SELECTABLE_ITEM_COUNT,
    completion_labels,
    resolve_item,
)


class ItemCatalogTests(unittest.TestCase):
    def test_catalog_is_pinned_to_pre_1_0_valheim_snapshot(self):
        self.assertEqual(CATALOG_GAME_VERSION, "0.221.12")
        self.assertGreaterEqual(CATALOG_ITEM_COUNT, 1000)
        self.assertGreaterEqual(CATALOG_SELECTABLE_ITEM_COUNT, 900)

    def test_resolves_prefab_case_insensitively_and_keeps_curated_limits(self):
        item = resolve_item("arrowwood")
        self.assertIsNotNone(item)
        self.assertEqual(item.prefab, "ArrowWood")
        self.assertEqual(item.max_stack, 100)

    def test_resolves_unique_human_readable_name(self):
        item = resolve_item("Breastplate of Ask")
        self.assertIsNotNone(item)
        self.assertEqual(item.prefab, "ArmorAshlandsMediumChest")

    def test_ambiguous_human_readable_name_requires_prefab_disambiguation(self):
        self.assertIsNone(resolve_item("Bronze Sword"))
        item = resolve_item("Bronze Sword — SwordBronze")
        self.assertIsNotNone(item)
        self.assertEqual(item.prefab, "SwordBronze")
        self.assertEqual(item.max_quality, 4)

    def test_resolves_current_generated_item_metadata(self):
        item = resolve_item("Breastplate of Ask")
        self.assertIsNotNone(item)
        self.assertEqual(item.prefab, "ArmorAshlandsMediumChest")
        self.assertEqual(item.item_type, "Chest")
        self.assertTrue(item.asset_id)

    def test_resolves_completion_label(self):
        label = "Megingjord — BeltStrength"
        item = resolve_item(label)
        self.assertIsNotNone(item)
        self.assertEqual(item.prefab, "BeltStrength")

    def test_internal_objectdb_rows_do_not_pollute_player_completion_list(self):
        internal = resolve_item("Abomination_attack1")
        self.assertIsNotNone(internal)
        labels = completion_labels()
        self.assertFalse(any("Abomination_attack1" in label for label in labels))

    def test_unknown_or_modded_prefab_is_not_coerced(self):
        self.assertIsNone(resolve_item("MyModdedLegendaryHammer"))

    def test_completion_labels_are_search_friendly(self):
        labels = completion_labels()
        self.assertIn("Wood Arrow — ArrowWood", labels)
        self.assertIn("Bronze Sword — SwordBronze", labels)


if __name__ == "__main__":
    unittest.main()
