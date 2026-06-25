"""
Gerador do diagrama da rede da colonia Aurora Siger (rede_colonia.pdf).

Este script NAO faz parte do sistema executavel (codigo_fonte.py); e uma
ferramenta auxiliar de build que produz o entregavel visual exigido no item
1.2 / 2.3 do enunciado. Le os dados reais do grafo em data/data_modules.py,
gera um arquivo DOT e o renderiza para PDF usando o Graphviz (comando `neato`).

Uso:
    python3 arquivos_auxiliares/gerar_rede_pdf.py

Requer o Graphviz instalado no sistema (comando `neato` no PATH).
"""

import os
import sys
import subprocess

# Permite importar o pacote `data` a partir da raiz do projeto.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from data.data_modules import (
    DEFAULT_MODULES,
    DEFAULT_CONNECTIONS,
    MODULE_POSITIONS,
    CONNECTION_TYPES,
)

# ---------------------------------------------------------------------------
# Paleta: cor do no por nivel de prioridade e cor da aresta por tipo.
# ---------------------------------------------------------------------------
# neato -n2 interpreta `pos` em pontos (1/72"). ~160pt por unidade da grade
# espaca bem os modulos (cada no tem ~1-1.5" de largura).
ESCALA = 160

COR_TIPO = {
    "energy": "#e67e22",  # laranja  - distribuicao de energia
    "data": "#2980b9",    # azul     - troca de dados
    "life": "#27ae60",    # verde    - suporte a vida (O2, medico)
}


def cor_no(prioridade: int) -> str:
    """Cor de preenchimento do no conforme a prioridade operacional."""
    if prioridade >= 9:
        return "#c0392b"  # critico (suporte a vida / controle)
    if prioridade >= 7:
        return "#e67e22"  # importante
    return "#5dade2"      # apoio


def tipo_conexao(id1: str, id2: str) -> str:
    """Busca o tipo da conexao tolerando a ordem das chaves."""
    return (
        CONNECTION_TYPES.get(f"{id1}-{id2}")
        or CONNECTION_TYPES.get(f"{id2}-{id1}")
        or "energy"
    )


def montar_dot() -> str:
    """Constroi o texto DOT do grafo a partir dos dados da colonia."""
    linhas = [
        "graph AuroraSiger {",
        '  graph [label="Rede da Colonia Aurora Siger - SIGIC\\n'
        'Nos = modulos | Arestas = conexoes (peso = distancia)", '
        'labelloc="t", fontsize=20, fontname="Helvetica-Bold", '
        'bgcolor="#fbfbfb", splines=true, overlap=false];',
        '  node [shape=box, style="rounded,filled", fontname="Helvetica", '
        'fontcolor="white", fontsize=11, margin="0.18,0.10"];',
        # Rotulos de peso grandes, em negrito e preto para alto contraste.
        '  edge [fontname="Helvetica-Bold", fontsize=18, fontcolor="black", '
        'penwidth=2.5];',
        "",
    ]

    # Nos com posicao fixa, cor por prioridade e rotulo informativo.
    for module_id, name, consumption, priority, _cap, _comm, _status in DEFAULT_MODULES:
        x, y = MODULE_POSITIONS.get(module_id, (0, 0))
        rotulo = f"{name}\\n{module_id} | P{priority} | {consumption} kWh"
        linhas.append(
            f'  "{module_id}" [label="{rotulo}", '
            f'fillcolor="{cor_no(priority)}", '
            f'pos="{x * ESCALA},{y * ESCALA}!"];'
        )

    linhas.append("")

    # Arestas com cor por tipo e rotulo de peso (distancia).
    for id1, id2, weight in DEFAULT_CONNECTIONS:
        tipo = tipo_conexao(id1, id2)
        cor = COR_TIPO.get(tipo, "#7f8c8d")
        linhas.append(
            f'  "{id1}" -- "{id2}" [label="{weight}", color="{cor}"];'
        )

    # Legenda em cluster separado.
    linhas += [
        "",
        "  subgraph cluster_legenda {",
        '    label="Legenda"; fontname="Helvetica-Bold"; fontsize=12; '
        'color="#bdc3c7"; style="rounded";',
        '    node [shape=plaintext, fillcolor="none", fontcolor="black", fontsize=10];',
        f'    leg [pos="{6.2 * ESCALA},{1.5 * ESCALA}!", label=<',
        '      <table border="0" cellborder="0" cellspacing="2">',
        '        <tr><td bgcolor="#c0392b" width="16"></td>'
        '<td align="left">Prioridade 9-10 (critico)</td></tr>',
        '        <tr><td bgcolor="#e67e22" width="16"></td>'
        '<td align="left">Prioridade 7-8 (importante)</td></tr>',
        '        <tr><td bgcolor="#5dade2" width="16"></td>'
        '<td align="left">Prioridade &lt;= 6 (apoio)</td></tr>',
        '        <tr><td><font color="#e67e22">&#9472;&#9472;</font></td>'
        '<td align="left">Conexao de energia</td></tr>',
        '        <tr><td><font color="#2980b9">&#9472;&#9472;</font></td>'
        '<td align="left">Conexao de dados</td></tr>',
        '        <tr><td><font color="#27ae60">&#9472;&#9472;</font></td>'
        '<td align="left">Suporte a vida</td></tr>',
        "      </table>>];",
        "  }",
        "}",
    ]
    return "\n".join(linhas)


def main() -> None:
    dot_texto = montar_dot()
    caminho_dot = os.path.join(RAIZ, "arquivos_auxiliares", "rede_colonia.dot")
    caminho_pdf = os.path.join(RAIZ, "rede_colonia.pdf")

    with open(caminho_dot, "w", encoding="utf-8") as arquivo:
        arquivo.write(dot_texto)
    print(f"DOT gerado: {caminho_dot}")

    # `neato -n2` honra as coordenadas `pos=...!` fixadas nos nos.
    try:
        subprocess.run(
            ["neato", "-n2", "-Tpdf", caminho_dot, "-o", caminho_pdf],
            check=True,
        )
    except FileNotFoundError:
        print("ERRO: Graphviz (`neato`) nao encontrado no PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as erro:
        print(f"ERRO ao renderizar o PDF: {erro}", file=sys.stderr)
        sys.exit(1)

    print(f"PDF gerado: {caminho_pdf}")


if __name__ == "__main__":
    main()
