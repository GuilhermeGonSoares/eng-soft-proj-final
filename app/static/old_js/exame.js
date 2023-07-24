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

// Obtém todas as instâncias dos elementos do tempo restante
const tempoRestanteTeste = document.querySelectorAll('.time-left');

// Função para atualizar o tempo restante em cada elemento
function atualizarTempoRestante(listTime) {
  listTime.forEach((element) => {
    const tempoRestante = element.textContent;

    // Divide o tempo restante em horas, minutos e segundos
    let [horas, minutos, segundos] = tempoRestante.split(':');

    // Converte as strings em números
    horas = parseInt(horas);
    minutos = parseInt(minutos);
    segundos = parseInt(segundos);

    // Diminui 1 segundo do tempo restante
    segundos--;

    // Verifica se é necessário ajustar as horas e minutos
    if (segundos < 0) {
      segundos = 59;
      minutos--;

      if (minutos < 0) {
        minutos = 59;
        horas--;

        if (horas < 0) {
          // Tempo restante expirado
          horas = 0;
          minutos = 0;
          segundos = 0;
        }
      }
    }

    // Formata os valores com zeros à esquerda
    const horasFormatadas = horas.toString().padStart(2, '0');
    const minutosFormatados = minutos.toString().padStart(2, '0');
    const segundosFormatados = segundos.toString().padStart(2, '0');

    // Atualiza o valor exibido no elemento
    element.textContent = `${horasFormatadas}:${minutosFormatados}:${segundosFormatados}`;
  });
}

// Chama a função atualizarTempoRestante a cada segundo
setInterval(() => atualizarTempoRestante(tempoRestanteTeste), 1000);
