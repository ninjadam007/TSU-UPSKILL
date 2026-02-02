// tailwind.config.js
module.exports = {
  darkMode: 'class', // รองรับการสลับโหมดมืด
  theme: {
    extend: {
      colors: {
        tsu: {
          blue: '#0056b3',   // ฟ้า TSU
          orange: '#ff8c00', // ส้ม TSU
          light: '#f8f9fa',  // ขาวนวล
          dark: '#121212',   // ดำเข้ม (Dark Mode)
        }
      }
    },
  },
}
