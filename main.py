#!/usr/bin/env python3
"""
Kolam Design Generator - CLI Application
A command-line tool for generating and customizing traditional Kolam designs.
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple
import json


class KolamDesignGenerator:
    """Main class for generating Kolam designs."""
    
    def __init__(self, size: int = 10, pattern: str = "default"):
        """
        Initialize the Kolam Design Generator.
        
        Args:
            size: Grid size for the Kolam design (default: 10)
            pattern: Pattern type to use (default, symmetrical, circular, etc.)
        """
        self.size = size
        self.pattern = pattern
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.design_name = f"kolam_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def create_default_pattern(self) -> None:
        """Create a default diamond/rhombus pattern."""
        center = self.size // 2
        
        for i in range(self.size):
            for j in range(self.size):
                distance = abs(i - center) + abs(j - center)
                if distance <= center - 1 and distance % 2 == 0:
                    self.grid[i][j] = '●'
                    
    def create_symmetrical_pattern(self) -> None:
        """Create a symmetrical dot pattern with 4-fold symmetry."""
        center = self.size // 2
        radius = center - 1
        
        # Create circular pattern with symmetry
        for i in range(self.size):
            for j in range(self.size):
                dx = abs(i - center)
                dy = abs(j - center)
                distance = (dx**2 + dy**2)**0.5
                
                if distance <= radius and int(distance) % 2 == 0:
                    self.grid[i][j] = '◆'
                    
    def create_circular_pattern(self) -> None:
        """Create a circular Kolam pattern."""
        center = self.size // 2
        radius = center - 1
        
        for i in range(self.size):
            for j in range(self.size):
                dx = i - center
                dy = j - center
                distance = (dx**2 + dy**2)**0.5
                
                # Create concentric circles
                if radius - 1 <= distance <= radius + 0.5:
                    self.grid[i][j] = '○'
                elif distance <= radius - 2 and int(distance) % 2 == 0:
                    self.grid[i][j] = '·'
                    
    def create_star_pattern(self) -> None:
        """Create a star-shaped Kolam pattern."""
        center = self.size // 2
        
        for i in range(self.size):
            for j in range(self.size):
                dx = abs(i - center)
                dy = abs(j - center)
                
                # Create star shape
                if (dx + dy) <= center - 1:
                    if (dx == 0 or dy == 0 or dx == dy) and (dx + dy) % 2 == 0:
                        self.grid[i][j] = '★'
                        
    def generate(self) -> None:
        """Generate the Kolam pattern based on selected type."""
        patterns = {
            'default': self.create_default_pattern,
            'symmetrical': self.create_symmetrical_pattern,
            'circular': self.create_circular_pattern,
            'star': self.create_star_pattern,
        }
        
        if self.pattern in patterns:
            patterns[self.pattern]()
        else:
            print(f"Warning: Unknown pattern '{self.pattern}'. Using default pattern.")
            self.create_default_pattern()
            
    def display(self, show_grid_numbers: bool = False) -> str:
        """
        Display the Kolam design.
        
        Args:
            show_grid_numbers: Whether to show grid coordinates
            
        Returns:
            String representation of the Kolam design
        """
        output = []
        
        # Add header
        output.append(f"\n{'='*40}")
        output.append(f"Kolam Design - Pattern: {self.pattern.upper()}")
        output.append(f"Grid Size: {self.size}x{self.size}")
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"{'='*40}\n")
        
        # Add grid numbers if requested
        if show_grid_numbers:
            output.append("   " + " ".join(f"{i:2d}" for i in range(self.size)))
            output.append("   " + "─" * (self.size * 3 - 1))
        
        # Add grid content
        for i, row in enumerate(self.grid):
            if show_grid_numbers:
                output.append(f"{i:2d}│ " + " ".join(row))
            else:
                output.append("  " + " ".join(row))
                
        output.append(f"\n{'='*40}\n")
        
        return "\n".join(output)
    
    def save_to_file(self, filename: Optional[str] = None, 
                     output_dir: str = "output") -> str:
        """
        Save the Kolam design to a file.
        
        Args:
            filename: Custom filename (without extension)
            output_dir: Directory to save the file
            
        Returns:
            Path to the saved file
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        if filename:
            self.design_name = filename
            
        filepath = Path(output_dir) / f"{self.design_name}.txt"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.display())
            
        return str(filepath)
    
    def export_as_json(self, filename: Optional[str] = None, 
                      output_dir: str = "output") -> str:
        """
        Export Kolam design as JSON.
        
        Args:
            filename: Custom filename (without extension)
            output_dir: Directory to save the file
            
        Returns:
            Path to the saved JSON file
        """
        Path(output_dir).mkdir(exist_ok=True)
        
        if filename:
            name = filename
        else:
            name = self.design_name
            
        filepath = Path(output_dir) / f"{name}.json"
        
        data = {
            "design_name": name,
            "pattern_type": self.pattern,
            "grid_size": self.size,
            "generated_at": datetime.now().isoformat(),
            "grid": self.grid
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        return str(filepath)
    
    def get_statistics(self) -> dict:
        """Get statistics about the generated Kolam."""
        filled_cells = sum(1 for row in self.grid for cell in row if cell != ' ')
        total_cells = self.size * self.size
        
        return {
            "total_cells": total_cells,
            "filled_cells": filled_cells,
            "empty_cells": total_cells - filled_cells,
            "fill_percentage": round((filled_cells / total_cells) * 100, 2)
        }


class KolamCLI:
    """Command-line interface for Kolam Design Generator."""
    
    def __init__(self):
        """Initialize the CLI application."""
        self.parser = self._create_parser()
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            prog='Kolam Design Generator',
            description='Generate beautiful traditional Kolam designs',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Generate default pattern
  python main.py
  
  # Generate circular pattern with size 15
  python main.py --pattern circular --size 15
  
  # Generate and save to file
  python main.py --pattern star --output kolam_design
  
  # Generate with all features
  python main.py --pattern symmetrical --size 12 --save --json --stats
            """
        )
        
        parser.add_argument(
            '--pattern', '-p',
            type=str,
            default='default',
            choices=['default', 'symmetrical', 'circular', 'star'],
            help='Pattern type to generate (default: default)'
        )
        
        parser.add_argument(
            '--size', '-s',
            type=int,
            default=10,
            help='Grid size for the design (default: 10)'
        )
        
        parser.add_argument(
            '--output', '-o',
            type=str,
            help='Output filename (without extension)'
        )
        
        parser.add_argument(
            '--save',
            action='store_true',
            help='Save design to text file'
        )
        
        parser.add_argument(
            '--json',
            action='store_true',
            help='Export design as JSON'
        )
        
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Display design statistics'
        )
        
        parser.add_argument(
            '--grid',
            action='store_true',
            help='Show grid coordinates'
        )
        
        parser.add_argument(
            '--version', '-v',
            action='version',
            version='Kolam Design Generator v1.0.0'
        )
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI application.
        
        Args:
            args: Command-line arguments (uses sys.argv if None)
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            parsed_args = self.parser.parse_args(args)
            
            # Validate size
            if parsed_args.size < 5 or parsed_args.size > 50:
                print("Error: Size must be between 5 and 50")
                return 1
            
            # Create and generate design
            kolam = KolamDesignGenerator(
                size=parsed_args.size,
                pattern=parsed_args.pattern
            )
            kolam.generate()
            
            # Display the design
            print(kolam.display(show_grid_numbers=parsed_args.grid))
            
            # Show statistics if requested
            if parsed_args.stats:
                stats = kolam.get_statistics()
                print(f"\n{'Statistics':─^40}")
                print(f"Total Cells: {stats['total_cells']}")
                print(f"Filled Cells: {stats['filled_cells']}")
                print(f"Empty Cells: {stats['empty_cells']}")
                print(f"Fill Percentage: {stats['fill_percentage']}%")
                print(f"{'─'*40}\n")
            
            # Save to files if requested
            if parsed_args.save or parsed_args.output:
                filename = parsed_args.output if parsed_args.output else None
                filepath = kolam.save_to_file(filename)
                print(f"✓ Design saved to: {filepath}")
            
            if parsed_args.json or parsed_args.output:
                filename = parsed_args.output if parsed_args.output else None
                filepath = kolam.export_as_json(filename)
                print(f"✓ JSON exported to: {filepath}")
            
            return 0
            
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1


def main():
    """Main entry point for the application."""
    cli = KolamCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
