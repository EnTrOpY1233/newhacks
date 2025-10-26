#!/bin/bash
# Script to organize markdown documentation files

echo "=========================================="
echo "   Organizing Markdown Documentation"
echo "=========================================="
echo ""

# Create md directory if it doesn't exist
if [ ! -d "md" ]; then
    mkdir -p md
    echo "✓ Created 'md' directory"
else
    echo "✓ 'md' directory already exists"
fi

echo ""
echo "Moving markdown files..."
echo ""

# Counter for moved files
moved=0

# Find all .md files in the root directory (not in subdirectories)
# Exclude README.md
for file in *.md; do
    # Check if file exists and is not README.md
    if [ -f "$file" ] && [ "$file" != "README.md" ]; then
        echo "  Moving: $file → md/$file"
        mv "$file" "md/$file"
        ((moved++))
    fi
done

# Find markdown files in subdirectories (optional - uncomment if needed)
# Exclude node_modules, venv, and .git directories
# for file in $(find . -name "*.md" -type f \
#     -not -path "./README.md" \
#     -not -path "./node_modules/*" \
#     -not -path "./venv/*" \
#     -not -path "./.git/*" \
#     -not -path "./md/*"); do
#     # Get the filename without path
#     filename=$(basename "$file")
#     # Skip if it's README.md
#     if [ "$filename" != "README.md" ]; then
#         echo "  Moving: $file → md/$filename"
#         mv "$file" "md/$filename"
#         ((moved++))
#     fi
# done

echo ""
echo "=========================================="
echo "✓ Moved $moved markdown file(s)"
echo "=========================================="
echo ""

# List files in md directory
if [ $moved -gt 0 ]; then
    echo "Contents of md/ directory:"
    echo ""
    ls -1 md/ | sed 's/^/  - /'
    echo ""
fi

echo "Done! README.md remains in the root directory."

