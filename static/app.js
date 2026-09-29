const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');
const suggestionButtons = document.querySelectorAll('.suggestion');

function addMessage(text, type) {
  const msg = document.createElement('div');
  msg.className = `message ${type}`;
  msg.textContent = text;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage(message) {
  if (!message.trim()) return;

  addMessage(message, 'user');
  userInput.value = '';

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    addMessage(data.reply, 'bot');
  } catch (error) {
    addMessage('Sorry, the chatbot is unavailable right now. Please try again.', 'bot');
  }
}

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  await sendMessage(userInput.value);
});

suggestionButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const text = button.textContent.trim();
    userInput.value = text;
    userInput.focus();
  });
});
