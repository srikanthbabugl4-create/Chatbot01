# LMS Query Chatbot

This project is a simple chatbot for handling LMS-related questions. It supports common student support queries such as:

- Course schedules and instructor information
- Assignment and deadline tracking
- Grades and performance summaries
- Announcements and updates
- Password and login help
- General LMS support questions

## Features

- Clean web interface
- Fast backend chatbot logic
- Starter knowledge base for LMS support
- Easy to extend with real LLM or database integration

## Run locally

1. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Start the app
   ```bash
   python app.py
   ```

4. Open your browser at:
   ```text
   http://127.0.0.1:5000
   ```

## Example prompts

- What is the schedule for biology?
- What assignments are due for math?
- Show my grades for history.
- I forgot my LMS password.
- What is the latest announcement for math?

## Next upgrade ideas

- Connect to a real LLM like OpenAI, Azure OpenAI, or Gemini
- Add authentication for students and faculty
- Store course and assignment data in a database
- Add chat history and admin dashboard
- Integrate with Moodle, Canvas, Blackboard, or custom LMS APIs
