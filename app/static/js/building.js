// const links = document.querySelectorAll('.nav-link');

// links.forEach((link) => {
//   link.addEventListener('click', (e) => {
//     links.forEach((l) => l.classList.remove('active'));
//     e.currentTarget.classList.add('active');
//   });
// });

const steps = document.querySelectorAll('.step');
const arrows = document.querySelectorAll('.arrow');

steps.forEach((step, i) => {
  step.addEventListener('click', (e, i) => {
    steps.forEach((s) => s.classList.remove('active'));
    e.currentTarget.classList.add('active');
  });
});

let questionCount = 0;

let multipleChoice = (questionCount) => `
<div class="alternatives">
    <label for="alternative1-${questionCount}" class="flex-group">
        <input type="radio" name="correctAlternative-multi-${questionCount}" value="A" />
        <input type="text" id="alternative1-${questionCount}" name="alternative1-${questionCount}" placeholder='Alternativa 1' class="alternative-field" />
    </label>
    <label for="alternative2-${questionCount}" class="flex-group">
        <input type="radio" name="correctAlternative-multi-${questionCount}" value="B" />
        <input type="text" id="alternative2-${questionCount}" name="alternative2-${questionCount}" placeholder='Alternativa 2' class="alternative-field" />
    </label>
    <label for="alternative3-${questionCount}" class="flex-group">
        <input type="radio" name="correctAlternative-multi-${questionCount}" value="C" />
        <input type="text" id="alternative3-${questionCount}" name="alternative3-${questionCount}" placeholder='Alternativa 3' class="alternative-field" />
    </label>
    <label for="alternative4-${questionCount}" class="flex-group">
        <input type="radio" name="correctAlternative-multi-${questionCount}" value="D" />
        <input type="text" id="alternative4-${questionCount}" name="alternative4-${questionCount}" placeholder='Alternativa 4' class="alternative-field" />
    </label>
</div>
`;

let trueOrFalse = (questionCount) => `
<div class="alternatives">
    <label for="verdadeiro-${questionCount}" class="flex-group">
        <input type="radio" name="correctAlternative-${questionCount}" value="Verdadeiro" />
        <input disabled  type="text" id="verdadeiro-${questionCount}" name="verdadeiro-${questionCount}" value="Verdadeiro" class="alternative-field" />
    </label>
    <label for="falso-${questionCount}" class="flex-group">
        <input type="radio" name="correctAlternative-${questionCount}" value="Falso" />
        <input disabled  type="text" id="falso-${questionCount}" name="falso-${questionCount}" value="Falso" class="alternative-field" />
    </label>
</div>
`;

let numeric = (questionCount) => `
<div class="alternatives">
    <label for="resposta-${questionCount}">
        <input type="number" id="resposta-${questionCount}" name="resposta-${questionCount}" placeholder="Resposta Numérica" class="alternative-field" style="width: 50%" />
    </label>
</div>
`;

const question = `
        <div class="question">
          <div class="form-group">
            <div class="input-container">
              <label
                for="nome"
                class="input-label"
                >Nome da Questão <span class="red">*</span></label
              >
              <input
                type="text"
                name="nome"
                id="nome"
                placeholder="Questão 1"
                class="input-field" />
            </div>
            <div class="input-container">
              <label
                for="nome"
                class="input-label"
                >Valor da Questão <span class="red">*</span></label
              >
              <input
                type="number"
                name="materia"
                id="materia"
                placeholder="1.5"
                class="input-field" />
            </div>
          </div>
          <div class="input-container">
            <label
              for="descricao"
              class="input-label"
              >Enunciado da Questão <span class="red">*</span>
            </label>
            <textarea
              name="enunciado"
              id="enunciado"
              cols="30"
              rows="5"
              placeholder="Joãozinho tem 5 maçãs..."
              class="input-field"></textarea>
          </div>
          <div class="input-container">
            <label
              for="tipo"
              class="input-label"
              >Tipo Da Questão <span class="red">*</span>
            </label>
            <!-- select input with 3 options -->
            <select
              name="tipo"
              id="tipo"
              data-answer="question-type"
              class="input-field">
              <option value="discursiva">Numérica</option>
              <option value="multipla_escolha">Múltipla Escolha</option>
              <option value="verdadeiro_falso">Verdadeiro ou Falso</option>
            </select>
            <div class="question-container">
              <div class="alternatives">
                <label for="resposta">
                  <input
                    type="number"
                    id="resposta"
                    name="resposta"
                    placeholder="Resposta Numérica"
                    class="alternative-field"
                    style="width: 50%" />
                </label>
              </div>
            </div>
          </div>
          <button class="btn-new-test">
            <img
              src="assets/plus.svg"
              alt=""
              id="novaQuestao" />Nova Questão
          </button>
        </div>`;

const generateAlternatives = (type, questionCount) => {
  switch (type) {
    case 'discursiva':
      return numeric(questionCount);
    case 'multipla_escolha':
      return multipleChoice(questionCount);
    case 'verdadeiro_falso':
      return trueOrFalse(questionCount);
    default:
      return numeric(questionCount);
  }
};

const addSelectChangeListener = (selectElement) => {
  selectElement.addEventListener('change', function (event) {
    const questionContainer = event.target
      .closest('.question')
      .querySelector('.alternatives');
    questionContainer.innerHTML = generateAlternatives(
      this.value,
      questionCount
    );
  });
};

document.getElementById('addQuestion').addEventListener('click', function (e) {
  e.preventDefault();
  questionCount++;

  const newQuestion = `
    <div class="question" id="question-${questionCount}">
      <div class="form-group">
        <div class="input-container">
          <label for="nome${questionCount}" class="input-label">Nome da Questão <span class="red">*</span></label>
          <input type="text" name="nome${questionCount}" id="nome${questionCount}" value="Questão ${questionCount}" class="input-field" />
        </div>
        <div class="input-container">
          <label for="materia${questionCount}" class="input-label">Valor da Questão <span class="red">*</span></label>
          <input type="number" name="materia${questionCount}" id="materia${questionCount}" placeholder="1.5" class="input-field" />
        </div>
      </div>
      <div class="input-container">
        <label for="descricao${questionCount}" class="input-label">Enunciado da Questão <span class="red">*</span></label>
        <textarea name="enunciado${questionCount}" id="enunciado${questionCount}" cols="30" rows="5" placeholder="Joãozinho tem 5 maçãs..." class="input-field"></textarea>
      </div>
      <div class="input-container">
        <label for="tipo${questionCount}" class="input-label">Tipo Da Questão <span class="red">*</span></label>
        <select name="tipo${questionCount}" id="tipo${questionCount}" data-answer="question-type${questionCount}" class="input-field question-type-select">
          <option value="discursiva">Numérica</option>
          <option value="multipla_escolha">Múltipla Escolha</option>
          <option value="verdadeiro_falso">Verdadeiro ou Falso</option>
        </select>
        <div id="alternatives-${questionCount}" class="alternatives-container">
          ${generateAlternatives('discursiva', questionCount)}
        </div>
      </div>
    </div>`;

  document
    .querySelector('.questions')
    .insertAdjacentHTML('beforeend', newQuestion);

  const selectElements = document.querySelectorAll('.question-type-select');
  selectElements.forEach(addSelectChangeListener);
});

const deleteQuestion = (questionId) => {
  const question = document.getElementById(questionId);
  question.remove();
};
const deleteButton = document.getElementById('deleteQuestion');

deleteButton.addEventListener('click', function (e) {
  e.preventDefault();
  const questionId = `question-${questionCount}`;
  deleteQuestion(questionId);
  questionCount--;
});

const submitButton = document.getElementById('saveAndContinue');

submitButton.addEventListener('click', function (e) {
  e.preventDefault();

  let questions = [];

  // Loop over each question
  for (let i = 1; i <= questionCount; i++) {
    const questionElement = document.getElementById(`question-${i}`);

    // Gather question data
    let questionData = {
      name: questionElement.querySelector(`#nome${i}`).value,
      score: parseInt(questionElement.querySelector(`#materia${i}`).value, 10),
      description: questionElement.querySelector(`#enunciado${i}`).value,
      type: questionElement.querySelector(`#tipo${i}`).value,
    };

    // Gather alternative data or answer based on the question type
    switch (questionData.type) {
      case 'multipla_escolha': {
        const alternativesElement = document.getElementById(
          `alternatives-${i}`
        );
        const alternativesInputElements =
          alternativesElement.querySelectorAll('.alternative-field');
        const correctAlternativeElements =
          alternativesElement.querySelectorAll('input[type=radio]');

        alternativesInputElements.forEach((inputElement, index) => {
          let alternativeData = {
            content: inputElement.value,
            isCorrect: correctAlternativeElements[index].checked,
          };

          questionData.alternatives = (questionData.alternatives || []).concat(
            alternativeData
          );
        });
        break;
      }
      case 'verdadeiro_falso': {
        questionData.answer = questionElement.querySelector(
          'input[type=radio]:checked'
        ).value;
        break;
      }
      case 'discursiva': {
        questionData.answer = parseInt(
          questionElement.querySelector('.alternative-field').value,
          10
        );
        break;
      }
      default:
        break;
    }

    questions.push(questionData);
  }

  // Fetch API to send the data to the server
  fetch(`http://localhost:5000/teacher/teste/${testeId}/questions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(questions),
  })
    .then((response) => {
      if (response.redirected) {
        window.location.href = response.url;
      } else {
        response.text().then((error) => {
          const errorMessage = error;
          console.error(errorMessage);
          alert('Erro ao criar o teste: ' + errorMessage);
        });
      }
    })
    .catch((error) => {
      alert('Erro ao criar o teste. Verifique a conexão e tente novamente.');
    });
});
