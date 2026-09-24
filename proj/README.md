# FinTrack

Um pequeno gerenciador financeiro pessoal para terminal, desenvolvido em Python.

O projeto foi criado para servir como exemplo prático no estudo de **Git Worktree**, mas também funciona como um pequeno projeto de portfólio.

## Funcionalidades

- Cadastro de receitas e despesas;
- Listagem de lançamentos;
- Resumo financeiro;
- Filtro por categoria;
- Persistência dos dados em JSON;
- Interface de terminal usando [Rich](https://github.com/Textualize/rich).

## Requisitos

- Python 3.10+
- pip

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso
```bash
python main.py
```

O programa apresenta um menu interativo:
```text
1 - Adicionar lançamento
2 - Listar lançamentos
3 - Resumo financeiro
4 - Ver categorias
0 - Sair
```

Os dados são armazenados localmente em:
```text
data/transactions.json
```

## Estrutura
```text
proj/
├── data/
├── fintrack/
│   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   ├── service.py
│   └── ui.py
├── main.py
├── requirements.txt
└── README.md
```

## Objetivo do projeto
O código é propositalmente pequeno, mas possui uma estrutura suficiente para criar branches de funcionalidade e simular um cenário real de desenvolvimento com Git Worktree.