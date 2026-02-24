/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cooperative-cream': '#FDF6EC',   // Background
        'cooperative-dark': '#003000',    // Primary text
        'cooperative-orange': '#F57C00',  // Accent buttons/links
        'cooperative-teal': '#2E7D32',    // Secondary elements
        'cooperative-brown': '#2E7D32',   // Headers/highlights
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