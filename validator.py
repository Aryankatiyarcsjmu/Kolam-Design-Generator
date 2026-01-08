"""
Pattern Validation Module for Kolam Design Generator

This module provides validation functionality for Kolam patterns against
mathematical rules including symmetry, connectivity, and geometric constraints.

Author: Kolam Design Generator
Date: 2026-01-08
"""

import math
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum


class SymmetryType(Enum):
    """Enum for different types of symmetry in Kolam patterns."""
    NONE = "none"
    RADIAL = "radial"
    BILATERAL = "bilateral"
    ROTATIONAL = "rotational"
    TRANSLATIONAL = "translational"


@dataclass
class Point:
    """Represents a point in 2D space."""
    x: float
    y: float

    def __hash__(self):
        return hash((round(self.x, 10), round(self.y, 10)))

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return (abs(self.x - other.x) < 1e-9 and 
                abs(self.y - other.y) < 1e-9)

    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angle_to(self, other: 'Point') -> float:
        """Calculate angle to another point in radians."""
        dx = other.x - self.x
        dy = other.y - self.y
        return math.atan2(dy, dx)


@dataclass
class ValidationResult:
    """Result of pattern validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict


class PatternValidator:
    """
    Main validator class for Kolam patterns.
    
    Validates patterns against mathematical rules including:
    - Connectivity constraints
    - Symmetry requirements
    - Geometric constraints
    - Dot alignment rules
    """

    def __init__(self, tolerance: float = 1e-6):
        """
        Initialize the pattern validator.
        
        Args:
            tolerance: Floating-point tolerance for comparisons
        """
        self.tolerance = tolerance
        self.errors = []
        self.warnings = []
        self.metadata = {}

    def validate_pattern(self, points: List[Point], 
                        connections: List[Tuple[int, int]],
                        pattern_type: str = "general") -> ValidationResult:
        """
        Validate a complete Kolam pattern.
        
        Args:
            points: List of Point objects representing the pattern
            connections: List of tuples (index1, index2) representing connections
            pattern_type: Type of pattern (general, circular, grid, etc.)
        
        Returns:
            ValidationResult object with validation status and details
        """
        self.errors = []
        self.warnings = []
        self.metadata = {}

        # Run all validation checks
        self._validate_points(points)
        self._validate_connections(points, connections)
        self._validate_geometric_constraints(points)
        self._validate_connectivity(points, connections)
        
        # Type-specific validations
        if pattern_type == "circular":
            self._validate_circular_pattern(points)
        elif pattern_type == "grid":
            self._validate_grid_pattern(points)
        
        is_valid = len(self.errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            errors=self.errors,
            warnings=self.warnings,
            metadata=self.metadata
        )

    def _validate_points(self, points: List[Point]) -> None:
        """Validate individual points in the pattern."""
        if not points:
            self.errors.append("Pattern must contain at least one point")
            return

        if len(points) > 10000:
            self.warnings.append(f"Pattern contains {len(points)} points, may affect performance")

        # Check for duplicate points
        unique_points = set()
        duplicates = []
        
        for i, point in enumerate(points):
            if not isinstance(point, Point):
                self.errors.append(f"Point {i} is not a valid Point object")
                continue
            
            if point in unique_points:
                duplicates.append(i)
            else:
                unique_points.add(point)

        if duplicates:
            self.warnings.append(f"Found {len(duplicates)} duplicate point(s) at indices: {duplicates}")

        self.metadata['total_points'] = len(points)
        self.metadata['unique_points'] = len(unique_points)

    def _validate_connections(self, points: List[Point], 
                             connections: List[Tuple[int, int]]) -> None:
        """Validate connections between points."""
        if not connections:
            self.warnings.append("Pattern has no connections")
            return

        if len(connections) > len(points) * (len(points) - 1) / 2:
            self.errors.append("Number of connections exceeds maximum possible")
            return

        for conn_idx, (p1_idx, p2_idx) in enumerate(connections):
            # Check valid indices
            if not (0 <= p1_idx < len(points)):
                self.errors.append(f"Connection {conn_idx}: point index {p1_idx} out of range")
            if not (0 <= p2_idx < len(points)):
                self.errors.append(f"Connection {conn_idx}: point index {p2_idx} out of range")
            
            # Check self-loops
            if p1_idx == p2_idx:
                self.warnings.append(f"Connection {conn_idx}: self-loop detected")

        self.metadata['total_connections'] = len(connections)

    def _validate_geometric_constraints(self, points: List[Point]) -> None:
        """Validate geometric constraints of the pattern."""
        if len(points) < 2:
            return

        # Calculate bounding box
        min_x = min(p.x for p in points)
        max_x = max(p.x for p in points)
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)

        width = max_x - min_x
        height = max_y - min_y

        if width == 0 or height == 0:
            self.warnings.append("Pattern is degenerate (all points on a line)")

        # Check aspect ratio
        aspect_ratio = width / height if height > 0 else float('inf')
        if aspect_ratio > 10 or aspect_ratio < 0.1:
            self.warnings.append(f"Pattern has extreme aspect ratio: {aspect_ratio:.2f}")

        self.metadata['bounding_box'] = {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'width': width,
            'height': height
        }

    def _validate_connectivity(self, points: List[Point], 
                              connections: List[Tuple[int, int]]) -> None:
        """Validate connectivity properties of the pattern."""
        if not connections:
            return

        # Build adjacency list
        adjacency = {i: [] for i in range(len(points))}
        for p1_idx, p2_idx in connections:
            if 0 <= p1_idx < len(points) and 0 <= p2_idx < len(points):
                adjacency[p1_idx].append(p2_idx)
                adjacency[p2_idx].append(p1_idx)

        # Check for isolated points
        isolated_points = [i for i, neighbors in adjacency.items() if not neighbors]
        if isolated_points:
            self.warnings.append(f"Found {len(isolated_points)} isolated point(s)")

        # Check connectivity
        if len(points) > 1:
            is_connected = self._is_graph_connected(adjacency, len(points))
            self.metadata['is_connected'] = is_connected
            if not is_connected:
                self.warnings.append("Pattern is not fully connected")

        # Calculate degree statistics
        degrees = [len(neighbors) for neighbors in adjacency.values()]
        self.metadata['degree_stats'] = {
            'min': min(degrees) if degrees else 0,
            'max': max(degrees) if degrees else 0,
            'mean': sum(degrees) / len(degrees) if degrees else 0
        }

    def _is_graph_connected(self, adjacency: Dict[int, List[int]], 
                           num_nodes: int) -> bool:
        """Check if graph is connected using BFS."""
        if num_nodes == 0:
            return True

        visited = set()
        queue = [0]
        visited.add(0)

        while queue:
            node = queue.pop(0)
            for neighbor in adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == num_nodes

    def _validate_circular_pattern(self, points: List[Point]) -> None:
        """Validate constraints for circular Kolam patterns."""
        if len(points) < 3:
            return

        # Check if points are arranged in a circle
        center_x = sum(p.x for p in points) / len(points)
        center_y = sum(p.y for p in points) / len(points)
        center = Point(center_x, center_y)

        distances = [p.distance_to(center) for p in points]
        avg_distance = sum(distances) / len(distances)
        max_deviation = max(abs(d - avg_distance) for d in distances)
        relative_deviation = max_deviation / avg_distance if avg_distance > 0 else 0

        self.metadata['circularity'] = {
            'center': {'x': center_x, 'y': center_y},
            'average_radius': avg_distance,
            'max_deviation': max_deviation,
            'relative_deviation': relative_deviation
        }

        if relative_deviation > 0.1:
            self.warnings.append(f"Pattern deviates from circular shape: {relative_deviation:.2%}")

    def _validate_grid_pattern(self, points: List[Point]) -> None:
        """Validate constraints for grid-based Kolam patterns."""
        if len(points) < 4:
            return

        # Extract unique x and y coordinates
        x_coords = sorted(set(p.x for p in points))
        y_coords = sorted(set(p.y for p in points))

        # Check for regular spacing
        if len(x_coords) > 1:
            x_diffs = [x_coords[i+1] - x_coords[i] for i in range(len(x_coords)-1)]
            x_variance = self._calculate_variance(x_diffs)
            if x_variance > 0.01:
                self.warnings.append("X-coordinates are not evenly spaced")

        if len(y_coords) > 1:
            y_diffs = [y_coords[i+1] - y_coords[i] for i in range(len(y_coords)-1)]
            y_variance = self._calculate_variance(y_diffs)
            if y_variance > 0.01:
                self.warnings.append("Y-coordinates are not evenly spaced")

        self.metadata['grid_info'] = {
            'unique_x_coords': len(x_coords),
            'unique_y_coords': len(y_coords)
        }

    def check_symmetry(self, points: List[Point]) -> SymmetryType:
        """
        Check the type of symmetry in the pattern.
        
        Args:
            points: List of points in the pattern
        
        Returns:
            SymmetryType indicating the primary symmetry type
        """
        if len(points) < 2:
            return SymmetryType.NONE

        # Calculate center
        center_x = sum(p.x for p in points) / len(points)
        center_y = sum(p.y for p in points) / len(points)
        center = Point(center_x, center_y)

        # Check for bilateral symmetry (reflection about y-axis)
        bilateral_match = 0
        for point in points:
            reflected = Point(2 * center_x - point.x, point.y)
            for other in points:
                if other.distance_to(reflected) < self.tolerance:
                    bilateral_match += 1
                    break

        if bilateral_match / len(points) > 0.9:
            return SymmetryType.BILATERAL

        # Check for rotational symmetry
        for rotation_angle in [90, 120, 180]:
            rad = math.radians(rotation_angle)
            rotational_match = 0
            for point in points:
                # Rotate point around center
                dx = point.x - center_x
                dy = point.y - center_y
                rotated_x = center_x + dx * math.cos(rad) - dy * math.sin(rad)
                rotated_y = center_y + dx * math.sin(rad) + dy * math.cos(rad)
                rotated = Point(rotated_x, rotated_y)

                for other in points:
                    if other.distance_to(rotated) < self.tolerance:
                        rotational_match += 1
                        break

            if rotational_match / len(points) > 0.9:
                return SymmetryType.ROTATIONAL

        return SymmetryType.NONE

    def validate_dot_alignment(self, points: List[Point], 
                               grid_spacing: float = 1.0,
                               tolerance: Optional[float] = None) -> Dict:
        """
        Validate that dots are properly aligned to a grid.
        
        Args:
            points: List of points to validate
            grid_spacing: Expected spacing between grid points
            tolerance: Tolerance for alignment (defaults to self.tolerance)
        
        Returns:
            Dictionary with alignment validation results
        """
        tolerance = tolerance or self.tolerance

        misaligned = []
        for i, point in enumerate(points):
            # Check alignment with nearest grid point
            grid_x = round(point.x / grid_spacing) * grid_spacing
            grid_y = round(point.y / grid_spacing) * grid_spacing
            
            distance = point.distance_to(Point(grid_x, grid_y))
            if distance > tolerance:
                misaligned.append({
                    'point_index': i,
                    'point': (point.x, point.y),
                    'nearest_grid': (grid_x, grid_y),
                    'distance': distance
                })

        return {
            'aligned': len(points) - len(misaligned),
            'misaligned': len(misaligned),
            'total': len(points),
            'alignment_percentage': ((len(points) - len(misaligned)) / len(points) * 100) if points else 0,
            'misaligned_points': misaligned
        }

    def validate_line_continuity(self, points: List[Point], 
                                connections: List[Tuple[int, int]],
                                max_gap: float = 0.1) -> Dict:
        """
        Validate continuity of lines in the pattern.
        
        Args:
            points: List of points
            connections: List of connections
            max_gap: Maximum allowed gap between connected points
        
        Returns:
            Dictionary with continuity validation results
        """
        discontinuities = []
        
        for conn_idx, (p1_idx, p2_idx) in enumerate(connections):
            if p1_idx >= len(points) or p2_idx >= len(points):
                continue
            
            distance = points[p1_idx].distance_to(points[p2_idx])
            if distance > max_gap:
                discontinuities.append({
                    'connection_index': conn_idx,
                    'points': (p1_idx, p2_idx),
                    'distance': distance
                })

        return {
            'continuous': len(connections) - len(discontinuities),
            'discontinuous': len(discontinuities),
            'total_connections': len(connections),
            'continuity_percentage': ((len(connections) - len(discontinuities)) / len(connections) * 100) if connections else 0,
            'discontinuities': discontinuities
        }

    @staticmethod
    def _calculate_variance(values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)


class PatternAnalyzer:
    """Analyzer for extracting features from Kolam patterns."""

    @staticmethod
    def calculate_pattern_complexity(points: List[Point], 
                                    connections: List[Tuple[int, int]]) -> float:
        """
        Calculate complexity score of the pattern.
        
        Args:
            points: List of points
            connections: List of connections
        
        Returns:
            Complexity score (0-1)
        """
        if not points or not connections:
            return 0

        # Complexity based on number of points and connections
        connectivity = len(connections) / (len(points) * (len(points) - 1) / 2)
        uniqueness = len(set(connections)) / len(connections) if connections else 0

        return min(1.0, (len(points) / 100) * connectivity * uniqueness)

    @staticmethod
    def extract_pattern_features(points: List[Point], 
                                connections: List[Tuple[int, int]]) -> Dict:
        """
        Extract numerical features from pattern.
        
        Args:
            points: List of points
            connections: List of connections
        
        Returns:
            Dictionary of extracted features
        """
        if not points:
            return {}

        # Calculate statistics
        x_coords = [p.x for p in points]
        y_coords = [p.y for p in points]

        def calculate_stats(values):
            if not values:
                return {}
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            return {
                'mean': mean,
                'min': min(values),
                'max': max(values),
                'variance': variance,
                'std_dev': math.sqrt(variance)
            }

        features = {
            'point_count': len(points),
            'connection_count': len(connections),
            'x_statistics': calculate_stats(x_coords),
            'y_statistics': calculate_stats(y_coords),
            'complexity': PatternAnalyzer.calculate_pattern_complexity(points, connections)
        }

        return features


if __name__ == "__main__":
    # Example usage and basic testing
    print("Kolam Pattern Validator Module")
    print("-" * 40)

    # Create sample pattern (simple triangle)
    sample_points = [
        Point(0, 0),
        Point(1, 0),
        Point(0.5, 1)
    ]
    sample_connections = [(0, 1), (1, 2), (2, 0)]

    # Validate
    validator = PatternValidator()
    result = validator.validate_pattern(sample_points, sample_connections)

    print(f"Valid: {result.is_valid}")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")
    print(f"Metadata: {result.metadata}")

    # Check symmetry
    symmetry = validator.check_symmetry(sample_points)
    print(f"Symmetry Type: {symmetry.value}")

    # Analyze pattern
    analyzer = PatternAnalyzer()
    features = analyzer.extract_pattern_features(sample_points, sample_connections)
    print(f"Features: {features}")
