#!/bin/bash
# Copy book artifacts to Samba share for Windows access

DEST="/ztank/secret/samba/other"
SRC="book_output"

echo "Copying artifacts to $DEST..."

# EPUBs
for f in $(find "$SRC" -name '*.epub' -print); do
    cp "$f" "$DEST/"
    echo "  $(basename "$f")"
done

# PDFs
for f in $(find "$SRC" -name '*.pdf' -print); do
    cp "$f" "$DEST/"
    echo "  $(basename "$f")"
done

# Manuscripts
for i in 1 2; do
    src="$SRC/volume_$i/book_manuscript.md"
    if [ -f "$src" ]; then
        cp "$src" "$DEST/mush_volume$i.md"
        echo "  mush_volume$i.md"
    fi
done

echo "Done."
