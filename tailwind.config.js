// Referred an online tutorial by user Sachin (https://dev.to/sachingeek/how-to-use-tailwindcss-with-flask-1hm9)
// This tutorial helped me set up Tailwind CSS in a Flask environment

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
