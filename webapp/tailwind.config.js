/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{html,js}"],
    theme: {
      extend: {},
      fontFamily: {
        'sans': ['Ubuntu','ui-sans-serif', 'system-ui'],
        'serif': ['ui-serif', 'Georgia'],
        'mono': ['"Ubuntu Mono"', 'ui-monospace', 'SFMono-Regular'],
        'display': ['Ubuntu'],
        'body': ['"Ubuntu Mono"'],
      }
    },
    plugins: [],
  }
  