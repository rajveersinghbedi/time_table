# Academic Data Collection Tool

A web-based application for collecting and managing academic data with multiple stages of information.

## Features

1. **Streams & Semesters Tab**: Manage academic streams and semesters
2. **Majors & Minors Tab**: Add majors and minors (with "Core" as default major that cannot be removed)
3. **Subjects & Teachers Tab**: Associate subjects with majors/minors and assign teachers to subjects
4. **Connections Tab**: Create connections between majors and minors

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python data_collection_app.py
   ```

3. Open your browser and go to `http://localhost:5000`

## Usage Instructions

### Tab 1: Streams & Semesters
- Add academic streams (e.g., Business, Engineering, Arts)
- Add semesters (e.g., Fall 2025, Spring 2026)

### Tab 2: Majors & Minors
- Add majors (e.g., Finance, Marketing, Operations)
- Add minors (e.g., Operations, Analytics)
- Note: "Core" is a default major that cannot be removed

### Tab 3: Subjects & Teachers
- Select a major/minor and add subjects to it
- Select a subject and assign teachers to it

### Tab 4: Connections
- Connect majors with minors (e.g., Finance major + Operations minor)
- View all established connections

### Data Management
- Save data to JSON file using the "Save Data" button
- Load previously saved data using the "Load Data" button

## Technical Details

- Built with Flask (Python web framework)
- Frontend uses HTML, CSS, and JavaScript
- Data stored in-memory during runtime
- JSON export/import functionality