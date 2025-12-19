import os
from mcp.server.fastmcp import FastMCP
from canvasapi import Canvas
import dotenv as env 

# Initialize FastMCP server
mcp = FastMCP("canvas-mcp")

env.load_dotenv()

# Configuration for Canvas API
API_URL = "https://canvas.qut.edu.au/" 
API_KEY = os.getenv("CANVAS_API_KEY")
canvas = Canvas(API_URL, API_KEY)

# List all active courses 
@mcp.tool()
def list_active_courses() -> str:
    """Lists your currently active courses."""
    user = canvas.get_current_user()
    courses = user.get_courses(enrollment_state='active')
    
    output = []
    for c in courses:
        try:
            output.append(f"ID: {c.id} | Name: {c.name} | Code: {c.course_code}")
        except AttributeError:
            continue
    return "\n".join(output) if output else "No active courses found."

# Get all assignments for a specific course
@mcp.tool()
def get_all_assignments(course_id: int) -> str: 
    """Get all assignments for a specific course ID."""
    try: 
        course = canvas.get_course(course_id)
        all_assignments = course.get_assignments()
        
        output = []
        for assignment in all_assignments: 
            due = assignment.due_at if hasattr(assignment, 'due_at') else "No date"
            output.append(f"- {assignment.name} (Due: {due})")
            
        return "\n".join(output) if output else "No upcoming assignments."
    except Exception as e:
        return f"Error fetching assignments: {str(e)}"

# Get upcoming assignments for a specific course
@mcp.tool()
def get_upcoming_assignments(course_id: int) -> str:
    """Get upcoming assignments for a specific course ID."""
    try:
        course = canvas.get_course(course_id)
        assignments = course.get_assignments(bucket='upcoming')
        
        output = []
        for a in assignments:
            due = a.due_at if hasattr(a, 'due_at') else "No date"
            output.append(f"- {a.name} (Due: {due})")
            
        return "\n".join(output) if output else "No upcoming assignments."
    except Exception as e:
        return f"Error fetching assignments: {str(e)}"

# Get recent 5 announcements for a specific course
@mcp.tool()
def get_recent_announcements(course_id: int) -> str:
    """Get the last 5 announcements for a course."""
    try:
        course = canvas.get_course(course_id)
        announcements = course.get_discussion_topics(only_announcements=True)
        
        output = []
        # Sort by date usually works, but we'll take the first 5 returned
        for ann in announcements[:5]: 
            output.append(f"Title: {ann.title}\nMessage: {str(ann.message)[:1000]}...\n---")
            
        return "\n".join(output) if output else "No announcements."
    except Exception as e:
        return f"Error: {str(e)}"

# List all groups in a specific course
@mcp.tool()
def list_course_groups(course_id: int) -> str:
    """Lists all groups in a specific course to find their IDs."""
    try:
        course = canvas.get_course(course_id)
        # Get groups available in this course
        groups = course.get_groups()
        
        result = []
        for group in groups:
            result.append(f"ID: {group.id} | Name: {group.name}")
            
        return "\n".join(result) if result else "No groups found in this course."
    except Exception as e:
        return f"Error fetching groups: {str(e)}"

# Get members of a specific group
@mcp.tool()
def get_group_members(group_id: int) -> str:
    """Gets the names and emails of all students in a specific group."""
    try:
        group = canvas.get_group(group_id)
        users = group.get_users()
        
        result = []
        for user in users:
            # We try to get email, but sometimes it is hidden depending on permissions
            email = getattr(user, 'email', 'No email visible')
            result.append(f"Name: {user.name} | ID: {user.id} | Email: {email}")
            
        return "\n".join(result) if result else "This group has no members."
    except Exception as e:
        return f"Error fetching group members: {str(e)}"

if __name__ == "__main__":
    mcp.run()