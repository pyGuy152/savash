
interface MessageListProps {
  messages: Number[];
}

const apiUrl = "https://api.codewasabi.xyz";

import { useNavigate } from "react-router-dom";
import { getToken } from "../types.ts";



function MessageList({ messages }: MessageListProps) {

  const navigate = useNavigate();

    if(messages.length == 0){
        return (<h1>You're all caught up</h1>)
    }

    function acceptClassInvite(code : Number) {
      const data = { code };
          console.log(apiUrl);
        fetch(apiUrl + "/classes/join", {
            body: JSON.stringify(data),
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "bearer " + getToken(document.cookie)
            },
        }).then(() => {
            navigate("/classes");
        });
    }

  return (
    <ul className="class-container">
      {messages.map((message : Number) => (
          <li className="class">
            <h2 className="">{message.toString()}</h2>
            <button onClick={() => acceptClassInvite(message)} className="submit">Accept</button>
          </li>
      ))}
    </ul>
  );
}

export default MessageList;
