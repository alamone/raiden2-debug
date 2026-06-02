#!/usr/bin/env python3
"""
patch_binary.py - Apply patches to a binary file.

Usage:
    python patch_binary.py <binary_file> <patch_list_file> [-o <output_file>]

Patch list format (one patch per line, comments with #):
    <hex_offset> <patch_file>

Example patch list:
    0x00001A00 fix_header.bin
    0x00FF0000 payload.bin
    # This is a comment
    1234       another.bin     # hex offset without 0x prefix is also fine
"""

import sys
import os
import argparse


def parse_patch_list(patch_list_path: str) -> list[tuple[int, str]]:
    """Parse the patch list file and return a list of (offset, patch_file) tuples."""
    patches = []
    base_dir = os.path.dirname(os.path.abspath(patch_list_path))

    with open(patch_list_path, "r") as f:
        for lineno, line in enumerate(f, 1):
            # Strip inline comments and whitespace
            line = line.split("#")[0].strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 2:
                raise ValueError(
                    f"Line {lineno}: expected '<hex_offset> <patch_file>', got: {line!r}"
                )

            offset_str, patch_file = parts[0], parts[1]

            # Parse hex offset (accept with or without 0x prefix)
            try:
                offset = int(offset_str, 16)
            except ValueError:
                raise ValueError(
                    f"Line {lineno}: invalid hex offset {offset_str!r}"
                )

            # Resolve patch file relative to the patch list's directory
            if not os.path.isabs(patch_file):
                patch_file = os.path.join(base_dir, patch_file)

            if not os.path.isfile(patch_file):
                raise FileNotFoundError(
                    f"Line {lineno}: patch file not found: {patch_file!r}"
                )

            patches.append((offset, patch_file))

    return patches


def apply_patches(
    binary_path: str, patches: list[tuple[int, str]], output_path: str
) -> None:
    """Read the binary, apply all patches in order, and write the output."""
    with open(binary_path, "rb") as f:
        data = bytearray(f.read())

    original_size = len(data)

    for offset, patch_file in patches:
        with open(patch_file, "rb") as pf:
            patch_data = pf.read()

        patch_size = len(patch_data)
        end = offset + patch_size

        # Extend the buffer if the patch writes beyond the current end
        if end > len(data):
            data.extend(b"\x00" * (end - len(data)))
            print(
                f"  [warn] Patch '{os.path.basename(patch_file)}' at 0x{offset:X} "
                f"extends binary by {end - original_size} byte(s)."
            )

        data[offset:end] = patch_data
        print(
            f"  [ok]   Applied '{os.path.basename(patch_file)}' "
            f"({patch_size} byte(s)) at offset 0x{offset:X}"
        )

    with open(output_path, "wb") as f:
        f.write(data)


def main():
    parser = argparse.ArgumentParser(
        description="Apply binary patches to a file using an offset/patch-file list."
    )
    parser.add_argument("binary_file", help="Path to the input binary file.")
    parser.add_argument(
        "patch_list_file",
        help=(
            "Path to the text file listing patches. "
            "Format per line: <hex_offset> <patch_file>"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help=(
            "Path for the patched output file. "
            "Defaults to '<binary_file>.patched'."
        ),
    )
    args = parser.parse_args()

    if not os.path.isfile(args.binary_file):
        print(f"Error: binary file not found: {args.binary_file!r}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.patch_list_file):
        print(
            f"Error: patch list file not found: {args.patch_list_file!r}",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = args.output or args.binary_file + ".patched"

    print(f"Input  : {args.binary_file}")
    print(f"Patches: {args.patch_list_file}")
    print(f"Output : {output_path}")
    print()

    try:
        patches = parse_patch_list(args.patch_list_file)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error parsing patch list: {e}", file=sys.stderr)
        sys.exit(1)

    if not patches:
        print("No patches found in patch list. Output will be a copy of the input.")

    try:
        apply_patches(args.binary_file, patches, output_path)
    except OSError as e:
        print(f"Error applying patches: {e}", file=sys.stderr)
        sys.exit(1)

    print()
    print(f"Done. Patched file written to: {output_path}")


if __name__ == "__main__":
    main()
