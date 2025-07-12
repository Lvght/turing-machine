# Máquina de Turing para Teste de Primalidade

Este repositório contém uma implementação de uma Máquina de Turing para avaliar se determinado valor é primo ou não.

## Estrutura do repositório

Os principais arquivos e diretórios deste repositório são:

- `src/`: Contém a implementação da Máquina de Turing e outras funções auxiliares.
- `src/base.py`: Implementação da classe `TuringMachine` e suas dependências.
- `src/definition.py`: Define a Máquina de Turing para o teste de primalidade. Também define algumas outras máquinas que foram usadas na composição da máquina final.
- `main.py`: Ponto de entrada do programa, onde a Máquina de Turing é configurada e executada.
- `main.ipynb`: Um notebook Jupyter que demonstra o uso da Máquina de Turing.

## Instruções de como executar o projeto

Você precisará ter Python instalado em sua máquina. Além disso, é necessário instalar as dependências do projeto. Você pode fazer isso executando:

```bash
pip install -r requirements.txt
```

Após isso, basta executar o arquivo `main.py`. O primeiro argumento indica se a máquina irá imprimir na tela cada passo. O segundo argumento é o valor a ser testado.

```bash
python main.py [True|False] [valor]
```

Por exemplo:

```bash
python main.py True 7
```

## Executando o app streamlit

Rode o comando abaixo.

```
python -m streamlit run app.py
```
