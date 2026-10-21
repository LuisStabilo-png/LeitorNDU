# LeitorNDU

Automação em Python que lê um boletim em PDF e transforma as tabelas de jogos em uma planilha Excel.

O PDF de exemplo (`Boletim1415Março.pdf`) é um boletim de campeonato universitário de vôlei masculino (Série B, Grupos A e B). A tabela de jogos fica espalhada por várias páginas e traz dia, horário, local, grupo, equipes, placar em sets e os parciais de cada set. Digitar isso à mão é lento e dá erro; o script faz a extração.

## Como funciona

O script `extract_camelot.py`:

1. Percorre as páginas 141 a 145 do PDF.
2. Em cada página, usa o [Camelot](https://camelot-py.readthedocs.io/) (modo `stream`) para detectar as tabelas e escolhe a 3ª (ou a última, se houver menos de 3).
3. Usa a primeira linha como cabeçalho e remove o texto "Parciais:" das células.
4. Junta as páginas em um único DataFrame do Pandas e salva em `tabelaNDU.xlsx`.

## Como rodar

```bash
pip install -r requirements.txt
python extract_camelot.py
```

O PDF precisa estar na mesma pasta do script. Para usar outro boletim, altere `arquivo_pdf` e `paginas_alvo` no começo do arquivo.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `extract_camelot.py` | Script de extração |
| `Boletim1415Março.pdf` | Boletim de exemplo (entrada) |
| `tabela_pg141_extraida.csv` / `.xlsx` | Resultado da extração só da página 141 (primeiro teste) |
| `tabelaNDU.xlsx` | Resultado final, páginas 141 a 145 |

## Limitações

- Os parâmetros do Camelot e a escolha da "3ª tabela" foram ajustados para este boletim; outro layout exige novos ajustes.
- A extração em modo `stream` pode deixar colunas deslocadas ou células vazias, então a planilha ainda pede uma revisão rápida.
- Páginas e arquivo de saída estão fixos no código. Um próximo passo seria receber isso por linha de comando.
