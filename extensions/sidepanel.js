const chatBox = document.getElementById('chat-box');
const input = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const typing = document.getElementById('typing-indicator');

function addMessage(text, side) {
  const div = document.createElement('div');
  div.className = `message ${side}-msg`;
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.onclick = async () => {
  const query = input.value.trim();
  if (!query) return;

  addMessage(query, 'user');
  input.value = '';
  typing.classList.remove('hidden');

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: query, url: tab.url })
    });
    
    const data = await response.json();
    typing.classList.add('hidden');
    addMessage(data.answer, 'bot');
    
  } catch (error) {
    typing.classList.add('hidden');
    addMessage("Error: Backend is not responding. Make sure main.py is running.", 'bot');
  }
};

// Allow Enter key to send
input.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendBtn.click(); });