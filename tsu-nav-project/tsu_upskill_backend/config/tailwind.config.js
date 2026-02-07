/** @type {import('tailwindcss').Config} */
module.exports = {
  // เปิดใช้งาน Dark Mode โดยใช้การเช็ค class 'dark' ที่ตัว <html> หรือ <body>
  darkMode: 'class',
  
  // ระบุไฟล์ที่ Tailwind จะไปสแกนหา class เพื่อสร้าง CSS ให้
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  
  theme: {
    extend: {
      // เพิ่มสีเอกลักษณ์ของ TSU เข้าไปในระบบ
      colors: {
        tsu: {
          blue: '#0056b3',    // สีน้ำเงินหลัก TSU
          orange: '#ff8c00',  // สีส้ม TSU
          light: '#f8f9fa',   // สีพื้นหลังโหมดสว่าง
          dark: '#121212',    // สีพื้นหลังโหมดมืด
        }
      },
      // แนะนำให้เพิ่ม Font ที่อ่านง่ายๆ เข้าไปด้วยครับ
      fontFamily: {
        sans: ['Inter', 'Sarabun', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
