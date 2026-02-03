import React, { useState, useEffect, useRef } from 'react';

const ChatPage = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [currentSession, setCurrentSession] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false); // เพิ่มเพื่อกันบัคกดส่งรัวๆ
  const messagesEndRef = useRef(null);

  const API_BASE_URL = 'http://localhost:8000/api';
  const token = localStorage.getItem('access_token');

  useEffect(() => {
    fetchSessions();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const fetchSessions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/sessions/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      const results = data.results || [];
      setSessions(results);
      
      if (results.length > 0) {
        // เลือกอันแรกถ้ายังไม่มีการเลือก
        if (!currentSession) await selectSession(results[0].id);
      } else {
        await createNewSession();
      }
    } catch (error) {
      console.error("Error fetching chat sessions:", error);
    }
  };

  const createNewSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/sessions/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setCurrentSession(data);
      setMessages([]);
      fetchSessions();
    } catch (error) {
      console.error("Error creating new session:", error);
    }
  };

  const selectSession = async (sessionId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/sessions/${sessionId}/messages/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      const selected = sessions.find(s => s.id === sessionId) || { id: sessionId };
      setCurrentSession(selected);
      setMessages(data.results || []);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const sendMessage = async () => {
    if (inputMessage.trim() === '' || !currentSession || isLoading) return;

    const userMessage = { 
      sender: 'user', 
      content: inputMessage, 
      created_at: new Date().toISOString() 
    };
    
    // แสดงข้อความฝั่งผู้ใช้ทันที
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat/sessions/${currentSession.id}/send-message/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: userMessage.content })
      });
      
      if (!response.ok) throw new Error('Network error');
      
      const data = await response.json();
      // อัปเดตข้อความทั้งหมด (รวมคำตอบ AI)
      setMessages(data.messages || []); 
      fetchSessions();

    } catch (error) {
      console.error("Error sending message:", error);
      setMessages(prev => [...prev, { 
        sender: 'system', 
        content: 'ขออภัยครับพี่ชาย ส่งข้อความไม่สำเร็จ กรุณาลองใหม่นะ', 
        created_at: new Date().toISOString() 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`${darkMode ? 'dark' : ''} min-h-screen flex flex-col bg-tsu-light dark:bg-tsu-dark text-gray-900 dark:text-white transition-colors duration-200`}>
      {/* Header */}
      <header className="p-4 flex justify-between items-center border-b border-tsu-blue dark:border-tsu-orange bg-white dark:bg-gray-800">
        <h1 className="text-2xl font-bold text-tsu-blue dark:text-tsu-orange">TSU AI Assistant</h1>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 px-4 rounded-full bg-tsu-blue text-white dark:bg-tsu-orange hover:opacity-90 transition-all"
        >
          {darkMode ? '☀️ โหมดสว่าง' : '🌙 โหมดมืด'}
        </button>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-1/4 p-4 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hidden lg:block overflow-y-auto">
          <button
            onClick={createNewSession}
            className="w-full mb-4 py-3 px-4 rounded-xl bg-green-500 text-white hover:bg-green-600 font-bold shadow-sm transition-all"
          >
            + เริ่มแชทใหม่
          </button>
          <div className="space-y-2">
            {sessions.map(session => (
              <div
                key={session.id}
                onClick={() => selectSession(session.id)}
                className={`p-4 rounded-xl cursor-pointer border transition-all ${
                  currentSession?.id === session.id
                    ? 'bg-tsu-blue text-white border-tsu-blue dark:bg-tsu-orange dark:border-tsu-orange shadow-md'
                    : 'bg-gray-50 hover:bg-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 border-transparent'
                }`}
              >
                <h3 className="font-semibold truncate">{session.title || `แชท #${session.id}`}</h3>
                <p className={`text-xs truncate mt-1 ${currentSession?.id === session.id ? 'text-blue-100' : 'text-gray-500'}`}>
                  {session.last_message?.content || 'ยังไม่มีข้อความ'}
                </p>
              </div>
            ))}
          </div>
        </aside>

        {/* Chat Area */}
        <main className="flex flex-col flex-1 p-4 bg-gray-50 dark:bg-gray-900">
          <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[80%] p-4 rounded-2xl shadow-sm ${
                    msg.sender === 'user'
                      ? 'bg-tsu-blue text-white rounded-tr-none'
                      : msg.sender === 'ai' || msg.sender === 'model'
                      ? 'bg-white text-gray-800 dark:bg-gray-700 dark:text-white rounded-tl-none border border-gray-200 dark:border-gray-600'
                      : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-200 rounded-tl-none border border-red-200 dark:border-red-800'
                  }`}
                >
                  <p className="text-sm md:text-base leading-relaxed">{msg.content}</p>
                  <span className={`block text-[10px] text-right mt-2 opacity-70`}>
                    {new Date(msg.created_at).toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 dark:bg-gray-700 p-3 rounded-lg animate-pulse text-xs text-gray-500 dark:text-gray-400">
                  TSU AI กำลังพิมพ์ข้อมูล...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="mt-4 flex gap-2 max-w-5xl mx-auto w-full">
            <input
              type="text"
              disabled={isLoading}
              className="flex-1 p-4 rounded-2xl border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-tsu-blue dark:focus:ring-tsu-orange shadow-inner"
              placeholder={isLoading ? "โปรดรอสักครู่..." : "พิมพ์ข้อความสอบถามที่นี่..."}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => { if (e.key === 'Enter') sendMessage(); }}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading}
              className="px-8 rounded-2xl bg-tsu-blue text-white dark:bg-tsu-orange hover:opacity-90 transition-opacity font-bold shadow-lg disabled:grayscale"
            >
              {isLoading ? '...' : 'ส่ง'}
            </button>
          </div>
        </main>
      </div>
    </div>
  );
};

export default ChatPage;
