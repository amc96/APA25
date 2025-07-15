# replit.md - Aplicativo de Análise de Parentesco

## Overview

This is a comprehensive web application built with Flask that analyzes kinship data between animals using the GRASPE method (Genetic Relationship Analysis for Strategic Pairing Enhancement). The system converts CSV files containing parentage data into relationship matrices and performs multiple GRASPE algorithm executions to find optimal breeding combinations with detailed statistical analysis and visualization.

## System Architecture

### Frontend Architecture
- **Technology**: HTML templates with Bootstrap 5 for responsive UI
- **Template Engine**: Jinja2 (Flask default)
- **Styling**: Bootstrap CSS framework for clean, mobile-responsive interface
- **Visualization**: Chart.js for interactive graphs and statistical displays
- **Pages**: 
  - Index page for file upload and configuration
  - Visualization page for matrix display and results with comprehensive statistics
  - Results page for GRASPE analysis with multiple execution support
  - Error page for exception handling

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Modular design with separate files for distinct responsibilities
- **Processing Pipeline**: CSV → Matrix Conversion → Multiple GRASPE Analysis → Statistical Processing → Results Display
- **File Handling**: Secure file upload with validation, temporary storage, and download capabilities

## Key Components

### 1. Flask Application (app.py)
- **Purpose**: Main web server and route handling
- **Key Routes**:
  - `/` - File upload and processing with execution configuration
  - `/visualizar/<filename>` - Matrix visualization with basic statistics
  - `/download/<filename>` - File download functionality
  - `/download_cruzamentos_csv` - Download breeding results in CSV format
- **Features**: File validation, error handling, flash messaging, multiple execution support

### 2. CSV to Matrix Converter (csv_to_matrix.py)
- **Purpose**: Transforms CSV data into relationship matrices
- **Input Format**: CSV with columns Animal_1, Animal_2, Coef
- **Output**: Pandas DataFrame matrix with animals as rows/columns
- **Statistics**: Calculates matrix dimensions, basic statistics, and animal counting

### 3. GRASPE Algorithm (graspe.py)
- **Purpose**: Implements GRASPE optimization method with multiple execution capability
- **Algorithm**: GRASP (Greedy Randomized Adaptive Search Procedure)
- **Functionality**: 
  - Finds optimal breeding combinations based on relationship coefficients
  - Supports multiple executions with randomized parameters
  - Calculates comprehensive statistics (mean, best, worst solutions)
  - Returns complete structure with objective values and averages
- **Optimization**: Uses local search to improve initial solutions with RCL (Restricted Candidate List)

### 4. Template System
- **Base Framework**: Bootstrap 5 for consistent styling
- **Key Templates**:
  - `index.html` - Main upload interface with execution configuration
  - `visualizar.html` - Matrix display with basic analysis
  - `resultados.html` - Comprehensive GRASPE results with charts and statistics
  - `error.html` - Error handling page
- **Features**: Responsive design, interactive charts, statistical displays, quality classification system

## Data Flow

1. **Input Stage**: User uploads CSV file with Animal_1, Animal_2, Coef columns
2. **Validation**: System validates file format and required columns
3. **Conversion**: CSV data converted to relationship matrix using pandas
4. **Configuration**: User selects number of GRASPE executions (default: multiple runs)
5. **Processing**: Multiple GRASPE algorithm executions with randomized parameters
6. **Analysis**: Statistical processing of all execution results
7. **Visualization**: Charts and tables displaying comprehensive results
8. **Output**: Download options for complete results in CSV format

## External Dependencies

### Python Packages
- **Flask**: Web framework for application server
- **Pandas**: Data manipulation and CSV/matrix operations
- **NumPy**: Numerical computations for matrix operations
- **Werkzeug**: WSGI utilities and secure filename handling

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive UI design
- **Chart.js**: JavaScript library for interactive data visualization
- **Bootstrap Icons**: Icon library for enhanced UI elements

### System Requirements
- **Python 3.7+**: Core runtime environment
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge for frontend
- **Operating System**: Cross-platform (Windows, macOS, Linux)

## Deployment Strategy

### Local Development
- **Startup Scripts**: 
  - `iniciar.bat` for Windows systems
  - `iniciar.sh` for Linux/macOS systems
- **Main Entry**: `main.py` serves as application entry point
- **Development Server**: Flask built-in server on localhost:5000

### Production Considerations
- **File Storage**: Local uploads folder with configurable path
- **Security**: Secure filename handling and file type validation
- **Scalability**: Designed for single-user or small team usage
- **Performance**: Matrix operations optimized for datasets up to medium size

### Configuration
- **Upload Limits**: 10MB maximum file size
- **Allowed Files**: CSV format only
- **Storage**: Temporary file storage in uploads directory
- **Session Management**: Flask secret key for session security

## Changelog

```
Changelog:
- June 29, 2025: Analyzed current GRASPE implementation code
- June 29, 2025: Removed unused template files (error.html, visualizar.html)
- June 29, 2025: Updated README.md to reflect actual implemented functionality
- June 29, 2025: Updated DOCUMENTACAO.md with accurate code analysis
- June 29, 2025: Maintained all functional code without breaking changes
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```