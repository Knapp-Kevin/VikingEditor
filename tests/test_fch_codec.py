import hashlib
import json
import struct
import tempfile
import unittest
from pathlib import Path

from subscripts.fchUtil import (
    MIN_CHARACTER_SAVE_VERSION,
    compile_fch,
    decompile_fch,
    parse_save,
    serialize_save,
)
from subscripts.saveErrors import SaveFormatError
from tests.fixture_saves import realistic_root_save


def _reframe(zpackage: bytes) -> bytes:
    digest = hashlib.sha512(zpackage).digest()
    return struct.pack("<i", len(zpackage)) + zpackage + struct.pack("<i", len(digest)) + digest


class FchCodecTests(unittest.TestCase):
    def test_round_trip_is_byte_identical(self):
        data = serialize_save(realistic_root_save())
        self.assertEqual(serialize_save(parse_save(data)), data)

    def test_parse_preserves_non_ascii_name_and_map_data(self):
        root = realistic_root_save()
        parsed = parse_save(serialize_save(root))
        self.assertEqual(parsed["character_name"], "Frostwülf")
        self.assertEqual(parsed["worlds"][0]["map_data_hex"], root["worlds"][0]["map_data_hex"])

    def test_trailing_bytes_inside_zpackage_raise(self):
        data = serialize_save(realistic_root_save())
        zlen = struct.unpack_from("<i", data, 0)[0]
        with self.assertRaises(SaveFormatError) as ctx:
            parse_save(_reframe(data[4:4 + zlen] + b"\x00" * 16))
        self.assertIn("unconsumed", str(ctx.exception).lower())

    def test_version_below_minimum_raises_with_clear_message(self):
        data = serialize_save(realistic_root_save())
        zlen = struct.unpack_from("<i", data, 0)[0]
        zpackage = struct.pack("<i", 39) + data[8:4 + zlen]
        with self.assertRaises(SaveFormatError) as ctx:
            parse_save(_reframe(zpackage))
        self.assertIn(str(MIN_CHARACTER_SAVE_VERSION), str(ctx.exception))
        self.assertIn("39", str(ctx.exception))

    def test_truncated_container_raises_save_format_error(self):
        data = serialize_save(realistic_root_save())
        zlen = struct.unpack_from("<i", data, 0)[0]
        with self.assertRaises(SaveFormatError):
            parse_save(_reframe(data[4:4 + zlen - 50]))

    def test_compile_fch_writes_serialize_save_bytes(self):
        root = realistic_root_save()
        with tempfile.TemporaryDirectory() as temp_dir:
            wrapper = Path(temp_dir) / "save.json"
            output = Path(temp_dir) / "save.fch"
            wrapper.write_text(json.dumps(root), encoding="utf-8")
            compile_fch(str(wrapper), str(output))
            self.assertEqual(output.read_bytes(), serialize_save(root))
            self.assertEqual(decompile_fch(str(output)), parse_save(serialize_save(root)))


if __name__ == "__main__":
    unittest.main()
