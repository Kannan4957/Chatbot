import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

export const Input = () => {
  const [tempmessage, setTempMessage] = useState('');
  const [answers, setAnswers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [answers]);

  const handleData = async (text) => {
    if (!text.trim()) return;

    setIsLoading(true);
    setAnswers(prev => [...prev, { sender: 'You', texts: text }]);

    try {
      const response = await axios.post('http://127.0.0.1:5000/chat', {
        message: text
      });

      setAnswers(prev => [...prev, { sender: 'Bot', texts: response.data.response }]);
    } catch (error) {
      console.error('Error:', error);
      setAnswers(prev => [...prev, {
        sender: 'Bot',
        texts: error.response?.data?.error || 'Connection error. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = () => {
    if (tempmessage.trim() && !isLoading) {
      handleData(tempmessage);
      setTempMessage('');
    }
  };

  return (
    <div className='bg-[#EFDCAB] min-h-4/5 flex justify-center items-center flex-col gap-2 p-2 flex-grow'>
      <div className='w-full md:w-3/4 flex flex-col justify-center items-center bg-[#443627] rounded-md m-3 flex-grow p-4'>
        <h1 className='text-white text-3xl mb-2'>Chat Section</h1>
        <div className='bg-[#EFDCAB] md:w-3/4 w-full p-2 flex flex-col rounded-xl max-h-[60vh] overflow-y-auto'>
          {answers.map((a, index) => (
            <div key={index} className={`flex ${a.sender === 'You' ? 'justify-start' : 'justify-end'}`}>
              <span className={`p-2 rounded-md max-w-xs md:max-w-md ${a.sender === 'You' ? 'bg-[#F2F6D0]' : 'bg-[#D98324]'}`}>
                {a.texts}
              </span>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-end">
              <span className="bg-[#D98324] p-2 rounded-md">Thinking...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className='flex justify-center items-center bg-[#443627] w-full md:w-3/4 py-4 px-2 rounded-lg mt-3'>
        <input
          type='text'
          className='w-full bg-[#443627] text-white outline-none px-4 py-2'
          value={tempmessage}
          onChange={(e) => setTempMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
          disabled={isLoading}
          placeholder="Type your message..."
        />
        <button
          className='bg-[#EFDCAB] rounded-lg p-2 px-4 ml-2 hover:bg-[#D98324] transition-all disabled:opacity-50'
          onClick={handleSubmit}
          disabled={isLoading || !tempmessage.trim()}
        >
          {isLoading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
};
