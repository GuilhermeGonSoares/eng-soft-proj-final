# Passo a Passo

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
