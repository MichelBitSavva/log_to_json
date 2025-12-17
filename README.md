# Log to JSON Parser (Streamlit GUI)

## Description

This application converts structured text logs
(formats like `Object(field=value, ...)`) into readable JSON.

It is designed for analyzing complex nested logs such as:


The tool provides a simple graphical interface for fast inspection and manual comparison of logs.

The application is built with **Python + Streamlit** and is intended for **local use**.

---

## Features

* Two independent input areas for logs
* Parsing of nested structures with arbitrary depth
* JSON output for each input
* Independent clearing of left and right panels
* Full state reset
* No need to run from PyCharm

---

## Project Structure

```
log_to_json/
├── main.py              # Streamlit UI
├── parser/
│   ├── __init__.py
│   └── parser.py        # parsing logic
├── run_app.bat          # application launcher
└── README.md
```

---

## Requirements

* Windows
* Python 3.11 or newer (recommended)
* `streamlit` Python package

---

## Installation

Install dependencies:

```powershell
pip install streamlit
```

(Use a virtual environment if preferred)

---

## Running the Application

### Option 1: Run via `.bat` file (recommended)

1. Make sure `run_app.bat` is located in the project root
2. Double-click `run_app.bat`
3. The browser will open automatically at:

```
http://localhost:8501
```

PyCharm is not required.

---

### Example `run_app.bat`

#### With virtual environment:

```bat
@echo off
cd /d C:\Users\YourUser\Path\To\log_to_json
call .venv\Scripts\activate
streamlit run main.py
pause
```

#### Without virtual environment:

```bat
@echo off
cd /d C:\Users\YourUser\Path\To\log_to_json
streamlit run main.py
pause
```

---

## Usage

1. Paste a log into the left or right input field
2. Click **Parse**
3. The parsed JSON will appear below the input
4. Use both panels to visually compare logs

---

## Limitations

* The application runs as a local web interface (Streamlit)
* A web browser is required
* Not intended for very large log files

---

## Intended Use

This tool is intended for:

* developers
* support engineers
* telecom log analysis
* debugging and structure inspection
