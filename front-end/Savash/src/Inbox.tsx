import "./Inbox.css";
import MessageList from "./components/MessageList";

import StudentNav from "./components/StudentNav";
import TeacherNav from "./components/TeacherNav";

import { useState, useEffect } from "react";
import { getToken } from "./types.ts";

let apiUrl = "https://api.codewasabi.xyz";

function Inbox() {
  const [messages, setMessages] = useState<Number[]>([]);

  function loadMessages() {
    fetch(apiUrl + "/users/", {
      method: "GET",
      headers: {
        Authorization: "bearer " + getToken(document.cookie),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data || data.join_req.length == 0) {
          setMessages([]);
          return;
        }
        console.log(data);
        setMessages(data.join_req.map((elem: string) => Number(elem)));
      });
  }

  useEffect(loadMessages, []);

  if (localStorage.getItem("role") == "teacher") {
    return (
      <>
        <TeacherNav />
        <MessageList messages={messages} />
      </>
    );
  } else {
    return (
      <>
        <StudentNav />
        <MessageList messages={messages} />
      </>
    );
  }
}

export default Inbox;
