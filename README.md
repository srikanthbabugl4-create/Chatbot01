# LMS Query Chatbot

This project is an upgraded chatbot for handling LMS-related questions and support requests. It includes a web-based chat interface, rule-based support logic, and optional integration with OpenAI for more natural responses.

## Features

- Course schedule and instructor lookup
- Assignment and deadline tracking
- Grade summaries
- Announcements and updates
- LMS login and password assistance
- Optional AI-powered responses using OpenAI
- Session-based conversation memory

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

3. Configure environment variables
   ```bash
   cp .env.example .env
   ```
   Then set `OPENAI_API_KEY` if you want AI responses.

4. Start the app
   ```bash
   python app.py
   ```

5. Open your browser:
   ```text
   http://127.0.0.1:5000
   ```

## Example prompts

- What is the schedule for biology?
- Show me the assignments due for math.
- How is my grade in history?
- I forgot my LMS password.
- What was the latest announcement for biology?

## Optional AI setup

Add the following to `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
SECRET_KEY=your_secret_key
```

If no API key is set, the app runs in demo mode using built-in LMS logic.

## Project structure

- `app.py` — Flask backend and chatbot logic
- `lms_data.py` — LMS knowledge base
- `templates/index.html` — chat UI
- `static/styles.css` — styling
- `static/app.js` — frontend interaction logic

## Future enhancements

- Add authentication for students and faculty
- Connect to real LMS APIs such as Moodle or Canvas
- Store conversations in a database
- Add analytics and admin dashboards
- Build multilingual support
