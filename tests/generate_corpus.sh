#!/bin/bash

INPUT_DIR="inputs"
OUT_DIR="corpus"

mkdir -p "$OUT_DIR"
count=0

# Temporary associative arrays
declare -A xsl_files
declare -A xml_files

# Collect all .xsl and .xml files recursively
while IFS= read -r -d '' file; do
  base=$(basename "$file")
  name="${base%.*}"
  ext="${base##*.}"

  if [[ "$ext" == "xsl" ]]; then
    xsl_files["$name"]="$file"
  elif [[ "$ext" == "xml" ]]; then
    xml_files["$name"]="$file"
  fi
done < <(find "$INPUT_DIR" -type f \( -iname "*.xsl" -o -iname "*.xml" \) -print0)

# Match and copy only valid pairs
for name in "${!xsl_files[@]}"; do
  if [[ -n "${xml_files[$name]}" ]]; then
    case_dir="$OUT_DIR/case$count"
    mkdir -p "$case_dir"
    cp "${xsl_files[$name]}" "$case_dir/input.xsl"
    cp "${xml_files[$name]}" "$case_dir/fixed.xml"
    echo "✔️  Paired: $name.xsl + $name.xml → $case_dir"
    ((count++))
  fi
done

echo "✅ Done. Created $count matched pairs in '$OUT_DIR'"
