const links = document.querySelectorAll('.nav-link');

links.forEach((link) => {
  link.addEventListener('click', (e) => {
    links.forEach((l) => l.classList.remove('active'));
    e.currentTarget.classList.add('active');
  });
});

const steps = document.querySelectorAll('.step');
const arrows = document.querySelectorAll('.arrow');

steps.forEach((step, i) => {
  step.addEventListener('click', (e, i) => {
    steps.forEach((s) => s.classList.remove('active'));
    e.currentTarget.classList.add('active');
  });
});

let questionCount = 0;

let multipleChoice = `
<div class="alternatives">
    <label for="alternative1" class="flex-group">
        <input type="radio" name="correctAlternative-${questionCount}" value="1" />
        <input type="text" id="alternative1" name="alternative1" placeholder='Alternativa 1' class="alternative-field" />
    </label>
    <label for="alternative2" class="flex-group">
        <input type="radio" name="correctAlternative-${questionCount} value="2" />
        <input type="text" id="alternative2" name="alternative2" placeholder='Alternativa 2' class="alternative-field" />
    </label>
    <label for="alternative3" class="flex-group">
        <input type="radio" name="correctAlternative-${questionCount} value="3" />
        <input type="text" id="alternative3" name="alternative3" placeholder='Alternativa 3' class="alternative-field" />
    </label>
    <label for="alternative4" class="flex-group">
        <input type="radio" name="correctAlternative-${questionCount} value="4" />
        <input type="text" id="alternative4" name="alternative4" placeholder='Alternativa 4' class="alternative-field" />
    </label>
</div>
`;

let trueOrFalse = `
<div class="alternatives">
    <label for="verdadeiro" class="flex-group">
        <input type="radio" name="correctAlternative-${questionCount} value="1" />
        <input type="text" id="verdadeiro" name="verdadeiro" value="Verdadeiro" class="alternative-field" />
    </label>
    <label for="falso" class="flex-group">
        <input type="radio" name="correctAlternative-${questionCount} value="2" />
        <input type="text" id="falso" name="falso" value="Falso" class="alternative-field" />
    </label>
</div>
`;

let numeric = `
<div class="alternatives">
    <label for="resposta">
        <input type="number" id="resposta" name="resposta" placeholder="Resposta Numérica" class="alternative-field" style="width: 50%" />
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
              <option value="1">Numérica</option>
              <option value="2">Múltipla Escolha</option>
              <option value="3">Verdadeiro ou Falso</option>
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

const generateAlternatives = (type) => {
  switch (type) {
    case '1':
      return numeric;
    case '2':
      return multipleChoice;
    case '3':
      return trueOrFalse;
    default:
      return numeric;
  }
};

const addSelectChangeListener = (selectElement) => {
  selectElement.addEventListener('change', function () {
    const questionContainer = document.getElementById(`alternatives-${this.name}`);
    questionContainer.innerHTML = generateAlternatives(this.value);
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
        <input type="text" name="nome${questionCount}" id="nome${questionCount}" placeholder="Questão ${questionCount}" class="input-field" />
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
      <select name="${questionCount}" id="tipo${questionCount}" data-answer="question-type" class="input-field question-type-select">
        <option value="1">Numérica</option>
        <option value="2">Múltipla Escolha</option>
        <option value="3">Verdadeiro ou Falso</option>
      </select>
      <div id="alternatives-${questionCount}" class="alternatives-container">
        ${generateAlternatives('1')}
      </div>
    </div>
  </div>`;

  document.querySelector('.questions').insertAdjacentHTML('beforeend', newQuestion);

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
