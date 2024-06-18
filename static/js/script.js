const API_URL = "http://127.0.0.1:5000/chat";

const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
// Get modal elements
const deleteModal = document.getElementById("deleteModal");
const closeModal = document.getElementsByClassName("close")[0];
const confirmDelete = document.getElementById("confirmDelete");
const cancelDelete = document.getElementById("cancelDelete");

let query = null;

const loadDataFromLocalstorage = () => {
  const themeColor = localStorage.getItem("themeColor");

  document.body.classList.toggle("light-mode", themeColor === "light_mode");
  themeButton.innerText = document.body.classList.contains("light-mode")
    ? "dark_mode"
    : "light_mode";

  const defaultText = `<div class="default-text">
                            <h1>Search Assistant</h1>
                            <p>I am your personal assistant that can perform web searches. How can I help you today?</p>
                        </div>`;

  chatContainer.innerHTML = localStorage.getItem("all-chats") || defaultText;
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
};

const createChatElement = (content, className) => {
  const chatDiv = document.createElement("div");
  chatDiv.classList.add("chat", className);
  chatDiv.innerHTML = content;
  return chatDiv;
};

const getChatResponse = async (incomingChatDiv) => {
  const pElement = document.createElement("p");

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: query,
    }),
  };

  try {
    const response = await (await fetch(API_URL, requestOptions)).json();
    const containsMarkdown =
      response.response.includes("###") ||
      response.response.includes("**") ||
      response.response.includes("- ");

    if (containsMarkdown) {
      const converter = new showdown.Converter();
      const htmlContent = converter.makeHtml(response.response);
      pElement.innerHTML = htmlContent;
    } else {
      pElement.textContent = response.response.trim();
    }
  } catch (error) {
    pElement.classList.add("error");
    pElement.textContent =
      "Oops! Something went wrong while retrieving the response. Please try again.";
  }

  incomingChatDiv.querySelector(".typing-animation").remove();
  incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
  localStorage.setItem("all-chats", chatContainer.innerHTML);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
};

const copyResponse = (copyBtn) => {
  const reponseTextElement = copyBtn.parentElement.querySelector("p");
  navigator.clipboard.writeText(reponseTextElement.textContent);
  copyBtn.textContent = "done";
  setTimeout(() => (copyBtn.textContent = "content_copy"), 1000);
};

const showTypingAnimation = () => {
  const html = `<div class="chat-content">
                    <div class="chat-details">
                    <img src="/static/images/chatbot.png" alt="chatbot-img">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                        </div>
                    </div>
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                </div>`;
  const incomingChatDiv = createChatElement(html, "incoming");
  chatContainer.appendChild(incomingChatDiv);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
  getChatResponse(incomingChatDiv);
};

const handleOutgoingChat = () => {
  query = chatInput.value.trim();
  if (!query) return;

  chatInput.value = "";
  chatInput.style.height = `${initialInputHeight}px`;

  const html = `<div class="chat-content">
                    <div class="chat-details">
                    <img src="/static/images/usericon.png" alt="user-img">
                        <p>${query}</p>
                    </div>
                </div>`;

  const outgoingChatDiv = createChatElement(html, "outgoing");
  chatContainer.querySelector(".default-text")?.remove();
  chatContainer.appendChild(outgoingChatDiv);
  chatContainer.scrollTo(0, chatContainer.scrollHeight);
  setTimeout(showTypingAnimation, 500);
};

// Show modal when delete button is clicked
deleteButton.addEventListener("click", () => {
  deleteModal.style.display = "block";
});

// Close modal when 'x' is clicked
closeModal.addEventListener("click", () => {
  deleteModal.style.display = "none";
});

// Close modal when 'No' button is clicked
cancelDelete.addEventListener("click", () => {
  deleteModal.style.display = "none";
});

// Perform delete action when 'Yes' button is clicked
confirmDelete.addEventListener("click", () => {
  localStorage.removeItem("all-chats");
  loadDataFromLocalstorage();
  deleteModal.style.display = "none";
});

// Close modal if user clicks outside of the modal
window.addEventListener("click", (event) => {
  if (event.target == deleteModal) {
    deleteModal.style.display = "none";
  }
});

themeButton.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
  localStorage.setItem("themeColor", themeButton.innerText);
  themeButton.innerText = document.body.classList.contains("light-mode")
    ? "dark_mode"
    : "light_mode";
});

const initialInputHeight = chatInput.scrollHeight;

chatInput.addEventListener("input", () => {
  chatInput.style.height = `${initialInputHeight}px`;
  chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
    e.preventDefault();
    handleOutgoingChat();
  }
});

loadDataFromLocalstorage();
sendButton.addEventListener("click", handleOutgoingChat);

document
  .getElementById("sidebar-toggle")
  .addEventListener("click", function () {
    document.getElementById("chat-history-sidebar").classList.toggle("open");
    this.classList.toggle("open");
  });

const updateChatHistorySidebar = () => {
  const chatHistoryContent = document.querySelector(".chat-history-content");
  chatHistoryContent.innerHTML = chatContainer.innerHTML;
};
