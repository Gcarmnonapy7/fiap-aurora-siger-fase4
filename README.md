# SIGIC — Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia

Projeto da **Atividade Integradora — Fase 4 (FIAP)**. Representa computacionalmente a
infraestrutura da colônia marciana **Aurora Siger** como um grafo ponderado e oferece
algoritmos de rede, modelagem matemática e análise de sustentabilidade (ESG).

> Desenvolvido em **Python puro** (somente biblioteca padrão), sem dependências externas.

## Como executar

```bash
python3 codigo_fonte.py
```

Requer apenas **Python 3.8+**. Navegue pelo menu interativo do terminal.

## Funcionalidades

- **Visualização da rede** — módulos, conexões, pesos e tipos.
- **Consulta de módulos** — detalhes e análise de eficiência por módulo.
- **Algoritmos de rede** — BFS, DFS, Dijkstra (caminho mínimo), Dijkstra com restrição de
  prioridade, detecção de pontos críticos, centralidade e eficiência.
- **Modelagem matemática** — projeção de consumo $C(t) = C_0 e^{rt}$, derivadas, otimização,
  perda energética e simulação de cenários.
- **Sustentabilidade e governança (ESG)**.
- **Simulações operacionais** — falha de módulo, pico de consumo, expansão e otimização.

## Exemplos de execução

### 1. Dijkstra — caminho mínimo (exemplo do enunciado)

Rota mais eficiente para enviar energia do **Armazenamento de Energia** ao **Suporte Médico**
(Menu `3 → 3`):

```
Origem: Armazenamento de Energia
Destino: Suporte Medico
...
Caminho encontrado:
   Armazenamento de Energia -> Habitacao -> Suporte Medico
   Distancia total: 4.00
```

### 2. Dijkstra — caminhos mínimos para todos os destinos

A partir do Armazenamento de Energia (Menu `3 → 5`), ordenado por distância:

```
Destino                | Dist. | Rota
----------------------------------------------------------------------
Centro de Controle     |   2.0 | Armazenamento de Energia -> Centro de Controle
Agricultura            |   2.0 | Armazenamento de Energia -> Agricultura
Oficina de Manutencao  |   2.0 | Armazenamento de Energia -> Oficina de Manutencao
Habitacao              |   3.0 | Armazenamento de Energia -> Habitacao
Producao de Oxigenio   |   3.0 | Armazenamento de Energia -> Producao de Oxigenio
Suporte Medico         |   4.0 | Armazenamento de Energia -> Habitacao -> Suporte Medico
```

### 3. BFS — exploração por níveis

A partir do Centro de Controle (Menu `3 → 1`):

```
Nivel 0: Centro de Controle
Nivel 1: Habitacao -> Armazenamento de Energia -> Comunicacao -> Laboratorio Cientifico -> Suporte Medico
Nivel 2: Agricultura -> Producao de Oxigenio -> Oficina de Manutencao -> Centro de Recreacao
```

### 4. Perda energética por distância (Menu `4 → 2`)

```
Distancia | Perda | Eficiencia
   1.0    |   4.9%  | 95.1%
   2.0    |   9.5%  | 90.5%
   3.0    |  13.9%  | 86.1%
```

## Estrutura do projeto

```
codigo_fonte.py            # Arquivo principal de execução
modules/                   # Module (vértice) e InfrastructureGraph (grafo)
algorithms/                # Dijkstra, BFS, DFS, análise de rede
modeling/                  # Modelagem matemática e cálculo diferencial
data/                      # Dados padronizados dos módulos e conexões
ui/                        # Menu interativo de terminal
visualization/             # Descrições textuais da rede
arquivos_auxiliares/       # Gerador do diagrama e documentação complementar
rede_colonia.pdf           # Diagrama visual da rede (gerado via Graphviz)
documentacao_complementar.pdf  # Documentação técnica detalhada
link_video.txt             # Link do vídeo de apresentação
```

## Conteúdos integrados

Grafos e algoritmos de redes · Estruturas de dados em Python (listas, matrizes, tuplas,
dicionários) · Modelagem matemática e cálculo diferencial · Otimização computacional ·
Sustentabilidade e governança ESG.

## Regeneração do diagrama (opcional)

O `rede_colonia.pdf` pode ser regenerado a partir dos dados do grafo (requer **Graphviz**):

```bash
python3 arquivos_auxiliares/gerar_rede_pdf.py
```

## Equipe

| Nome | RM | E-mail |
|------|----|--------|
| Gabriel Carmona Bittencourt | RM569239 | gabrielcarmabittencourtpy@gmail.com |
| Marcio Francisco dos Santos Junior | RM570758 | marciofsantos65@gmail.com |
| Iúri Leão de Almeida | RM570215 | iurileao@gmail.com |
| Maria Sophia Domingues dos Santos | RM571209 | maria.sophia.domingues@gmail.com |

## Licença

[MIT](LICENSE)
