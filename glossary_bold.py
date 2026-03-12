#!/usr/bin/env python3
"""
Glossary Term Bolding Pass

Scans chapter markdown files and bolds the first occurrence of each glossary
term (from glossary_terms.yaml) that appears unbolded. Skips headings,
footnote blocks, blockquotes, and text already inside bold/italic markup.

Usage:
    python glossary_bold.py --dry-run                    # Preview changes
    python glossary_bold.py --dry-run --pattern "1-*.md"  # Preview Volume 1
    python glossary_bold.py                               # Apply to all files
    python glossary_bold.py --pattern "2-01-*.md"         # Apply to one file
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


def load_glossary_terms(glossary_path: str = 'glossary_terms.yaml') -> List[dict]:
    """Load terms from glossary_terms.yaml."""
    filepath = Path(glossary_path)
    if not filepath.exists():
        print(f"Error: {glossary_path} not found.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data.get('terms', [])


def build_term_patterns(terms: List[dict]) -> List[Tuple[re.Pattern, str]]:
    """Build regex patterns for each term and its aliases.

    Returns list of (compiled_pattern, canonical_display_form) tuples,
    sorted longest-first so longer terms match before shorter substrings.
    """
    # Collect all matchable forms with their case sensitivity flag
    forms = []  # (form_text, display_name, case_sensitive)
    for entry in terms:
        canonical = entry['term']
        cs = entry.get('case_sensitive', False)
        forms.append((canonical, canonical, cs))
        for alias in entry.get('aliases', []) or []:
            forms.append((alias, alias, cs))  # Bold the alias as-is

    # Sort longest first so "Dead Sea Scrolls" matches before "Dead Sea"
    forms.sort(key=lambda x: len(x[0]), reverse=True)

    patterns = []
    for form_text, display, case_sensitive in forms:
        # Word-boundary match
        # Negative lookbehind/ahead for * to avoid matching inside existing bold
        pattern_str = (
            r'(?<!\*)'           # Not preceded by *
            r'\b'
            + re.escape(form_text)
            + r'\b'
            r'(?!\*)'           # Not followed by *
        )
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled = re.compile(pattern_str, flags)
        patterns.append((compiled, display))

    return patterns


def is_skip_line(line: str) -> bool:
    """Check if a line should be skipped (headings, footnotes, blockquotes, etc.)."""
    stripped = line.lstrip()

    # Headings
    if stripped.startswith('#'):
        return True

    # Blockquotes
    if stripped.startswith('>'):
        return True

    # Footnote lines (bold footnote headers and their continuation)
    if re.match(r'\s*\*\*Footnote\s+\d+', stripped):
        return True

    # YAML frontmatter delimiters
    if stripped == '---':
        return True

    # Empty lines
    if not stripped:
        return True

    return False


def bold_terms_in_file(filepath: Path, term_patterns: List[Tuple[re.Pattern, str]],
                       dry_run: bool = False) -> Tuple[int, List[str]]:
    """Bold first occurrence of each glossary term in a file.

    Returns (number_of_changes, list_of_change_descriptions).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    changes = []
    bolded_terms = set()  # Track which terms we've already bolded (lowercase)

    # Track frontmatter region
    in_frontmatter = False
    frontmatter_count = 0

    # Track footnote region (from **Footnote N:** to end of file or next section)
    in_footnote_region = False

    new_lines = []
    for line in lines:
        # Handle YAML frontmatter
        if line.strip() == '---':
            frontmatter_count += 1
            if frontmatter_count == 1:
                in_frontmatter = True
            elif frontmatter_count == 2:
                in_frontmatter = False
            new_lines.append(line)
            continue

        if in_frontmatter:
            new_lines.append(line)
            continue

        # Detect footnote region start
        if re.match(r'\s*\*\*Footnote\s+\d+', line.lstrip()):
            in_footnote_region = True

        # Skip lines that shouldn't be modified
        if is_skip_line(line) or in_footnote_region:
            new_lines.append(line)
            continue

        # Process this line: try each term pattern
        modified_line = line
        for pattern, display in term_patterns:
            term_key = display.lower()

            # Skip if we've already bolded this term in this file
            if term_key in bolded_terms:
                continue

            # Check if the term appears on this line (unbolded)
            match = pattern.search(modified_line)
            if not match:
                continue

            # Verify the match isn't inside existing markdown formatting
            # Check for surrounding * or [ characters that indicate markup
            start, end = match.start(), match.end()
            context_before = modified_line[max(0, start - 2):start]
            context_after = modified_line[end:end + 2]

            # Skip if inside existing bold (**term**) or italic (*term*)
            if '**' in context_before or '**' in context_after:
                continue
            if context_before.endswith('*') or context_after.startswith('*'):
                continue
            # Skip if inside a markdown link [term](url)
            if context_before.endswith('[') or context_after.startswith(']'):
                continue

            # Apply bolding: replace just this first match
            matched_text = match.group(0)
            modified_line = (
                modified_line[:start]
                + '**' + matched_text + '**'
                + modified_line[end:]
            )

            bolded_terms.add(term_key)
            changes.append(f"  + **{matched_text}** (line {lines.index(line) + 1})")

        new_lines.append(modified_line)

    if changes and not dry_run:
        new_content = '\n'.join(new_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return len(changes), changes


def main():
    parser = argparse.ArgumentParser(
        description="Bold first occurrence of glossary terms in chapter files"
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--pattern', default=None,
        help='Glob pattern for files to process (default: all chapter files)'
    )
    parser.add_argument(
        '--glossary', default='glossary_terms.yaml',
        help='Path to glossary terms file (default: glossary_terms.yaml)'
    )
    parser.add_argument(
        '--verbose', action='store_true',
        help='Show each individual term change'
    )
    args = parser.parse_args()

    if args.dry_run:
        print("DRY RUN - No files will be modified\n")

    # Load terms and build patterns
    terms = load_glossary_terms(args.glossary)
    if not terms:
        print("No terms found in glossary.")
        sys.exit(0)

    term_patterns = build_term_patterns(terms)
    print(f"Loaded {len(terms)} terms ({len(term_patterns)} matchable forms)\n")

    # Gather files
    project_dir = Path('.')
    if args.pattern:
        files = sorted(project_dir.glob(args.pattern))
    else:
        files = []
        for vol in range(1, 9):
            files.extend(sorted(project_dir.glob(f'{vol}-*.md')))

    files = [
        f for f in files
        if f.suffix == '.md'
        and not f.name.startswith(('README', 'CLAUDE'))
    ]

    if not files:
        print("No files found to process.")
        sys.exit(1)

    # Process files
    total_changes = 0
    files_changed = 0

    for filepath in files:
        num_changes, change_list = bold_terms_in_file(
            filepath, term_patterns, dry_run=args.dry_run
        )

        if num_changes > 0:
            files_changed += 1
            total_changes += num_changes
            print(f"{filepath.name}: {num_changes} terms bolded")
            if args.verbose:
                for desc in change_list:
                    print(desc)
        elif args.verbose:
            print(f"{filepath.name}: no changes")

    # Summary
    print(f"\nSummary:")
    print(f"  Files scanned: {len(files)}")
    print(f"  Files {'that would be ' if args.dry_run else ''}modified: {files_changed}")
    print(f"  Terms {'that would be ' if args.dry_run else ''}bolded: {total_changes}")

    if args.dry_run and total_changes > 0:
        print(f"\nRun without --dry-run to apply changes")


if __name__ == '__main__':
    main()
