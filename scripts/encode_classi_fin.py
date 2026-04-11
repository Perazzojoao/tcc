#!/usr/bin/env python3
"""Cria uma copia do CSV com a coluna CLASSI_FIN codificada.

Mapeamento aplicado:
  - CHIKUNGUNYA -> 1
    - DENGUE -> 2
    - OUTRAS_DOENCAS -> 0

Uso:
  python scripts/encode_classi_fin.py "data/data_set_formatted.csv"
    python scripts/encode_classi_fin.py "data/data_set_formatted.csv" -o "data/data_set_final.csv"
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

CLASSIFICATION_MAP = {
    "CHIKUNGUNYA": "1",
    "DENGUE": "2",
    "OUTRAS_DOENCAS": "0",
}


def build_default_output_path(input_path: Path) -> Path:
    return input_path.with_name("data_set_final.csv")


def normalize_label(value: str) -> str:
    return value.strip().upper()


def encode_classification(input_path: Path, output_path: Path) -> tuple[int, int]:
    rows_written = 0

    with (
        input_path.open("r", encoding="utf-8", errors="replace", newline="") as src,
        output_path.open("w", encoding="utf-8", newline="") as dst,
    ):
        reader = csv.DictReader(src)
        if reader.fieldnames is None:
            raise ValueError("Arquivo CSV vazio ou sem cabecalho")
        if "CLASSI_FIN" not in reader.fieldnames:
            raise ValueError("Coluna CLASSI_FIN nao encontrada no CSV")

        writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)
        writer.writeheader()

        unknown_labels = set()
        for row_index, row in enumerate(reader, start=2):
            raw_value = (row.get("CLASSI_FIN") or "").strip()
            normalized = normalize_label(raw_value)

            if normalized not in CLASSIFICATION_MAP:
                unknown_labels.add(normalized or "<vazio>")
            else:
                row["CLASSI_FIN"] = CLASSIFICATION_MAP[normalized]

            writer.writerow(row)
            rows_written += 1

    if unknown_labels:
        labels = ", ".join(sorted(unknown_labels))
        raise ValueError(
            "Foram encontrados valores sem mapeamento em CLASSI_FIN: "
            f"{labels}. Atualize CLASSIFICATION_MAP e execute novamente."
        )

    return rows_written, len(reader.fieldnames)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cria uma copia do CSV trocando CLASSI_FIN por codigos numericos."
    )
    parser.add_argument("input", type=Path, help="Caminho do CSV de entrada")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Caminho do CSV de saida (padrao: data_set_final.csv no mesmo diretorio)",
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

    rows_written, columns = encode_classification(input_path, output_path)
    print(f"Arquivo codificado criado: {output_path}")
    print(f"Linhas gravadas: {rows_written}")
    print(f"Colunas por linha: {columns}")


if __name__ == "__main__":
    main()
