/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f3ff',
          100: '#edd6fe',
          200: '#ddd6fe',
          300: '#c084fc',
          400: '#a855f7',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        'premium': '0 4px 20px -2px rgba(124, 58, 237, 0.12), 0 2px 8px -1px rgba(124, 58, 237, 0.08)',
        'premium-hover': '0 10px 25px -3px rgba(124, 58, 237, 0.18), 0 4px 12px -2px rgba(124, 58, 237, 0.12)',
      },
    },
  },
  plugins: [],
}
