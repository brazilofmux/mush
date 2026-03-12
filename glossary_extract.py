#!/usr/bin/env python3
"""
Glossary Term Candidate Extractor

Scans all chapter markdown files for bold terms (**term**), filters out noise
(footnote headers, section markers, single-word emphasis), counts occurrences,
and outputs a candidate YAML file for human review.

Usage:
    python glossary_extract.py                    # Scan all chapter files
    python glossary_extract.py --pattern "1-*.md" # Scan Volume 1 only
    python glossary_extract.py --min-count 3      # Only terms appearing 3+ times
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict


# Patterns to exclude from candidates
NOISE_PATTERNS = [
    r'^Footnote\s+\d+',          # Footnote headers
    r'^Part \d+',                 # Part headers
    r'^Chapter \d+',             # Chapter headers
    r'^Level \d+',               # Conformance levels
    r'^Implementation Note',      # Implementation notes
    r'^Compatibility Note',       # Compatibility notes
    r'^Syntax',                   # Syntax headers
    r'^Description',              # Description headers
    r'^Example',                  # Example headers
]

# Compile noise patterns
NOISE_RE = [re.compile(p, re.IGNORECASE) for p in NOISE_PATTERNS]


def extract_frontmatter_title(content):
    """Extract the title from YAML frontmatter."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        fm = match.group(1)
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
        if title_match:
            return title_match.group(1)
    return None


def extract_chapter_label(content, filename):
    """Extract a chapter label like 'Ch. 6' from the file content or filename."""
    name = Path(filename).stem
    parts = name.split('-', 2)  # e.g. ['1', '06', 'Attributes']

    # Extract chapter number from filename (e.g., "1-06" -> "Ch. 6")
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        vol = parts[0]
        ch = int(parts[1])
        if ch == 0:
            return f"Vol. {vol} Intro"
        return f"Ch. {ch}"

    # Fall back to frontmatter title
    title = extract_frontmatter_title(content)
    if title:
        return title

    # Fall back to first heading
    match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    return name


def is_noise(term):
    """Check if a bold term is noise that should be filtered out."""
    # Match against noise patterns
    for pattern in NOISE_RE:
        if pattern.search(term):
            return True

    # Filter single words that are likely just emphasis (not proper nouns or terms)
    words = term.split()
    if len(words) == 1:
        word = words[0].strip('.,;:!?')
        # Keep single words that look like proper nouns or technical terms
        if word[0:1].isupper() and len(word) > 2:
            return False
        # Filter generic single-word emphasis
        return True

    # Filter very long phrases (likely bold sentences, not terms)
    if len(words) > 8:
        return True

    return False


def scan_file(filepath):
    """Scan a markdown file for bold terms. Returns dict of term -> count."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    chapter_label = extract_chapter_label(content, filepath.name)

    # Find all bold terms
    bold_pattern = r'\*\*([^*]+?)\*\*'
    matches = re.findall(bold_pattern, content)

    terms = defaultdict(int)
    for match in matches:
        term = match.strip()
        if not term:
            continue
        if is_noise(term):
            continue
        # Normalize: collapse whitespace
        term = re.sub(r'\s+', ' ', term)
        terms[term] += 1

    return terms, chapter_label


def normalize_term(term):
    """Create a normalized key for grouping similar terms."""
    return term.lower().strip().rstrip('.,;:!?')


def main():
    parser = argparse.ArgumentParser(
        description="Extract glossary term candidates from bold text in markdown files"
    )
    parser.add_argument(
        '--pattern', default=None,
        help='Glob pattern for files to scan (default: all chapter files)'
    )
    parser.add_argument(
        '--min-count', type=int, default=2,
        help='Minimum total occurrences to include (default: 2)'
    )
    parser.add_argument(
        '--output', default='glossary_candidates.yaml',
        help='Output file (default: glossary_candidates.yaml)'
    )
    args = parser.parse_args()

    project_dir = Path('.')

    # Gather files
    if args.pattern:
        files = sorted(project_dir.glob(args.pattern))
    else:
        # All volume chapter files (1-*.md through 8-*.md)
        files = []
        for vol in range(1, 9):
            files.extend(sorted(project_dir.glob(f'{vol}-*.md')))

    # Filter to .md files, skip non-content files
    files = [
        f for f in files
        if f.suffix == '.md'
        and not f.name.startswith(('README', 'CLAUDE'))
    ]

    if not files:
        print("No files found to scan.")
        sys.exit(1)

    print(f"Scanning {len(files)} files...")

    # Collect all terms across all files
    # term_data[normalized_key] = {
    #   'display': preferred display form,
    #   'total_count': int,
    #   'file_count': int,
    #   'chapters': [chapter_labels],
    #   'variants': {variant: count}
    # }
    term_data = {}

    for filepath in files:
        terms, chapter_label = scan_file(filepath)

        for term, count in terms.items():
            key = normalize_term(term)

            if key not in term_data:
                term_data[key] = {
                    'display': term,
                    'total_count': 0,
                    'file_count': 0,
                    'chapters': [],
                    'variants': defaultdict(int),
                }

            term_data[key]['total_count'] += count
            term_data[key]['file_count'] += 1
            term_data[key]['chapters'].append(chapter_label)
            term_data[key]['variants'][term] += count

            # Prefer the most common variant as display name
            variants = term_data[key]['variants']
            term_data[key]['display'] = max(variants, key=variants.get)

    # Filter by minimum count
    filtered = {
        k: v for k, v in term_data.items()
        if v['total_count'] >= args.min_count
    }

    # Sort alphabetically by display name
    sorted_terms = sorted(filtered.values(), key=lambda x: x['display'].lower())

    print(f"Found {len(term_data)} unique terms, {len(sorted_terms)} with {args.min_count}+ occurrences")

    # Write YAML output (manual formatting for clean output without PyYAML dependency)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("# Glossary Term Candidates\n")
        f.write("# Generated by glossary_extract.py\n")
        f.write("# Review these candidates and add selected terms to glossary_terms.yaml\n")
        f.write("#\n")
        f.write(f"# Total unique terms found: {len(term_data)}\n")
        f.write(f"# Terms with {args.min_count}+ occurrences: {len(sorted_terms)}\n")
        f.write(f"# Files scanned: {len(files)}\n")
        f.write("#\n")
        f.write("# For each term:\n")
        f.write("#   term: the canonical display name\n")
        f.write("#   occurrences: total times it appears across all files\n")
        f.write("#   files: number of files it appears in\n")
        f.write("#   chapters: which chapters reference it\n")
        f.write("#   variants: alternative forms found (if any)\n")
        f.write("\n")
        f.write("candidates:\n")

        for entry in sorted_terms:
            display = entry['display']
            # Escape YAML special chars in term
            if ':' in display or '"' in display or "'" in display:
                display_yaml = f'"{display}"'
            else:
                display_yaml = display

            f.write(f"\n  - term: {display_yaml}\n")
            f.write(f"    occurrences: {entry['total_count']}\n")
            f.write(f"    files: {entry['file_count']}\n")

            # Deduplicate chapters while preserving order
            seen_chapters = []
            for ch in entry['chapters']:
                if ch not in seen_chapters:
                    seen_chapters.append(ch)
            chapters_str = ', '.join(seen_chapters)
            f.write(f"    chapters: [{chapters_str}]\n")

            # Show variants if more than one form exists
            if len(entry['variants']) > 1:
                f.write("    variants:\n")
                for variant, vcount in sorted(entry['variants'].items()):
                    if ':' in variant or '"' in variant:
                        variant_yaml = f'"{variant}"'
                    else:
                        variant_yaml = variant
                    f.write(f"      - {variant_yaml} ({vcount})\n")

    print(f"\nCandidates written to {args.output}")
    print(f"Review and add selected terms to glossary_terms.yaml")


if __name__ == '__main__':
    main()
