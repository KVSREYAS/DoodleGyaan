import { useState } from "react";
import "./TextSender.css"; // Import the external CSS file

export default function TextSender() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5001/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error("Error communicating with the server", error);
    }
  };

  return (
    <div className="container">
      {/* <h2 className="heading">ENTER YOUR TOPIC</h2> */}
      <textarea
        className="textarea"
        rows="4"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="What's on your mind today?"
      />
        {<button className="button" onClick={handleSubmit}>START CREATING</button>}
        {response && (
        <div className="response-box">
          <strong>Response:</strong> {response}
        </div>
      )}
    </div>
  );
}