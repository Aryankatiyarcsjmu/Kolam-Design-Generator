"""
Kolam Design Generator Core Module

This module provides the KolamGenerator class for creating traditional kolam designs
with support for grid generation, pattern traversal, and symmetry operations.

Author: Aryan Katiyar
Date: 2026-01-08
"""

import numpy as np
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum
import copy


class SymmetryType(Enum):
    """Enumeration of supported symmetry operations."""
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    ROTATIONAL_90 = 3
    ROTATIONAL_180 = 4
    ROTATIONAL_270 = 5
    DIAGONAL_MAIN = 6
    DIAGONAL_ANTI = 7


@dataclass
class Point:
    """Represents a point in the kolam grid."""
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def to_tuple(self) -> Tuple[int, int]:
        """Convert point to tuple format."""
        return (self.x, self.y)


class KolamGenerator:
    """
    Core class for generating traditional kolam designs.
    
    Supports:
    - Grid generation with customizable dimensions
    - Pattern traversal with various algorithms
    - Symmetry operations (horizontal, vertical, rotational, diagonal)
    - Pattern merging and composition
    """

    def __init__(self, width: int, height: int, grid_type: str = "square"):
        """
        Initialize the KolamGenerator.

        Args:
            width: Width of the grid
            height: Height of the grid
            grid_type: Type of grid - "square", "hexagonal", or "triangular"
        """
        self.width = width
        self.height = height
        self.grid_type = grid_type
        self.grid = self._initialize_grid()
        self.patterns: Dict[str, Set[Point]] = {}
        self.symmetry_type = SymmetryType.NONE

    def _initialize_grid(self) -> np.ndarray:
        """
        Initialize an empty grid.

        Returns:
            2D numpy array representing the grid
        """
        return np.zeros((self.height, self.width), dtype=int)

    def add_pattern(self, pattern_name: str, points: List[Tuple[int, int]]) -> None:
        """
        Add a named pattern to the generator.

        Args:
            pattern_name: Name identifier for the pattern
            points: List of (x, y) coordinate tuples
        """
        point_set = {Point(x, y) for x, y in points}
        self.patterns[pattern_name] = point_set

    def get_pattern(self, pattern_name: str) -> Optional[Set[Point]]:
        """
        Retrieve a stored pattern by name.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Set of Point objects or None if not found
        """
        return self.patterns.get(pattern_name)

    def draw_pattern(self, pattern_name: str, value: int = 1) -> None:
        """
        Draw a pattern onto the grid.

        Args:
            pattern_name: Name of the pattern to draw
            value: Value to assign to grid cells (default: 1)
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        for point in pattern:
            if 0 <= point.x < self.width and 0 <= point.y < self.height:
                self.grid[point.y, point.x] = value

    def traverse_pattern_dfs(self, start_point: Tuple[int, int], 
                            connected_only: bool = True) -> List[Point]:
        """
        Traverse a pattern using Depth-First Search.

        Args:
            start_point: Starting (x, y) coordinate
            connected_only: If True, only traverse connected cells

        Returns:
            List of Point objects in traversal order
        """
        visited = set()
        traversal = []

        def dfs(point: Point):
            if (point.x, point.y) in visited:
                return
            if not (0 <= point.x < self.width and 0 <= point.y < self.height):
                return
            if self.grid[point.y, point.x] == 0:
                return

            visited.add((point.x, point.y))
            traversal.append(point)

            # Check 4-connectivity
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(Point(point.x + dx, point.y + dy))

        dfs(Point(start_point[0], start_point[1]))
        return traversal

    def traverse_pattern_bfs(self, start_point: Tuple[int, int]) -> List[Point]:
        """
        Traverse a pattern using Breadth-First Search.

        Args:
            start_point: Starting (x, y) coordinate

        Returns:
            List of Point objects in traversal order
        """
        from collections import deque

        visited = set()
        queue = deque([Point(start_point[0], start_point[1])])
        traversal = []

        while queue:
            point = queue.popleft()

            if (point.x, point.y) in visited:
                continue
            if not (0 <= point.x < self.width and 0 <= point.y < self.height):
                continue
            if self.grid[point.y, point.x] == 0:
                continue

            visited.add((point.x, point.y))
            traversal.append(point)

            # Check 4-connectivity
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                neighbor = Point(point.x + dx, point.y + dy)
                if (neighbor.x, neighbor.y) not in visited:
                    queue.append(neighbor)

        return traversal

    def apply_horizontal_symmetry(self, pattern_name: str) -> Set[Point]:
        """
        Apply horizontal (mirror) symmetry to a pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            New set of points with symmetry applied
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        # Mirror across vertical center line
        center_x = self.width / 2
        symmetric_pattern = set()

        for point in pattern:
            mirrored_x = int(2 * center_x - point.x - 1)
            symmetric_pattern.add(Point(mirrored_x, point.y))
            symmetric_pattern.add(point)

        return symmetric_pattern

    def apply_vertical_symmetry(self, pattern_name: str) -> Set[Point]:
        """
        Apply vertical (mirror) symmetry to a pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            New set of points with symmetry applied
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        # Mirror across horizontal center line
        center_y = self.height / 2
        symmetric_pattern = set()

        for point in pattern:
            mirrored_y = int(2 * center_y - point.y - 1)
            symmetric_pattern.add(Point(point.x, mirrored_y))
            symmetric_pattern.add(point)

        return symmetric_pattern

    def apply_rotational_symmetry(self, pattern_name: str, 
                                 angle: int = 90) -> Set[Point]:
        """
        Apply rotational symmetry to a pattern.

        Args:
            pattern_name: Name of the pattern
            angle: Rotation angle in degrees (90, 180, 270)

        Returns:
            New set of points with rotational symmetry applied
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        symmetric_pattern = set(pattern)
        center_x, center_y = self.width / 2, self.height / 2

        for _ in range(angle // 90):
            rotated = set()
            for point in symmetric_pattern:
                # Rotate around center
                dx = point.x - center_x
                dy = point.y - center_y
                new_x = int(center_x - dy)
                new_y = int(center_y + dx)

                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    rotated.add(Point(new_x, new_y))

            symmetric_pattern.update(rotated)

        return symmetric_pattern

    def apply_diagonal_symmetry(self, pattern_name: str, 
                               main_diagonal: bool = True) -> Set[Point]:
        """
        Apply diagonal symmetry to a pattern.

        Args:
            pattern_name: Name of the pattern
            main_diagonal: If True, mirror across main diagonal (top-left to bottom-right)
                          If False, mirror across anti-diagonal

        Returns:
            New set of points with diagonal symmetry applied
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        symmetric_pattern = set()

        for point in pattern:
            symmetric_pattern.add(point)

            if main_diagonal:
                # Reflect across main diagonal
                reflected = Point(point.y, point.x)
            else:
                # Reflect across anti-diagonal
                reflected = Point(self.width - 1 - point.y, 
                                self.height - 1 - point.x)

            if 0 <= reflected.x < self.width and 0 <= reflected.y < self.height:
                symmetric_pattern.add(reflected)

        return symmetric_pattern

    def compose_patterns(self, pattern_names: List[str], 
                        offsets: Optional[List[Tuple[int, int]]] = None) -> Set[Point]:
        """
        Compose multiple patterns with optional offsets.

        Args:
            pattern_names: List of pattern names to compose
            offsets: List of (x, y) offset tuples (default: no offset)

        Returns:
            Combined set of points from all patterns
        """
        if offsets is None:
            offsets = [(0, 0)] * len(pattern_names)

        composed = set()

        for pattern_name, (offset_x, offset_y) in zip(pattern_names, offsets):
            pattern = self.get_pattern(pattern_name)
            if pattern is None:
                raise ValueError(f"Pattern '{pattern_name}' not found")

            for point in pattern:
                new_x = point.x + offset_x
                new_y = point.y + offset_y

                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    composed.add(Point(new_x, new_y))

        return composed

    def get_grid_as_list(self) -> List[List[int]]:
        """
        Get the current grid as a nested list.

        Returns:
            2D list representation of the grid
        """
        return self.grid.tolist()

    def clear_grid(self) -> None:
        """Reset the grid to all zeros."""
        self.grid = self._initialize_grid()

    def get_bounding_box(self, pattern_name: str) -> Optional[Tuple[int, int, int, int]]:
        """
        Get the bounding box of a pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Tuple of (min_x, min_y, max_x, max_y) or None if pattern not found
        """
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            return None

        xs = [p.x for p in pattern]
        ys = [p.y for p in pattern]

        return (min(xs), min(ys), max(xs), max(ys))

    def translate_pattern(self, pattern_name: str, dx: int, dy: int) -> Set[Point]:
        """
        Translate a pattern by given offsets.

        Args:
            pattern_name: Name of the pattern
            dx: Horizontal translation
            dy: Vertical translation

        Returns:
            New set of translated points
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        translated = set()
        for point in pattern:
            new_x = point.x + dx
            new_y = point.y + dy

            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                translated.add(Point(new_x, new_y))

        return translated

    def scale_pattern(self, pattern_name: str, scale_factor: int) -> Set[Point]:
        """
        Scale a pattern by a given factor.

        Args:
            pattern_name: Name of the pattern
            scale_factor: Scaling factor (2 = double size)

        Returns:
            New set of scaled points
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        scaled = set()
        for point in pattern:
            # Generate scaled points in a square region
            for i in range(scale_factor):
                for j in range(scale_factor):
                    new_x = point.x * scale_factor + i
                    new_y = point.y * scale_factor + j

                    if 0 <= new_x < self.width and 0 <= new_y < self.height:
                        scaled.add(Point(new_x, new_y))

        return scaled

    def get_pattern_statistics(self, pattern_name: str) -> Dict:
        """
        Get statistics about a pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Dictionary with pattern statistics
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            return {}

        bbox = self.get_bounding_box(pattern_name)

        return {
            "point_count": len(pattern),
            "bounding_box": bbox,
            "width": bbox[2] - bbox[0] + 1 if bbox else 0,
            "height": bbox[3] - bbox[1] + 1 if bbox else 0,
        }

    def export_pattern_as_matrix(self, pattern_name: str) -> np.ndarray:
        """
        Export a pattern as a binary matrix.

        Args:
            pattern_name: Name of the pattern

        Returns:
            2D numpy array with 1s for pattern points, 0s otherwise
        """
        pattern = self.get_pattern(pattern_name)
        if pattern is None:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        matrix = np.zeros((self.height, self.width), dtype=int)

        for point in pattern:
            if 0 <= point.x < self.width and 0 <= point.y < self.height:
                matrix[point.y, point.x] = 1

        return matrix

    def create_concentric_squares(self, num_squares: int, 
                                 pattern_name: str = "concentric_squares") -> None:
        """
        Generate a concentric squares pattern.

        Args:
            num_squares: Number of concentric squares
            pattern_name: Name to store the pattern as
        """
        points = []
        center_x, center_y = self.width // 2, self.height // 2
        max_distance = max(center_x, center_y)

        for distance in range(1, min(num_squares + 1, max_distance)):
            # Top edge
            for x in range(center_x - distance, center_x + distance + 1):
                points.append((x, center_y - distance))

            # Bottom edge
            for x in range(center_x - distance, center_x + distance + 1):
                points.append((x, center_y + distance))

            # Left edge
            for y in range(center_y - distance + 1, center_y + distance):
                points.append((center_x - distance, y))

            # Right edge
            for y in range(center_y - distance + 1, center_y + distance):
                points.append((center_x + distance, y))

        self.add_pattern(pattern_name, points)

    def create_concentric_circles(self, num_circles: int, 
                                 pattern_name: str = "concentric_circles") -> None:
        """
        Generate concentric circles pattern using Bresenham's algorithm.

        Args:
            num_circles: Number of concentric circles
            pattern_name: Name to store the pattern as
        """
        points = []
        center_x, center_y = self.width // 2, self.height // 2

        for radius in range(1, num_circles + 1):
            circle_points = self._bresenham_circle(center_x, center_y, radius)
            points.extend(circle_points)

        self.add_pattern(pattern_name, points)

    def _bresenham_circle(self, center_x: int, center_y: int, 
                         radius: int) -> List[Tuple[int, int]]:
        """
        Generate circle points using Bresenham's circle algorithm.

        Args:
            center_x: X coordinate of center
            center_y: Y coordinate of center
            radius: Radius of circle

        Returns:
            List of (x, y) points on the circle
        """
        points = []
        x, y = 0, radius
        d = 3 - 2 * radius

        while x <= y:
            # Generate 8 symmetric points
            for px, py in [(x, y), (y, x), (-x, y), (-y, x),
                          (-x, -y), (-y, -x), (x, -y), (y, -x)]:
                cx, cy = center_x + px, center_y + py
                if 0 <= cx < self.width and 0 <= cy < self.height:
                    points.append((cx, cy))

            if d < 0:
                d = d + 4 * x + 6
            else:
                d = d + 4 * (x - y) + 10
                y -= 1

            x += 1

        return list(set(points))  # Remove duplicates

    def __str__(self) -> str:
        """String representation of the current grid."""
        return str(self.grid)

    def __repr__(self) -> str:
        """Detailed representation of the KolamGenerator."""
        return (f"KolamGenerator(width={self.width}, height={self.height}, "
                f"grid_type='{self.grid_type}', patterns={len(self.patterns)})")


# Example usage and testing
if __name__ == "__main__":
    # Create a 21x21 grid
    kolam = KolamGenerator(21, 21)

    # Create some basic patterns
    kolam.add_pattern("center_point", [(10, 10)])

    # Create concentric squares
    kolam.create_concentric_squares(5, "squares")

    # Create concentric circles
    kolam.create_concentric_circles(3, "circles")

    # Draw patterns
    kolam.draw_pattern("squares", value=1)
    kolam.draw_pattern("circles", value=2)

    # Get pattern statistics
    stats = kolam.get_pattern_statistics("squares")
    print(f"Square pattern stats: {stats}")

    # Apply symmetry
    symmetric = kolam.apply_rotational_symmetry("squares", angle=90)
    print(f"Rotational symmetry applied: {len(symmetric)} points")

    print("\nKolamGenerator initialized successfully!")
