/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {
      brightness: {
        25: '.25',
      }
    },
  },
  plugins: [],
}
