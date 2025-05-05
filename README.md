#  Simulador de Autômatos em Python 

Este programa simula autômatos finitos determinísticos (AFD), não determinísticos (AFND) e com transições-ε (AFND-ε), lendo sua definição de um arquivo `.json` e testando palavras a partir de um `.csv`.

---

## Entradas

- **Arquivo JSON**: descreve o autômato (estados, transições, estado inicial e finais).
- **Arquivo CSV**: contém palavras e o resultado esperado (`1` ou `0`) 

---

##  Funcionamento

1. **Leitura do autômato**:
 - O arquivo JSON é carregado.
 - Cada transição é transformada em um objeto `Transition`.

2. **Determinação do tipo de autômato**:
 - Se houver transição com leitura vazia (`""` ou `null`), é **AFND-ε**.
 - Se houver múltiplas transições para um mesmo estado e símbolo, é **AFND**.
 - Caso contrário, é **AFD**.

3. **Simulação**:
 - O programa escolhe a função apropriada:
   - `run_AFD` para autômatos determinísticos.
   - `run_AFND` para não determinísticos.
   - `run_AFND_E` para os com transições-ε.
 - Cada palavra é processada e avaliada se é aceita ou rejeitada.

4. **Geração do CSV de saída**:
 - Para cada palavra:
   - É registrada a palavra, o valor esperado, o valor obtido, e o tempo de execução (em nanosegundos).



---

##  Como executar

No terminal (CMD), dentro da pasta onde está o script e os arquivos:

```bash
python simulador.py meu_auto.json entrada.csv saida.csv
