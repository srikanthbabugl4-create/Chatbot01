const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');

function addMessage(text, type) {
  const msg = document.createElement('div');
  msg.className = `message ${type}`;
  msg.textContent = text;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = userInput.value.trim();

  if (!message) return;

  addMessage(message, 'user');
  userInput.value = '';

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    addMessage(data.reply, 'bot');
  } catch (error) {
    addMessage('Sorry, something went wrong. Please try again.', 'bot');
  }
});
