#!/usr/bin/env python3
"""
JSON to Figma Validation Script

This script validates JSON files for common issues before importing into Figma.
It checks for:
1. Invalid counterAxisAlignItems values
2. Missing layoutAlign on elements with primaryAxisSizingMode: "FIXED"
3. Unsupported SVG path commands (Arc, relative commands, etc.)
4. Common configuration errors

Usage:
    python validate_json.py <json_file>
    python validate_json.py examples/*.json
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ValidationError:
    """Represents a validation error with location and fix suggestion"""

    def __init__(self, path: str, issue: str, fix: str, severity: str = "error"):
        self.path = path
        self.issue = issue
        self.fix = fix
        self.severity = severity

    def __str__(self):
        icon = "❌" if self.severity == "error" else "⚠️"
        return f"{icon} {self.path}\n   Issue: {self.issue}\n   Fix: {self.fix}\n"


class FigmaJSONValidator:
    """Validates Figma JSON for common issues"""

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

        # Valid values for Figma properties
        self.valid_counter_axis_align = {"MIN", "CENTER", "MAX", "BASELINE"}
        self.valid_primary_axis_align = {"MIN", "CENTER", "MAX", "SPACE_BETWEEN"}

        # Unsupported SVG path commands
        self.unsupported_path_commands = re.compile(r'\b[AaHhVvSsTt]\b')
        self.relative_commands = re.compile(r'\b[mlhvcsqtaz]\b')

    def validate_file(self, filepath: Path) -> bool:
        """Validate a JSON file and return True if valid"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"\n🔍 Validating: {filepath.name}")
            print("=" * 60)

            self.errors = []
            self.warnings = []

            self._validate_node(data, "root")

            # Print results
            if self.errors:
                print(f"\n❌ Found {len(self.errors)} error(s):\n")
                for error in self.errors:
                    print(error)

            if self.warnings:
                print(f"\n⚠️  Found {len(self.warnings)} warning(s):\n")
                for warning in self.warnings:
                    print(warning)

            if not self.errors and not self.warnings:
                print("✅ No issues found!\n")
                return True

            return len(self.errors) == 0

        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return False
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False

    def _validate_node(self, node: Dict[str, Any], path: str):
        """Recursively validate a node and its children"""
        if not isinstance(node, dict):
            return

        node_type = node.get("type", "UNKNOWN")
        node_name = node.get("name", "unnamed")
        current_path = f"{path} > {node_type}[{node_name}]"

        # Check counterAxisAlignItems
        if "counterAxisAlignItems" in node:
            value = node["counterAxisAlignItems"]
            if value not in self.valid_counter_axis_align:
                self.errors.append(ValidationError(
                    current_path,
                    f'Invalid counterAxisAlignItems: "{value}"',
                    f'Use one of: {", ".join(sorted(self.valid_counter_axis_align))}'
                ))

        # Check primaryAxisSizingMode: "FIXED" without width or layoutAlign
        if node.get("primaryAxisSizingMode") == "FIXED":
            has_width = "width" in node
            has_height = "height" in node
            has_layout_align = "layoutAlign" in node

            # For horizontal layouts, check width
            parent_layout = self._get_parent_layout_mode(node)
            if parent_layout == "VERTICAL" and not has_width and not has_layout_align:
                self.warnings.append(ValidationError(
                    current_path,
                    'primaryAxisSizingMode: "FIXED" without explicit width or layoutAlign',
                    'Add "width" property or "layoutAlign": "STRETCH"',
                    "warning"
                ))
            elif parent_layout == "HORIZONTAL" and not has_height and not has_layout_align:
                self.warnings.append(ValidationError(
                    current_path,
                    'primaryAxisSizingMode: "FIXED" without explicit height or layoutAlign',
                    'Add "height" property or "layoutAlign": "STRETCH"',
                    "warning"
                ))

        # Check for elements that commonly need layoutAlign: "STRETCH"
        if self._should_have_layout_align(node) and "layoutAlign" not in node:
            self.warnings.append(ValidationError(
                current_path,
                f'{node_type} element may need layoutAlign',
                'Consider adding "layoutAlign": "STRETCH" if it should fill parent width',
                "warning"
            ))

        # Check vector paths for unsupported commands
        self._validate_vector_paths(node, current_path)

        # Check fillGeometry for unsupported commands
        self._validate_fill_geometry(node, current_path)

        # Validate children recursively
        if "children" in node and isinstance(node["children"], list):
            for i, child in enumerate(node["children"]):
                self._validate_node(child, f"{current_path}/children[{i}]")

    def _get_parent_layout_mode(self, node: Dict[str, Any]) -> str:
        """Determine parent layout mode (simplified - would need full tree context)"""
        # This is a simplified check - in reality we'd need to track parent context
        return "VERTICAL"  # Default assumption

    def _should_have_layout_align(self, node: Dict[str, Any]) -> bool:
        """Check if node type commonly needs layoutAlign"""
        node_type = node.get("type")
        node_name = node.get("name", "").lower()

        # Common patterns that need layoutAlign
        common_patterns = [
            "header", "footer", "divider", "separator",
            "button", "input", "field", "menu", "item"
        ]

        # Check if it's a container type with fixed sizing
        is_container = node_type in {"FRAME", "COMPONENT"}
        has_fixed_sizing = node.get("primaryAxisSizingMode") == "FIXED"
        matches_pattern = any(pattern in node_name for pattern in common_patterns)

        return is_container and has_fixed_sizing and matches_pattern

    def _validate_vector_paths(self, node: Dict[str, Any], path: str):
        """Validate vectorPaths for unsupported commands"""
        if "vectorPaths" not in node:
            return

        for i, vector_path in enumerate(node["vectorPaths"]):
            if not isinstance(vector_path, dict):
                continue

            data = vector_path.get("data", "")

            # Check for Arc commands
            if re.search(r'\bA\b', data):
                self.errors.append(ValidationError(
                    f"{path}/vectorPaths[{i}]",
                    'Arc command (A) is not supported by Figma',
                    'Convert arc commands to cubic bezier curves (C). See vector-construction.md'
                ))

            # Check for relative commands
            if self.relative_commands.search(data):
                self.errors.append(ValidationError(
                    f"{path}/vectorPaths[{i}]",
                    'Relative path commands (lowercase) are not supported',
                    'Convert to absolute commands (uppercase): m→M, l→L, c→C, etc.'
                ))

            # Check for other unsupported commands
            unsupported = self.unsupported_path_commands.findall(data)
            if unsupported:
                commands = ", ".join(set(unsupported))
                self.errors.append(ValidationError(
                    f"{path}/vectorPaths[{i}]",
                    f'Unsupported path commands: {commands}',
                    'Use only M, L, C, Q, Z commands. Convert H/V to L, S/T to C/Q'
                ))

    def _validate_fill_geometry(self, node: Dict[str, Any], path: str):
        """Validate fillGeometry for unsupported commands"""
        if "fillGeometry" not in node:
            return

        for i, geometry in enumerate(node["fillGeometry"]):
            if not isinstance(geometry, dict):
                continue

            data = geometry.get("data", "")

            # Check for Arc commands
            if re.search(r'\bA\b', data):
                self.errors.append(ValidationError(
                    f"{path}/fillGeometry[{i}]",
                    'Arc command (A) is not supported by Figma',
                    'Convert arc commands to cubic bezier curves (C). See vector-construction.md'
                ))

            # Check for relative commands
            if self.relative_commands.search(data):
                self.errors.append(ValidationError(
                    f"{path}/fillGeometry[{i}]",
                    'Relative path commands (lowercase) are not supported',
                    'Convert to absolute commands (uppercase): m→M, l→L, c→C, etc.'
                ))


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python validate_json.py <json_file> [json_file2 ...]")
        print("\nExample:")
        print("  python validate_json.py examples/login-page.json")
        print("  python validate_json.py examples/*.json")
        sys.exit(1)

    validator = FigmaJSONValidator()
    all_valid = True

    for filepath_str in sys.argv[1:]:
        filepath = Path(filepath_str)
        if not filepath.exists():
            print(f"❌ File not found: {filepath}")
            all_valid = False
            continue

        if not validator.validate_file(filepath):
            all_valid = False

    print("\n" + "=" * 60)
    if all_valid:
        print("✅ All files passed validation!")
        sys.exit(0)
    else:
        print("❌ Some files have errors. Please fix them before importing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
