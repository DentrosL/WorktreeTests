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
WorktreeTests/
```

Para executar:
```bash
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

## 2. Inicializando o Git

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
.../WorktreeTests  <commit>[branch]
.../WorktreeTests  3e653bf [main]
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
git worktree add ../WorktreeTestsFeature feature/dashboard
```

Agora temos:

```bash
git worktree list

.../WorktreeTests         d464825 [main]
.../WorktreeTestsFeature  d464825 [feature/dashboard]
```

Os dois worktrees começaram no mesmo commit, mas agora cada diretório está associado a uma branch diferente.


## 5. Trabalhando na feature

Entramos no worktree da feature:

```bash
cd ../WorktreeTestsFeature
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
modified: WorktreeTests/fintrack/ui.py
modified: WorktreeTests/fintrack/service.py
```
Neste momento, imagine que o dashboard ainda não está pronto.

## 6. Surge um problema urgente
Agora imagine que alguém encontrou um problema na versão estável da `main`.

O cálculo do saldo está incorreto.

A **situação** é:
```text
WorktreeTestsFeature/ [feature/dashboard]
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
ou fazer um commit temporário. Só depois:
```bash
git switch main
```
Corrigir o problema. Depois voltar para:
```bash
git switch feature/dashboard
```
E recuperar o trabalho.

## 7. Utilizando o Worktree
Como já temos um worktree separado para a feature, podemos simplesmente trabalhar em outro diretório.

Voltamos para o diretório principal:

```bash
cd ../WorktreeTests
```
Esse diretório está na:
```text
main
```
Enquanto isso:
```text
WorktreeTests/ [main]
WorktreeTestsFeature/ [feature/dashboard]
```
O código incompleto da feature continua intacto em:
```text
WorktreeTestsFeature/
```
- Não precisamos fazer `stash`.
- Não precisamos criar um commit temporário.
- Não precisamos copiar arquivos.

## 8. Criando o Worktree para o hotfix
Agora vamos criar uma branch específica para a correção:
```bash
git worktree add -b hotfix/saldo ../WorktreeTestsFix main
```

Esse comando:
1. cria a branch `hotfix/saldo`;
2. cria o worktree `../WorktreeTestsFix`;
3. utiliza a `main` como ponto de partida.

Agora temos:
```text
WorktreeTests/          [main]
WorktreeTestsFeature/   [feature/dashboard]
WorktreeTestsFix/       [hotfix/saldo]
```

Podemos confirmar:

![alt text](/imgs/image-2.png)

## 9. Corrigindo o problema
Entramos no worktree do hotfix:

```bash
cd ../WorktreeTestsFix
```

Agora estamos na:
```text
hotfix/saldo
```
Fazemos a correção normalmente. E depois:
```bash
git add .
git commit -m "fix: corrige cálculo do saldo"
```
O hotfix está pronto.

## 10. O que aconteceu com a feature?

Enquanto corrigíamos o problema, a feature continuou exatamente como estava:
```text
WorktreeTestsFeature/ [feature/dashboard]
    ↓
código incompleto
alterações não commitadas
```
![alt text](/imgs/image-3.png)

Não precisamos interromper o trabalho.

Esse é justamente o cenário em que o Worktree começa a fazer sentido.

Temos:
```text
                        Repositório
           ┌─────────────────┼───────────────────────────┐
           ↓                 ↓                           ↓
        main            dashboard                    hotfix
           ↓                 ↓                           ↓
    WorktreeTests/   WorktreeTestsFeature/      WorktreeTestsFix/
```

Cada branch está aberta em seu próprio diretório.

## 11. Finalizando o hotfix

Depois de corrigir o problema, podemos enviar a branch para o remoto:

```bash
git push -u origin hotfix/saldo
```

Depois que o hotfix for integrado à `main`, o worktree pode ser removido:

```bash
git worktree remove ../WorktreeTestsFix
```

A branch não é automaticamente removida:

```bash
git branch
```
![alt text](/imgs/image-4.png)

Ela continuará existindo até ser excluída explicitamente.

## 12. Continuando a feature

Agora podemos voltar para:

```bash
cd ../WorktreeTestsFeature
```

E continuar exatamente de onde paramos.

```text
feature/dashboard
    ↓
continua o desenvolvimento
```

O trabalho da feature não precisou ser guardado ou interrompido para corrigir o problema urgente.

## 13. Visualizando todos os Worktrees

Durante todo o processo podemos utilizar:

```bash
git worktree list
```
![alt text](/imgs/image-5.png)

Isso mostra fisicamente onde cada branch está aberta.

## 14. Removendo o Worktree da feature

Quando a feature terminar e o branch não precisar mais de um worktree separado:

```bash
git worktree remove ../WorktreeTestsFeature
```

Depois podemos verificar:

![alt text](/imgs/image-6.png)

E, se alguma referência antiga permanecer:

```bash
git worktree prune
```

## 15. O que aprendemos

Neste exemplo, utilizamos três branches:

```text
main
feature/dashboard
hotfix/saldo
```

E três diretórios:
```text
WorktreeTests/
WorktreeTestsFeature/
WorktreeTestsFix/
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
                        Repositório
           ┌─────────────────┼───────────────────────────┐
           ↓                 ↓                           ↓
        main            dashboard                    hotfix
           ↓                 ↓                           ↓
    WorktreeTests/   WorktreeTestsFeature/      WorktreeTestsFix/
```

Assim, quando uma alteração urgente aparece, podemos simplesmente entrar no diretório correspondente à branch que precisa ser alterada.

# Por fim
Agora que as duas alterações foram concluídas, podemos fazer o merge das branches `fix` e `feature` na `main`.

Primeiro, voltamos para o worktree da `main`:
```bash
cd ../WorktreeTests
```
Depois, fazemos o merge da branch de correção:
```bash
git merge hotfix/corrige-saldo
```
E em seguida, fazemos o merge da feature:
```bash
git merge feature/dashboard
```

Assim, a main passa a conter tanto a correção urgente quanto a nova funcionalidade desenvolvida separadamente nos outros worktrees.

Por fim, podemos conferir o estado das branches e dos worktrees:
```bash
git status
git worktree list
```
Dessa forma, o fluxo completo ficou:
```text

                  ┌──── hotfix/saldo ─────┐
                  │                       │
main ─────────────┼───────────────────────┼── merge
                  │                       │
                  └── feature/dashboard ──┘
                                          ↓
                                        main
```

> O objetivo do Worktree aqui foi permitir que a feature/dashboard continuasse em desenvolvimento enquanto a correção urgente era feita de forma independente, sem precisar interromper ou guardar o trabalho da feature.