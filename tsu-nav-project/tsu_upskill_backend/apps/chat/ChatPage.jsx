import React, { useState, useEffect, useRef } from 'react';

const ChatPage = () => {
  const [darkMode, setDarkMode] = useState(false); // สมมติว่ามี state สำหรับ Dark Mode
  const [currentSession, setCurrentSession] = useState(null); // Session ที่กำลังแชทอยู่
  const [sessions, setSessions] = useState([]); // รายการ Session ทั้งหมด
  const [messages, setMessages] = useState([]); // ข้อความใน Session ปัจจุบัน
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);

  const API_BASE_URL = 'http://localhost:8000/api'; // อย่าลืมเปลี่ยนเป็น Production URL เมื่อ Deploy
  const token = localStorage.getItem('access_token'); // ต้องเก็บ token หลังจาก Login

  useEffect(() => {
    // โหลด Sessions เมื่อ Component โหลดครั้งแรก
    fetchSessions();
  }, []);

  useEffect(() => {
    // เลื่อน Scroll ไปล่างสุดเมื่อมีข้อความใหม่
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const fetchSessions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/sessions/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setSessions(data.results || []);
      if (data.results && data.results.length > 0) {
        // เลือก Session ล่าสุด หรือสร้างใหม่
        await selectSession(data.results[0].id); 
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
      setMessages([]); // ล้างข้อความสำหรับ Session ใหม่
      fetchSessions(); // โหลด Sessions ใหม่หลังจากสร้าง
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
      const selectedSession = sessions.find(s => s.id === sessionId);
      setCurrentSession(selectedSession);
      setMessages(data.results || []);
    } catch (error) {
      console.error("Error fetching messages for session:", error);
    }
  };

  const sendMessage = async () => {
    if (inputMessage.trim() === '' || !currentSession) return;

    const userMessage = { sender: 'user', content: inputMessage, created_at: new Date().toISOString() };
    setMessages(prevMessages => [...prevMessages, userMessage]); // แสดงข้อความผู้ใช้ทันที
    setInputMessage('');

    try {
      const response = await fetch(`${API_BASE_URL}/chat/sessions/${currentSession.id}/send-message/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ content: userMessage.content })
      });
      const data = await response.json();

      // Backend จะส่งข้อความกลับมาทั้ง User และ AI (หรือ Admin)
      // เราจะอัปเดตข้อความทั้งหมดตามที่ Backend ส่งมาเพื่อความถูกต้อง
      setMessages(data.messages || []); 

      // อัปเดตข้อมูล Session ล่าสุด
      fetchSessions();

    } catch (error) {
      console.error("Error sending message:", error);
      // กรณีเกิดข้อผิดพลาด อาจจะแสดงข้อความว่าส่งไม่สำเร็จ
      setMessages(prevMessages => [...prevMessages, { sender: 'system', content: 'ส่งข้อความไม่สำเร็จ', created_at: new Date().toISOString() }]);
    }
  };

  return (
    <div className={`${darkMode ? 'dark' : ''} min-h-screen flex flex-col bg-tsu-light dark:bg-tsu-dark text-gray-900 dark:text-white`}>
      {/* Header */}
      <header className="p-4 flex justify-between items-center border-b border-tsu-blue dark:border-tsu-orange">
        <h1 className="text-2xl font-bold text-tsu-blue dark:text-tsu-orange">TSU AI Chatbot</h1>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 rounded-full bg-tsu-blue text-white dark:bg-tsu-orange"
        >
          {darkMode ? '🌙 Dark Mode' : '☀️ Light Mode'}
        </button>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar for Chat Sessions */}
        <aside className="w-1/4 p-4 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-y-auto">
          <button
            onClick={createNewSession}
            className="w-full mb-4 py-2 px-4 rounded-lg bg-green-500 text-white hover:bg-green-600"
          >
            + New Chat
          </button>
          {sessions.map(session => (
            <div
              key={session.id}
              onClick={() => selectSession(session.id)}
              className={`p-3 mb-2 rounded-lg cursor-pointer ${
                currentSession?.id === session.id
                  ? 'bg-tsu-blue text-white dark:bg-tsu-orange'
                  : 'bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600'
              }`}
            >
              <h3 className="font-semibold">{session.title || `Chat #${session.id}`}</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {session.last_message?.content ? session.last_message.content.substring(0, 30) + '...' : 'No messages yet'}
              </p>
            </div>
          ))}
        </aside>

        {/* Chat Area */}
        <main className="flex flex-col flex-1 p-4 bg-gray-50 dark:bg-gray-900">
          <div className="flex-1 overflow-y-auto space-y-4 pr-2">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-md p-3 rounded-lg shadow ${
                    msg.sender === 'user'
                      ? 'bg-tsu-blue text-white'
                      : msg.sender === 'ai'
                      ? 'bg-gray-200 text-gray-900 dark:bg-gray-700 dark:text-white'
                      : 'bg-red-200 text-red-800 dark:bg-red-700 dark:text-red-100' // สำหรับ admin หรือ system message
                  }`}
                >
                  <p>{msg.content}</p>
                  <span className="block text-xs text-right opacity-75 mt-1">
                    {new Date(msg.created_at).toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} /> {/* สำหรับ Scroll อัตโนมัติ */}
          </div>

          {/* Input Area */}
          <div className="mt-4 flex">
            <input
              type="text"
              className="flex-1 p-3 rounded-l-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-tsu-blue dark:focus:ring-tsu-orange"
              placeholder="พิมพ์ข้อความที่นี่..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => { if (e.key === 'Enter') sendMessage(); }}
            />
            <button
              onClick={sendMessage}
              className="p-3 rounded-r-lg bg-tsu-blue text-white dark:bg-tsu-orange hover:bg-opacity-90 transition-opacity"
            >
              ส่ง
            </button>
          </div>
        </main>
      </div>
    </div>
  );
};

export default ChatPage;
