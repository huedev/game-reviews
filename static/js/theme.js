// Referred to Tailwind CSS documentation (https://tailwindcss.com/docs/dark-mode#supporting-system-preference-and-manual-selection)
// For supporting system preferences and manual selection of light/dark modes

const enableDarkModeButton = document.querySelector("#enable-dark-mode");
const enableLightModeButton = document.querySelector("#enable-light-mode");

// On page load or when changing themes
function updateTheme()
{
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        enableDarkModeButton.classList.add('hidden');
        enableLightModeButton.classList.remove('hidden');
    } else {
        document.documentElement.classList.remove('dark');
        enableDarkModeButton.classList.remove('hidden');
        enableLightModeButton.classList.add('hidden');
    }
}

updateTheme();
  
// Whenever the user explicitly chooses light mode
enableLightModeButton.addEventListener("click", () => {
    localStorage.theme = 'light';
    updateTheme();
});

// Whenever the user explicitly chooses dark mode
enableDarkModeButton.addEventListener("click", () => {
    localStorage.theme = 'dark';
    updateTheme();
});