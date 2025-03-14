# 565_Project: Python-based Compiler

**565_Project** is a Python application that acts as a simple compiler. It takes a high-level language (HLC) script as input, converts it into assembly-level code, and finally translates that into machine-level code. This project demonstrates key compiler design principles through a modular and easy-to-follow implementation.

---

## Overview

- **High-Level to Assembly Translation:** Converts HLC scripts into assembly instructions.
- **Assembly to Machine Code Conversion:** Compiles the generated assembly code into machine-level code.
- **Modular Architecture:** Organized into separate modules for core functionality, memory management, and runtime data handling.

---

## File Structure

- **`main.py`**  
  Contains all the core functions and methods that drive the compilation process.

- **`Memory.py`**  
  Defines variables and values associated with memory management.

- **`data.py`**  
  Houses the data structures and runtime variables used to handle intermediate values during compilation.

- **`test.txt`**  
  Contains a sample HLC script for testing. *(Modify this file as needed.)*

- **`Requirements`**  
  Currently empty – list any project dependencies here in the future.

---

## Getting Started

### Prerequisites

- **Python** (Ensure you have Python installed on your machine)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/565_Project.git
    ```
2. **Navigate to the project directory:**
    ```bash
    cd 565_Project
    ```
3. **(Optional) Set up a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r Requirements.txt
    ```

### Usage

To run the compiler:
```bash
python main.py
