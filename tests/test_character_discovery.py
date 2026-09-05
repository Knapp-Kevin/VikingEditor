import json
import os
import tempfile
import unittest
from pathlib import Path

from subscripts.characterDiscovery import candidate_character_directories, discover_character_saves
from subscripts.fchUtil import compile_fch


def minimal_save_data(name="TestViking"):
    return {
        "version": 43,
        "stats": [],
        "first_spawn": True,
        "worlds": [],
        "character_name": name,
        "player_id": 1234,
        "start_seed": "test-seed",
        "used_cheats": False,
        "date_created_unix": 0,
        "known_worlds": {},
        "known_world_keys": {},
        "known_commands": {},
        "enemy_stats": {},
        "item_pickup_stats": {},
        "item_craft_stats": {},
        "player_data_hex": None,
    }


def write_save(path: Path, name: str):
    wrapper = path.with_suffix(".json")
    wrapper.write_text(json.dumps(minimal_save_data(name)), encoding="utf-8")
    compile_fch(str(wrapper), str(path))
    wrapper.unlink()


class CharacterDiscoveryTests(unittest.TestCase):
    def test_windows_local_and_cloud_directories_are_discovered(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            local_dir = home / "AppData" / "LocalLow" / "IronGate" / "Valheim" / "characters_local"
            cloud_dir = home / "SteamRoot" / "userdata" / "123456" / "892970" / "remote" / "characters"
            local_dir.mkdir(parents=True)
            cloud_dir.mkdir(parents=True)

            previous = os.environ.get("STEAM_DIR")
            os.environ["STEAM_DIR"] = str(home / "SteamRoot")
            try:
                directories = candidate_character_directories(home=home, system_name="Windows")
            finally:
                if previous is None:
                    os.environ.pop("STEAM_DIR", None)
                else:
                    os.environ["STEAM_DIR"] = previous

            self.assertIn((local_dir.resolve(), "Local"), directories)
            self.assertIn((cloud_dir.resolve(), "Steam Cloud"), directories)

    def test_discovery_returns_verified_character_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            local_dir = home / ".config" / "unity3d" / "IronGate" / "Valheim" / "characters_local"
            local_dir.mkdir(parents=True)
            save_path = local_dir / "kevin.fch"
            write_save(save_path, "Kevin")

            results = discover_character_saves(home=home, system_name="Linux")

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].name, "Kevin")
            self.assertEqual(results[0].source, "Local")
            self.assertTrue(results[0].valid)
            self.assertEqual(results[0].version, 43)

    def test_corrupt_character_is_listed_but_marked_invalid(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            local_dir = home / ".config" / "unity3d" / "IronGate" / "Valheim" / "characters_local"
            local_dir.mkdir(parents=True)
            bad_path = local_dir / "broken.fch"
            bad_path.write_bytes(b"not-a-valid-save")

            results = discover_character_saves(home=home, system_name="Linux")

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].name, "broken")
            self.assertFalse(results[0].valid)
            self.assertIsNotNone(results[0].error)


if __name__ == "__main__":
    unittest.main()
