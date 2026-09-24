# Explicação Prática
> Nesta etapa vamos utilizar o projeto **FinTrack**, um pequeno gerenciador financeiro desenvolvido em Python, para praticar o uso do `git worktree`.

A ideia é simular uma situação comum no desenvolvimento:
- existe uma versão estável na `main`;
- estamos desenvolvendo uma feature maior em outra branch;
- a feature ainda está incompleta;
- aparece um problema urgente na `main`;
- utilizamos um segundo worktree para trabalhar no hotfix sem mexer no trabalho que ainda está em andamento.

## 1. Conhecendo o projeto

O projeto está dentro de:

```text
proj/
```

Para executar:
```bash
cd proj

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python main.py
```

O sistema possui quatro funcionalidades:
```text
1 - Adicionar lançamento
2 - Listar lançamentos
3 - Resumo financeiro
4 - Ver categorias
0 - Sair
```

Neste ponto temos uma versão inicial e estável do projeto.

## 2. Inicializando o Git (passo feito)

Dentro do projeto:
```bash
cd proj

git init
git add .
git commit -m "feat:✨ cria fintrack"
```

Podemos conferir a branch atual:
```bash
git branch
```

E listar os worktrees:
```bash
git worktree list
```

Inicialmente teremos apenas o diretório principal:
```text
.../proj  <commit>[branch]
.../proj  8a77cd5 [master]
```

## 3. Criando a branch da nova feature
Vamos imaginar que surgiu uma nova funcionalidade:
> Adicionar um dashboard com uma visão mais completa das finanças.

Criamos a branch:
```bash
git switch -c feature/dashboard
```

Agora começamos a trabalhar normalmente.

A diferença é que, neste exemplo, queremos simular uma feature suficientemente grande para ainda não estar pronta quando surgir uma urgência.

## 4. Criando um Worktree para a feature

Em vez de continuar utilizando apenas o diretório original, podemos criar um worktree para a feature:

```bash
git switch main
git worktree add ../proj_dashboard feature/dashboard
```

Agora temos:

```text
proj/            → main
proj_dashboard/  → feature/dashboard
```

Podemos confirmar:

```bash
git worktree list
```

Algo semelhante a:

```text
.../proj             abc1234 [main]
.../proj_dashboard   abc1234 [feature/dashboard]
```

Os dois worktrees começaram no mesmo commit, mas agora cada diretório está associado a uma branch diferente.

---

## 5. Trabalhando na feature

Entramos no worktree da feature:

```bash
cd ../proj_dashboard
```

Agora podemos começar a desenvolver o dashboard.

Por exemplo, podemos alterar a interface para apresentar:

```text
╭────────────── FinTrack ──────────────╮
│                                      │
│ Receitas       R$ 4.500,00           │
│ Despesas       R$ 2.100,00           │
│ Saldo          R$ 2.400,00           │
│                                      │
╰──────────────────────────────────────╯
```

Durante o desenvolvimento, podemos ter vários arquivos modificados e código incompleto.

Por exemplo:

```bash
git status
```

pode mostrar:

```text
modified: fintrack/ui.py
modified: fintrack/service.py
```

Neste momento, imagine que o dashboard ainda não está pronto.

---

## 6. Surge um problema urgente

Agora imagine que alguém encontrou um problema na versão estável da `main`.

O cálculo do saldo está incorreto.

A situação é:

```text
proj_dashboard/
    ↓
feature/dashboard
    ↓
código incompleto
arquivos modificados
feature ainda não pronta
```

Precisamos corrigir a `main`.

### Sem Worktree

Teríamos que guardar o trabalho atual:

```bash
git stash
```

ou fazer um commit temporário.

Depois:

```bash
git switch main
```

Corrigir o problema.

Depois voltar para:

```bash
git switch feature/dashboard
```

E recuperar o trabalho.

---

## 7. Utilizando o Worktree

Como já temos um worktree separado para a feature, podemos simplesmente trabalhar em outro diretório.

Voltamos para o diretório principal:

```bash
cd ../proj
```

Esse diretório está na:

```text
main
```

Enquanto isso:

```text
proj/
    → main

proj_dashboard/
    → feature/dashboard
```

O código incompleto da feature continua intacto em:

```text
proj_dashboard/
```

Não precisamos fazer `stash`.

Não precisamos criar um commit temporário.

Não precisamos copiar arquivos.

---

## 8. Criando o Worktree para o hotfix

Agora vamos criar uma branch específica para a correção:

```bash
git worktree add -b hotfix/saldo ../proj_fix main
```

Esse comando:

1. cria a branch `hotfix/saldo`;
2. cria o worktree `../proj_fix`;
3. utiliza a `main` como ponto de partida.

Agora temos:

```text
proj/
    → main

proj_dashboard/
    → feature/dashboard

proj_fix/
    → hotfix/saldo
```

Podemos confirmar:

```bash
git worktree list
```

---

## 9. Corrigindo o problema

Entramos no worktree do hotfix:

```bash
cd ../proj_fix
```

Agora estamos na:

```text
hotfix/saldo
```

Fazemos a correção normalmente.

Depois:

```bash
git add .
git commit -m "fix: corrige cálculo do saldo"
```

O hotfix está pronto.

---

## 10. O que aconteceu com a feature?

Enquanto corrigíamos o problema, a feature continuou exatamente como estava:

```text
proj_dashboard/
    ↓
feature/dashboard
    ↓
código incompleto
alterações não commitadas
```

Não precisamos interromper o trabalho.

Esse é justamente o cenário em que o Worktree começa a fazer sentido.

Temos:

```text
                    Repositório

              ┌────────┼─────────┐
              ↓        ↓         ↓
            main   dashboard   hotfix
              ↓        ↓         ↓
           proj/   proj_dashboard/  proj_fix/
```

Cada branch está aberta em seu próprio diretório.

---

## 11. Finalizando o hotfix

Depois de corrigir o problema, podemos enviar a branch para o remoto:

```bash
git push -u origin hotfix/saldo
```

Depois que o hotfix for integrado à `main`, o worktree pode ser removido:

```bash
git worktree remove ../proj_fix
```

A branch não é automaticamente removida:

```bash
git branch
```

Ela continuará existindo até ser excluída explicitamente.

---

## 12. Continuando a feature

Agora podemos voltar para:

```bash
cd ../proj_dashboard
```

E continuar exatamente de onde paramos.

```text
feature/dashboard
    ↓
continua o desenvolvimento
```

O trabalho da feature não precisou ser guardado ou interrompido para corrigir o problema urgente.

---

## 13. Visualizando todos os Worktrees

Durante todo o processo podemos utilizar:

```bash
git worktree list
```

Por exemplo:

```text
.../proj             abc1234 [main]
.../proj_dashboard   def5678 [feature/dashboard]
.../proj_fix         ghi9012 [hotfix/saldo]
```

Isso mostra fisicamente onde cada branch está aberta.

---

## 14. Removendo o Worktree da feature

Quando a feature terminar e o branch não precisar mais de um worktree separado:

```bash
git worktree remove ../proj_dashboard
```

Depois podemos verificar:

```bash
git worktree list
```

E, se alguma referência antiga permanecer:

```bash
git worktree prune
```

---

## 15. O que aprendemos

Neste exemplo, utilizamos três branches:

```text
main
feature/dashboard
hotfix/saldo
```

E três diretórios:

```text
proj/
proj_dashboard/
proj_fix/
```

O ponto principal é que **uma branch não precisa ficar presa ao mesmo diretório que as outras branches**.

O Worktree permite manter essas linhas de desenvolvimento abertas simultaneamente.

### Sem Worktree

```text
1 diretório
    ↓
troca de branch
    ↓
outro estado do projeto
```

### Com Worktree

```text
             repositório
          /       |                ↓        ↓        ↓
       main   dashboard   hotfix
         ↓        ↓        ↓
      proj/   proj_dashboard/  proj_fix/
```

Assim, quando uma alteração urgente aparece, podemos simplesmente entrar no diretório correspondente à branch que precisa ser alterada.