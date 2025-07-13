import colors from 'tailwindcss/colors';

export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}' // Include all template and script files
  ],
  darkMode: 'class',
  theme: {
    colors: {
      white: colors.white,
      black: colors.black,
      stone: colors.stone,
      green: colors.green,
      red: colors.red,
      blue: colors.blue,
      transparent: colors.transparent,
    }
  },
};