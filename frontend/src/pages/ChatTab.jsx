import { useState } from "react";

function ChatTab({ report = {}, investigation = {}, messageLog = [] }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hello! I can help you understand the current network diagnosis. Ask me about the report, evidence, or investigation.",
    },
  ]);

  function handleSend(event) {
    event.preventDefault();

    const text = question.trim();
    if (!text) return;

    const answer = `Current diagnosis status: ${
      report.status || "Not available"
    }. Investigation mode: ${
      investigation.mode || "Not available"
    }. For a detailed explanation, review the Diagnosis and Evidence tabs.`;

    setMessages((previous) => [
      ...previous,
      { role: "user", text },
      { role: "assistant", text: answer },
    ]);

    setQuestion("");
  }

  return (
    <section className="panel chat-panel">
      <div className="panel-heading">
        <div>
          <h2>NetCoop AI Assistant</h2>
          <p>Ask questions about your network diagnosis</p>
        </div>
        <span className="pipeline-mode">Assistant</span>
      </div>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${
              message.role === "user" ? "user-message" : "assistant-message"
            }`}
          >
            <span className="chat-role">
              {message.role === "user" ? "You" : "NetCoop AI"}
            </span>
            <p>{message.text}</p>
          </div>
        ))}
      </div>

      <form className="chat-form" onSubmit={handleSend}>
        <input
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask about the network diagnosis..."
        />
        <button type="submit" disabled={!question.trim()}>
          Send
        </button>
      </form>

      <p className="chat-disclaimer">
        This assistant currently provides basic report-based responses. It
        does not perform a new network investigation.
      </p>
    </section>
  );
}

export default ChatTab;