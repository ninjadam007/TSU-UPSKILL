import React from 'react';
import ChatPage from './pages/ChatPage'; // ชี้ไปที่โฟลเดอร์ pages

function App() {
  return (
    <div className="App min-h-screen bg-gray-100">
      {/* เรียกใช้งานหน้า ChatPage ที่เราจะเขียน UI กัน */}
      <ChatPage />
    </div>
  );
}

export default App;
