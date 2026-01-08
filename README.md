# Kolam Design Generator

A powerful Python application for generating and visualizing traditional Indian Kolam designs using geometric algorithms and artistic patterns.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

The Kolam Design Generator is an innovative tool that creates authentic Kolam patterns inspired by traditional Indian art forms. Kolams are decorative designs traditionally drawn on floors during festivals and special occasions, particularly in South India. This generator uses computational geometry and algorithmic design principles to produce beautiful, intricate patterns that honor this cultural heritage.

### What is a Kolam?

A Kolam (also known as Rangoli in other parts of India) is a colorful art form involving the creation of patterns on floors using colored powders, rice flour, or flowers. These designs are deeply rooted in Indian culture and carry significant cultural and spiritual significance.

## ✨ Features

- **Multiple Kolam Pattern Generation**: Generate various types of Kolam designs including:
  - Symmetrical geometric patterns
  - Floral-inspired designs
  - Traditional diamond patterns
  - Spiral and concentric patterns
  - Custom hybrid patterns

- **Visualization**: 
  - Real-time preview of generated patterns
  - High-resolution output capabilities
  - Export to multiple image formats (PNG, SVG, PDF)

- **Customization Options**:
  - Adjustable complexity levels (simple, medium, complex)
  - Custom color palettes
  - Variable pattern sizes and scales
  - Rotation and reflection options
  - Symmetry configuration

- **Performance**:
  - Fast pattern generation algorithms
  - Optimized rendering pipeline
  - Support for batch processing

- **User-Friendly Interface**:
  - Command-line interface with intuitive commands
  - Interactive parameter adjustment
  - Detailed help documentation

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Aryankatiyarcsjmu/Kolam-Design-Generator.git
   cd Kolam-Design-Generator
   ```

2. **Create a Virtual Environment** (Optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -m kolam_generator --version
   ```

### Dependencies

The project requires the following packages (see `requirements.txt` for specific versions):
- `numpy` - Numerical computations
- `matplotlib` - Visualization and plotting
- `pillow` - Image processing
- `opencv-python` - Advanced image operations
- `click` - Command-line interface
- `pyyaml` - Configuration management

## 🚀 Usage

### Basic Usage

#### Generate a Simple Kolam Pattern
```bash
python -m kolam_generator generate --pattern geometric --output kolam_output.png
```

#### Generate with Custom Parameters
```bash
python -m kolam_generator generate \
  --pattern floral \
  --complexity high \
  --size 1024 \
  --colors gold,pink,white \
  --output my_kolam.png
```

#### List Available Patterns
```bash
python -m kolam_generator list-patterns
```

#### Generate Multiple Patterns
```bash
python -m kolam_generator batch --count 5 --pattern random --output-dir ./kolams
```

### Advanced Usage

#### Using the Python API Directly

```python
from kolam_generator import KolamGenerator, PatternConfig

# Create a configuration
config = PatternConfig(
    pattern_type='geometric',
    complexity='medium',
    size=800,
    colors=['#FF6B6B', '#4ECDC4', '#45B7D1'],
    symmetry=8,
    seed=42
)

# Generate the pattern
generator = KolamGenerator(config)
kolam = generator.generate()

# Save the output
kolam.save('my_kolam.png')

# Display the pattern
kolam.show()
```

### Command-Line Arguments

```
Usage: kolam_generator [OPTIONS] COMMAND [ARGS]...

Commands:
  generate       Generate a single Kolam pattern
  batch          Generate multiple Kolam patterns
  list-patterns  List all available pattern types
  configure      Set default configuration

Options:
  --help        Show help message
  --version     Show version number
```

### Configuration File

Create a `config.yaml` file to set default parameters:

```yaml
generation:
  default_pattern: geometric
  default_complexity: medium
  default_size: 1024

output:
  format: png
  quality: high
  output_directory: ./output

colors:
  palette1:
    - "#FF6B6B"
    - "#4ECDC4"
    - "#45B7D1"
  palette2:
    - "#FFE66D"
    - "#95E1D3"
    - "#F38181"
```

## 📁 Project Structure

```
Kolam-Design-Generator/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── setup.py                           # Package setup configuration
├── config.yaml                        # Default configuration
│
├── kolam_generator/                   # Main package directory
│   ├── __init__.py                    # Package initialization
│   ├── main.py                        # Entry point for CLI
│   │
│   ├── core/                          # Core functionality
│   │   ├── __init__.py
│   │   ├── generator.py               # Main KolamGenerator class
│   │   ├── patterns.py                # Pattern definitions and algorithms
│   │   └── config.py                  # Configuration management
│   │
│   ├── patterns/                      # Specific pattern implementations
│   │   ├── __init__.py
│   │   ├── geometric.py               # Geometric patterns
│   │   ├── floral.py                  # Floral patterns
│   │   ├── diamond.py                 # Diamond patterns
│   │   ├── spiral.py                  # Spiral patterns
│   │   └── custom.py                  # Custom/hybrid patterns
│   │
│   ├── rendering/                     # Rendering and visualization
│   │   ├── __init__.py
│   │   ├── renderer.py                # Core rendering engine
│   │   ├── colors.py                  # Color management and palettes
│   │   └── effects.py                 # Visual effects and filters
│   │
│   ├── utils/                         # Utility functions
│   │   ├── __init__.py
│   │   ├── geometry.py                # Geometric calculations
│   │   ├── helpers.py                 # Helper functions
│   │   └── validators.py              # Input validation
│   │
│   └── cli/                           # Command-line interface
│       ├── __init__.py
│       ├── commands.py                # CLI commands
│       └── output_handlers.py         # Output formatting
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── test_generator.py              # Generator tests
│   ├── test_patterns.py               # Pattern tests
│   ├── test_rendering.py              # Rendering tests
│   └── test_utils.py                  # Utility function tests
│
├── examples/                          # Example scripts
│   ├── basic_usage.py                 # Basic usage examples
│   ├── advanced_usage.py              # Advanced usage examples
│   └── batch_generation.py            # Batch processing example
│
├── docs/                              # Documentation
│   ├── INSTALLATION.md                # Detailed installation guide
│   ├── API_REFERENCE.md               # API documentation
│   ├── PATTERN_GUIDE.md               # Pattern types and customization
│   ├── TUTORIAL.md                    # User tutorial
│   └── CONTRIBUTING.md                # Contribution guidelines
│
└── output/                            # Default output directory
    └── .gitkeep                       # Placeholder file
```

### Directory Descriptions

| Directory | Purpose |
|-----------|---------|
| `kolam_generator/` | Main package containing all source code |
| `kolam_generator/core/` | Core generation logic and algorithms |
| `kolam_generator/patterns/` | Specific pattern type implementations |
| `kolam_generator/rendering/` | Visualization and rendering engines |
| `kolam_generator/utils/` | Utility functions and helpers |
| `kolam_generator/cli/` | Command-line interface implementation |
| `tests/` | Comprehensive test suite |
| `examples/` | Usage examples and demonstrations |
| `docs/` | Extended documentation |
| `output/` | Default location for generated patterns |

## ⚙️ Configuration

### Environment Variables

```bash
KOLAM_OUTPUT_DIR=/path/to/output        # Output directory
KOLAM_THEME=dark                        # UI theme (light/dark)
KOLAM_LOG_LEVEL=INFO                    # Logging level
KOLAM_USE_GPU=false                     # Enable GPU acceleration
```

### Default Color Palettes

The generator comes with pre-defined color palettes:

- **Traditional**: Gold, crimson, green, white
- **Festival**: Vibrant reds, yellows, greens, purples
- **Elegant**: Soft pastels and metallic accents
- **Modern**: Contemporary color schemes

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Write or update tests as needed
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/Aryankatiyarcsjmu/Kolam-Design-Generator.git
cd Kolam-Design-Generator
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 kolam_generator/
black kolam_generator/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Traditional Kolam artists who inspire this project
- The open-source community for excellent libraries
- Contributors and users who provide feedback and improvements
- Indian cultural heritage and artistic traditions

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation in the `docs/` directory
- Review examples in the `examples/` directory

## 🔗 Related Resources

- [Kolam - Wikipedia](https://en.wikipedia.org/wiki/Kolam)
- [Rangoli - Indian Art Form](https://en.wikipedia.org/wiki/Rangoli)
- [Computational Geometry](https://en.wikipedia.org/wiki/Computational_geometry)

---

**Last Updated**: January 8, 2026

**Version**: 1.0.0

**Repository**: [Kolam-Design-Generator](https://github.com/Aryankatiyarcsjmu/Kolam-Design-Generator)
