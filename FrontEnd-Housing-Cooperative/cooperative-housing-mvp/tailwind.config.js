/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cooperative-cream': '#FFECD1',   // Background
        'cooperative-dark': '#001524',    // Primary text
        'cooperative-orange': '#FF7D00',  // Accent buttons/links
        'cooperative-teal': '#15616D',    // Secondary elements
        'cooperative-brown': '#78290F',   // Headers/highlights
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      screens: {
        'custom-1000': '980px',
      },
    },
  },
  plugins: [],
};