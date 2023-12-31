# Projeto ES.UnB 2023/1

## Descrição do Projeto

O projeto ES.UnB 2023/1 é uma aplicação web desenvolvida para auxiliar professores e estudantes em todo o processo de criação, realização e correção de exames e avaliações acadêmicas. A plataforma oferece uma experiência amigável e intuitiva, permitindo que os usuários interajam de forma fácil e eficiente.

## Funcionalidades Principais

### Para Professores:

1. **Criação de Questões Diversificadas:** Os professores podem cadastrar questões de múltipla escolha, verdadeiro ou falso, e com resposta numérica, proporcionando uma variedade de formatos de perguntas nas avaliações.
2. **Composição Personalizada de Exames:** Os professores podem criar exames com um número arbitrário de questões, permitindo a adaptação das avaliações de acordo com a turma e os conteúdos abordados.
3. **Agendamento de Exames:** Os professores têm a possibilidade de definir datas e horários de abertura e encerramento dos exames, controlando o período em que os estudantes podem realizar a avaliação.
4. **Atribuição de Pesos às Questões:** Ao cadastrar exames, os professores podem atribuir valores diferentes para cada questão, tornando possível ponderar a nota final com base na importância de cada pergunta.
5. **Relatórios Detalhados:** Os professores têm acesso a relatórios com as respostas dos estudantes, possibilitando uma análise abrangente do desempenho e identificação de pontos a serem melhorados.

### Para Estudantes:

1. **Realização de Exames Online:** Os estudantes podem realizar exames completos, respondendo às questões propostas e concluindo a avaliação ao final.
2. **Visualização de Notas:** Após a conclusão do exame, os estudantes podem imediatamente verificar suas notas e desempenho.
3. **Revisão de Respostas:** Os estudantes podem revisar as questões acertadas e erradas após a finalização do exame, permitindo aprendizado com os erros e acertos.
4. **Listagem de Exames Disponíveis:** Os estudantes têm acesso a uma lista de exames disponíveis, possibilitando o planejamento e preparação para as avaliações.

## Telas do Projeto

O projeto conta com diversas telas que facilitam a interação dos usuários com o sistema:

1. **Tela de Login e Registro:** Os usuários podem acessar a plataforma por meio desta tela, utilizando suas credenciais de login.
   [Tela de Login](https://imgur.com/WYiUkCv)
   [Tela de Registro](https://imgur.com/3hvtJL0)

3. **Tela de Gerenciamento do Professor:** Permite aos professores cadastrar novas questões de diferentes tipos para compor os exames, além de abrir e fechar exames, apagar exames criados e fazer o download do relatório dos alunos em cada exame.
   [Tela de Gerenciamento Professor](https://imgur.com/OFAjvQo)

4. **Tela de Realização do Exame:** Os estudantes realizam os exames, respondendo às questões propostas.
   [Tela de Realização de Exame](https://imgur.com/srwvGUy)

5. **Tela Home do Aluno:** Visualização das avaliações disponíveis, futuras e passadas pelo aluno. Houveram mudanças nessa tela e a parte de baixo armazena as provas passadas enquanto o carrossel acima armazena as provas atuais e futuras.
   [Tela Home Aluno](https://imgur.com/tynuD8n)

# Passo a Passo para rodar o Projeto

1. Criar um ambiente virtual:
    - python3 -m venv nome_do_ambiente
2. Depois de criar precisamos ativá-lo:
    - No Windows:
      - nome_do_ambiente\Scripts\activate
    - No macOS/Linux:
      - source nome_do_ambiente/bin/activate

3. Com o ambiente ativo vamos instalar as dependências as quais estão listadas no arquivo *requirements.txt*
```shell
    pip install -r requirements.txt
```

4. Com as dependências instaladas basta executar, estando na raiz do projeto:
```shell
    python run.py
```
5. Rodar o projeto no navegador utilizando a seguinte URL (substituir http://127.0.0.1:5000/ por):
```shell
    http://localhost:5000/
```

6. As matrículas destinadas para os professores são:
   - 999999999, 888888888, 777777777
   - Utilize-as para criar um professor
   
