/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"), require('daisyui'),
  ],
  daisyui: {
    themes: [
      "light",
      "dark",
      "cupcake",
      "bumblebee",
      "emerald",
      "corporate",
      "synthwave",
      "garden",
      "lofi",
      "pastel",
      "fantasy",
      "wireframe",
      "dracula",
      "cmyk",
      "lemonade",
      "winter",
      "dim",
      "nord",
      "sunset",
    ],
  },
}