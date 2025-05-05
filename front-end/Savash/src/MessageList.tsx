
interface MessageListProps {
  messages: string[];
}

function MessageList({ messages }: MessageListProps) {
    if(messages.length == 0){
        return (<h1>You're all caught up</h1>)
    }
  return (
    <ul className="class-container">
      {messages.map((message : string) => (
          <li className="class">
            <h2 className="code">{message}</h2>
          </li>
      ))}
    </ul>
  );
}

export default MessageList;
