document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const question = userInput.value.trim();
            if (!question) return;

            // Append User Message
            appendMessage('Commander', question, 'user-message');
            userInput.value = '';

            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });

                const data = await response.json();
                if (data.response) {
                    appendMessage('War AI Command', data.response, 'ai-message');
                } else {
                    appendMessage('War AI Command', 'Error retrieving response.', 'ai-message');
                }
            } catch (err) {
                appendMessage('War AI Command', 'Communication error with AI core.', 'ai-message');
            }

            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }
});

function sendQuickPrompt(text) {
    const input = document.getElementById('user-input');
    if (input) {
        input.value = text;
        document.getElementById('chat-form').dispatchEvent(new Event('submit'));
    }
}

function appendMessage(sender, text, messageClass) {
    const chatMessages = document.getElementById('chat-messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${messageClass}`;

    const iconHtml = messageClass === 'user-message'
        ? '<i class="fa-solid fa-user"></i> '
        : '<i class="fa-solid fa-brain"></i> ';

    // Basic markdown replacement for bold and italic
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br/>');

    msgDiv.innerHTML = `
        <div class="message-sender">${iconHtml}${sender}</div>
        <div class="message-body">${formattedText}</div>
    `;

    chatMessages.appendChild(msgDiv);
}
