const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");

let userMessage;
// const API_KEY= "secret_key"; //pe care ar trebui eu sa o iau de pe site

const createChatLi = (message, className) => {
  //create a chat <li> element with passed message and className
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  let chatContent =
    className === "outgoing"
      ? `<p>${message}</p>`
      : `<span class="material-symbols-outlined"><svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#FFFFFF"><path d="M160-360q-50 0-85-35t-35-85q0-50 35-85t85-35v-80q0-33 23.5-56.5T240-760h120q0-50 35-85t85-35q50 0 85 35t35 85h120q33 0 56.5 23.5T800-680v80q50 0 85 35t35 85q0 50-35 85t-85 35v160q0 33-23.5 56.5T720-120H240q-33 0-56.5-23.5T160-200v-160Zm200-80q25 0 42.5-17.5T420-500q0-25-17.5-42.5T360-560q-25 0-42.5 17.5T300-500q0 25 17.5 42.5T360-440Zm240 0q25 0 42.5-17.5T660-500q0-25-17.5-42.5T600-560q-25 0-42.5 17.5T540-500q0 25 17.5 42.5T600-440ZM320-280h320v-80H320v80Zm-80 80h480v-480H240v480Zm240-240Z"/></svg></span><p>${message}</p>`;
  chatLi.innerHTML = chatContent;
  return chatLi;
};

const handleChat = () => {
  userMessage = chatInput.value.trim();

  if (!userMessage) return;

  chatbox.scrollTo(0, chatbox.scrollHeight);

  async function apelareTest() {
    // Apelează funcția Python și așteaptă răspunsul
    const raspuns = await eel.chatbot(userMessage)();

    // Afișează rezultatul în elementul cu id-ul "result"
    setTimeout(() => {
      //Display thinking message while waiting for the respons
      chatbox.appendChild(createChatLi("Thinking...", "incoming"));
      chatbox.appendChild(createChatLi(raspuns, "incoming"));

      //   raspunsuri.forEach((raspuns) => {
      //     chatbox.appendChild(createChatLi(raspuns, "incoming"));
      //   });
      chatbox.appendChild(incomingChatLi);
      chatbox.scrollTo(0, chatbox.scrollHeight);
      // generateResponse(incomingChatLi);
    }, 600);
  }

  apelareTest();
};
sendChatBtn.addEventListener("click", handleChat);

//acum adaugam iconita in fata mesajelor trimise
document.addEventListener("DOMContentLoaded", () => {
  const chatInput = document.querySelector(".chat-input textarea");
  const chatBox = document.querySelector(".chatbox");
  const sendButton = document.querySelector(".chat-input span");

  // Funcție pentru adăugarea unui nou mesaj trimis de utilizator
  function addOutgoingMessage(messageText) {
    // Creează elementul de mesaj
    const messageElement = document.createElement("li");
    messageElement.classList.add("chat", "outgoing");

    // Creează paragraful pentru textul mesajului
    const messageParagraph = document.createElement("p");
    messageParagraph.textContent = messageText;

    // Creează span-ul pentru iconiță
    const iconSpan = document.createElement("span");
    iconSpan.classList.add("material-symbols-outlined");
    iconSpan.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" height="44Spx" viewBox="0 -960 960 960" width="40px" fill="rgb(94, 96, 124)">
                <path d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0-60Zm0 360Z"/>
            </svg>
        `;
    // Adaugă iconița și textul în mesaj

    messageElement.appendChild(messageParagraph);
    messageElement.appendChild(iconSpan);

    // Adaugă mesajul în chatBox
    chatBox.appendChild(messageElement);

    // Derulează la ultimul mesaj
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Event listener pentru butonul de trimitere
  sendButton.addEventListener("click", () => {
    const messageText = chatInput.value.trim();
    if (messageText !== "") {
      addOutgoingMessage(messageText); //creeaza un element html nou pentru fiecare mesaj trimis
      chatInput.value = ""; // Golește zona de text după trimiterea mesajului
    }
  });

  // Opțiune pentru a trimite mesajul cu tasta Enter
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // Previi trimiterea unui nou rând în textarea
      sendButton.click();
    }
  });
});
