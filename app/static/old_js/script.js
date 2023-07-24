const darkModeBtn = document.querySelector('.dark-mode-btn');
const darkModeIcon = document.querySelector('.dark-mode-icon');

darkModeBtn.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  darkModeIcon.src = document.body.classList.contains('dark')
    ? '/static/images/Sun.svg'
    : '/static/images/Moon.svg';
});

const submitBtn = document.querySelector('.submit-btn');
submitBtn.addEventListener('click', (e) => {
  e.preventDefault();
});
