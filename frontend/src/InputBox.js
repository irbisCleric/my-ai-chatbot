import * as React from 'react';

const InputBox = ({ input, setInput, handleSend }) => {
  return (
    <div className="input-box">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Input your message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default InputBox;
