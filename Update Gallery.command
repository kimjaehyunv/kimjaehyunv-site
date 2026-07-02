#!/bin/bash
cd "$(dirname "$0")"
echo "Update Gallery"
echo "=============="
echo ""
echo "This will:"
echo "  1. Detect new/changed JPG files listed in slides.txt"
echo "  2. Optimize JPG images for web delivery"
echo "  3. Generate WebP files automatically"
echo "  4. Build gallery.json files"
echo ""
python3 scripts/build-gallery.py
status=$?
echo ""
if [ $status -eq 0 ]; then
  echo "Done."
  echo "You only need to manage JPG files and slides.txt."
  echo "Upload the changes to GitHub to publish the site."
else
  echo "Update failed. Check the error messages above."
fi
echo ""
read -r -p "Press Enter to close..."
