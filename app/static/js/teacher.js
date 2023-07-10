// Obtém uma referência a todos os botões de opções
const optionButtons = document.querySelectorAll('.question-options-btn');

// Adiciona o evento de clique a cada botão de opção
optionButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const option = button.dataset.option;
    addQuestion(option);
  });
});

let questionIndex = 0; // Índice único para cada questão
console.log('questionIndex', questionIndex);
function addQuestion(option) {
  console.log(option);
  // Cria um elemento de div para a questão de múltipla escolha
  const questionContainer = document.createElement('div');
  questionContainer.classList.add('multiple-choice-container');

  switch (option) {
    case 'multiple-choice':
      questionContainer.innerHTML = `
        <h3 class="multiple-choice-title">Questão de Múltipla Escolha</h3>
        <input
          type="text"
          name=""
          class="problem-input"
          style="word-wrap: break-word"
          placeholder="Enunciado da questão..."
        />
        <div class="choice-container">
          <input type="radio" name="choice-${questionIndex}" value="A" id="choice-${questionIndex}-a" />
          <label for="choice-${questionIndex}-a"></label>
          <input type="text" class="choice-input" placeholder="Alternativa a..." />
        </div>
        <div class="choice-container">
          <input type="radio" name="choice-${questionIndex}" value="B" id="choice-${questionIndex}-b" />
          <label for="choice-${questionIndex}-b"></label>
          <input type="text" class="choice-input" placeholder="Alternativa b..." />
        </div>
        <div class="choice-container">
          <input type="radio" name="choice-${questionIndex}" value="C" id="choice-${questionIndex}-c" />
          <label for="choice-${questionIndex}-c"></label>
          <input type="text" class="choice-input" placeholder="Alternativa C..." />
        </div>
        <div class="choice-container">
          <input type="radio" name="choice-${questionIndex}" value="D" id="choice-${questionIndex}-d" />
          <label for="choice-${questionIndex}-d"></label>
          <input type="text" class="choice-input" placeholder="Alternativa d..." />
        </div>
      `;
      break;
    case 'true-false':
      questionContainer.innerHTML = `
        <h3 class="multiple-choice-title">Questão de Verdadeiro ou Falso</h3>
        <input
          type="text"
          name=""
          class="problem-input"
          placeholder="Enunciado da questão..."
        />
        <div class="choice-container">
          <input type="radio" name="choice-vf-${questionIndex}" value="Verdadeiro" id="true-${questionIndex}" />
          <label for="true-${questionIndex}"></label>
          <input type="text" class="choice-input" value="Verdadeiro" />
        </div>
        <div class="choice-container">
          <input type="radio" name="choice-vf-${questionIndex}" value="Falso" id="false-${questionIndex}" />
          <label for="false-${questionIndex}"></label>
          <input type="text" class="choice-input" value="Falso" />
        </div>
      `;
      break;
    case 'numeric-response':
      questionContainer.innerHTML = `
        <h3 class="multiple-choice-title">Questão de Resposta Numérica</h3>
        <input
          type="text"
          name=""
          class="problem-input"
          placeholder="Enunciado da questão..."
        />
        <input type="number" class="num-choice-input" placeholder="Resposta" />
      `;
      break;
    default:
      // Opção inválida
      break;
  }

  // Adiciona a questão ao container
  const questionContainerElement =
    document.getElementById('question-container');
  questionContainerElement.appendChild(questionContainer);

  questionIndex++; // Incrementa o índice único para a próxima questão
}

// Evento de clique no botão "Criar Teste"
const createTestBtn = document.getElementById('create-test-btn');
createTestBtn.addEventListener('click', createTest);

// Função para criar o teste
function createTest() {
  const questionContainers = document.querySelectorAll(
    '.multiple-choice-container'
  );
  const questions = [];

  for (const questionContainer of questionContainers) {
    const titleElement = questionContainer.querySelector(
      '.multiple-choice-title'
    );

    if (titleElement.textContent === 'Questão de Múltipla Escolha') {
      // Questão de Múltipla Escolha
      const enunciado = questionContainer.querySelector('.problem-input').value;

      const alternativas = [];
      const choices = questionContainer.querySelectorAll('.choice-container');

      for (const choice of choices) {
        const texto = choice.querySelector('.choice-input').value;
        alternativas.push(texto);
      }

      const resposta = questionContainer.querySelector(
        'input[name^="choice"]:checked'
      ).value;

      const question = {
        tipo: 'multipla_escolha',
        enunciado,
        alternativas,
        resposta,
      };

      questions.push(question);
    } else if (titleElement.textContent === 'Questão de Verdadeiro ou Falso') {
      // Questão de Verdadeiro ou Falso
      const enunciado = questionContainer.querySelector('.problem-input').value;
      const alternativas = ['Verdadeiro', 'Falso'];

      const resposta = questionContainer.querySelector(
        'input[name^="choice-vf"]:checked'
      ).value;

      const question = {
        tipo: 'verdadeiro_falso',
        enunciado,
        alternativas,
        resposta,
      };

      questions.push(question);
    } else if (titleElement.textContent === 'Questão de Resposta Numérica') {
      // Questão de Resposta Numérica
      const enunciado = questionContainer.querySelector('.problem-input').value;
      const resposta =
        questionContainer.querySelector('.num-choice-input').value;

      const question = {
        tipo: 'discursiva',
        enunciado,
        resposta,
      };

      questions.push(question);
    }
  }

  // Enviar as questões para o controller
  fetch('http://localhost:5000/teacher/teste', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ questions }),
  });
}
