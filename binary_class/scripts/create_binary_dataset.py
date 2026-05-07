#!/usr/bin/env python3
"""Gera uma versao binaria do dataset a partir de CLASSI_FIN.

Regras de transformacao:
- remove linhas com CLASSI_FIN == 1 (CHIKUNGUNYA)
- remapeia CLASSI_FIN == 2 para 1 (DENGUE)
- mantem CLASSI_FIN == 0 (OUTRAS_DOENCAS)

Uso (padrao recomendado):
  python3 binary_class/scripts/create_binary_dataset.py

Uso com caminhos explicitos:
  python3 binary_class/scripts/create_binary_dataset.py \
      --input binary_class/data/data_set_final_multiclass.csv \
      --output binary_class/data/data_set_final.csv
"""

from __future__ import annotations

import argparse
import csv
import os
import tempfile
from collections import Counter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT_DIR / "binary_class" / "data" / "data_set_final_multiclass.csv"
DEFAULT_OUTPUT = ROOT_DIR / "binary_class" / "data" / "data_set_final.csv"
TARGET_COL = "CLASSI_FIN"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cria dataset binario removendo CHIKUNGUNYA e remapeando DENGUE.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"CSV de entrada (padrao: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"CSV de saida (padrao: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


def normalize_class(value: str) -> int:
    text = (value or "").strip()
    try:
        return int(float(text))
    except ValueError as exc:
        raise ValueError(f"Valor invalido em {TARGET_COL}: {value!r}") from exc


def validate_multiclass_origin(before_counts: Counter) -> None:
    has_class_2 = before_counts.get(2, 0) > 0
    has_class_1 = before_counts.get(1, 0) > 0

    if (not has_class_2) and has_class_1:
        raise ValueError(
            "Entrada parece ja estar em formato binario (ha classe 1 e nao ha classe 2). "
            "Use como entrada a base multiclasse codificada, por exemplo: "
            "binary_class/data/data_set_final_multiclass.csv."
        )


def create_binary_dataset(input_path: Path, output_path: Path) -> tuple[Counter, Counter, int]:
    before_counts: Counter = Counter()
    after_counts: Counter = Counter()
    removed_rows = 0

    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_fd, temp_name = tempfile.mkstemp(
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        dir=output_path.parent,
        text=True,
    )
    os.close(temp_fd)
    temp_path = Path(temp_name)

    try:
        with (
            input_path.open("r", encoding="utf-8", errors="replace", newline="") as src,
            temp_path.open("w", encoding="utf-8", newline="") as dst,
        ):
            reader = csv.DictReader(src)
            if reader.fieldnames is None:
                raise ValueError("Arquivo CSV vazio ou sem cabecalho")
            if TARGET_COL not in reader.fieldnames:
                raise ValueError(f"Coluna obrigatoria ausente: {TARGET_COL}")

            writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                class_value = normalize_class(row[TARGET_COL])
                before_counts[class_value] += 1

                if class_value == 1:
                    removed_rows += 1
                    continue

                if class_value == 2:
                    row[TARGET_COL] = "1"
                    after_counts[1] += 1
                elif class_value == 0:
                    row[TARGET_COL] = "0"
                    after_counts[0] += 1
                else:
                    raise ValueError(
                        f"Valor inesperado em {TARGET_COL}: {class_value}. "
                        "Esperado apenas 0, 1 ou 2."
                    )

                writer.writerow(row)

        validate_multiclass_origin(before_counts)
        os.replace(temp_path, output_path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise

    return before_counts, after_counts, removed_rows


def format_counts(counts: Counter) -> str:
    if not counts:
        return "(sem registros)"
    keys = sorted(counts.keys())
    return ", ".join(f"{key}: {counts[key]}" for key in keys)


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo de entrada nao encontrado: {input_path}")
    if input_path == output_path:
        raise ValueError("Entrada e saida devem ser arquivos diferentes")

    before_counts, after_counts, removed_rows = create_binary_dataset(input_path, output_path)

    print(f"Entrada: {input_path}")
    print(f"Saida:   {output_path}")
    print(f"Contagens antes ({TARGET_COL}): {format_counts(before_counts)}")
    print(f"Contagens depois ({TARGET_COL}): {format_counts(after_counts)}")
    print(f"Linhas removidas (CHIKUNGUNYA=1): {removed_rows}")
    print(f"Linhas finais gravadas: {sum(after_counts.values())}")


if __name__ == "__main__":
    main()
