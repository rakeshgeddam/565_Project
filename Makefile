# Determine the operating system
ifeq ($(OS),Windows_NT)
    # Windows
    PYTHON = python
    RM = del /Q
    MKDIR = mkdir
    SEP = \\
else
    # Linux/Unix
    PYTHON = python3
    RM = rm -f
    MKDIR = mkdir -p
    SEP = /
endif

# Define targets
.PHONY: install run

# Install dependencies
install:
    $(PYTHON) -m pip install -r requirements.txt

# Run the main program after installing dependencies
run: install
    $(PYTHON) main.py
