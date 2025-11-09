# JSON to Figma - Validation and Conversion Scripts

This directory contains utility scripts to help validate and convert JSON files before importing them into Figma.

## Scripts Overview

### 1. validate_json.py

Validates JSON files for common issues that would cause import failures or rendering problems.

**What it checks:**
- ✅ Invalid `counterAxisAlignItems` values (e.g., "STRETCH")
- ✅ Missing `layoutAlign` on elements with `primaryAxisSizingMode: "FIXED"`
- ✅ Unsupported SVG path commands (Arc, relative commands, etc.)
- ✅ Common configuration errors

**Usage:**

```bash
# Validate a single file
python scripts/validate_json.py examples/login-page.json

# Validate multiple files
python scripts/validate_json.py examples/*.json

# Validate all example files
python scripts/validate_json.py examples/login-page.json examples/dashboard-card.json examples/mobile-profile.json
```

**Example Output:**

```
🔍 Validating: login-page.json
============================================================

❌ Found 2 error(s):

❌ root > FRAME[Form] > FRAME[Email Field]
   Issue: primaryAxisSizingMode: "FIXED" without explicit width or layoutAlign
   Fix: Add "width" property or "layoutAlign": "STRETCH"

❌ root > FRAME[Container]/vectorPaths[0]
   Issue: Arc command (A) is not supported by Figma
   Fix: Convert arc commands to cubic bezier curves (C). See vector-construction.md
```

### 2. convert_svg_paths.py

Converts SVG path commands to Figma-compatible format by:
- Converting Arc commands (A) to Cubic Bezier curves (C)
- Converting relative commands to absolute commands
- Converting H/V commands to L commands
- Converting S/T commands to C/Q commands

**Usage:**

```bash
# Convert a single path string
python scripts/convert_svg_paths.py "M 12 2 A 10 10 0 1 1 12 22 Z"

# Convert all paths in a JSON file
python scripts/convert_svg_paths.py --file examples/mobile-profile.json --output examples/mobile-profile-fixed.json

# Convert in-place (overwrites original)
python scripts/convert_svg_paths.py --file examples/mobile-profile.json --output examples/mobile-profile.json
```

**Example Output:**

```
Converting paths in examples/mobile-profile.json...
✅ Converted 2 path(s)

Modified paths:
  - root/children[0]/vectorPaths[0]
  - root/children[0]/fillGeometry[0]

Saved to examples/mobile-profile-fixed.json
```

**Single Path Conversion Example:**

```bash
$ python scripts/convert_svg_paths.py "M 12 2 A 10 10 0 1 1 12 22 Z"

Original:
  M 12 2 A 10 10 0 1 1 12 22 Z

Converted:
  M 12.0 2.0 C 17.522847498307933 2.0 22.0 6.477152501692066 22.0 12.0 C 22.0 17.522847498307933 17.522847498307933 22.0 12.0 22.0 C 6.477152501692066 22.0 2.0 17.522847498307933 2.0 12.0 C 2.0 6.477152501692066 6.477152501692066 2.0 12.0 2.0 Z
```

## Recommended Workflow

### Before Importing to Figma

1. **Generate your JSON** using the json2figma-skill

2. **Validate the JSON**:
   ```bash
   python scripts/validate_json.py your-file.json
   ```

3. **Fix any errors** reported by the validator:
   - Add missing `layoutAlign: "STRETCH"` properties
   - Change invalid `counterAxisAlignItems: "STRETCH"` to `"MIN"` or other valid values
   - Convert unsupported path commands

4. **Convert SVG paths** (if needed):
   ```bash
   python scripts/convert_svg_paths.py --file your-file.json --output your-file-fixed.json
   ```

5. **Validate again** to ensure all issues are resolved:
   ```bash
   python scripts/validate_json.py your-file-fixed.json
   ```

6. **Import to Figma** using the json2figma plugin

### Quick Check Commands

```bash
# Check for invalid counterAxisAlignItems
grep -n '"counterAxisAlignItems": "STRETCH"' your-file.json

# Check for primaryAxisSizingMode: "FIXED" without width or layoutAlign
grep -B5 -A5 '"primaryAxisSizingMode": "FIXED"' your-file.json | grep -v '"width"' | grep -v '"layoutAlign"'

# Check for Arc commands in paths
grep -n '"data":.*A ' your-file.json

# Check for relative path commands (lowercase)
grep -n '"data":.*[mlhvcsqtaz]' your-file.json
```

## Common Issues and Solutions

### Issue 1: Element width is only 100px

**Cause:** `primaryAxisSizingMode: "FIXED"` without explicit `width` or `layoutAlign`

**Solution:**
```json
{
  "type": "FRAME",
  "name": "Header",
  "primaryAxisSizingMode": "FIXED",
  "layoutAlign": "STRETCH"  // ← Add this
}
```

### Issue 2: Invalid counterAxisAlignItems value

**Cause:** Using `"STRETCH"` which is not a valid value

**Solution:**
```json
{
  "layoutMode": "VERTICAL",
  "counterAxisAlignItems": "MIN"  // ← Change from "STRETCH" to "MIN"
}
```

### Issue 3: Vector path with Arc command fails

**Cause:** Figma doesn't support SVG Arc commands (A)

**Solution:**
```bash
# Use the conversion script
python scripts/convert_svg_paths.py --file your-file.json --output your-file-fixed.json
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Troubleshooting

### Script not found

Make sure you're running the command from the `json2figma-skill` directory:

```bash
cd /path/to/json2figma-skill
python scripts/validate_json.py examples/login-page.json
```

### Permission denied

On Unix-like systems, you may need to make the scripts executable:

```bash
chmod +x scripts/validate_json.py
chmod +x scripts/convert_svg_paths.py
```

Then you can run them directly:

```bash
./scripts/validate_json.py examples/login-page.json
```

### Python version issues

Check your Python version:

```bash
python --version  # or python3 --version
```

If you have multiple Python versions, use `python3` explicitly:

```bash
python3 scripts/validate_json.py examples/login-page.json
```

## Contributing

If you find additional validation rules that would be helpful, please:
1. Add them to `validate_json.py`
2. Update this README with examples
3. Add test cases if possible

## Related Documentation

- [faq-best-practices.md](../references/faq-best-practices.md) - Common issues and solutions
- [vector-construction.md](../references/vector-construction.md) - Vector path construction guide
- [figma-api-schema.md](../references/figma-api-schema.md) - Complete API reference
- [generation-checklist.md](../references/generation-checklist.md) - JSON generation checklist
