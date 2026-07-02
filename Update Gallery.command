#!/bin/bash
cd "$(dirname "$0")"
echo "Updating gallery from slides.txt..."
echo ""
python3 scripts/build-gallery.py
status=$?
echo ""
if [ $status -eq 0 ]; then
  echo "Done. gallery.json files were updated."
  echo "Upload the changes to GitHub to publish the site."
else
  echo "Update failed. Check the error messages above."
fi
echo ""
read -r -p "Press Enter to close..."
