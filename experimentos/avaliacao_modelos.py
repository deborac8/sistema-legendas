from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from jiwer import wer, cer


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.models.transcriber import Transcriber


DEFAULT_AUDIO = ROOT / "storage" / "processed" / "entrevista_01.wav"
DEFAULT_REFERENCE = (
    ROOT / "storage" / "evaluation" / "references" /
    "entrevista_01.txt"
)
RESULTS_DIR = ROOT / "experimentos" / "resultados"

MODELS = ["tiny", "base", "small"]


def normalize_text(text: str) -> str:
    """Normaliza caixa, espaços e pontuação, preservando acentos."""
    text = text.lower()
    text = "".join(
        char for char in text
        if not unicodedata.category(char).startswith("P")
    )
    return re.sub(r"\s+", " ", text).strip()


def count_words(segments: list[dict]) -> int:
    words = sum(
        len(segment.get("words", []))
        for segment in segments
    )
    if words:
        return words
    return sum(
        len(segment.get("text", "").split())
        for segment in segments
    )


def make_graph(rows: list[dict], field: str, title: str,
               ylabel: str, filename: Path) -> None:
    valid = [
        row for row in rows
        if row.get(field) is not None
    ]
    if not valid:
        return

    names = [row["model"] for row in valid]
    values = [row[field] for row in valid]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(names, values)
    plt.title(title)
    plt.xlabel("Modelo Whisper")
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.3)

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.3f}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def evaluate_model(
    model_size: str,
    audio_path: Path,
    device: str,
    compute_type: str,
) -> dict:
    print(f"\n{'=' * 55}")
    print(f"AVALIANDO MODELO: {model_size.upper()}")
    print(f"{'=' * 55}")

    transcriber = Transcriber(
        model_size=model_size,
        device=device,
        compute_type=compute_type,
    )

    start_load = time.perf_counter()
    transcriber.load_model()
    load_time = time.perf_counter() - start_load

    start_transcription = time.perf_counter()
    result = transcriber.transcribe(audio_path)
    transcription_time = time.perf_counter() - start_transcription

    duration = result["duration"]
    rtf = (
        transcription_time / duration
        if duration > 0 else None
    )

    segments = result["segments"]
    transcript = " ".join(
        segment["text"].strip()
        for segment in segments
    ).strip()

    probabilities = [
        word["probability"]
        for segment in segments
        for word in segment.get("words", [])
        if word.get("probability") is not None
    ]

    row = {
        "model": model_size,
        "device": device,
        "compute_type": compute_type,
        "audio_duration_seconds": duration,
        "model_load_seconds": load_time,
        "transcription_seconds": transcription_time,
        "rtf": rtf,
        "processing_speed": (
            duration / transcription_time
            if transcription_time > 0 else None
        ),
        "language_detected": result["language"],
        "language_probability": result["language_probability"],
        "segment_count": len(segments),
        "word_count": count_words(segments),
        "mean_word_probability": (
            mean(probabilities) if probabilities else None
        ),
        "transcript": transcript,
        "wer": None,
        "cer": None,
    }

    print(f"Idioma detectado: {row['language_detected']}")
    print(f"Tempo de carregamento: {load_time:.2f} s")
    print(f"Tempo de transcricao: {transcription_time:.2f} s")
    print(f"RTF: {rtf:.3f}" if rtf is not None else "RTF indisponivel")
    print(f"Palavras: {row['word_count']}")

    return row


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compara modelos Whisper e gera metricas e graficos."
    )
    parser.add_argument(
        "--audio",
        type=Path,
        default=DEFAULT_AUDIO,
        help="Arquivo WAV de entrada.",
    )
    parser.add_argument(
        "--reference",
        type=Path,
        default=DEFAULT_REFERENCE,
        help="Transcricao humana revisada em TXT.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=MODELS,
        choices=["tiny", "base", "small", "medium"],
        help="Modelos que serao comparados.",
    )
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--compute-type", default="int8")

    args = parser.parse_args()

    if not args.audio.is_file():
        raise SystemExit(
            f"Arquivo de audio nao encontrado: {args.audio}"
        )

    run_name = datetime.now().strftime("execucao_%Y%m%d_%H%M%S")
    output_dir = RESULTS_DIR / run_name
    output_dir.mkdir(parents=True, exist_ok=True)

    reference = None
    if args.reference.is_file():
        reference = normalize_text(
            args.reference.read_text(encoding="utf-8")
        )
        if not reference:
            print("Aviso: arquivo de referencia vazio. WER/CER nao serao calculados.")
            reference = None
    else:
        print(
            "Aviso: transcricao humana de referencia nao encontrada. "
            "WER/CER ficarao indisponiveis."
        )

    rows = []

    for model_size in args.models:
        try:
            row = evaluate_model(
                model_size,
                args.audio,
                args.device,
                args.compute_type,
            )

            if reference is not None:
                hypothesis = normalize_text(row["transcript"])
                row["wer"] = wer(reference, hypothesis)
                row["cer"] = cer(reference, hypothesis)
                print(f"WER: {row['wer']:.4f}")
                print(f"CER: {row['cer']:.4f}")

            rows.append(row)

        except Exception as error:
            print(f"Falha no modelo {model_size}: {error}")

    if not rows:
        raise SystemExit("Nenhum modelo foi avaliado com sucesso.")

    csv_path = output_dir / "metricas.csv"
    json_path = output_dir / "resultados.json"

    columns = [
        "model",
        "device",
        "compute_type",
        "audio_duration_seconds",
        "model_load_seconds",
        "transcription_seconds",
        "rtf",
        "processing_speed",
        "language_detected",
        "language_probability",
        "segment_count",
        "word_count",
        "mean_word_probability",
        "wer",
        "cer",
        "transcript",
    ]

    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    make_graph(
        rows, "transcription_seconds",
        "Tempo de transcricao por modelo",
        "Tempo (segundos)",
        output_dir / "tempo_transcricao.png",
    )
    make_graph(
        rows, "model_load_seconds",
        "Tempo de carregamento por modelo",
        "Tempo (segundos)",
        output_dir / "tempo_carregamento.png",
    )
    make_graph(
        rows, "rtf",
        "Real Time Factor (RTF) por modelo",
        "RTF",
        output_dir / "rtf.png",
    )
    make_graph(
        rows, "wer",
        "Word Error Rate (WER) por modelo",
        "WER",
        output_dir / "wer.png",
    )
    make_graph(
        rows, "cer",
        "Character Error Rate (CER) por modelo",
        "CER",
        output_dir / "cer.png",
    )

    print(f"\nResultados salvos em: {output_dir}")
    print(f"CSV: {csv_path.name}")
    print(f"JSON: {json_path.name}")
    print("Avaliacao concluida.")


if __name__ == "__main__":
    main()
