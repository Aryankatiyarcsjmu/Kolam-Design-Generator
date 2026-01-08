"""
Kolam Visualizer Module
A comprehensive visualization module for rendering traditional Kolam patterns.
Supports both matplotlib and plotly for static and interactive visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Tuple, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum


class KolamStyle(Enum):
    """Different styles of Kolam patterns."""
    GEOMETRIC = "geometric"
    FLORAL = "floral"
    RELIGIOUS = "religious"
    TRADITIONAL = "traditional"
    MODERN = "modern"


@dataclass
class Point:
    """Represents a 2D point in the Kolam pattern."""
    x: float
    y: float
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert point to tuple."""
        return (self.x, self.y)
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point."""
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


@dataclass
class KolamPattern:
    """Represents a Kolam pattern with its attributes."""
    name: str
    points: List[Point]
    lines: List[Tuple[int, int]]  # Indices of connected points
    style: KolamStyle = KolamStyle.TRADITIONAL
    colors: Optional[List[str]] = None
    filled: bool = False
    symmetry: int = 4  # Number of symmetry axes


class KolamVisualizer:
    """
    Main visualizer class for rendering Kolam patterns.
    Supports both matplotlib and plotly backends.
    """
    
    def __init__(self, pattern: KolamPattern):
        """
        Initialize the visualizer with a Kolam pattern.
        
        Args:
            pattern: KolamPattern object to visualize
        """
        self.pattern = pattern
        self.fig = None
        self.ax = None
        self.plotly_fig = None
        
    def _generate_symmetric_pattern(self) -> List[Point]:
        """
        Generate symmetric points based on the pattern's symmetry setting.
        
        Returns:
            List of points including symmetric copies
        """
        all_points = self.pattern.points.copy()
        center_x = np.mean([p.x for p in self.pattern.points])
        center_y = np.mean([p.y for p in self.pattern.points])
        
        for symmetry_idx in range(1, self.pattern.symmetry):
            angle = (2 * np.pi * symmetry_idx) / self.pattern.symmetry
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            
            for point in self.pattern.points:
                # Translate to center, rotate, translate back
                x = point.x - center_x
                y = point.y - center_y
                
                new_x = cos_a * x - sin_a * y + center_x
                new_y = sin_a * x + cos_a * y + center_y
                
                all_points.append(Point(new_x, new_y))
        
        return all_points
    
    def render_matplotlib(self, 
                         figsize: Tuple[int, int] = (10, 10),
                         dpi: int = 100,
                         show_grid: bool = False,
                         line_width: float = 2.0,
                         point_size: float = 50,
                         save_path: Optional[str] = None) -> plt.Figure:
        """
        Render the Kolam pattern using matplotlib.
        
        Args:
            figsize: Figure size (width, height)
            dpi: Dots per inch for the figure
            show_grid: Whether to show grid lines
            line_width: Width of pattern lines
            point_size: Size of pattern points
            save_path: Path to save the figure (optional)
            
        Returns:
            matplotlib Figure object
        """
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi)
        
        # Set background
        self.ax.set_facecolor('#fffaf0')  # Floral white background
        self.fig.patch.set_facecolor('white')
        
        # Generate symmetric pattern if needed
        points = self._generate_symmetric_pattern() if self.pattern.symmetry > 1 else self.pattern.points
        
        # Draw lines
        for line_idx, (start, end) in enumerate(self.pattern.lines):
            if start < len(points) and end < len(points):
                p1 = points[start]
                p2 = points[end]
                
                # Use colors if provided
                color = 'black'
                if self.pattern.colors and line_idx < len(self.pattern.colors):
                    color = self.pattern.colors[line_idx]
                
                self.ax.plot([p1.x, p2.x], [p1.y, p2.y], 
                           color=color, linewidth=line_width, zorder=2)
        
        # Draw points
        if len(points) > 0:
            point_xs = [p.x for p in points]
            point_ys = [p.y for p in points]
            self.ax.scatter(point_xs, point_ys, s=point_size, 
                          color='red', zorder=3, alpha=0.7)
        
        # Styling
        self.ax.set_aspect('equal')
        self.ax.set_title(f'Kolam Pattern: {self.pattern.name}', 
                         fontsize=16, fontweight='bold', pad=20)
        
        if show_grid:
            self.ax.grid(True, alpha=0.3, linestyle='--')
        else:
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        
        # Remove spines for cleaner look
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        
        return self.fig
    
    def render_plotly(self,
                     width: int = 800,
                     height: int = 800,
                     show_grid: bool = False,
                     line_width: float = 2,
                     point_size: float = 8,
                     save_path: Optional[str] = None) -> go.Figure:
        """
        Render the Kolam pattern using plotly (interactive).
        
        Args:
            width: Figure width in pixels
            height: Figure height in pixels
            show_grid: Whether to show grid lines
            line_width: Width of pattern lines
            point_size: Size of pattern points
            save_path: Path to save the figure as HTML (optional)
            
        Returns:
            plotly Figure object
        """
        # Generate symmetric pattern if needed
        points = self._generate_symmetric_pattern() if self.pattern.symmetry > 1 else self.pattern.points
        
        self.plotly_fig = go.Figure()
        
        # Draw lines
        for line_idx, (start, end) in enumerate(self.pattern.lines):
            if start < len(points) and end < len(points):
                p1 = points[start]
                p2 = points[end]
                
                color = 'black'
                if self.pattern.colors and line_idx < len(self.pattern.colors):
                    color = self.pattern.colors[line_idx]
                
                self.plotly_fig.add_trace(go.Scatter(
                    x=[p1.x, p2.x],
                    y=[p1.y, p2.y],
                    mode='lines',
                    line=dict(color=color, width=line_width),
                    hoverinfo='skip',
                    showlegend=False
                ))
        
        # Draw points
        if len(points) > 0:
            point_xs = [p.x for p in points]
            point_ys = [p.y for p in points]
            
            self.plotly_fig.add_trace(go.Scatter(
                x=point_xs,
                y=point_ys,
                mode='markers',
                marker=dict(size=point_size, color='red', opacity=0.7),
                hovertemplate='<b>Point</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>',
                showlegend=False
            ))
        
        # Update layout
        self.plotly_fig.update_layout(
            title=dict(
                text=f'Kolam Pattern: {self.pattern.name}',
                font=dict(size=20),
                x=0.5,
                xanchor='center'
            ),
            width=width,
            height=height,
            hovermode='closest',
            plot_bgcolor='#fffaf0',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=show_grid,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                showgrid=show_grid,
                zeroline=False,
                showticklabels=False,
                scaleanchor='x',
                scaleratio=1
            )
        )
        
        # Save if path provided
        if save_path:
            self.plotly_fig.write_html(save_path)
            print(f"Interactive figure saved to {save_path}")
        
        return self.plotly_fig
    
    def show_matplotlib(self):
        """Display the matplotlib figure."""
        if self.fig is None:
            self.render_matplotlib()
        plt.show()
    
    def show_plotly(self):
        """Display the plotly figure."""
        if self.plotly_fig is None:
            self.render_plotly()
        self.plotly_fig.show()


class GeometricKolamGenerator:
    """Generate common geometric Kolam patterns."""
    
    @staticmethod
    def create_dot_grid_pattern(rows: int = 5, cols: int = 5, 
                               dot_spacing: float = 1.0) -> KolamPattern:
        """
        Create a Kolam pattern based on a dot grid.
        
        Args:
            rows: Number of rows
            cols: Number of columns
            dot_spacing: Distance between dots
            
        Returns:
            KolamPattern object
        """
        points = []
        for i in range(rows):
            for j in range(cols):
                points.append(Point(j * dot_spacing, i * dot_spacing))
        
        # Create connecting lines (simple grid connection)
        lines = []
        for i in range(rows):
            for j in range(cols - 1):
                start_idx = i * cols + j
                end_idx = i * cols + j + 1
                lines.append((start_idx, end_idx))
        
        for i in range(rows - 1):
            for j in range(cols):
                start_idx = i * cols + j
                end_idx = (i + 1) * cols + j
                lines.append((start_idx, end_idx))
        
        return KolamPattern(
            name="Dot Grid Pattern",
            points=points,
            lines=lines,
            style=KolamStyle.GEOMETRIC,
            symmetry=1
        )
    
    @staticmethod
    def create_star_pattern(points_count: int = 8, radius: float = 5.0) -> KolamPattern:
        """
        Create a star-shaped Kolam pattern.
        
        Args:
            points_count: Number of star points
            radius: Radius of the star
            
        Returns:
            KolamPattern object
        """
        points = []
        center = Point(0, 0)
        points.append(center)
        
        for i in range(points_count):
            angle = (2 * np.pi * i) / points_count
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            points.append(Point(x, y))
        
        # Connect center to all outer points
        lines = [(0, i + 1) for i in range(points_count)]
        
        # Connect adjacent outer points
        for i in range(points_count):
            lines.append((i + 1, ((i + 1) % points_count) + 1))
        
        return KolamPattern(
            name="Star Pattern",
            points=points,
            lines=lines,
            style=KolamStyle.GEOMETRIC,
            symmetry=points_count
        )
    
    @staticmethod
    def create_concentric_circles_pattern(circle_count: int = 5, 
                                         radius_step: float = 1.0,
                                         points_per_circle: int = 12) -> KolamPattern:
        """
        Create a concentric circles Kolam pattern.
        
        Args:
            circle_count: Number of concentric circles
            radius_step: Distance between circles
            points_per_circle: Number of points per circle
            
        Returns:
            KolamPattern object
        """
        points = []
        lines = []
        point_idx = 0
        
        for circle in range(circle_count):
            radius = (circle + 1) * radius_step
            circle_start_idx = point_idx
            
            for i in range(points_per_circle):
                angle = (2 * np.pi * i) / points_per_circle
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                points.append(Point(x, y))
                
                # Connect to next point on same circle
                if i < points_per_circle - 1:
                    lines.append((point_idx, point_idx + 1))
                else:
                    lines.append((point_idx, circle_start_idx))
                
                point_idx += 1
            
            # Connect to previous circle if exists
            if circle > 0:
                prev_circle_start = circle_start_idx - points_per_circle
                for i in range(points_per_circle):
                    lines.append((circle_start_idx + i, prev_circle_start + i))
        
        return KolamPattern(
            name="Concentric Circles Pattern",
            points=points,
            lines=lines,
            style=KolamStyle.GEOMETRIC,
            symmetry=points_per_circle
        )


def create_custom_kolam(name: str, points: List[Tuple[float, float]], 
                       lines: List[Tuple[int, int]], 
                       style: KolamStyle = KolamStyle.TRADITIONAL,
                       colors: Optional[List[str]] = None,
                       symmetry: int = 1) -> KolamPattern:
    """
    Create a custom Kolam pattern.
    
    Args:
        name: Name of the pattern
        points: List of (x, y) coordinate tuples
        lines: List of (start_idx, end_idx) tuples defining connections
        style: KolamStyle of the pattern
        colors: Optional list of colors for lines
        symmetry: Number of symmetry axes
        
    Returns:
        KolamPattern object
    """
    point_objects = [Point(x, y) for x, y in points]
    return KolamPattern(
        name=name,
        points=point_objects,
        lines=lines,
        style=style,
        colors=colors,
        symmetry=symmetry
    )


# Example usage and helper functions
def example_visualize_star_pattern():
    """Example: Create and visualize a star pattern."""
    pattern = GeometricKolamGenerator.create_star_pattern(points_count=8, radius=5.0)
    visualizer = KolamVisualizer(pattern)
    
    # Render using both backends
    visualizer.render_matplotlib(save_path='star_pattern_matplotlib.png')
    visualizer.render_plotly(save_path='star_pattern_plotly.html')
    
    return visualizer


def example_visualize_concentric_pattern():
    """Example: Create and visualize concentric circles pattern."""
    pattern = GeometricKolamGenerator.create_concentric_circles_pattern(
        circle_count=4, 
        radius_step=1.5,
        points_per_circle=16
    )
    visualizer = KolamVisualizer(pattern)
    
    # Render using both backends
    visualizer.render_matplotlib(save_path='concentric_pattern_matplotlib.png')
    visualizer.render_plotly(save_path='concentric_pattern_plotly.html')
    
    return visualizer


if __name__ == "__main__":
    # Example: Create and display patterns
    print("Generating Kolam patterns...")
    
    # Star pattern
    print("\nGenerating star pattern...")
    star_visualizer = example_visualize_star_pattern()
    
    # Concentric circles pattern
    print("Generating concentric circles pattern...")
    concentric_visualizer = example_visualize_concentric_pattern()
    
    # Dot grid pattern
    print("Generating dot grid pattern...")
    grid_pattern = GeometricKolamGenerator.create_dot_grid_pattern(rows=6, cols=6)
    grid_visualizer = KolamVisualizer(grid_pattern)
    grid_visualizer.render_matplotlib(save_path='dot_grid_pattern_matplotlib.png')
    grid_visualizer.render_plotly(save_path='dot_grid_pattern_plotly.html')
    
    print("\nPatterns generated successfully!")
    print("Matplotlib files: *_matplotlib.png")
    print("Plotly files: *_plotly.html")
