// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        tsu: {
          blue: '#0056b3',
          orange: '#ff8c00',
          light: '#f8f9fa',
          dark: '#121212',
        }
      }
    },
  },
  plugins: [],
}
