# Step-by-Step Guide: Running the LMS Chatbot

Follow these steps to get the chatbot running on your machine.

---

## Prerequisites

- **Python 3.8+** installed on your system
- **pip** (Python package manager, comes with Python)
- A terminal or command prompt
- (Optional) An OpenAI API key for AI responses

---

## Step 1: Clone or Download the Repository

If you have Git installed:
```bash
git clone https://github.com/srikanthbabugl4-create/Chatbot01.git
cd Chatbot01
```

Or download the repository as a ZIP and extract it, then open a terminal in that folder.

---

## Step 2: Create a Virtual Environment

A virtual environment keeps project dependencies isolated.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Expected output:**  
Your terminal prompt should now show `(venv)` at the beginning.

---

## Step 3: Install Dependencies

Make sure you're in the project folder with the virtual environment activated, then run:

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- python-dotenv (environment variables)
- openai (optional, for AI responses)

**Expected output:**  
You'll see installation progress messages ending with "Successfully installed..."

---

## Step 4: (Optional) Set Up Environment Variables for AI

If you want to enable AI-powered responses using OpenAI:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   (On Windows, use: `copy .env.example .env`)

2. Open the `.env` file in a text editor and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   OPENAI_MODEL=gpt-4o-mini
   SECRET_KEY=lms-chatbot-secret
   ```

3. Save the file.

**Note:** Without this step, the chatbot still works in demo mode using built-in LMS logic.

---

## Step 5: Start the Flask App

Run the application:

```bash
python app.py
```

**Expected output:**
```
WARNING in app.run_with_reloader is not thread safe and has known issues, continue anyway? (yes/no): yes
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

## Step 6: Open the Chatbot in Your Browser

Open your web browser and go to:

```
http://127.0.0.1:5000
```

You should see the LMS Chatbot interface with a welcome message.

---

## Step 7: Try Example Queries

Ask the chatbot any of these:

- **"What is the schedule for biology?"**
- **"Show me assignments for math"**
- **"What are my grades in history?"**
- **"I forgot my LMS password"**
- **"What's the latest announcement for biology?"**

Type your question and click **Send** (or press Enter).

---

## Step 8: Stop the App

To stop the chatbot, go back to your terminal and press:

```
CTRL+C
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'flask'`
**Solution:** Make sure your virtual environment is activated and dependencies are installed.
```bash
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Issue: Port 5000 is already in use
**Solution:** The Flask app will tell you. Either:
- Close the other app using port 5000, or
- Change the port in `app.py`, line 151: `app.run(debug=True, port=5001)`

### Issue: `.env` file not loading
**Solution:** Make sure you created the `.env` file in the project root (same folder as `app.py`).

### Issue: AI responses not working
**Solution:** Check that:
1. You have a valid `OPENAI_API_KEY` in `.env`
2. You have internet access
3. Your OpenAI account has available credits

---

## Project Structure

```
Chatbot01/
├── app.py                 # Main Flask application
├── lms_data.py            # Course, assignment, grade data
├── requirements.txt       # Python dependencies
├── .env.example           # Template for environment variables
├── .env                   # Your actual secrets (create this)
├── templates/
│   └── index.html         # Chat UI
└── static/
    ├── styles.css         # Styling
    └── app.js             # Frontend logic
```

---

## Next Steps

- **To customize courses:** Edit `lms_data.py`
- **To add more features:** Modify `app.py`
- **To style the UI:** Update `static/styles.css`
- **To deploy:** See the README.md for deployment options

---

## Need Help?

If something doesn't work:
1. Check the terminal error message
2. Make sure Python 3.8+ is installed: `python --version`
3. Verify the virtual environment is activated
4. Clear pip cache: `pip cache purge` then reinstall

Happy chatting! 🚀
