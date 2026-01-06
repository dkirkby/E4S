#!/usr/bin/env python3

'''
Run this script to generate an updated E4S-libraries-<version>.zip file:

    cd bin
    python update-libs.py <input.zip> <bundle.zip>

where <input.zip> is the existing E4S-libraries-<version>.zip file to be updated to a new version,
and <bundle.zip> is the new E4S bundle zip file containing updated versions of all library files,
normally downloaded from a CircuitPython auto release, e.g.

  https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20251231/adafruit-circuitpython-bundle-10.x-mpy-20251231.zip

The new version number will be extracted from the bundle zip filename. The script first fills a
temporary output directory with library files extracted from the bundle zip, matching the files
found in the input zip under the 'lib/' directory. It then creates a new output zip file named
E4S-libraries-<version>.zip containing the updated library files under 'lib/', omitting any
macOS special files. The script will print warnings in case any files from the input zip are
missing in the bundle zip.

Sample command used to update from 9.x to 10.x for 2026:

    python update-libs.py E4S-libraries-9.x.zip ~/Downloads/adafruit-circuitpython-bundle-10.x-mpy-20251231.zip

This generates E4S-libraries-10.x.zip in the current directory, ready to commit to the github repo.

To check the contents of the created zip file, you can use:

    unzip -l E4S-libraries-10.x.zip
'''
import os
import re
import sys
import tempfile
import zipfile
from pathlib import PurePosixPath, Path
from typing import Dict, List

VERSION_RE = re.compile(r"-([0-9]+\.x)-")

# Common macOS junk we don't want in the output zip
SKIP_DIRS = {"__MACOSX", ".Spotlight-V100", ".Trashes", ".fseventsd"}
SKIP_FILES = {".DS_Store", "Icon\r"}  # "Icon\r" shows up sometimes on mac volumes


def extract_version(bundle_zip_name: str) -> str:
    m = VERSION_RE.search(os.path.basename(bundle_zip_name))
    if not m:
        raise ValueError(f"Could not extract version tag like '10.x' from: {bundle_zip_name}")
    return m.group(1)


def safe_posix_path(zip_member_name: str) -> PurePosixPath:
    p = PurePosixPath(zip_member_name)

    # Strip harmless leading "./"
    while p.parts and p.parts[0] == ".":
        p = PurePosixPath(*p.parts[1:])

    if p.is_absolute() or any(part == ".." for part in p.parts):
        raise ValueError(f"Unsafe zip path: {zip_member_name}")
    return p


def apply_mode_if_present(info: zipfile.ZipInfo, out_path: Path) -> None:
    mode = (info.external_attr >> 16) & 0o7777
    if mode:
        try:
            os.chmod(out_path, mode)
        except OSError:
            pass


def build_bundle_index(zbundle: zipfile.ZipFile) -> Dict[str, zipfile.ZipInfo]:
    """
    Index bundle entries by:
      - exact path
      - path with one leading top-level directory stripped
    """
    index: Dict[str, zipfile.ZipInfo] = {}

    for info in zbundle.infolist():
        if info.is_dir():
            continue

        try:
            p = safe_posix_path(info.filename)
        except ValueError:
            continue

        raw = p.as_posix()
        keys = [raw]

        if len(p.parts) >= 2:
            keys.append(PurePosixPath(*p.parts[1:]).as_posix())

        for k in keys:
            if k not in index:
                index[k] = info
            else:
                # Prefer the entry that's closer to root (shorter stored filename)
                if len(index[k].filename) > len(info.filename):
                    index[k] = info

    return index


def find_suffix_candidates(bundle_keys: List[str], wanted: str, limit: int = 5) -> List[str]:
    out = [k for k in bundle_keys if k.endswith(wanted)]
    out.sort(key=len)
    return out[:limit]


def is_macos_junk(rel_posix: str) -> bool:
    p = PurePosixPath(rel_posix)
    # Skip if any directory component is a known junk dir
    if any(part in SKIP_DIRS for part in p.parts[:-1]):
        return True
    name = p.name
    if name in SKIP_FILES:
        return True
    # AppleDouble resource fork files
    if name.startswith("._"):
        return True
    return False


def create_output_zip_from_dir(out_dir: Path, output_zip_path: Path) -> None:
    """
    Zip the contents of out_dir into output_zip_path.
    - All archived paths must start with 'lib/'.
    - Omit macOS special files.
    """
    with zipfile.ZipFile(output_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for root, dirnames, filenames in os.walk(out_dir):
            # Prune junk dirs early
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

            root_path = Path(root)
            for fn in filenames:
                full_path = root_path / fn
                rel_path = full_path.relative_to(out_dir)

                rel_posix = PurePosixPath(*rel_path.parts).as_posix()

                if not rel_posix.startswith("lib/"):
                    # Enforce output zip layout rule
                    continue
                if is_macos_junk(rel_posix):
                    continue

                # Ensure stable timestamps? (optional; leaving as default)
                zout.write(full_path, arcname=rel_posix)


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.zip> <bundle.zip>", file=sys.stderr)
        sys.exit(1)

    input_zip = sys.argv[1]
    bundle_zip = sys.argv[2]

    try:
        version = extract_version(bundle_zip)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    output_zip_name = f"E4S-libraries-{version}.zip"

    out_dir = Path(tempfile.mkdtemp(prefix=f"E4S-libraries-{version}-"))

    try:
        with zipfile.ZipFile(input_zip, "r") as zin, zipfile.ZipFile(bundle_zip, "r") as zbundle:
            bundle_index = build_bundle_index(zbundle)
            bundle_keys = list(bundle_index.keys())

            for in_info in zin.infolist():
                if in_info.is_dir():
                    continue

                try:
                    in_path = safe_posix_path(in_info.filename)
                except ValueError as e:
                    print(f"Warning: {e}; skipping", file=sys.stderr)
                    continue

                # Require input entries under lib/
                if not (in_path.parts and in_path.parts[0] == "lib"):
                    print(f"Warning: input entry not under 'lib/': '{in_info.filename}'; skipping", file=sys.stderr)
                    continue

                wanted = in_path.as_posix()  # keep 'lib/' for matching
                binfo = bundle_index.get(wanted)

                if binfo is None:
                    print(f"Warning: missing in bundle_zip: '{wanted}'; skipping", file=sys.stderr)
                    cands = find_suffix_candidates(bundle_keys, wanted, limit=5)
                    if cands:
                        print("  Candidates (bundle keys ending with wanted path):", file=sys.stderr)
                        for c in cands:
                            print(f"    {c}", file=sys.stderr)
                    continue

                out_path = out_dir / Path(*in_path.parts)
                out_path.parent.mkdir(parents=True, exist_ok=True)

                try:
                    with zbundle.open(binfo, "r") as src, open(out_path, "wb") as dst:
                        dst.write(src.read())
                    apply_mode_if_present(binfo, out_path)
                except OSError as e:
                    print(f"Warning: failed writing '{out_path}': {e}; skipping", file=sys.stderr)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except zipfile.BadZipFile as e:
        print(f"Error: bad zip file: {e}", file=sys.stderr)
        sys.exit(1)

    # Create the target output zip from temp dir contents
    output_zip_path = Path.cwd() / output_zip_name
    try:
        create_output_zip_from_dir(out_dir, output_zip_path)
    except OSError as e:
        print(f"Error: failed creating output zip '{output_zip_path}': {e}", file=sys.stderr)
        sys.exit(1)

    # Finally, print the location of the tmp output dir
    print(f'Created {output_zip_path} from {str(out_dir)}')


if __name__ == "__main__":
    main()
