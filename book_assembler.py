#!/usr/bin/env python3
"""
MUSH Book Series Assembler

Assembles individual markdown files into complete book manuscripts or volumes,
handling ordering, cross-references, and preparation for pandoc conversion.
"""

import os
import re
import yaml
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass

try:
    from glossary_build import (
        load_glossary_terms, build_search_patterns,
        get_volume_files, scan_volume,
        generate_glossary_md, generate_index_md,
    )
    HAS_GLOSSARY = True
except ImportError:
    HAS_GLOSSARY = False


@dataclass
class BookConfig:
    """Configuration for book assembly."""
    title: str
    subtitle: str
    author: str
    description: str
    publisher: str = ""
    copyright_year: str = "2026"
    cover_image: str = "cover.png"

    # Chapter organization
    include_files: List[str] = None
    exclude_files: List[str] = None

    # Output settings
    output_format: str = "both"  # "epub", "pdf", "both"
    output_dir: str = "book_output"


@dataclass
class VolumeConfig:
    """Configuration for individual volumes."""
    volume_number: int
    title: str
    subtitle: str
    description: str
    include_files: List[str]
    output_name: str
    exclude_files: List[str] = None


@dataclass
class MultiVolumeConfig:
    """Configuration for multi-volume assembly."""
    title: str
    subtitle: str
    author: str
    description: str
    publisher: str = ""
    copyright_year: str = "2026"
    volumes: List[VolumeConfig] = None
    output_format: str = "both"
    base_output_dir: str = "book_output"
    cover_image_prefix: str = "cover_vol"
    pdf_profile: str = "trade"
    pdf_profiles: Dict[str, Dict] = None


class BookAssembler:
    """Assembles markdown content into a book or volumes."""

    def __init__(self, config_file: str = "volume_config.yaml", volume_mode: bool = True):
        self.config_file = Path(config_file)
        self.volume_mode = volume_mode

        if volume_mode:
            self.config = self._load_volume_config()
        else:
            self.config = self._load_config()

        # Create output directory
        if volume_mode:
            self.base_output_dir = Path(self.config.base_output_dir)
            self.base_output_dir.mkdir(exist_ok=True)
        else:
            self.output_dir = Path(self.config.output_dir)
            self.output_dir.mkdir(exist_ok=True)

    def _load_config(self) -> BookConfig:
        """Load configuration from YAML file."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                data = yaml.safe_load(f)
            return BookConfig(**data)
        else:
            raise FileNotFoundError(f"Config file {self.config_file} not found.")

    def _load_volume_config(self) -> MultiVolumeConfig:
        """Load volume configuration from YAML file."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                data = yaml.safe_load(f)

            # Convert volume data to VolumeConfig objects
            volumes = []
            for vol_data in data.get('volumes', []):
                volumes.append(VolumeConfig(**vol_data))

            # Remove volumes from data to avoid duplicate key error
            config_data = {k: v for k, v in data.items() if k != 'volumes'}
            config_data['volumes'] = volumes

            return MultiVolumeConfig(**config_data)
        else:
            raise FileNotFoundError(f"Volume config file {self.config_file} not found")

    def get_files_to_include(self, include_patterns: List[str], exclude_patterns: List[str] = None) -> List[Path]:
        """Get ordered list of files to include based on patterns."""
        all_files = []

        if include_patterns:
            for pattern in include_patterns:
                files = sorted(Path(".").glob(pattern))
                all_files.extend(files)
        else:
            # Default: all numbered markdown files
            all_files = sorted(Path(".").glob("[0-9][0-9]-*.md"))

        # Filter out excluded files
        if exclude_patterns:
            filtered_files = []
            for file_path in all_files:
                exclude = False
                for pattern in exclude_patterns:
                    if file_path.match(pattern):
                        exclude = True
                        break
                if not exclude:
                    filtered_files.append(file_path)
            all_files = filtered_files

        # Remove duplicates while preserving order
        seen = set()
        unique_files = []
        for f in all_files:
            if f not in seen:
                seen.add(f)
                unique_files.append(f)

        return unique_files

    def create_front_matter(self, title: str, subtitle: str, author: str,
                          description: str, publisher: str, copyright_year: str,
                          cover_image: str, volume_number: Optional[int] = None) -> str:
        """Create front matter for the book."""
        if volume_number:
            book_title = f"{self.config.title} Volume {volume_number}"
        else:
            book_title = title

        return f"""---
title: "{book_title}"
subtitle: "{subtitle}"
author: "{author}"
description: "{description}"
publisher: "{publisher}"
rights: "Copyright {copyright_year} {author}"
cover-image: "{cover_image}"
stylesheet: "book-style.css"
lang: "en-US"
toc: true
toc-depth: 3
---

"""

    def create_introduction(self, volume_number: Optional[int] = None) -> str:
        """Create an introduction/preface for the book or volume."""
        introduction_content = ""

        # For Volume 1, include the preface
        if volume_number == 1:
            preface_file = "0-00-00-Preface.md"
            if os.path.exists(preface_file):
                with open(preface_file, 'r') as f:
                    preface_content = f.read()
                    if preface_content.startswith('---'):
                        parts = preface_content.split('---', 2)
                        if len(parts) >= 3:
                            preface_content = parts[2].strip()
                    introduction_content = preface_content + "\n\n\\newpage\n\n"
                    print(f"  Including preface for Volume 1")

        # Try to read from volume-specific introduction file
        if volume_number:
            intro_file = f"{volume_number}-00-00-Volume{volume_number}Introduction.md"
            if os.path.exists(intro_file):
                with open(intro_file, 'r') as f:
                    content = f.read()
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            content = parts[2].strip()
                    introduction_content += content
                    return introduction_content
            else:
                print(f"  Introduction file not found: {intro_file}")
                return introduction_content
        else:
            intro_file = "00-00-Introduction.md"
            if os.path.exists(intro_file):
                with open(intro_file, 'r') as f:
                    content = f.read()
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            content = parts[2].strip()
                    return content
            else:
                return ""

    def process_content(self, content: str, file_path: Path, footnote_offset: int = 0) -> Tuple[str, int]:
        """Process individual file content for book integration.

        Returns: (processed_content, number_of_footnotes_in_this_chapter)
        """
        # Strip YAML front matter from individual files
        content = self._strip_yaml_front_matter(content)

        # Renumber footnotes if needed
        if footnote_offset > 0:
            content, num_footnotes = self._renumber_footnotes(content, footnote_offset)
        else:
            # Count footnotes even if not renumbering
            num_footnotes = len(re.findall(r'\[\^(\d+)\]:', content))

        # Fix cross-references between files
        content = self._fix_cross_references(content)

        # Ensure proper chapter breaks
        content = self._ensure_chapter_breaks(content)

        return content, num_footnotes

    def _fix_cross_references(self, content: str) -> str:
        """Fix cross-references that might break in book format."""
        return content

    def _strip_yaml_front_matter(self, content: str) -> str:
        """Strip YAML front matter from individual files to avoid conflicts."""
        lines = content.split('\n')
        if lines and lines[0].strip() == '---':
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    return '\n'.join(lines[i+1:])
        return content

    def _ensure_chapter_breaks(self, content: str) -> str:
        """Ensure proper chapter breaks for book format."""
        content = re.sub(r'^(# [^#])', r'\\cleardoublepage\n\n\1', content, flags=re.MULTILINE)
        content = re.sub(r'^(## [^#])', r'\\newpage\n\n\1', content, flags=re.MULTILINE)
        return content

    def _renumber_footnotes(self, content: str, offset: int) -> Tuple[str, int]:
        """Renumber footnotes in content starting from offset+1."""
        footnote_refs = re.findall(r'\[\^(\d+)\](?!:)', content)
        footnote_defs = re.findall(r'\[\^(\d+)\]:', content)

        seen = set()
        unique_nums = []
        for num in footnote_refs:
            if num not in seen:
                seen.add(num)
                unique_nums.append(num)

        for num in sorted(set(footnote_defs) - seen, key=int):
            unique_nums.append(num)
            seen.add(num)

        mapping = {}
        for i, old_num in enumerate(unique_nums):
            mapping[old_num] = str(offset + i + 1)

        result = content
        for old_num, new_num in mapping.items():
            result = re.sub(rf'\[\^{old_num}\](?!:)', f'[^{new_num}]', result)
            result = re.sub(rf'\[\^{old_num}\]:', f'[^{new_num}]:', result)

        return result, len(unique_nums)

    def assemble_book(self, include_files: List[str], exclude_files: List[str] = None,
                     title: str = None, subtitle: str = None, description: str = None,
                     volume_number: Optional[int] = None) -> str:
        """Assemble files into a single book manuscript."""
        if not title:
            title = self.config.title
        if not subtitle:
            subtitle = self.config.subtitle
        if not description:
            description = self.config.description

        print(f"Assembling {'volume ' + str(volume_number) if volume_number else 'book'}...")

        files = self.get_files_to_include(include_files, exclude_files)

        # Filter out introduction files already handled by create_introduction()
        if volume_number:
            intro_name = f"{volume_number}-00-00-Volume{volume_number}Introduction.md"
        else:
            intro_name = "00-00-Introduction.md"
        files = [f for f in files if f.name != intro_name]

        print(f"Including {len(files)} files")

        # Determine cover image
        if volume_number and hasattr(self.config, 'cover_image_prefix'):
            cover_image = f"{self.config.cover_image_prefix}{volume_number}.png"
        else:
            cover_image = getattr(self.config, 'cover_image', 'cover.png')

        # Start with front matter
        book_content = self.create_front_matter(
            title, subtitle, self.config.author, description,
            self.config.publisher, self.config.copyright_year,
            cover_image, volume_number
        )
        book_content += self.create_introduction(volume_number)

        # Add each file's content
        footnote_offset = 0

        for file_path in files:
            print(f"  Processing {file_path.name}")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                processed_content, num_footnotes = self.process_content(content, file_path, footnote_offset)
                footnote_offset += num_footnotes

                book_content += "\n\n---\n\n"
                book_content += processed_content
                book_content += "\n\n"

            except Exception as e:
                print(f"  Error processing {file_path}: {e}")
                continue

        return book_content

    def create_metadata_files(self, output_dir: Path, title: str, subtitle: str,
                            description: str, cover_image: str) -> None:
        """Create metadata files for pandoc conversion."""
        epub_meta = {
            'title': title,
            'subtitle': subtitle,
            'author': self.config.author,
            'description': description,
            'publisher': self.config.publisher,
            'rights': f'Copyright {self.config.copyright_year} {self.config.author}',
            'cover-image': cover_image,
            'stylesheet': 'book-style.css',
            'lang': 'en-US',
            'toc': True,
            'toc-depth': 3,
            'split-level': 1,
            'epub-metadata': f'<dc:type>Text</dc:type><dc:language>en-US</dc:language>'
        }

        with open(output_dir / 'epub-meta.yaml', 'w') as f:
            yaml.dump(epub_meta, f, default_flow_style=False)

        css_path = output_dir / 'book-style.css'
        if not css_path.exists():
            css_content = """
/* Book styling for MUSH Book Series */
body {
    font-family: "Georgia", "Times New Roman", serif;
    line-height: 1.6;
    margin: 0;
    padding: 1em;
}

h1, h2, h3, h4, h5, h6 {
    font-family: "Arial", "Helvetica", sans-serif;
    color: #333;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

h1 {
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
}

blockquote {
    border-left: 4px solid #ccc;
    margin: 1em 0;
    padding-left: 1em;
    font-style: italic;
}

code {
    background-color: #f5f5f5;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: "Courier New", monospace;
}

pre {
    background-color: #f5f5f5;
    padding: 1em;
    border-radius: 5px;
    overflow-x: auto;
    border: 1px solid #ddd;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Footnotes */
.footnote {
    font-size: 0.9em;
    line-height: 1.4;
}

/* Tables for function/command references */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ccc;
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #f0f0f0;
    font-weight: bold;
}
"""
            with open(css_path, 'w') as f:
                f.write(css_content)

    def copy_cover_image(self, output_dir: Path, cover_image: str) -> bool:
        """Copy cover image from top-level directory to output directory."""
        source_path = Path(cover_image)
        if source_path.exists():
            dest_path = output_dir / cover_image
            try:
                shutil.copy2(source_path, dest_path)
                print(f"  Copied cover image: {cover_image}")
                return True
            except Exception as e:
                print(f"  Failed to copy cover image {cover_image}: {e}")
                return False
        else:
            print(f"  Cover image not found: {cover_image}")
            return False

    def generate_back_matter(self, vol_dict: Dict, volume_dir: Path) -> str:
        """Generate glossary and index back matter for a volume."""
        back = ""

        if HAS_GLOSSARY:
            try:
                terms = load_glossary_terms()
                if terms:
                    patterns = build_search_patterns(terms)
                    volume_files = get_volume_files({
                        'include_files': vol_dict['include_files'],
                    })
                    if volume_files:
                        term_chapters = scan_volume(volume_files, patterns)
                        vol_title = vol_dict['title']
                        glossary_md = generate_glossary_md(terms, term_chapters, vol_title)
                        index_md = generate_index_md(terms, term_chapters, vol_title)
                        back += "\n\n\\newpage\n\n" + glossary_md
                        back += "\n\n\\newpage\n\n" + index_md
                        print(f"  Generated glossary ({len(term_chapters)} terms) and index")
                        return back
            except Exception as e:
                print(f"  Warning: glossary generation failed: {e}")

        for name in ('glossary.md', 'index.md'):
            path = volume_dir / name
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    back += "\n\n\\newpage\n\n" + f.read()
                print(f"  Including pre-existing {name}")

        return back

    def _get_pdf_profile(self) -> Dict[str, str]:
        """Return the active PDF profile settings from config."""
        defaults = {
            'papersize': '{6in,9in}', 'inner': '0.75in', 'outer': '0.5in',
            'top': '0.5in', 'bottom': '0.75in', 'footskip': '0.5in',
            'fontsize': '10pt', 'documentclass': 'book', 'classoption': 'openright',
        }
        if not hasattr(self.config, 'pdf_profiles') or not self.config.pdf_profiles:
            return defaults
        profile_name = getattr(self.config, 'pdf_profile', 'trade')
        profile = self.config.pdf_profiles.get(profile_name)
        if not profile:
            print(f"  PDF profile '{profile_name}' not found, using trade defaults")
            return defaults
        result = dict(defaults)
        for k in defaults:
            if k in profile:
                result[k] = str(profile[k])
        return result

    def generate_conversion_scripts(self, output_dir: Path, output_base: str,
                                  cover_image: str = "cover.png") -> None:
        """Generate pandoc conversion scripts."""
        p = self._get_pdf_profile()
        ps = p['papersize']
        ps_part = f"papersize={ps}" if '{' in ps else ps
        geo = (f"{ps_part},inner={p['inner']},outer={p['outer']},"
               f"top={p['top']},bottom={p['bottom']},footskip={p['footskip']}")
        pdf_vars = (
            f'    --variable=geometry:"{geo}" \\\n'
            f"    --variable=fontsize:{p['fontsize']} \\\n"
            f"    --variable=linkcolor:blue \\\n"
            f"    --variable=documentclass:{p['documentclass']} \\\n"
            f"    --variable=classoption:{p['classoption']} \\\n"
            f"    --variable=pagestyle:plain \\"
        )

        epub_script = f"""#!/bin/bash
# Convert to EPUB using Docker pandoc

echo "Converting to EPUB..."
COVER_ARG=""
if [ -s "{cover_image}" ]; then
    COVER_ARG="--epub-cover-image={cover_image}"
fi
docker run --rm -v $(pwd):/data pandoc \\
    -s -f markdown -t epub3 \\
    --metadata-file=epub-meta.yaml \\
    --toc --toc-depth=3 \\
    --split-level=1 \\
    --standalone \\
    $COVER_ARG \\
    --css=book-style.css \\
    book_manuscript.md \\
    -o "{output_base}.epub"

echo "EPUB generated: {output_base}.epub"
"""

        pdf_script = f"""#!/bin/bash
# Convert to PDF using Docker pandoc

echo "Converting to PDF..."

docker run --rm -v $(pwd):/data pandoc \\
    -s -f markdown -t pdf \\
    --metadata-file=epub-meta.yaml \\
    --toc --toc-depth=3 \\
    --pdf-engine=xelatex \\
{pdf_vars}
    book_manuscript.md \\
    -o "{output_base}.pdf"

echo "PDF generated: {output_base}.pdf"
"""

        both_script = f"""#!/bin/bash
# Convert to both EPUB and PDF using Docker pandoc

OUTPUT_BASE="{output_base}"

echo "Converting to EPUB..."
COVER_ARG=""
if [ -s "{cover_image}" ]; then
    COVER_ARG="--epub-cover-image={cover_image}"
fi
docker run --rm -v $(pwd):/data pandoc \\
    -s -f markdown -t epub3 \\
    --metadata-file=epub-meta.yaml \\
    --toc --toc-depth=3 \\
    --split-level=1 \\
    --standalone \\
    $COVER_ARG \\
    --css=book-style.css \\
    book_manuscript.md \\
    -o "${{OUTPUT_BASE}}.epub"

echo "EPUB generated: ${{OUTPUT_BASE}}.epub"

echo "Converting to PDF..."
docker run --rm -v $(pwd):/data pandoc \\
    -s -f markdown -t pdf \\
    --metadata-file=epub-meta.yaml \\
    --toc --toc-depth=3 \\
    --pdf-engine=xelatex \\
{pdf_vars}
    book_manuscript.md \\
    -o "${{OUTPUT_BASE}}.pdf"

echo "PDF generated: ${{OUTPUT_BASE}}.pdf"
echo "Both formats generated successfully!"
"""

        scripts = {
            'convert_to_epub.sh': epub_script,
            'convert_to_pdf.sh': pdf_script,
            'convert_to_both.sh': both_script
        }

        for script_name, script_content in scripts.items():
            script_path = output_dir / script_name
            with open(script_path, 'w') as f:
                f.write(script_content)
            script_path.chmod(0o755)

    def run_volumes(self) -> None:
        """Run the complete assembly process for multiple volumes."""
        print(f"Assembling {len(self.config.volumes)} volumes of: {self.config.title}")

        for volume in self.config.volumes:
            print(f"\nProcessing Volume {volume.volume_number}: {volume.title}")

            volume_dir = self.base_output_dir / f"volume_{volume.volume_number}"
            volume_dir.mkdir(exist_ok=True)

            book_content = self.assemble_book(
                volume.include_files,
                volume.exclude_files,
                volume.title,
                volume.subtitle,
                volume.description,
                volume.volume_number
            )

            vol_dict = {
                'title': volume.title,
                'include_files': volume.include_files,
                'volume_number': volume.volume_number,
            }
            book_content += self.generate_back_matter(vol_dict, volume_dir)

            manuscript_path = volume_dir / 'book_manuscript.md'
            with open(manuscript_path, 'w', encoding='utf-8') as f:
                f.write(book_content)

            print(f"Volume {volume.volume_number} manuscript saved: {manuscript_path}")

            cover_image = f"{self.config.cover_image_prefix}{volume.volume_number}.png"

            self.create_metadata_files(
                volume_dir,
                f"{volume.title}",
                volume.subtitle,
                volume.description,
                cover_image
            )
            self.copy_cover_image(volume_dir, cover_image)

            self.generate_conversion_scripts(
                volume_dir,
                volume.output_name,
                cover_image
            )

        # Create a master conversion script
        num_volumes = len(self.config.volumes)
        master_script = f"""#!/bin/bash
# Convert all volumes to both EPUB and PDF

echo "Converting all volumes..."

for i in {{1..{num_volumes}}}; do
    echo ""
    echo "Processing Volume $i..."
    if [ -d "volume_$i" ]; then
        cd "volume_$i"
        if [ -f "convert_to_both.sh" ]; then
            ./convert_to_both.sh
        else
            echo "No conversion script found for Volume $i"
        fi
        cd ..
    else
        echo "Volume $i directory not found"
    fi
done

echo ""
echo "All volumes processed!"
"""

        master_script_path = self.base_output_dir / 'convert_all_volumes.sh'
        with open(master_script_path, 'w') as f:
            f.write(master_script)
        master_script_path.chmod(0o755)

        print(f"\nBase output directory: {self.base_output_dir}")
        for volume in self.config.volumes:
            print(f"  volume_{volume.volume_number}/")
        print("  convert_all_volumes.sh")
        print(f"\nRun: cd {self.base_output_dir} && ./convert_all_volumes.sh")

    def run(self) -> None:
        """Run the appropriate assembly process based on configuration."""
        if self.volume_mode:
            self.run_volumes()
        else:
            self.run_single_book()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Assemble MUSH book content into volumes")
    parser.add_argument("--config", default="volume_config.yaml", help="Config file")
    parser.add_argument("--volumes", action="store_true", default=True, help="Use volume mode")
    parser.add_argument("--volume-config", default="volume_config.yaml", help="Volume config file")

    args = parser.parse_args()

    assembler = BookAssembler(args.volume_config, volume_mode=True)
    assembler.run()


if __name__ == "__main__":
    main()
