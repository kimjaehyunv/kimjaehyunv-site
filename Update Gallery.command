#!/bin/bash
cd "$(dirname "$0")"

echo "Update Gallery"
echo "=============="
echo ""
echo "This will automatically:"
echo "  1. Remove files not listed in slides.txt (originals, web JPG, WebP)"
echo "  2. Read originals from images/*/originals/ (originals are never modified)"
echo "  3. Generate optimized web JPG files (new/changed only)"
echo "  4. Generate WebP files (new/changed only)"
echo "  5. Build gallery.json files"
echo "  6. git add → git commit → git push origin main"
echo ""

python3 scripts/build-gallery.py
BUILD_STATUS=$?

if [ $BUILD_STATUS -ne 0 ]; then
  echo ""
  echo "Gallery build failed. Git publish was skipped."
  echo ""
  read -r -p "Press Enter to close..."
  exit $BUILD_STATUS
fi

bash scripts/publish-gallery.sh
PUBLISH_STATUS=$?

echo ""
if [ $PUBLISH_STATUS -eq 0 ]; then
  echo "All done."
  echo "You only manage originals/ JPG files and slides.txt."
else
  echo "Gallery was built, but GitHub publish failed."
  echo "Fix the error above and run Update Gallery.command again."
fi
echo ""
read -r -p "Press Enter to close..."
exit $PUBLISH_STATUS
