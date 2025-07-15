# Animal Breeding Optimization System

## Overview

This is a Streamlit-based web application that implements a GRASP (Greedy Randomized Adaptive Search Procedure) meta-heuristic algorithm to optimize animal breeding decisions. The system aims to minimize coancestry coefficients in breeding programs by finding optimal mating pairs between animals.

## User Preferences

Preferred communication style: Simple, everyday language.
Interface language: Portuguese (Brazilian)
Request for multiple execution comparison with random parameters
Preference for separated results page
Request for automatic page redirection after completing executions
Request for CSV file generation with best breeding results
Request for breeding matrix with highlighted best crossings
Request for iteration range adjustment (0-100 instead of 50-1000)
Request for installation and execution scripts for Windows and Linux
Request for single executable that checks dependencies, installs if needed, and opens browser automatically
Request for detailed technical documentation and user manual

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Layout**: Wide layout with sidebar for configuration
- **Components**: 
  - File upload interface for CSV data
  - Parameter configuration sliders
  - Results visualization using Plotly charts
  - Interactive dashboard with real-time updates

### Backend Architecture
- **Language**: Python
- **Architecture Pattern**: Modular design with separate classes for data processing and optimization
- **Core Components**:
  - `DataProcessor`: Handles CSV file validation and preprocessing
  - `GRASPOptimizer`: Implements the meta-heuristic optimization algorithm
  - `app.py`: Main Streamlit application orchestrating the workflow

### Data Processing Pipeline
- **Input**: CSV files with breeding data containing Animal_1, Animal_2, and Coef columns
- **Validation**: Ensures required columns exist and data types are correct
- **Processing**: Converts breeding pair data into coancestry matrices for optimization

## Key Components

### 1. Data Processor (`data_processor.py`)
- **Purpose**: Validates and processes uploaded CSV breeding data
- **Key Features**:
  - Data validation for required columns and data types
  - Null value checking
  - Animal pair extraction from string format
  - Coancestry matrix generation

### 2. GRASP Optimizer (`grasp_algorithm.py`)
- **Purpose**: Implements the GRASP meta-heuristic for breeding optimization
- **Key Features**:
  - Greedy randomized construction phase
  - Local search improvement phase
  - Convergence tracking
  - Cost calculation for breeding solutions

### 3. Main Application (`app.py`)
- **Purpose**: Streamlit web interface orchestrating the entire workflow
- **Key Features**:
  - Multi-page interface with separated data analysis and results pages
  - File upload and parameter configuration
  - Session state management
  - Multiple execution support with random parameter generation
  - Real-time optimization progress
  - Results visualization with Plotly charts
  - Comprehensive comparison of multiple executions

## Data Flow

1. **Data Input**: User uploads CSV file with breeding data
2. **Data Validation**: System validates file format and required columns
3. **Data Processing**: Raw data is converted into coancestry matrices
4. **Parameter Configuration**: User sets GRASP algorithm parameters
5. **Optimization**: GRASP algorithm finds optimal breeding assignments
6. **Results Display**: System shows optimization results and convergence graphs

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive data visualization
- **plotly.express**: High-level plotting interface
- **plotly.graph_objects**: Low-level plotting objects
- **plotly.subplots**: Multiple subplot creation

### Data Requirements
- CSV files with specific column structure (Animal_1, Animal_2, Coef)
- Numeric coancestry coefficients
- No missing values in required columns

## Deployment Strategy

### Local Development
- Standard Python virtual environment setup
- Streamlit development server for local testing
- File-based data input through web interface

### Production Considerations
- **Platform**: Replit-compatible Python environment
- **Dependencies**: All required packages installable via pip
- **State Management**: Session state for maintaining data between interactions
- **File Handling**: In-memory CSV processing without persistent storage
- **Performance**: Optimized for small to medium-sized breeding datasets

### Configuration
- **Parameters**: Configurable through web interface
  - Maximum iterations (0-100)
  - Alpha greedy factor (0.1-1.0)
  - Local search iterations (10-100)
- **UI**: Responsive design with sidebar controls
- **Visualization**: Real-time charts showing optimization progress

## Technical Notes

The application uses a modular architecture that separates concerns:
- Data handling is isolated in the DataProcessor class
- Optimization logic is contained in the GRASPOptimizer class
- The main application handles user interface and orchestration

The system is designed to handle breeding optimization problems where the goal is to minimize coancestry coefficients between offspring by optimally assigning males to females in breeding programs.

## Recent Changes

**2025-07-14:**
- **MAJOR PERFORMANCE OPTIMIZATION**: Resolved critical performance issue with GRASP algorithm
- Fixed algorithm execution timeout that prevented optimization from completing
- Optimized DataProcessor to use vectorized pandas operations (reduced processing time from minutes to ~6 seconds)
- Optimized GRASPOptimizer with candidate limiting and pre-sorted crossings cache
- Reduced search space from full matrix to top 500 candidates for construction and 200 for local search
- Adjusted default parameters: max_iterations 5-25, local_search 5-20, crossings selection limited to 15-30
- Algorithm now executes in ~0.02 seconds after data processing
- Maintained algorithm correctness while dramatically improving performance for large datasets
- Tested successfully with 44,850 row dataset (300 unique pairs)
- **DIVERSIFICATION IMPROVEMENTS**: Enhanced algorithm to avoid sequential animal usage
- Added randomization to candidate selection to prevent predictable patterns
- Implemented animal usage tracking to ensure diverse crossing selections
- Added weighted random parameter generation for better solution diversity
- Created diversify_solution() method to maximize unique animal usage
- Improved local search with shuffled candidate exploration
- Fixed Streamlit slider error that prevented execution
- Verified solution diversity across multiple executions (22-24 unique animals per solution)
- Ensured different solutions between executions while maintaining optimal costs
- **MATRIX IMPROVEMENTS**: Enhanced breeding recommendations matrix with advanced features
- Added configurable number of recommendations per female (1-10 options)
- Implemented flexible male reuse settings (allow/prevent reuse)
- Added intelligent female sorting by breeding quality
- Created quality classification system (Excellent/Good/Regular/Avoid)
- Enhanced statistics dashboard with detailed metrics and usage percentages
- Implemented tabbed interface for matrix visualization (Complete/Quality Analysis/Charts)
- Added comprehensive quality analysis by female with detailed breakdowns
- Created interactive charts for coancestry distribution and quality visualization
- Enhanced download options with complete and simplified CSV formats
- Added matrix heatmap visualization with highlighted best crossings
- Improved visual presentation with color-coded quality indicators
- **ITERATION RANGE EXPANSION**: Adjusted maximum iterations from 0-100 to 50-1000 range
- Implemented adaptive performance optimization for high iteration counts
- Added early convergence detection to prevent unnecessary computation
- Created iteration-based candidate limiting for balanced performance vs quality
- Optimized local search frequency for high iteration scenarios
- Enhanced random parameter generation for 50-1000 iteration range
- Algorithm now supports up to 1000 iterations with convergence detection

**2025-07-13:**
- **MAJOR ARCHITECTURAL CHANGE**: Refactored GRASP algorithm to work directly on the crossing matrix
- Modified GRASPOptimizer to operate on coancestry matrix instead of breeding matrix (females x males)
- Algorithm now selects optimal crossing pairs from all possible combinations in the CSV data
- Updated construction phase to use greedy randomized selection of crossing pairs
- Improved local search to swap and optimize crossing selections
- Added methods to extract and visualize best crossings with detailed information
- Enhanced results page to show selected crossings with pair names and coancestry coefficients
- Added matrix visualization with highlighted best crossings (red stars)
- Implemented comparison charts between all possible crossings vs. selected ones
- Updated download functionality to export crossing pairs instead of breeding assignments
- Added comprehensive crossing analysis with statistics and distribution charts
- Maintained backward compatibility with previous breeding matrix approach

**2025-07-12:**
- Fixed pandas dtype warning by converting matrix to string type before highlighting
- Adjusted iteration range from 50-1000 to 0-100 for better performance
- Adjusted random parameter generation to 10-100 iterations range
- Added automatic page redirection after completing all executions
- Created CSV download for best breeding combinations (sorted by coancestry)
- Created breeding matrix download with highlighted best crossings (★)
- Added statistical summary of best crossings (mean, min, max, std deviation)
- Added distribution histogram of coancestry coefficients
- Created installation scripts for Windows (install_windows.bat, run_windows.bat)
- Created installation scripts for Linux (install_linux.sh, run_linux.sh)
- Created comprehensive technical documentation (DOCUMENTACAO_TECNICA.md)
- Created detailed user manual (MANUAL_USUARIO.md)
- Created dependencies reference file (dependencies.txt)
- Updated replit.md with user preferences and recent changes
- Expanded number of executions parameter from 1-10 to 1-100 range
- Replaced multiple installation/execution scripts with single executables (executar_sistema.bat/.sh)
- Added automatic dependency checking and installation
- Added automatic browser opening functionality
- Updated documentation to reflect single-executable approach