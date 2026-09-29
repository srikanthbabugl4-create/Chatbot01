import os
import re
from typing import Optional

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session
from openai import OpenAI

from lms_data import LMS_DATA

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "lms-chatbot-secret")


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower()).strip()


def extract_course(text: str) -> Optional[str]:
    normalized = normalize(text)
    for course in LMS_DATA["courses"]:
        if course in normalized:
            return course
    return None


def build_rule_response(message: str) -> str:
    text = normalize(message)
    course = extract_course(text)

    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    if any(word in text for word in greetings):
        return "Hello! I can help with course schedules, assignments, grades, announcements, and LMS access issues."

    if "schedule" in text or "course" in text or "class" in text or "teacher" in text or "instructor" in text:
        if course:
            info = LMS_DATA["courses"][course]
            return (
                f"{course.title()} is taught by {info['teacher']} and meets {info['schedule']}. "
                f"Meeting link: {info['meeting_link']}. Office hours: {info['office_hours']}."
            )
        return "I can provide details for math, biology, and history. Which course would you like to know about?"

    if any(keyword in text for keyword in ["assignment", "homework", "deadline", "due", "submission"]):
        if course:
            tasks = LMS_DATA["assignments"].get(course, [])
            if tasks:
                details = "; ".join(
                    f"{item['name']} (due {item['due']}, status: {item['status']})" for item in tasks
                )
                return f"Assignments for {course.title()}: {details}."
            return f"I could not find assignment data for {course.title()} in the LMS records."
        return "For which course do you want the assignment list?"

    if any(keyword in text for keyword in ["grade", "marks", "result", "score", "gpa", "performance"]):
        if course:
            grade_info = LMS_DATA["grades"].get(course)
            if grade_info:
                summary = "; ".join(f"{key.replace('_', ' ').title()}: {value}" for key, value in grade_info.items())
                return f"Grade summary for {course.title()}: {summary}."
            return f"There is no grade record for {course.title()} available yet."
        return "Which subject would you like me to check for grades?"

    if any(keyword in text for keyword in ["announcement", "news", "update", "notice"]):
        if course:
            response = LMS_DATA["announcements"].get(course)
            return response if response else f"There are no announcements for {course.title()} right now."
        return "I can provide announcements for math, biology, or history. Which course do you mean?"

    if any(keyword in text for keyword in ["password", "forgot password", "reset password", "login issue", "sign in"]) :
        if "password" in text or "forgot" in text or "reset" in text:
            return LMS_DATA["support"]["password"]
        return LMS_DATA["support"]["login"]

    if any(keyword in text for keyword in ["support", "help", "issue", "problem"]):
        return "I can help with course access, deadlines, assignments, grades, login issues, and support requests. Tell me what you need." 

    if "attendance" in text:
        return "Your attendance is tracked in the LMS. If you notice an error, contact your instructor or the registrar." 

    if any(keyword in text for keyword in ["exam", "midterm", "final", "assessment"]):
        return "Exam schedules are usually listed in the course calendar and LMS timeline. For a specific course, ask me by name."

    if "thank" in text:
        return "You’re welcome! I’m here to help with LMS questions anytime."

    return (
        "I can help with course information, assignments, grades, deadlines, announcements, and LMS support. "
        "Try asking: 'What is the schedule for biology?'"
    )


def build_ai_prompt(message: str) -> str:
    formatted_courses = []
    for course_name, course_data in LMS_DATA["courses"].items():
        assignments = LMS_DATA["assignments"].get(course_name, [])
        grades = LMS_DATA["grades"].get(course_name, {})
        announcement = LMS_DATA["announcements"].get(course_name, "No announcement")
        formatted_courses.append(
            f"Course: {course_name.title()}\n"
            f"Teacher: {course_data['teacher']}\n"
            f"Schedule: {course_data['schedule']}\n"
            f"Office hours: {course_data['office_hours']}\n"
            f"Assignments: {', '.join(item['name'] + ' (' + item['due'] + ')' for item in assignments) if assignments else 'None'}\n"
            f"Grades: {', '.join(f'{key}: {value}' for key, value in grades.items()) if grades else 'None'}\n"
            f"Announcement: {announcement}"
        )

    context = "\n\n".join(formatted_courses)
    return (
        "You are a helpful LMS assistant for a university portal. "
        "Use only the information in the course context below. "
        "If unsure, answer conservatively and ask a clarifying question.\n\n"
        f"Context:\n{context}\n\nUser query: {message}"
    )


def get_ai_response(message: str) -> Optional[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly and precise LMS support assistant. "
                        "Answer student questions using the provided course information."
                    ),
                },
                {"role": "user", "content": build_ai_prompt(message)},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


@app.route("/")
def index():
    llm_status = "AI enabled" if os.environ.get("OPENAI_API_KEY") else "Demo mode"
    return render_template("index.html", llm_status=llm_status)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please enter a message so I can help you."})

    history = session.get("history", [])
    history.append({"role": "user", "content": message})

    direct_reply = build_rule_response(message)
    ai_reply = get_ai_response(message)
    final_reply = ai_reply if ai_reply else direct_reply

    history.append({"role": "assistant", "content": final_reply})
    session["history"] = history[-12:]

    return jsonify({"reply": final_reply})


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "ai_enabled": bool(os.environ.get("OPENAI_API_KEY")),
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    })


if __name__ == "__main__":
    app.run(debug=True)









































































































