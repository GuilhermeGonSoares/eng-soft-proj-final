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
   <blockquote class="imgur-embed-pub" lang="en" data-id="tynuD8n"><a href="https://imgur.com/tynuD8n">View post on imgur.com</a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
   [Imgur](https://imgur.com/WYiUkCv)
   [Imgur](https://imgur.com/PmjIiQo)
   [Imgur](https://imgur.com/3hvtJL0)

2. **Tela de Gerenciamento do Professor:** Permite aos professores cadastrar novas questões de diferentes tipos para compor os exames, além de abrir e fechar exames, apagar exames criados e fazer o download do relatório dos alunos em cada exame.
   [Imgur](https://imgur.com/OFAjvQo)

3. **Tela de Realização do Exame:** Os estudantes realizam os exames, respondendo às questões propostas.
   [Imgur](https://imgur.com/srwvGUy)

4. **Tela Home do Aluno:** Visualização das avaliações disponíveis, futuras e passadas pelo aluno. Houveram mudanças nessa tela e a parte de baixo armazena as provas passadas enquanto o carrossel acima armazena as provas atuais e futuras.
   [Imgur](https://imgur.com/tynuD8n)

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
5. Rodar o projeto no navegador utilizando a seguinte URL:
```shell
    http://localhost:5000/
```
