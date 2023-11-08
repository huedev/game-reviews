/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: ["./templates/**/*.{html,htm}"],
  darkMode: 'class',
  theme: {
    extend: {
      brightness: {
        25: '.25',
      },
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
