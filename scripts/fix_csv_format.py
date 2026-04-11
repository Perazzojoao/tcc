#!/usr/bin/env python3
"""Cria uma copia formatada de um CSV com delimitador inadequado para visualizacao.

Uso:
  python scripts/fix_csv_format.py "data/data set.csv"
  python scripts/fix_csv_format.py "data/data set.csv" -o "data/data_set_corrigido.csv"
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

POSSIBLE_DELIMITERS = [";", ",", "\t", "|"]


def detect_delimiter(input_path: Path) -> str:
    """Detecta delimitador com fallback para ';' se o sniffer falhar."""
    sample = input_path.read_text(encoding="utf-8", errors="replace")[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters="".join(POSSIBLE_DELIMITERS))
        return dialect.delimiter
    except csv.Error:
        return ";"


def build_default_output_path(input_path: Path) -> Path:
    stem = input_path.stem.replace(" ", "_")
    return input_path.with_name(f"{stem}_formatted.csv")


def convert_to_comma_csv(input_path: Path, output_path: Path) -> tuple[int, int]:
    delimiter = detect_delimiter(input_path)

    rows_written = 0
    with (
        input_path.open("r", encoding="utf-8", errors="replace", newline="") as src,
        output_path.open("w", encoding="utf-8", newline="") as dst,
    ):
        reader = csv.reader(src, delimiter=delimiter)
        writer = csv.writer(dst, delimiter=",", quoting=csv.QUOTE_MINIMAL)

        expected_cols = None
        for row in reader:
            if expected_cols is None:
                expected_cols = len(row)
            elif len(row) != expected_cols:
                raise ValueError(
                    f"Linha com numero de colunas inconsistente. Esperado: {expected_cols}, recebido: {len(row)}"
                )
            writer.writerow(row)
            rows_written += 1

    return rows_written, expected_cols or 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cria uma copia do CSV com delimitador virgula para abrir corretamente em visualizadores tabulares."
    )
    parser.add_argument("input", type=Path, help="Caminho do arquivo CSV original")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Caminho do arquivo de saida (padrao: <nome>_formatted.csv no mesmo diretorio)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = args.input
    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {input_path}")

    output_path = args.output or build_default_output_path(input_path)
    if output_path.resolve() == input_path.resolve():
        raise ValueError("O arquivo de saida deve ser diferente do arquivo de entrada")

    rows_written, columns = convert_to_comma_csv(input_path, output_path)
    print(f"Arquivo corrigido criado: {output_path}")
    print(f"Linhas gravadas: {rows_written}")
    print(f"Colunas por linha: {columns}")


if __name__ == "__main__":
    main()
