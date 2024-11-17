const chatInput = document.querySelector(".chatbox__input");
const chatInputBtn = document.getElementById("sendBTN");
const chatBox = document.querySelector(".chatbox");

// Create chat message element
const createChatLi = (message, className) => {
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  chatLi.innerHTML = `<p>${message}</p>`;
  return chatLi;
};

// Handle sending messages
async function handleChat(e) {
  e.preventDefault(); // Prevent form submission if button is in a form

  const userInput = chatInput.value.trim();
  if (!userInput) return;
  // Add user message to chat
  chatBox.appendChild(createChatLi(userInput, "chat-outgoing"));
  // Clear input
  chatInput.value = "";

  // Add thinking message
  const thinkingLi = createChatLi("Thinking....", "chat-incoming");
  chatBox.appendChild(thinkingLi);

  try {
    // Send to Flask backend
    const response = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();

    // Remove thinking message

    if (data.status === "success") {
      // Add success message
      chatBox.appendChild(
        createChatLi(`${data.action} completed successfully`, "chat-incoming")
      );

      // If there's database content, display it
      if (data.current_data) {
        const dbContent = data.current_data
          .map((row) => `Key: ${row[0]}, Value: ${row[1]}`)
          .join("\n");
        chatBox.appendChild(
          createChatLi(
            `Current Database Content:\n${dbContent}`,
            "chat-incoming"
          )
        );
      }
    } else {
      // Add error message
      chatBox.appendChild(
        createChatLi(`Error: ${data.message}`, "chat-incoming")
      );
    }
  } catch (error) {
    // Remove thinking message
    chatBox.removeChild(thinkingLi);

    // Add error message
    chatBox.appendChild(
      createChatLi("Error communicating with server", "chat-incoming")
    );
    console.error("Error:", error);
  }

  // Scroll to bottom
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Add event listeners
chatInputBtn.addEventListener("click", handleChat);

// Add Enter key support
chatInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    handleChat(e);
  }
});
