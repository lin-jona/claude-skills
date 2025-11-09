#!/usr/bin/env python3
"""
SVG Path Converter for Figma

Converts SVG path commands to Figma-compatible format:
- Converts Arc commands (A) to Cubic Bezier curves (C)
- Converts relative commands to absolute commands
- Converts H/V commands to L commands
- Converts S/T commands to C/Q commands

Usage:
    python convert_svg_paths.py "M 12 2 A 10 10 0 1 1 12 22 Z"
    python convert_svg_paths.py --file input.json --output output.json
"""

import argparse
import json
import math
import re
from pathlib import Path
from typing import List, Tuple


class PathConverter:
    """Converts SVG paths to Figma-compatible format"""

    def __init__(self):
        self.current_x = 0.0
        self.current_y = 0.0
        self.start_x = 0.0
        self.start_y = 0.0
        self.last_control_x = 0.0
        self.last_control_y = 0.0
        self.last_command = ""

    def convert_path(self, path_data: str) -> str:
        """Convert a complete SVG path to Figma format"""
        # Reset state
        self.current_x = 0.0
        self.current_y = 0.0
        self.start_x = 0.0
        self.start_y = 0.0
        self.last_control_x = 0.0
        self.last_control_y = 0.0
        self.last_command = ""

        # Parse path commands
        commands = self._parse_path(path_data)
        converted = []

        for cmd, params in commands:
            result = self._convert_command(cmd, params)
            if result:
                converted.extend(result)

        return " ".join(converted)

    def _parse_path(self, path_data: str) -> List[Tuple[str, List[float]]]:
        """Parse SVG path data into commands and parameters"""
        # Split by command letters
        tokens = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', path_data)

        commands = []
        current_cmd = None
        params = []

        for token in tokens:
            if re.match(r'[MmLlHhVvCcSsQqTtAaZz]', token):
                if current_cmd:
                    commands.append((current_cmd, params))
                current_cmd = token
                params = []
            else:
                params.append(float(token))

        if current_cmd:
            commands.append((current_cmd, params))

        return commands

    def _convert_command(self, cmd: str, params: List[float]) -> List[str]:
        """Convert a single command to Figma format"""
        if cmd == 'M':
            return self._move_to_abs(params)
        elif cmd == 'm':
            return self._move_to_rel(params)
        elif cmd == 'L':
            return self._line_to_abs(params)
        elif cmd == 'l':
            return self._line_to_rel(params)
        elif cmd == 'H':
            return self._horizontal_line_abs(params)
        elif cmd == 'h':
            return self._horizontal_line_rel(params)
        elif cmd == 'V':
            return self._vertical_line_abs(params)
        elif cmd == 'v':
            return self._vertical_line_rel(params)
        elif cmd == 'C':
            return self._cubic_bezier_abs(params)
        elif cmd == 'c':
            return self._cubic_bezier_rel(params)
        elif cmd == 'S':
            return self._smooth_cubic_abs(params)
        elif cmd == 's':
            return self._smooth_cubic_rel(params)
        elif cmd == 'Q':
            return self._quadratic_bezier_abs(params)
        elif cmd == 'q':
            return self._quadratic_bezier_rel(params)
        elif cmd == 'T':
            return self._smooth_quadratic_abs(params)
        elif cmd == 't':
            return self._smooth_quadratic_rel(params)
        elif cmd == 'A':
            return self._arc_abs(params)
        elif cmd == 'a':
            return self._arc_rel(params)
        elif cmd in ['Z', 'z']:
            return self._close_path()
        else:
            return []

    def _move_to_abs(self, params: List[float]) -> List[str]:
        """M command"""
        self.current_x = params[0]
        self.current_y = params[1]
        self.start_x = self.current_x
        self.start_y = self.current_y
        self.last_command = 'M'
        return [f"M {self.current_x} {self.current_y}"]

    def _move_to_rel(self, params: List[float]) -> List[str]:
        """m command - convert to absolute"""
        self.current_x += params[0]
        self.current_y += params[1]
        self.start_x = self.current_x
        self.start_y = self.current_y
        self.last_command = 'M'
        return [f"M {self.current_x} {self.current_y}"]

    def _line_to_abs(self, params: List[float]) -> List[str]:
        """L command"""
        self.current_x = params[0]
        self.current_y = params[1]
        self.last_command = 'L'
        return [f"L {self.current_x} {self.current_y}"]

    def _line_to_rel(self, params: List[float]) -> List[str]:
        """l command - convert to absolute"""
        self.current_x += params[0]
        self.current_y += params[1]
        self.last_command = 'L'
        return [f"L {self.current_x} {self.current_y}"]

    def _horizontal_line_abs(self, params: List[float]) -> List[str]:
        """H command - convert to L"""
        self.current_x = params[0]
        self.last_command = 'L'
        return [f"L {self.current_x} {self.current_y}"]

    def _horizontal_line_rel(self, params: List[float]) -> List[str]:
        """h command - convert to L"""
        self.current_x += params[0]
        self.last_command = 'L'
        return [f"L {self.current_x} {self.current_y}"]

    def _vertical_line_abs(self, params: List[float]) -> List[str]:
        """V command - convert to L"""
        self.current_y = params[0]
        self.last_command = 'L'
        return [f"L {self.current_x} {self.current_y}"]

    def _vertical_line_rel(self, params: List[float]) -> List[str]:
        """v command - convert to L"""
        self.current_y += params[0]
        self.last_command = 'L'
        return [f"L {self.current_x} {self.current_y}"]

    def _cubic_bezier_abs(self, params: List[float]) -> List[str]:
        """C command"""
        x1, y1, x2, y2, x, y = params[:6]
        self.last_control_x = x2
        self.last_control_y = y2
        self.current_x = x
        self.current_y = y
        self.last_command = 'C'
        return [f"C {x1} {y1} {x2} {y2} {x} {y}"]

    def _cubic_bezier_rel(self, params: List[float]) -> List[str]:
        """c command - convert to absolute"""
        x1 = self.current_x + params[0]
        y1 = self.current_y + params[1]
        x2 = self.current_x + params[2]
        y2 = self.current_y + params[3]
        x = self.current_x + params[4]
        y = self.current_y + params[5]
        self.last_control_x = x2
        self.last_control_y = y2
        self.current_x = x
        self.current_y = y
        self.last_command = 'C'
        return [f"C {x1} {y1} {x2} {y2} {x} {y}"]

    def _smooth_cubic_abs(self, params: List[float]) -> List[str]:
        """S command - convert to C"""
        # Reflect last control point
        if self.last_command in ['C', 'S']:
            x1 = 2 * self.current_x - self.last_control_x
            y1 = 2 * self.current_y - self.last_control_y
        else:
            x1 = self.current_x
            y1 = self.current_y

        x2, y2, x, y = params[:4]
        self.last_control_x = x2
        self.last_control_y = y2
        self.current_x = x
        self.current_y = y
        self.last_command = 'C'
        return [f"C {x1} {y1} {x2} {y2} {x} {y}"]

    def _smooth_cubic_rel(self, params: List[float]) -> List[str]:
        """s command - convert to C"""
        if self.last_command in ['C', 'S']:
            x1 = 2 * self.current_x - self.last_control_x
            y1 = 2 * self.current_y - self.last_control_y
        else:
            x1 = self.current_x
            y1 = self.current_y

        x2 = self.current_x + params[0]
        y2 = self.current_y + params[1]
        x = self.current_x + params[2]
        y = self.current_y + params[3]
        self.last_control_x = x2
        self.last_control_y = y2
        self.current_x = x
        self.current_y = y
        self.last_command = 'C'
        return [f"C {x1} {y1} {x2} {y2} {x} {y}"]

    def _quadratic_bezier_abs(self, params: List[float]) -> List[str]:
        """Q command"""
        x1, y1, x, y = params[:4]
        self.last_control_x = x1
        self.last_control_y = y1
        self.current_x = x
        self.current_y = y
        self.last_command = 'Q'
        return [f"Q {x1} {y1} {x} {y}"]

    def _quadratic_bezier_rel(self, params: List[float]) -> List[str]:
        """q command - convert to absolute"""
        x1 = self.current_x + params[0]
        y1 = self.current_y + params[1]
        x = self.current_x + params[2]
        y = self.current_y + params[3]
        self.last_control_x = x1
        self.last_control_y = y1
        self.current_x = x
        self.current_y = y
        self.last_command = 'Q'
        return [f"Q {x1} {y1} {x} {y}"]

    def _smooth_quadratic_abs(self, params: List[float]) -> List[str]:
        """T command - convert to Q"""
        if self.last_command in ['Q', 'T']:
            x1 = 2 * self.current_x - self.last_control_x
            y1 = 2 * self.current_y - self.last_control_y
        else:
            x1 = self.current_x
            y1 = self.current_y

        x, y = params[:2]
        self.last_control_x = x1
        self.last_control_y = y1
        self.current_x = x
        self.current_y = y
        self.last_command = 'Q'
        return [f"Q {x1} {y1} {x} {y}"]

    def _smooth_quadratic_rel(self, params: List[float]) -> List[str]:
        """t command - convert to Q"""
        if self.last_command in ['Q', 'T']:
            x1 = 2 * self.current_x - self.last_control_x
            y1 = 2 * self.current_y - self.last_control_y
        else:
            x1 = self.current_x
            y1 = self.current_y

        x = self.current_x + params[0]
        y = self.current_y + params[1]
        self.last_control_x = x1
        self.last_control_y = y1
        self.current_x = x
        self.current_y = y
        self.last_command = 'Q'
        return [f"Q {x1} {y1} {x} {y}"]

    def _arc_abs(self, params: List[float]) -> List[str]:
        """A command - convert to cubic bezier curves"""
        rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y = params[:7]
        return self._arc_to_bezier(
            self.current_x, self.current_y,
            rx, ry, x_axis_rotation, large_arc_flag, sweep_flag,
            x, y
        )

    def _arc_rel(self, params: List[float]) -> List[str]:
        """a command - convert to cubic bezier curves"""
        rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, dx, dy = params[:7]
        x = self.current_x + dx
        y = self.current_y + dy
        return self._arc_to_bezier(
            self.current_x, self.current_y,
            rx, ry, x_axis_rotation, large_arc_flag, sweep_flag,
            x, y
        )

    def _arc_to_bezier(self, x1: float, y1: float, rx: float, ry: float,
                       phi: float, large_arc: float, sweep: float,
                       x2: float, y2: float) -> List[str]:
        """
        Convert an elliptical arc to cubic bezier curves
        Based on: https://www.w3.org/TR/SVG/implnotes.html#ArcImplementationNotes
        """
        # Handle degenerate cases
        if rx == 0 or ry == 0:
            self.current_x = x2
            self.current_y = y2
            return [f"L {x2} {y2}"]

        # Convert angle to radians
        phi_rad = math.radians(phi)
        cos_phi = math.cos(phi_rad)
        sin_phi = math.sin(phi_rad)

        # Compute center point
        dx = (x1 - x2) / 2
        dy = (y1 - y2) / 2
        x1_prime = cos_phi * dx + sin_phi * dy
        y1_prime = -sin_phi * dx + cos_phi * dy

        # Correct radii if needed
        lambda_ = (x1_prime / rx) ** 2 + (y1_prime / ry) ** 2
        if lambda_ > 1:
            rx *= math.sqrt(lambda_)
            ry *= math.sqrt(lambda_)

        # Compute center
        sq = max(0, (rx * ry) ** 2 - (rx * y1_prime) ** 2 - (ry * x1_prime) ** 2)
        sq = math.sqrt(sq / ((rx * y1_prime) ** 2 + (ry * x1_prime) ** 2))

        if large_arc == sweep:
            sq = -sq

        cx_prime = sq * rx * y1_prime / ry
        cy_prime = -sq * ry * x1_prime / rx

        cx = cos_phi * cx_prime - sin_phi * cy_prime + (x1 + x2) / 2
        cy = sin_phi * cx_prime + cos_phi * cy_prime + (y1 + y2) / 2

        # Compute angles
        def angle_between(ux, uy, vx, vy):
            n = math.sqrt(ux * ux + uy * uy) * math.sqrt(vx * vx + vy * vy)
            c = (ux * vx + uy * vy) / n
            c = max(-1, min(1, c))
            angle = math.acos(c)
            if ux * vy - uy * vx < 0:
                angle = -angle
            return angle

        theta1 = angle_between(1, 0, (x1_prime - cx_prime) / rx, (y1_prime - cy_prime) / ry)
        dtheta = angle_between(
            (x1_prime - cx_prime) / rx, (y1_prime - cy_prime) / ry,
            (-x1_prime - cx_prime) / rx, (-y1_prime - cy_prime) / ry
        )

        if sweep == 0 and dtheta > 0:
            dtheta -= 2 * math.pi
        elif sweep == 1 and dtheta < 0:
            dtheta += 2 * math.pi

        # Split arc into multiple bezier curves (max 90 degrees each)
        segments = max(1, int(math.ceil(abs(dtheta) / (math.pi / 2))))
        delta = dtheta / segments
        t = (8 / 3) * math.sin(delta / 4) ** 2 / math.sin(delta / 2)

        curves = []
        for i in range(segments):
            theta_start = theta1 + i * delta
            theta_end = theta_start + delta

            cos_start = math.cos(theta_start)
            sin_start = math.sin(theta_start)
            cos_end = math.cos(theta_end)
            sin_end = math.sin(theta_end)

            # Control points
            q1x = cos_start
            q1y = sin_start
            q2x = cos_end
            q2y = sin_end

            cp1x = q1x - q1y * t
            cp1y = q1y + q1x * t
            cp2x = q2x + q2y * t
            cp2y = q2y - q2x * t

            # Transform back
            def transform(x, y):
                return (
                    cos_phi * rx * x - sin_phi * ry * y + cx,
                    sin_phi * rx * x + cos_phi * ry * y + cy
                )

            cp1 = transform(cp1x, cp1y)
            cp2 = transform(cp2x, cp2y)
            end = transform(q2x, q2y)

            curves.append(f"C {cp1[0]} {cp1[1]} {cp2[0]} {cp2[1]} {end[0]} {end[1]}")

        self.current_x = x2
        self.current_y = y2
        self.last_command = 'C'
        return curves

    def _close_path(self) -> List[str]:
        """Z command"""
        self.current_x = self.start_x
        self.current_y = self.start_y
        self.last_command = 'Z'
        return ["Z"]


def convert_json_file(input_path: Path, output_path: Path):
    """Convert all paths in a JSON file"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    converter = PathConverter()
    changes = []

    def process_node(node, path="root"):
        if not isinstance(node, dict):
            return

        # Convert vectorPaths
        if "vectorPaths" in node:
            for i, vp in enumerate(node["vectorPaths"]):
                if "data" in vp:
                    original = vp["data"]
                    converted = converter.convert_path(original)
                    if original != converted:
                        vp["data"] = converted
                        changes.append(f"{path}/vectorPaths[{i}]")

        # Convert fillGeometry
        if "fillGeometry" in node:
            for i, fg in enumerate(node["fillGeometry"]):
                if "data" in fg:
                    original = fg["data"]
                    converted = converter.convert_path(original)
                    if original != converted:
                        fg["data"] = converted
                        changes.append(f"{path}/fillGeometry[{i}]")

        # Process children
        if "children" in node:
            for i, child in enumerate(node["children"]):
                process_node(child, f"{path}/children[{i}]")

    process_node(data)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Converted {len(changes)} path(s)")
    if changes:
        print("\nModified paths:")
        for change in changes:
            print(f"  - {change}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert SVG paths to Figma-compatible format"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="SVG path string to convert"
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Input JSON file"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON file (default: input_converted.json)"
    )

    args = parser.parse_args()

    if args.file:
        # Convert JSON file
        output = args.output or args.file.parent / f"{args.file.stem}_converted.json"
        print(f"Converting paths in {args.file}...")
        convert_json_file(args.file, output)
        print(f"Saved to {output}")
    elif args.path:
        # Convert single path
        converter = PathConverter()
        result = converter.convert_path(args.path)
        print("\nOriginal:")
        print(f"  {args.path}")
        print("\nConverted:")
        print(f"  {result}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
