const icons = document.querySelectorAll('.icon');
const paperclipLabel = document.querySelector('.paperclip-label');
const paperclipIcon = document.querySelector('.icon');
[paperclipIcon, paperclipLabel].forEach((element) =>
  element.addEventListener('click', () => {
    icons.forEach((icon) => {
      if (icon.classList.contains('active')) {
        icon.classList.remove('active');
      }
    });
    userIcon.src = userIcon.classList.contains('active')
      ? '/static/assets/user-active.svg'
      : '/static/assets/user.svg';
    paperclipIcon.classList.add('active');
    paperclipIcon.src = paperclipIcon.classList.contains('active')
      ? '/static/assets/paperclip-active.svg'
      : '/static/assets/paperclip.svg';
  })
);

const userIcon = document.querySelector('.user-icon');
const userLabel = document.querySelector('.user-label');
[userIcon, userLabel].forEach((element) =>
  element.addEventListener('click', () => {
    icons.forEach((icon) => {
      if (icon.classList.contains('active')) {
        icon.classList.remove('active');
      }
    });
    paperclipIcon.src = paperclipIcon.classList.contains('active')
      ? '/static/assets/paperclip-active.svg'
      : '/static/assets/paperclip.svg';
    userIcon.classList.add('active');
    userIcon.src = userIcon.classList.contains('active')
      ? '/static/assets/user-active.svg'
      : '/static/assets/user.svg';
  })
);

const questionContainers = document.querySelectorAll('.question-container');

console.log(questionContainers);

questionContainers.forEach((questionContainer) => {
  questionContainer.addEventListener('click', () => {
    questionContainers.forEach((innerContainer) => {
      if (innerContainer.classList.contains('current')) {
        innerContainer.classList.remove('current');
      }
    });
    questionContainer.classList.add('current');
  });
});
