/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#F58220",
      },
      fontFamily:{
        mont : ["Montserrat", "sans-serif"],
      }
    },
  },
  plugins: [],
}