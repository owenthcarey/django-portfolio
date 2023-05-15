const darkModeSwitch = document.querySelector('#darkModeSwitch');
const body = document.querySelector('body');
const navbar = document.querySelector('.navbar');

// Initial check
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  body.classList.add('dark-mode');
  navbar.classList.add('bg-dark');
  navbar.setAttribute('data-bs-theme', 'dark');
  darkModeSwitch.checked = true;
}

// Listen for a click on the switch
darkModeSwitch.addEventListener('change', function () {
  if (this.checked) {
    // If the switch is checked, add dark mode
    body.classList.add('dark-mode');
    navbar.classList.add('bg-dark');
    navbar.setAttribute('data-bs-theme', 'dark');
  } else {
    // Otherwise, remove it
    body.classList.remove('dark-mode');
    navbar.classList.remove('bg-dark');
    navbar.removeAttribute('data-bs-theme');
  }
});
