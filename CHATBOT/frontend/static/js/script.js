const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

const userId = 'user_' + Math.random().toString(36).substr(2, 9);

document.addEventListener('DOMContentLoaded', () => {
  messageInput.focus();
  sendButton.addEventListener('click', sendMessage);
  messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
  addBotMessage("Hello! How can I help you today?");
});

function sendMessage() {
  const message = messageInput.value.trim();
  if (message.length === 0) return;

  addUserMessage(message);
  messageInput.value = '';

  fetch("http://localhost:8000/api/chat", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: message, user_id: userId }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      addBotMessage(data.data.response);
    } else {
      addBotMessage("Error: " + data.error);
    }
  })
  .catch(error => {
    console.error('Fetch Error:', error);
    addBotMessage("Error: Unable to reach server.");
  });
}

function addUserMessage(message) {
  const messageElement = document.createElement('div');
  messageElement.className = 'message user-message';
  messageElement.textContent = message;
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(message) {
  const messageElement = document.createElement('div');
  messageElement.className = 'message bot-message';
  messageElement.textContent = message;
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
