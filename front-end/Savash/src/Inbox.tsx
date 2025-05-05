
import "./Inbox.css";
import MessageList from "./MessageList";

import StudentNav from "./components/StudentNav"

import { useState, useEffect } from "react";

function Inbox() {
    const [messages, setMessages] = useState<string[]>([]);

    function loadMessages() {
        let messagesLocal = localStorage.getItem("join_req");
        if(!messagesLocal){

            return;
        }
        let messageData = JSON.parse(messagesLocal);
        setMessages(messageData);
    }

    useEffect(loadMessages);

    return (
    <>
        <StudentNav />
        <MessageList messages={messages}/>
    </>
    )
}

export default Inbox;