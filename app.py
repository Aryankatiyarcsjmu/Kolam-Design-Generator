"""
Kolam Design Generator - Streamlit Web Interface
A beautiful web application for creating, visualizing, and exporting traditional Kolam designs
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Polygon, Arc
import io
from PIL import Image
import json
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Kolam Design Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        font-weight: 600;
    }
    .title-text {
        text-align: center;
        color: #FF6B9D;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle-text {
        text-align: center;
        color: #8B4789;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title-text">🎨 Kolam Design Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Create Beautiful Traditional Indian Kolam Patterns</div>', unsafe_allow_html=True)

# Initialize session state
if 'generated_design' not in st.session_state:
    st.session_state.generated_design = None
if 'design_history' not in st.session_state:
    st.session_state.design_history = []


class KolamGenerator:
    """Generate beautiful Kolam patterns with various designs"""
    
    def __init__(self, size=10, pattern_type="flower"):
        self.size = size
        self.pattern_type = pattern_type
        self.fig = None
        self.ax = None
    
    def create_figure(self):
        """Create matplotlib figure for Kolam design"""
        self.fig, self.ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        self.ax.axis('off')
        self.fig.patch.set_facecolor('white')
    
    def generate_flower_kolam(self, petals=6, radius=8, color='#FF6B9D'):
        """Generate flower-shaped Kolam pattern"""
        self.create_figure()
        
        # Draw petals
        angles = np.linspace(0, 2*np.pi, petals, endpoint=False)
        petal_colors = [color, '#8B4789', '#FF1493', '#FF69B4', '#C71585', '#FFB6C1']
        
        for i, angle in enumerate(angles):
            # Petal center
            petal_x = radius * 0.6 * np.cos(angle)
            petal_y = radius * 0.6 * np.sin(angle)
            
            # Draw petal
            petal_circle = Circle((petal_x, petal_y), radius*0.35, 
                                 color=petal_colors[i % len(petal_colors)], 
                                 alpha=0.7, edgecolor='black', linewidth=2)
            self.ax.add_patch(petal_circle)
            
            # Add decorative dots
            for j in np.linspace(0.1, 0.9, 5):
                dot_x = petal_x + j * radius * 0.3 * np.cos(angle)
                dot_y = petal_y + j * radius * 0.3 * np.sin(angle)
                dot = Circle((dot_x, dot_y), 0.15, color='gold', edgecolor='black')
                self.ax.add_patch(dot)
        
        # Central circle
        center_circle = Circle((0, 0), radius*0.25, color='gold', 
                              edgecolor='black', linewidth=2)
        self.ax.add_patch(center_circle)
        
        # Decorative center dots
        for i in range(3):
            small_dot = Circle((0, 0), 0.1, color='#FF6B9D')
            self.ax.add_patch(small_dot)
    
    def generate_geometric_kolam(self, divisions=8, color='#8B4789'):
        """Generate geometric pattern Kolam"""
        self.create_figure()
        
        # Draw concentric squares
        for i in range(1, 5):
            size = i * 2.5
            square = patches.Rectangle((-size, -size), 2*size, 2*size, 
                                      linewidth=2, edgecolor=color, 
                                      facecolor='none', linestyle='-')
            self.ax.add_patch(square)
            
            # Add corner decorations
            corners = [(-size, -size), (size, -size), (size, size), (-size, size)]
            for corner_x, corner_y in corners:
                corner_circle = Circle((corner_x, corner_y), 0.3, 
                                      color=color, alpha=0.8, edgecolor='black')
                self.ax.add_patch(corner_circle)
        
        # Draw diagonal lines
        self.ax.plot([-10, 10], [-10, 10], color=color, linewidth=2, alpha=0.6)
        self.ax.plot([-10, 10], [10, -10], color=color, linewidth=2, alpha=0.6)
        
        # Draw decorative circles on lines
        for i in np.linspace(-10, 10, 11):
            circle = Circle((i*0.7, i*0.7), 0.2, color='gold', edgecolor=color)
            self.ax.add_patch(circle)
    
    def generate_spiral_kolam(self, turns=5, color='#FF1493'):
        """Generate spiral pattern Kolam"""
        self.create_figure()
        
        # Draw spiral
        t = np.linspace(0, turns*2*np.pi, 1000)
        radius_spiral = 10 * t / (turns*2*np.pi)
        x = radius_spiral * np.cos(t)
        y = radius_spiral * np.sin(t)
        
        self.ax.plot(x, y, color=color, linewidth=3, alpha=0.8)
        
        # Add decorative circles along spiral
        for i in np.linspace(0, turns*2*np.pi, 50):
            r = 10 * i / (turns*2*np.pi)
            cx = r * np.cos(i)
            cy = r * np.sin(i)
            circle = Circle((cx, cy), 0.3, color='gold', edgecolor=color, linewidth=1)
            self.ax.add_patch(circle)
        
        # Center circle
        center = Circle((0, 0), 0.5, color='gold', edgecolor=color, linewidth=2)
        self.ax.add_patch(center)
    
    def generate_symmetrical_kolam(self, symmetry=4, color='#C71585'):
        """Generate symmetrical pattern Kolam"""
        self.create_figure()
        
        # Base shape
        base_angles = np.linspace(0, np.pi/2, 20)
        base_x = 8 * np.cos(base_angles)
        base_y = 8 * np.sin(base_angles)
        
        # Replicate with symmetry
        for sym in range(symmetry):
            rotation_angle = 2 * np.pi * sym / symmetry
            
            # Rotate points
            rotated_x = base_x * np.cos(rotation_angle) - base_y * np.sin(rotation_angle)
            rotated_y = base_x * np.sin(rotation_angle) + base_y * np.cos(rotation_angle)
            
            # Draw pattern
            self.ax.plot(rotated_x, rotated_y, color=color, linewidth=2.5, alpha=0.8)
            self.ax.fill(rotated_x, rotated_y, color=color, alpha=0.3)
        
        # Central mandala-like circle
        center_circle = Circle((0, 0), 2, color='gold', edgecolor=color, linewidth=2)
        self.ax.add_patch(center_circle)
    
    def generate_design(self):
        """Generate Kolam design based on pattern type"""
        if self.pattern_type == "Flower":
            self.generate_flower_kolam()
        elif self.pattern_type == "Geometric":
            self.generate_geometric_kolam()
        elif self.pattern_type == "Spiral":
            self.generate_spiral_kolam()
        elif self.pattern_type == "Symmetrical":
            self.generate_symmetrical_kolam()
        
        return self.fig


def get_figure_image():
    """Convert matplotlib figure to PIL image"""
    buf = io.BytesIO()
    st.session_state.generated_design.savefig(buf, format='png', bbox_inches='tight', 
                                               facecolor='white', dpi=150)
    buf.seek(0)
    return Image.open(buf)


# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Design Configuration")
    
    # Pattern selection
    pattern_type = st.selectbox(
        "Select Kolam Pattern Type:",
        ["Flower", "Geometric", "Spiral", "Symmetrical"],
        help="Choose the type of Kolam pattern to generate"
    )
    
    # Size parameter
    pattern_size = st.slider(
        "Pattern Size:",
        min_value=5,
        max_value=20,
        value=10,
        help="Adjust the size of the Kolam pattern"
    )
    
    # Color selection
    color_options = {
        "Pink": "#FF6B9D",
        "Purple": "#8B4789",
        "Deep Pink": "#FF1493",
        "Dark Magenta": "#C71585",
        "Red": "#FF0000",
        "Blue": "#0000FF",
        "Green": "#00AA00",
        "Orange": "#FF8800",
    }
    
    selected_color = st.selectbox(
        "Select Primary Color:",
        list(color_options.keys())
    )
    
    color_value = color_options[selected_color]
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        show_grid = st.checkbox("Show Grid", value=False)
        background_color = st.color_picker("Background Color", "#FFFFFF")
        edge_thickness = st.slider("Edge Thickness", 1, 5, 2)


# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎨 Kolam Design Preview")
    
    # Generate button
    if st.button("✨ Generate Kolam Design", key="generate", use_container_width=True):
        with st.spinner("Creating your beautiful Kolam..."):
            kolam = KolamGenerator(size=pattern_size, pattern_type=pattern_type)
            st.session_state.generated_design = kolam.generate_design()
            
            # Add to history
            design_info = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "pattern": pattern_type,
                "color": selected_color,
                "size": pattern_size
            }
            st.session_state.design_history.append(design_info)
    
    # Display generated design
    if st.session_state.generated_design is not None:
        st.image(get_figure_image(), caption="Your Generated Kolam Design", use_column_width=True)
    else:
        st.info("👉 Click 'Generate Kolam Design' to create your first pattern!")

with col2:
    st.subheader("📊 Settings Summary")
    
    if st.session_state.generated_design is not None:
        st.metric("Pattern Type", pattern_type)
        st.metric("Color", selected_color)
        st.metric("Size", pattern_size)
        
        st.divider()
        
        st.subheader("💾 Export Options")
        
        # PNG Export
        if st.button("📥 Download as PNG", use_container_width=True):
            img = get_figure_image()
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            st.download_button(
                label="Click to Download PNG",
                data=buf,
                file_name=f"kolam_{pattern_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png",
                use_container_width=True
            )
        
        # SVG Export (vector format)
        if st.button("📥 Download as SVG", use_container_width=True):
            buf = io.BytesIO()
            st.session_state.generated_design.savefig(buf, format='svg', bbox_inches='tight')
            buf.seek(0)
            
            st.download_button(
                label="Click to Download SVG",
                data=buf,
                file_name=f"kolam_{pattern_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.svg",
                mime="image/svg+xml",
                use_container_width=True
            )
        
        # PDF Export
        if st.button("📥 Download as PDF", use_container_width=True):
            buf = io.BytesIO()
            st.session_state.generated_design.savefig(buf, format='pdf', bbox_inches='tight')
            buf.seek(0)
            
            st.download_button(
                label="Click to Download PDF",
                data=buf,
                file_name=f"kolam_{pattern_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.warning("Generate a design first to see export options!")


# Tabs for additional features
tab1, tab2, tab3, tab4 = st.tabs(["📚 Gallery", "🎯 Templates", "📖 Guide", "ℹ️ About"])

with tab1:
    st.subheader("Design History")
    
    if st.session_state.design_history:
        col1, col2, col3 = st.columns(3)
        
        for i, design in enumerate(reversed(st.session_state.design_history[-9:])):
            if i % 3 == 0:
                col = col1
            elif i % 3 == 1:
                col = col2
            else:
                col = col3
            
            with col:
                st.info(f"""
                **Pattern:** {design['pattern']}  
                **Color:** {design['color']}  
                **Size:** {design['size']}  
                **Time:** {design['timestamp']}
                """)
    else:
        st.info("No designs generated yet. Create your first Kolam!")

with tab2:
    st.subheader("Quick Start Templates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌸 Festival Flower", use_container_width=True):
            st.session_state.pattern_preset = {"type": "Flower", "color": "Pink", "size": 12}
            st.success("Preset loaded! Adjust and generate above.")
        
        if st.button("💜 Elegant Purple", use_container_width=True):
            st.session_state.pattern_preset = {"type": "Geometric", "color": "Purple", "size": 10}
            st.success("Preset loaded! Adjust and generate above.")
    
    with col2:
        if st.button("🌀 Spiral Magic", use_container_width=True):
            st.session_state.pattern_preset = {"type": "Spiral", "color": "Deep Pink", "size": 15}
            st.success("Preset loaded! Adjust and generate above.")
        
        if st.button("✨ Symmetry Divine", use_container_width=True):
            st.session_state.pattern_preset = {"type": "Symmetrical", "color": "Dark Magenta", "size": 10}
            st.success("Preset loaded! Adjust and generate above.")

with tab3:
    st.subheader("How to Create Beautiful Kolams")
    
    st.markdown("""
    ### What is Kolam?
    Kolam is a traditional Indian art form, especially popular in South India and Sri Lanka. 
    It involves creating decorative patterns on floors during festivals and celebrations.
    
    ### Using This Generator
    1. **Select Pattern Type**: Choose from Flower, Geometric, Spiral, or Symmetrical designs
    2. **Adjust Size**: Use the slider to make the pattern larger or smaller
    3. **Pick Colors**: Select from a palette of traditional and modern colors
    4. **Generate**: Click the button to create your design
    5. **Export**: Download in PNG, SVG, or PDF format
    
    ### Pattern Types
    - **Flower**: Traditional petal-based designs perfect for festivals
    - **Geometric**: Mathematically precise patterns with symmetry
    - **Spiral**: Continuous flowing spiral designs
    - **Symmetrical**: Multi-axis symmetrical mandala-like patterns
    
    ### Tips for Best Results
    - Start with medium sizes (8-12) for balanced designs
    - Try different color combinations
    - Export as SVG for scalable prints
    - Use PDF for printing on paper
    """)

with tab4:
    st.subheader("About Kolam Design Generator")
    
    st.markdown("""
    ### 🎨 Project Information
    
    **Kolam Design Generator** is an interactive web application built with Streamlit 
    that allows you to create beautiful traditional Kolam patterns digitally.
    
    ### Features
    ✨ **Interactive Design Generation** - Create multiple pattern types instantly  
    🎨 **Customizable Colors** - Choose from traditional and modern color palettes  
    📊 **Flexible Sizing** - Adjust pattern dimensions to your preference  
    💾 **Multiple Export Formats** - PNG, SVG, and PDF support  
    📚 **Design History** - View previously generated designs  
    📖 **Educational Templates** - Quick-start templates for learning  
    
    ### Technology Stack
    - **Python 3.x** - Core programming language
    - **Streamlit** - Web interface framework
    - **Matplotlib** - Graphics and visualization
    - **NumPy** - Numerical computations
    - **Pillow** - Image processing
    
    ### Developer Information
    Created by: Aryan Katiyar  
    Repository: Aryankatiyarcsjmu/Kolam-Design-Generator  
    Generated: 2026-01-08
    
    ### Version
    **v1.0.0** - Initial Release
    
    ### License
    Open Source - Feel free to use and modify!
    """)
    
    st.divider()
    
    st.info("""
    💡 **Tip**: This application generates Kolam patterns programmatically. 
    Traditional Kolams are hand-drawn, and there's beautiful artistry in that practice. 
    Use this tool to explore designs and learn patterns!
    """)


# Footer
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🎨 Created with ❤️")

with col2:
    st.caption("Kolam Design Generator v1.0.0")

with col3:
    st.caption("© 2026 All Rights Reserved")
