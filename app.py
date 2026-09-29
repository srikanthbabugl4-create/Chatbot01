from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

LMS_DATA = {
    "courses": {
        "math": {
            "teacher": "Dr. Patel",
            "schedule": "Mon/Wed/Fri, 10:00 AM - 11:30 AM",
            "meeting_link": "https://meet.example.com/math-101",
            "office_hours": "Tue/Thu, 2:00 PM - 3:00 PM"
        },
        "biology": {
            "teacher": "Prof. Nguyen",
            "schedule": "Tue/Thu, 1:00 PM - 2:30 PM",
            "meeting_link": "https://meet.example.com/bio-201",
            "office_hours": "Wed, 11:00 AM - 12:00 PM"
        },
        "history": {
            "teacher": "Dr. Alvarez",
            "schedule": "Mon/Wed, 9:00 AM - 10:30 AM",
            "meeting_link": "https://meet.example.com/hist-110",
            "office_hours": "Fri, 1:00 PM - 2:00 PM"
        }
    },
    "assignments": {
        "math": [
            {"name": "Algebra Quiz 1", "due": "Sep 30", "status": "pending"},
            {"name": "Homework Set 2", "due": "Oct 05", "status": "pending"}
        ],
        "biology": [
            {"name": "Lab Report 3", "due": "Oct 02", "status": "pending"},
            {"name": "Midterm Review", "due": "Oct 08", "status": "in review"}
        ],
        "history": [
            {"name": "Essay Draft", "due": "Sep 28", "status": "submitted"},
            {"name": "Research Notes", "due": "Oct 10", "status": "pending"}
        ]
    },
    "grades": {
        "math": {"midterm": "A-", "quiz_average": "A", "overall": "A"},
        "biology": {"lab_average": "B+", "midterm": "B", "overall": "B+"},
        "history": {"essay": "A", "participation": "A-", "overall": "A-"}
    },
    "announcements": {
        "math": "The quiz on fractions has been moved to Friday.",
        "biology": "Lab safety training is required before the experiment.",
        "history": "The reading list for Week 5 is now available."
    },
    "support": {
        "password": "Reset your password by clicking 'Forgot Password' on the LMS login page, or contact the help desk at helpdesk@campus.edu.",
        "login": "If you cannot log in, check your university email, clear browser cache, and contact IT support if the issue persists.",
        "deadline": "Deadlines are listed in the course calendar and assignment pages. You can also ask the chatbot for upcoming tasks by course."
    }
}


def normalize(text):
    return re.sub(r"[^a-z0-9\s]", " ", text.lower()).strip()


def extract_course(text):
    normalized = normalize(text)
    for course in LMS_DATA["courses"]:
        if course in normalized:
            return course
    return None


def handle_lms_query(message):
    text = normalize(message)
    course = extract_course(text)

    if any(word in text for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "Hello! I can help with course info, assignments, grades, deadlines, LMS access, and general support. Ask me anything about your learning portal."

    if "course" in text or "schedule" in text or "class" in text:
        if course:
            info = LMS_DATA["courses"][course]
            return (
                f"{course.title()} is taught by {info['teacher']} and meets {info['schedule']}. "
                f"The meeting link is {info['meeting_link']}. Office hours are {info['office_hours']}."
            )
        return "I can help with math, biology, and history. Which course would you like details for?"

    if "assignment" in text or "homework" in text or "deadline" in text or "due" in text:
        if course:
            tasks = LMS_DATA["assignments"].get(course, [])
            if tasks:
                details = "; ".join(
                    f"{item['name']} (due {item['due']}, status: {item['status']})" for item in tasks
                )
                return f"Here are the current assignments for {course.title()}: {details}."
            return f"I don’t see any assignment records for {course.title()} right now."
        return "Which course would you like to check assignments for?"

    if "grade" in text or "marks" in text or "gpa" in text:
        if course:
            grade_info = LMS_DATA["grades"].get(course)
            if grade_info:
                return f"Current grade summary for {course.title()}: " + "; ".join(
                    f"{k.replace('_', ' ').title()}: {v}" for k, v in grade_info.items()
                ) + "."
            return f"I don’t have grade information for {course.title()} yet."
        return "Which course would you like to check grades for?"

    if "announcement" in text or "news" in text or "update" in text:
        if course:
            return LMS_DATA["announcements"].get(course, f"There are no announcements for {course.title()} at the moment.")
        return "I can help with announcements for math, biology, or history. Which course are you asking about?"

    if "password" in text or "forgot" in text or "login" in text or "sign in" in text:
        return LMS_DATA["support"]["password"] if "password" in text or "forgot" in text else LMS_DATA["support"]["login"]

    if "support" in text or "help" in text or "issue" in text:
        return "I can help with LMS login issues, password resets, deadlines, course access, and assignments. Tell me what you need help with."

    if "attendance" in text:
        return "Your attendance is updated automatically in the LMS. If you believe there is an error, contact your instructor or the registrar office."

    if "exam" in text or "midterm" in text or "final" in text:
        return "Exam schedules are published in the course calendar. If you want, I can tell you the planned assessment dates for a specific course."

    if "thank" in text:
        return "You’re welcome! I’m here to help with LMS queries anytime."

    return (
        "I can help with these LMS tasks: course information, deadlines, assignments, grades, announcements, "
        "login/password help, and general support. Try asking: 'What is the schedule for biology?'"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    response = handle_lms_query(message)
    return jsonify({"reply": response})


if __name__ == "__main__":
    app.run(debug=True)
















































































































