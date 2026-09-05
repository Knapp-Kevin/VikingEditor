import json
import os
import tempfile
import unittest
from datetime import datetime, timezone

from subscripts.fchUtil import compile_fch
from subscripts.saveSafety import (
    SaveVerificationError,
    create_timestamped_backup,
    replace_verified_save,
    verify_fch_round_trip,
)


def minimal_save_data():
    return {
        "version": 43,
        "stats": [],
        "first_spawn": True,
        "worlds": [],
        "character_name": "TestViking",
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


class SaveSafetyTests(unittest.TestCase):
    def compile_candidate(self, directory, save_data=None):
        save_data = save_data or minimal_save_data()
        wrapper_path = os.path.join(directory, "wrapper.json")
        candidate_path = os.path.join(directory, "candidate.fch")

        with open(wrapper_path, "w", encoding="utf-8") as wrapper:
            json.dump(save_data, wrapper)

        compile_fch(wrapper_path, candidate_path)
        return candidate_path, save_data

    def test_round_trip_verification_accepts_valid_save(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate_path, expected = self.compile_candidate(temp_dir)
            parsed = verify_fch_round_trip(candidate_path, expected)
            self.assertEqual(parsed, expected)

    def test_round_trip_verification_rejects_checksum_tampering(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate_path, expected = self.compile_candidate(temp_dir)

            with open(candidate_path, "r+b") as candidate:
                candidate.seek(4)
                original = candidate.read(1)
                candidate.seek(4)
                candidate.write(bytes([original[0] ^ 0x01]))

            with self.assertRaises(SaveVerificationError):
                verify_fch_round_trip(candidate_path, expected)

    def test_timestamped_backup_preserves_existing_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = os.path.join(temp_dir, "character.fch")
            original_bytes = b"known-good-save"
            with open(destination, "wb") as existing:
                existing.write(original_bytes)

            timestamp = datetime(2026, 9, 5, 12, 34, 56, tzinfo=timezone.utc)
            backup_path = create_timestamped_backup(destination, timestamp)

            self.assertEqual(
                backup_path,
                f"{destination}.20260905T123456Z.bak"
            )
            with open(backup_path, "rb") as backup:
                self.assertEqual(backup.read(), original_bytes)

    def test_verified_replace_backs_up_then_replaces_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate_path, expected = self.compile_candidate(temp_dir)
            with open(candidate_path, "rb") as candidate:
                expected_candidate_bytes = candidate.read()

            destination = os.path.join(temp_dir, "character.fch")
            original_bytes = b"known-good-save"
            with open(destination, "wb") as existing:
                existing.write(original_bytes)

            backup_path = replace_verified_save(candidate_path, destination, expected)

            self.assertIsNotNone(backup_path)
            self.assertFalse(os.path.exists(candidate_path))
            with open(destination, "rb") as saved:
                self.assertEqual(saved.read(), expected_candidate_bytes)
            with open(backup_path, "rb") as backup:
                self.assertEqual(backup.read(), original_bytes)

    def test_failed_verification_leaves_destination_untouched(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate_path, expected = self.compile_candidate(temp_dir)
            destination = os.path.join(temp_dir, "character.fch")
            original_bytes = b"known-good-save"
            with open(destination, "wb") as existing:
                existing.write(original_bytes)

            with open(candidate_path, "ab") as candidate:
                candidate.write(b"trailing-corruption")

            with self.assertRaises(SaveVerificationError):
                replace_verified_save(candidate_path, destination, expected)

            with open(destination, "rb") as existing:
                self.assertEqual(existing.read(), original_bytes)
            backups = [name for name in os.listdir(temp_dir) if name.endswith(".bak")]
            self.assertEqual(backups, [])


if __name__ == "__main__":
    unittest.main()
