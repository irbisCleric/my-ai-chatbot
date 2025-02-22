import * as React from 'react';

import axios from 'axios';
import Message from './Message';
import InputBox from './InputBox';

const Chatbot = () => {
  const [messages, setMessages] = React.useState([]);
  const [input, setInput] = React.useState('');

  const handleSend = async () => {
    if (input.trim()) {
      // Adding user message
      setMessages([...messages, { text: input, sender: 'user' }]);

      // Sending messages to API
      try {
        const response = await axios.post('http://localhost:5000/api/chat', { message: input });
        const botMessage = response.data.reply;
        setMessages([...messages, { text: input, sender: 'user' }, { text: botMessage, sender: 'bot' }]);
      } catch (error) {
        console.error('Error fetching response:', error);
      }
    }
    setInput('');
  };

  return (
    <div className="chatbot">
      <div className="messages">
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} />
        ))}
      </div>
      <InputBox input={input} setInput={setInput} handleSend={handleSend} />
    </div>
  );
};

export default Chatbot;
