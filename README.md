# Canvas MCP Server

A Model Context Protocol (MCP) server that interfaces with the Canvas Learning Management System (LMS). This server allows AI models to interact with Canvas to retrieve course data, assignments, announcements and group project details.

## Features

MCP client tools includes:

- **`list_active_courses`**: Lists the user's currently active courses.
- **`get_all_assignments`**: Retrieves all assignments for a specific course ID.
- **`get_upcoming_assignments`**: Retrieves only upcoming assignments for a specific course ID.
- **`get_announcements`**: Fetches the last 5 announcements for a course.
- **`list_course_groups`**: Lists all student groups within a specific course.
- **`list_group_members`**: Lists the names and emails of students in a specific group.

## Prerequisites

- Python 3.10 or higher
- A Canvas API Key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd canvas-mcp-server
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install mcp httpx python-dotenv canvasapi
   ```

## Configuration

1. Create a `.env` file in the root directory of the project.
2. Add your Canvas API key to the `.env` file:

   ```env
   CANVAS_API_KEY=your_canvas_api_key_here
   ```

> **Note**: The Canvas API URL is currently hardcoded to `https://canvas.qut.edu.au/` in `src/server.py`. If you are using a different Canvas instance, you will need to modify the `API_URL` variable in that file.

## Usage

To run the server, execute the `src/server.py` script:

```bash
python src/server.py
```

This will start the FastMCP server, which can then be connected to an MCP client (like Claude Desktop or an IDE extension).
