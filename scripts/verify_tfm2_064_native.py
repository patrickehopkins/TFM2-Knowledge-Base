#!/usr/bin/env python3
"""Read-only exact-build native relocation verifier for Teamfight Manager 2 0.6.4.
No third-party modules; never changes the executable, process, or SDK.
Use: python verify_tfm2_064_native.py "C:\...\TeamfightManager2.exe"
"""
from __future__ import annotations
import argparse
import hashlib
import struct
import sys
from pathlib import Path

EXPECTED_SHA256 = "a1d05045405a12e2bed182daeafcad8c8a40cf29ab68ba6ea5bfd30257439582"
EXPECTED_PE_TIMESTAMP = 0x6ACF3112
EXPECTED_IMAGE_SIZE = 0x0533F000
SIM_PROLOGUE = bytes.fromhex("55 41 57 41 56 41 55 41 54 56 57 53")
RESOURCE_PROLOGUE = bytes.fromhex("55 56 57 48 83 EC 70 48 8D 6C 24 70")
ANIMATION_PROLOGUE = bytes.fromhex("41 56 56 57 53 48 81 EC 98 00 00 00")
SITES = {
    "simulation A": (0x00C526A0, SIM_PROLOGUE),
    "simulation B": (0x00C53130, SIM_PROLOGUE),
    "simulation C": (0x00C53BC0, SIM_PROLOGUE),
    "world-resource resolver": (0x02AAB520, RESOURCE_PROLOGUE),
    "animation-key resolver": (0x02AB4400, ANIMATION_PROLOGUE),
}
SEMANTIC_BRANCHES = {
    "world-resource minion branch": (0x02AAB6C2, bytes.fromhex("41 B8 30 00 00 00 31 D2")),
    "animation minion suffix": (0x02AB44FA, bytes.fromhex("41 B8 6D 69 6E 69 44 33")),
    "animation melee branch": (0x02AB45C4, bytes.fromhex("48 B9 6D 65 6C 65 65 5F 6D 69")),
    "asset minion literal": (0x03B13468, b"asset/base/aseprite_resources/UI_aseprite/minion"),
}
COMMON_SIM_CALLS = (0x016CCBE0, 0x016BB1F0)

def verify(path: Path) -> int:
    raw = path.read_bytes()
    failures = []
    if raw[:2] != b"MZ":
        raise ValueError("not an MZ/PE executable")
    pe_offset = struct.unpack_from("<I", raw, 0x3C)[0]
    if raw[pe_offset:pe_offset + 4] != b"PE\x00\x00":
        raise ValueError("PE signature mismatch")
    machine, count, timestamp = struct.unpack_from("<HHI", raw, pe_offset + 4)
    optional = pe_offset + 24
    size_of_image = struct.unpack_from("<I", raw, optional + 56)[0]
    section_start = optional + struct.unpack_from("<H", raw, pe_offset + 20)[0]
    sections = []
    for index in range(count):
        offset = section_start + 40 * index
        name = raw[offset:offset + 8].rstrip(b"\x00").decode("ascii", "replace")
        _, rva, rsize, disk_offset = struct.unpack_from("<IIII", raw, offset + 8)
        sections.append((name, rva, rsize, disk_offset))

    def location(rva: int, length: int) -> bytes:
        for name, start, disk_length, disk_offset in sections:
            if start <= rva and rva + length <= start + disk_length:
                return raw[disk_offset + rva - start:disk_offset + rva - start + length]
        raise ValueError(f"RVA {rva:#x} cannot be mapped to file bytes")

    digest = hashlib.sha256(raw).hexdigest()
    print(f"game={path.name} sha256={digest} pe_timestamp={timestamp:#010x} image_size={size_of_image:#010x}")
    for label, ok in (
        ("exact SHA-256", digest == EXPECTED_SHA256),
        ("x64 executable", machine == 0x8664),
        ("PE timestamp", timestamp == EXPECTED_PE_TIMESTAMP),
        ("PE image size", size_of_image == EXPECTED_IMAGE_SIZE),
    ):
        print(f"{'PASS' if ok else 'FAIL'} {label}")
        if not ok:
            failures.append(label)
    if failures:
        print("NOT VERIFIED: exact-build fingerprint differs")
        return 1

    pdata = next(((rva, disk_len) for name, rva, disk_len, _ in sections if name == ".pdata"), None)
    if pdata is None:
        raise ValueError("missing PE unwind .pdata section")
    known_starts = set()
    data = location(*pdata)
    for offset in range(0, len(data) - 11, 12):
        begin, end, unwind = struct.unpack_from("<III", data, offset)
        if 0x1000 <= begin < end < size_of_image:
            known_starts.add(begin)

    for label, (rva, signature) in SITES.items():
        ok = rva in known_starts and location(rva, len(signature)) == signature
        print(f"{'PASS' if ok else 'FAIL'} {label} at {rva:#010x}: .pdata function start and original prologue")
        if not ok:
            failures.append(label)

    for label, (rva, signature) in SEMANTIC_BRANCHES.items():
        ok = location(rva, len(signature)) == signature
        print(f"{'PASS' if ok else 'FAIL'} {label} at {rva:#010x}")
        if not ok:
            failures.append(label)

    if SITES["simulation B"][0] - SITES["simulation A"][0] != 0xA90 or SITES["simulation C"][0] - SITES["simulation B"][0] != 0xA90:
        failures.append("simulation A/B/C stride")
    for target in COMMON_SIM_CALLS:
        matches = []
        for site in ("simulation A", "simulation B", "simulation C"):
            start = SITES[site][0]
            block = location(start, 0x300)
            n = sum(1 for i in range(len(block) - 4)
                    if block[i] == 0xE8 and start + i + 5 + struct.unpack_from("<i", block, i + 1)[0] == target)
            matches.append(n)
        ok = all(n > 0 for n in matches)
        print(f"{'PASS' if ok else 'FAIL'} shared simulation call {target:#010x}: A/B/C counts {matches}")
        if not ok:
            failures.append(f"shared simulation call {target:#010x}")

    print("STATIC RELOCATION CHECK PASSED — in-game hook/simulation behavior STILL REQUIRES TESTING" if not failures
          else "STATIC RELOCATION CHECK FAILED — do not install a native hook from this profile")
    return 0 if not failures else 1

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exe", type=Path, help="local original 0.6.4 TeamfightManager2.exe")
    args = parser.parse_args()
    try:
        return verify(args.exe)
    except (OSError, ValueError, struct.error) as exc:
        print(f"ERROR (fail closed): {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
