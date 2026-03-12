#!/usr/bin/env python3
"""
Glossary & Index Generator

Reads the curated master term list (glossary_terms.yaml) and volume configuration
(volume_config.yaml), scans chapter files for term occurrences, and generates
per-volume glossary.md and index.md files.

Usage:
    python glossary_build.py                # Generate for all volumes
    python glossary_build.py --volume 1     # Generate for Volume 1 only
    python glossary_build.py --dry-run      # Preview without writing files
"""

import re
import sys
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


def load_glossary_terms(path='glossary_terms.yaml'):
    """Load the curated master term list."""
    filepath = Path(path)
    if not filepath.exists():
        print(f"Error: {path} not found. Create it or run glossary_extract.py first.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    terms = data.get('terms', [])
    if not terms:
        print(f"Warning: No terms found in {path}.")
        return []

    return terms


def load_volume_config(path='volume_config.yaml'):
    """Load volume configuration."""
    filepath = Path(path)
    if not filepath.exists():
        print(f"Error: {path} not found.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data


def get_volume_files(volume_config):
    """Resolve glob patterns to actual files for a volume."""
    patterns = volume_config.get('include_files', [])
    project_dir = Path('.')

    all_files = []
    seen = set()

    for pattern in patterns:
        for filepath in sorted(project_dir.glob(pattern)):
            if filepath.suffix != '.md':
                continue
            if filepath.name.startswith(('README', 'CLAUDE')):
                continue
            if filepath not in seen:
                seen.add(filepath)
                all_files.append(filepath)

    return all_files


def extract_chapter_label(content, filename):
    """Extract a human-readable chapter label from file content.

    For MUSH book files named like 1-06-Attributes.md, extracts the chapter
    number from the filename and the title from the first # heading.
    """
    name = Path(filename).stem
    parts = name.split('-', 2)  # e.g. ['1', '06', 'Attributes']

    # Extract chapter number from filename (e.g., "1-06" -> "Ch. 6")
    ch_label = None
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        vol = parts[0]
        ch = int(parts[1])
        if ch == 0:
            ch_label = f"Vol. {vol} Intro"
        else:
            ch_label = f"Ch. {ch}"

    # Get title from first # heading
    match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    title = match.group(1).strip() if match else None

    if ch_label:
        return ch_label, title

    # Fall back to frontmatter title
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm_match.group(1), re.MULTILINE)
        if title_match:
            return title_match.group(1), None

    return title or name, None


def build_search_patterns(terms):
    """Build compiled regex patterns for each term and its aliases.

    Returns a list of (term_entry, compiled_pattern) tuples.
    The pattern matches the term or any alias as a whole word, case-insensitive.
    """
    patterns = []
    for entry in terms:
        term = entry['term']
        aliases = entry.get('aliases', []) or []

        # Build alternation: term|alias1|alias2
        all_forms = [re.escape(term)] + [re.escape(a) for a in aliases]
        pattern_str = r'\b(?:' + '|'.join(all_forms) + r')\b'
        compiled = re.compile(pattern_str, re.IGNORECASE)
        patterns.append((entry, compiled))

    return patterns


def scan_volume(volume_files, search_patterns):
    """Scan files in a volume for term occurrences.

    Returns a dict: term_name -> list of chapter labels where it appears.
    """
    term_chapters = {}

    for filepath in volume_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        chapter_label, _ = extract_chapter_label(content, filepath.name)

        for entry, pattern in search_patterns:
            term_name = entry['term']
            if pattern.search(content):
                if term_name not in term_chapters:
                    term_chapters[term_name] = []
                if chapter_label not in term_chapters[term_name]:
                    term_chapters[term_name].append(chapter_label)

    return term_chapters


def generate_glossary_md(terms, term_chapters, volume_title):
    """Generate glossary markdown content for a volume."""
    lines = []
    lines.append(f"# Glossary")
    lines.append("")
    lines.append(f"*{volume_title}*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Filter to only terms that appear in this volume, sort alphabetically
    volume_terms = [
        t for t in terms
        if t['term'] in term_chapters
    ]
    volume_terms.sort(key=lambda t: t['term'].lower())

    if not volume_terms:
        lines.append("*No glossary terms found in this volume.*")
        return '\n'.join(lines) + '\n'

    for entry in volume_terms:
        term = entry['term']
        definition = entry.get('definition', '').strip()
        aliases = entry.get('aliases', []) or []

        if aliases:
            lines.append(f"**{term}** ({', '.join(aliases)})")
        else:
            lines.append(f"**{term}**")
        lines.append(f"")
        lines.append(f"{definition}")
        lines.append("")

    return '\n'.join(lines) + '\n'


def generate_index_md(terms, term_chapters, volume_title):
    """Generate index markdown content for a volume."""
    lines = []
    lines.append(f"# Index")
    lines.append("")
    lines.append(f"*{volume_title}*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Filter and sort
    index_terms = [
        t for t in terms
        if t['term'] in term_chapters
    ]
    index_terms.sort(key=lambda t: t['term'].lower())

    if not index_terms:
        lines.append("*No index entries found for this volume.*")
        return '\n'.join(lines) + '\n'

    for entry in index_terms:
        term = entry['term']
        chapters = term_chapters[term]
        chapter_str = ', '.join(chapters)
        lines.append(f"**{term}** — {chapter_str}")
        lines.append("")

    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(
        description="Generate per-volume glossary and index from curated term list"
    )
    parser.add_argument(
        '--volume', type=int, default=None,
        help='Generate for a single volume number (default: all)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview output without writing files'
    )
    parser.add_argument(
        '--terms', default='glossary_terms.yaml',
        help='Path to glossary terms file (default: glossary_terms.yaml)'
    )
    parser.add_argument(
        '--config', default='volume_config.yaml',
        help='Path to volume config file (default: volume_config.yaml)'
    )
    args = parser.parse_args()

    # Load data
    terms = load_glossary_terms(args.terms)
    if not terms:
        print("No terms to process. Add terms to glossary_terms.yaml first.")
        sys.exit(0)

    config = load_volume_config(args.config)
    volumes = config.get('volumes', [])
    base_output_dir = Path(config.get('base_output_dir', 'book_output'))

    if args.volume:
        volumes = [v for v in volumes if v['volume_number'] == args.volume]
        if not volumes:
            print(f"Error: Volume {args.volume} not found in config.")
            sys.exit(1)

    # Build search patterns once
    search_patterns = build_search_patterns(terms)

    total_glossary_terms = 0
    total_index_entries = 0

    for vol in volumes:
        vol_num = vol['volume_number']
        vol_title = vol['title']
        print(f"\nProcessing {vol_title}...")

        # Get files for this volume
        volume_files = get_volume_files(vol)
        if not volume_files:
            print(f"  Warning: No files found for volume {vol_num}")
            continue

        print(f"  Scanning {len(volume_files)} files...")

        # Scan for term occurrences
        term_chapters = scan_volume(volume_files, search_patterns)
        terms_found = len(term_chapters)
        total_glossary_terms += terms_found
        total_index_entries += sum(len(chs) for chs in term_chapters.values())

        print(f"  Found {terms_found} terms in this volume")

        # Generate output
        glossary_md = generate_glossary_md(terms, term_chapters, vol_title)
        index_md = generate_index_md(terms, term_chapters, vol_title)

        # Output directory
        output_dir = base_output_dir / f"volume_{vol_num}"

        if args.dry_run:
            print(f"\n  --- glossary.md preview ({vol_title}) ---")
            # Show first 30 lines
            preview_lines = glossary_md.split('\n')[:30]
            for line in preview_lines:
                print(f"  {line}")
            if len(glossary_md.split('\n')) > 30:
                print(f"  ... ({len(glossary_md.split(chr(10)))} total lines)")

            print(f"\n  --- index.md preview ({vol_title}) ---")
            preview_lines = index_md.split('\n')[:30]
            for line in preview_lines:
                print(f"  {line}")
            if len(index_md.split('\n')) > 30:
                print(f"  ... ({len(index_md.split(chr(10)))} total lines)")
        else:
            output_dir.mkdir(parents=True, exist_ok=True)

            glossary_path = output_dir / 'glossary.md'
            with open(glossary_path, 'w', encoding='utf-8') as f:
                f.write(glossary_md)
            print(f"  Wrote {glossary_path}")

            index_path = output_dir / 'index.md'
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_md)
            print(f"  Wrote {index_path}")

    # Summary
    print(f"\nSummary:")
    print(f"  Volumes processed: {len(volumes)}")
    print(f"  Total glossary entries: {total_glossary_terms}")
    print(f"  Total index references: {total_index_entries}")

    if args.dry_run:
        print(f"\n  (dry run — no files written)")


if __name__ == '__main__':
    main()
