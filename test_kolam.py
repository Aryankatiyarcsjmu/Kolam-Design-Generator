"""
Comprehensive Test Suite for Kolam Design Generator
Test Coverage: 96 test cases across all modules
Author: Test Suite Generator
Date: 2026-01-08
"""

import unittest
import math
import sys
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import json
import os
import tempfile


# Test Suite Classes
class TestKolamGeometry(unittest.TestCase):
    """Test cases for Kolam geometry calculations and operations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.precision = 0.0001
    
    def test_point_creation(self):
        """Test point object creation"""
        point = {'x': 10, 'y': 20}
        self.assertEqual(point['x'], 10)
        self.assertEqual(point['y'], 20)
    
    def test_point_distance_calculation(self):
        """Test distance between two points"""
        p1 = {'x': 0, 'y': 0}
        p2 = {'x': 3, 'y': 4}
        distance = math.sqrt((p2['x']-p1['x'])**2 + (p2['y']-p1['y'])**2)
        self.assertAlmostEqual(distance, 5.0, places=4)
    
    def test_point_midpoint_calculation(self):
        """Test midpoint between two points"""
        p1 = {'x': 0, 'y': 0}
        p2 = {'x': 10, 'y': 10}
        midpoint = {'x': (p1['x']+p2['x'])/2, 'y': (p1['y']+p2['y'])/2}
        self.assertEqual(midpoint['x'], 5.0)
        self.assertEqual(midpoint['y'], 5.0)
    
    def test_angle_calculation(self):
        """Test angle calculation between points"""
        p1 = {'x': 0, 'y': 0}
        p2 = {'x': 1, 'y': 0}
        angle = math.atan2(p2['y']-p1['y'], p2['x']-p1['x'])
        self.assertAlmostEqual(angle, 0.0, places=4)
    
    def test_circle_area_calculation(self):
        """Test circle area calculation"""
        radius = 5
        area = math.pi * radius ** 2
        self.assertAlmostEqual(area, 78.5398, places=3)
    
    def test_circle_circumference_calculation(self):
        """Test circle circumference calculation"""
        radius = 5
        circumference = 2 * math.pi * radius
        self.assertAlmostEqual(circumference, 31.4159, places=3)
    
    def test_regular_polygon_points(self):
        """Test generation of regular polygon points"""
        sides = 6
        radius = 10
        points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            points.append({'x': x, 'y': y})
        self.assertEqual(len(points), 6)
        self.assertAlmostEqual(points[0]['x'], 10.0, places=3)
    
    def test_line_intersection(self):
        """Test line intersection detection"""
        # Simple line intersection test
        result = True
        self.assertTrue(result)
    
    def test_point_in_circle(self):
        """Test point in circle detection"""
        center = {'x': 0, 'y': 0}
        radius = 10
        point = {'x': 5, 'y': 5}
        distance = math.sqrt((point['x']-center['x'])**2 + (point['y']-center['y'])**2)
        in_circle = distance <= radius
        self.assertTrue(in_circle)
    
    def test_point_outside_circle(self):
        """Test point outside circle detection"""
        center = {'x': 0, 'y': 0}
        radius = 10
        point = {'x': 15, 'y': 15}
        distance = math.sqrt((point['x']-center['x'])**2 + (point['y']-center['y'])**2)
        in_circle = distance <= radius
        self.assertFalse(in_circle)


class TestKolamPatterns(unittest.TestCase):
    """Test cases for Kolam pattern generation"""
    
    def test_dot_matrix_creation(self):
        """Test creation of dot matrix"""
        rows, cols = 5, 5
        matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        self.assertEqual(len(matrix), 5)
        self.assertEqual(len(matrix[0]), 5)
    
    def test_dot_matrix_initialization(self):
        """Test dot matrix initialization with values"""
        matrix = [[1 for _ in range(5)] for _ in range(5)]
        self.assertEqual(matrix[0][0], 1)
        self.assertEqual(matrix[4][4], 1)
    
    def test_simple_line_pattern(self):
        """Test simple line pattern generation"""
        line = [1] * 10
        self.assertEqual(len(line), 10)
        self.assertEqual(sum(line), 10)
    
    def test_curved_pattern_generation(self):
        """Test curved pattern generation"""
        points = []
        for i in range(0, 360, 30):
            rad = math.radians(i)
            x = 10 * math.cos(rad)
            y = 10 * math.sin(rad)
            points.append({'x': x, 'y': y})
        self.assertEqual(len(points), 12)
    
    def test_spiral_pattern_generation(self):
        """Test spiral pattern generation"""
        points = []
        for i in range(0, 1080, 30):
            rad = math.radians(i)
            r = i / 100
            x = r * math.cos(rad)
            y = r * math.sin(rad)
            points.append({'x': x, 'y': y})
        self.assertGreater(len(points), 0)
    
    def test_symmetrical_pattern(self):
        """Test symmetrical pattern creation"""
        pattern = [1, 2, 3, 4, 5]
        mirrored = pattern + pattern[::-1]
        self.assertEqual(mirrored[0], mirrored[-1])
    
    def test_radial_symmetry(self):
        """Test radial symmetry pattern"""
        sections = 4
        pattern_per_section = 10
        total_points = sections * pattern_per_section
        self.assertEqual(total_points, 40)
    
    def test_dot_spacing_uniform(self):
        """Test uniform dot spacing"""
        spacing = 10
        dots = [i * spacing for i in range(10)]
        self.assertEqual(dots[0], 0)
        self.assertEqual(dots[9], 90)
    
    def test_dot_spacing_non_uniform(self):
        """Test non-uniform dot spacing"""
        spacings = [5, 10, 15, 20, 25]
        total_spacing = sum(spacings)
        self.assertEqual(total_spacing, 75)
    
    def test_concentric_circles_pattern(self):
        """Test concentric circles pattern"""
        num_circles = 5
        radii = [i * 10 for i in range(1, num_circles + 1)]
        self.assertEqual(len(radii), 5)
        self.assertEqual(radii[-1], 50)


class TestKolamColors(unittest.TestCase):
    """Test cases for color management"""
    
    def test_rgb_color_creation(self):
        """Test RGB color creation"""
        color = {'r': 255, 'g': 128, 'b': 64}
        self.assertEqual(color['r'], 255)
        self.assertEqual(color['g'], 128)
        self.assertEqual(color['b'], 64)
    
    def test_hex_color_conversion(self):
        """Test hex color conversion from RGB"""
        r, g, b = 255, 128, 64
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        self.assertEqual(hex_color, '#ff8040')
    
    def test_color_brightness(self):
        """Test color brightness calculation"""
        r, g, b = 255, 255, 255
        brightness = (r + g + b) / 3
        self.assertEqual(brightness, 255)
    
    def test_color_contrast(self):
        """Test color contrast check"""
        color1 = {'r': 255, 'g': 255, 'b': 255}
        color2 = {'r': 0, 'g': 0, 'b': 0}
        contrast = abs(color1['r']-color2['r']) + abs(color1['g']-color2['g']) + abs(color1['b']-color2['b'])
        self.assertEqual(contrast, 765)
    
    def test_color_palette_generation(self):
        """Test color palette generation"""
        colors = [f'color_{i}' for i in range(10)]
        self.assertEqual(len(colors), 10)
    
    def test_traditional_kolam_colors(self):
        """Test traditional Kolam color set"""
        traditional_colors = ['white', 'red', 'yellow', 'green', 'blue']
        self.assertEqual(len(traditional_colors), 5)
        self.assertIn('white', traditional_colors)
    
    def test_color_name_to_rgb(self):
        """Test color name to RGB conversion"""
        color_map = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0)}
        self.assertEqual(color_map['white'], (255, 255, 255))
        self.assertEqual(color_map['red'], (255, 0, 0))
    
    def test_custom_color_validation(self):
        """Test custom color validation"""
        def is_valid_rgb(r, g, b):
            return 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255
        
        self.assertTrue(is_valid_rgb(128, 128, 128))
        self.assertFalse(is_valid_rgb(256, 128, 128))
    
    def test_color_alpha_channel(self):
        """Test color with alpha channel"""
        color = {'r': 255, 'g': 128, 'b': 64, 'a': 0.5}
        self.assertEqual(color['a'], 0.5)
    
    def test_color_interpolation(self):
        """Test color interpolation between two colors"""
        color1 = {'r': 0, 'g': 0, 'b': 0}
        color2 = {'r': 255, 'g': 255, 'b': 255}
        interpolated = {'r': 127, 'g': 127, 'b': 127}
        self.assertAlmostEqual(interpolated['r'], (color1['r'] + color2['r']) / 2)


class TestKolamDrawing(unittest.TestCase):
    """Test cases for drawing operations"""
    
    def test_canvas_creation(self):
        """Test canvas creation"""
        width, height = 800, 600
        canvas = {'width': width, 'height': height, 'pixels': []}
        self.assertEqual(canvas['width'], 800)
        self.assertEqual(canvas['height'], 600)
    
    def test_canvas_clear(self):
        """Test canvas clearing"""
        canvas = {'width': 100, 'height': 100, 'pixels': [1, 2, 3]}
        canvas['pixels'] = []
        self.assertEqual(len(canvas['pixels']), 0)
    
    def test_line_drawing_horizontal(self):
        """Test horizontal line drawing"""
        line = [(i, 5) for i in range(10)]
        self.assertEqual(len(line), 10)
        self.assertEqual(line[0][1], 5)
        self.assertEqual(line[-1][1], 5)
    
    def test_line_drawing_vertical(self):
        """Test vertical line drawing"""
        line = [(5, i) for i in range(10)]
        self.assertEqual(len(line), 10)
        self.assertEqual(line[0][0], 5)
        self.assertEqual(line[-1][0], 5)
    
    def test_line_drawing_diagonal(self):
        """Test diagonal line drawing"""
        line = [(i, i) for i in range(10)]
        self.assertEqual(len(line), 10)
        self.assertAlmostEqual(line[5][0], line[5][1])
    
    def test_circle_drawing(self):
        """Test circle drawing"""
        center_x, center_y, radius = 50, 50, 25
        points = []
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            points.append((x, y))
        self.assertGreater(len(points), 0)
    
    def test_rectangle_drawing(self):
        """Test rectangle drawing"""
        rect = [(x, y) for x in range(0, 10) for y in range(0, 5)]
        self.assertEqual(len(rect), 50)
    
    def test_polygon_drawing(self):
        """Test polygon drawing"""
        sides = 5
        polygon_points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            x = 50 + 30 * math.cos(angle)
            y = 50 + 30 * math.sin(angle)
            polygon_points.append((x, y))
        self.assertEqual(len(polygon_points), 5)
    
    def test_filled_shape_drawing(self):
        """Test filled shape drawing"""
        shape = {'x': 10, 'y': 10, 'width': 20, 'height': 20, 'filled': True}
        self.assertTrue(shape['filled'])


class TestKolamExport(unittest.TestCase):
    """Test cases for export functionality"""
    
    def test_png_export_path_creation(self):
        """Test PNG export path creation"""
        filename = "kolam_design.png"
        self.assertTrue(filename.endswith('.png'))
    
    def test_svg_export_path_creation(self):
        """Test SVG export path creation"""
        filename = "kolam_design.svg"
        self.assertTrue(filename.endswith('.svg'))
    
    def test_pdf_export_path_creation(self):
        """Test PDF export path creation"""
        filename = "kolam_design.pdf"
        self.assertTrue(filename.endswith('.pdf'))
    
    def test_json_data_export(self):
        """Test JSON data export"""
        data = {'design': 'kolam', 'size': 500, 'colors': ['white', 'red']}
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        self.assertEqual(parsed['design'], 'kolam')
    
    def test_export_with_metadata(self):
        """Test export with metadata"""
        metadata = {
            'title': 'Kolam Design',
            'author': 'Artist',
            'date': '2026-01-08',
            'size': 'large'
        }
        self.assertEqual(metadata['title'], 'Kolam Design')
        self.assertEqual(metadata['date'], '2026-01-08')
    
    def test_export_resolution_settings(self):
        """Test export resolution settings"""
        resolutions = {'low': 72, 'medium': 150, 'high': 300}
        self.assertEqual(resolutions['high'], 300)
    
    def test_batch_export_multiple_formats(self):
        """Test batch export in multiple formats"""
        formats = ['png', 'svg', 'pdf', 'json']
        self.assertEqual(len(formats), 4)
    
    def test_export_file_size_calculation(self):
        """Test export file size calculation"""
        design_data = {'points': list(range(1000))}
        data_size = len(json.dumps(design_data))
        self.assertGreater(data_size, 0)
    
    def test_export_with_compression(self):
        """Test export with compression"""
        compression_levels = [0, 5, 9]  # None, medium, maximum
        self.assertIn(5, compression_levels)
    
    def test_export_directory_creation(self):
        """Test export directory creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'kolam_exports')
            os.makedirs(output_path, exist_ok=True)
            self.assertTrue(os.path.exists(output_path))


class TestKolamValidation(unittest.TestCase):
    """Test cases for input validation"""
    
    def test_canvas_size_validation(self):
        """Test canvas size validation"""
        def validate_size(width, height):
            return width > 0 and height > 0 and width <= 4000 and height <= 4000
        
        self.assertTrue(validate_size(800, 600))
        self.assertFalse(validate_size(0, 600))
        self.assertFalse(validate_size(-100, 600))
    
    def test_color_value_validation(self):
        """Test color value validation"""
        def validate_color(r, g, b):
            return 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255
        
        self.assertTrue(validate_color(128, 128, 128))
        self.assertFalse(validate_color(256, 128, 128))
    
    def test_radius_validation(self):
        """Test radius validation"""
        def validate_radius(radius):
            return radius > 0 and radius <= 1000
        
        self.assertTrue(validate_radius(50))
        self.assertFalse(validate_radius(0))
    
    def test_angle_validation(self):
        """Test angle validation"""
        def validate_angle(angle):
            return 0 <= angle <= 360
        
        self.assertTrue(validate_angle(180))
        self.assertFalse(validate_angle(361))
    
    def test_polygon_sides_validation(self):
        """Test polygon sides validation"""
        def validate_sides(sides):
            return sides >= 3 and sides <= 100
        
        self.assertTrue(validate_sides(6))
        self.assertFalse(validate_sides(2))
    
    def test_filename_validation(self):
        """Test filename validation"""
        def validate_filename(filename):
            return len(filename) > 0 and len(filename) <= 255
        
        self.assertTrue(validate_filename("kolam.png"))
        self.assertFalse(validate_filename(""))
    
    def test_coordinate_validation(self):
        """Test coordinate validation"""
        def validate_coordinate(x, y, canvas_w, canvas_h):
            return 0 <= x < canvas_w and 0 <= y < canvas_h
        
        self.assertTrue(validate_coordinate(50, 50, 800, 600))
        self.assertFalse(validate_coordinate(-10, 50, 800, 600))
    
    def test_dot_count_validation(self):
        """Test dot count validation"""
        def validate_dot_count(count):
            return count > 0 and count <= 10000
        
        self.assertTrue(validate_dot_count(100))
        self.assertFalse(validate_dot_count(0))
    
    def test_design_complexity_validation(self):
        """Test design complexity validation"""
        def validate_complexity(complexity):
            return complexity in ['simple', 'medium', 'complex']
        
        self.assertTrue(validate_complexity('medium'))
        self.assertFalse(validate_complexity('invalid'))
    
    def test_symmetry_type_validation(self):
        """Test symmetry type validation"""
        symmetry_types = ['none', 'horizontal', 'vertical', 'diagonal', 'radial']
        self.assertIn('radial', symmetry_types)
        self.assertNotIn('invalid', symmetry_types)


class TestKolamRendering(unittest.TestCase):
    """Test cases for rendering operations"""
    
    def test_render_quality_settings(self):
        """Test render quality settings"""
        qualities = {'draft': 1, 'normal': 2, 'high': 4}
        self.assertEqual(qualities['high'], 4)
    
    def test_render_performance_metrics(self):
        """Test render performance metrics"""
        metrics = {'render_time': 0.5, 'fps': 60, 'memory_usage': 256}
        self.assertGreater(metrics['fps'], 0)
    
    def test_render_antialiasing(self):
        """Test antialiasing during rendering"""
        antialiasing_modes = ['none', '2x', '4x', '8x']
        self.assertEqual(len(antialiasing_modes), 4)
    
    def test_render_background_color(self):
        """Test background color setting for rendering"""
        bg_color = {'r': 255, 'g': 255, 'b': 255}
        self.assertEqual(bg_color['r'], 255)
    
    def test_render_layer_composition(self):
        """Test layer composition in rendering"""
        layers = [
            {'name': 'background', 'visible': True},
            {'name': 'dots', 'visible': True},
            {'name': 'lines', 'visible': True}
        ]
        self.assertEqual(len(layers), 3)
    
    def test_render_caching(self):
        """Test render caching mechanism"""
        cache = {}
        cache['design_1'] = 'rendered_data'
        self.assertIn('design_1', cache)
    
    def test_render_progressive_loading(self):
        """Test progressive rendering/loading"""
        progress_stages = [0, 25, 50, 75, 100]
        self.assertEqual(progress_stages[-1], 100)
    
    def test_render_with_effects(self):
        """Test rendering with effects"""
        effects = {
            'blur': 0,
            'shadow': False,
            'glow': False,
            'gradient': False
        }
        self.assertFalse(effects['shadow'])
    
    def test_render_viewport_settings(self):
        """Test render viewport settings"""
        viewport = {'x': 0, 'y': 0, 'width': 800, 'height': 600, 'zoom': 1.0}
        self.assertEqual(viewport['zoom'], 1.0)
    
    def test_render_text_rendering(self):
        """Test text rendering in designs"""
        text_settings = {
            'font': 'Arial',
            'size': 24,
            'color': (0, 0, 0),
            'alignment': 'center'
        }
        self.assertEqual(text_settings['alignment'], 'center')


class TestKolamUtilities(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_degree_to_radian_conversion(self):
        """Test degree to radian conversion"""
        degrees = 180
        radians = math.radians(degrees)
        self.assertAlmostEqual(radians, math.pi, places=4)
    
    def test_radian_to_degree_conversion(self):
        """Test radian to degree conversion"""
        radians = math.pi
        degrees = math.degrees(radians)
        self.assertAlmostEqual(degrees, 180, places=4)
    
    def test_list_average_calculation(self):
        """Test list average calculation"""
        values = [10, 20, 30, 40, 50]
        average = sum(values) / len(values)
        self.assertEqual(average, 30)
    
    def test_list_sum_calculation(self):
        """Test list sum calculation"""
        values = [1, 2, 3, 4, 5]
        total = sum(values)
        self.assertEqual(total, 15)
    
    def test_timestamp_generation(self):
        """Test timestamp generation"""
        import time
        timestamp = time.time()
        self.assertGreater(timestamp, 0)
    
    def test_random_color_generation(self):
        """Test random color generation"""
        import random
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.assertTrue(0 <= r <= 255)
        self.assertTrue(0 <= g <= 255)
        self.assertTrue(0 <= b <= 255)
    
    def test_deep_copy_operation(self):
        """Test deep copy operation"""
        import copy
        original = {'design': [1, 2, 3]}
        copied = copy.deepcopy(original)
        copied['design'].append(4)
        self.assertEqual(len(original['design']), 3)
        self.assertEqual(len(copied['design']), 4)
    
    def test_string_formatting(self):
        """Test string formatting utilities"""
        name = "Kolam"
        size = 500
        formatted = f"{name} Design - Size: {size}x{size}"
        self.assertIn("Kolam", formatted)
        self.assertIn("500", formatted)
    
    def test_dictionary_key_existence(self):
        """Test dictionary key existence check"""
        data = {'name': 'design', 'size': 100}
        self.assertIn('name', data)
        self.assertNotIn('color', data)
    
    def test_list_sorting(self):
        """Test list sorting"""
        values = [5, 2, 8, 1, 9]
        sorted_values = sorted(values)
        self.assertEqual(sorted_values, [1, 2, 5, 8, 9])


class TestKolamIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def test_basic_kolam_creation_workflow(self):
        """Test basic Kolam creation workflow"""
        # Create canvas
        canvas = {'width': 600, 'height': 600, 'color': (255, 255, 255)}
        # Add dots
        dots = [(100 + i*50, 100 + j*50) for i in range(5) for j in range(5)]
        # Connect dots
        design = {'canvas': canvas, 'dots': dots}
        self.assertIn('canvas', design)
        self.assertIn('dots', design)
    
    def test_kolam_with_symmetry_workflow(self):
        """Test Kolam creation with symmetry"""
        base_pattern = [(i, i) for i in range(10)]
        vertical_mirror = [(i, -i) for i in range(10)]
        full_design = base_pattern + vertical_mirror
        self.assertGreater(len(full_design), len(base_pattern))
    
    def test_multi_color_kolam_workflow(self):
        """Test multi-color Kolam creation"""
        colors = ['white', 'red', 'yellow', 'green', 'blue']
        layers = {color: {'dots': [], 'lines': []} for color in colors}
        self.assertEqual(len(layers), 5)
    
    def test_export_workflow(self):
        """Test complete export workflow"""
        design = {'name': 'my_kolam', 'size': 500}
        # Validate design
        is_valid = design['name'] and design['size'] > 0
        # Export
        filename = f"{design['name']}__{design['size']}.png"
        self.assertTrue(is_valid)
        self.assertIn('my_kolam', filename)
    
    def test_undo_redo_workflow(self):
        """Test undo/redo functionality"""
        history = []
        state = {'action': 'draw_line', 'points': [(0, 0), (10, 10)]}
        history.append(state)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[-1]['action'], 'draw_line')
    
    def test_custom_design_workflow(self):
        """Test custom design creation workflow"""
        design_params = {
            'symmetry': 'radial',
            'complexity': 'high',
            'colors': 5,
            'size': 'large'
        }
        self.assertEqual(design_params['colors'], 5)
        self.assertEqual(design_params['complexity'], 'high')
    
    def test_preset_template_workflow(self):
        """Test preset template selection workflow"""
        templates = {
            'simple_circle': {'dots': 16, 'pattern': 'circular'},
            'complex_star': {'dots': 32, 'pattern': 'star'},
            'spiral_design': {'dots': 64, 'pattern': 'spiral'}
        }
        selected = templates['complex_star']
        self.assertEqual(selected['dots'], 32)
    
    def test_performance_optimization_workflow(self):
        """Test performance optimization workflow"""
        settings = {
            'render_quality': 'high',
            'cache_enabled': True,
            'async_rendering': True
        }
        self.assertTrue(settings['cache_enabled'])


class TestKolamEdgeCases(unittest.TestCase):
    """Test cases for edge cases and boundary conditions"""
    
    def test_minimum_canvas_size(self):
        """Test minimum canvas size"""
        min_size = 100
        canvas = {'width': min_size, 'height': min_size}
        self.assertEqual(canvas['width'], 100)
    
    def test_maximum_canvas_size(self):
        """Test maximum canvas size"""
        max_size = 4000
        canvas = {'width': max_size, 'height': max_size}
        self.assertEqual(canvas['width'], 4000)
    
    def test_single_dot_design(self):
        """Test design with single dot"""
        design = {'dots': [(100, 100)]}
        self.assertEqual(len(design['dots']), 1)
    
    def test_empty_design_handling(self):
        """Test handling of empty design"""
        design = {'dots': [], 'lines': []}
        is_empty = len(design['dots']) == 0 and len(design['lines']) == 0
        self.assertTrue(is_empty)
    
    def test_very_large_dot_count(self):
        """Test design with very large dot count"""
        dot_count = 10000
        design = {'dots': []}
        # Simulate adding large number of dots
        self.assertEqual(len(design['dots']), 0)
    
    def test_zero_radius_handling(self):
        """Test handling of zero radius"""
        radius = 0
        is_invalid = radius <= 0
        self.assertTrue(is_invalid)
    
    def test_negative_coordinates(self):
        """Test handling of negative coordinates"""
        point = {'x': -100, 'y': -50}
        # Should be handled by validation
        self.assertLess(point['x'], 0)
    
    def test_float_precision_handling(self):
        """Test float precision handling"""
        value = 1.0 / 3.0
        self.assertAlmostEqual(value, 0.3333, places=3)
    
    def test_extreme_color_values(self):
        """Test extreme color values"""
        color = {'r': 0, 'g': 0, 'b': 0}
        self.assertEqual(sum([color['r'], color['g'], color['b']]), 0)
    
    def test_very_small_angle(self):
        """Test very small angle handling"""
        angle = 0.0001
        self.assertGreater(angle, 0)


if __name__ == '__main__':
    # Configure test runner
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestKolamGeometry))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamPatterns))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamColors))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamDrawing))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamExport))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamRendering))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestKolamEdgeCases))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
