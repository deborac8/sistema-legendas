
from pathlib import Path


def format_timestamp(seconds: float) -> str:
    """Converte segundos para HH:MM:SS,mmm."""
    total_ms = round(seconds * 1000)

    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds_part, milliseconds = divmod(remainder, 1000)

    return (
        f"{hours:02d}:{minutes:02d}:"
        f"{seconds_part:02d},{milliseconds:03d}"
    )


def generate_srt(subtitles: list[dict]) -> str:
    """Gera o conteúdo textual de um arquivo SRT."""
    blocks = []

    for number, subtitle in enumerate(subtitles, start=1):
        start = float(subtitle["start"])
        end = float(subtitle["end"])
        text = subtitle["text"].strip()

        if start < 0 or end <= start:
            raise ValueError(
                f"Intervalo de tempo inválido na legenda {number}."
            )

        if not text:
            continue

        lines = text.splitlines()

        if len(lines) > 2:
            raise ValueError(
                f"Legenda {number} possui mais de duas linhas."
            )

        if any(len(line) > 42 for line in lines):
            raise ValueError(
                f"Legenda {number} possui linha com mais de 42 caracteres."
            )

        block = (
            f"{number}\n"
            f"{format_timestamp(start)} --> "
            f"{format_timestamp(end)}\n"
            f"{text}"
        )

        blocks.append(block)

    return "\n\n".join(blocks) + ("\n" if blocks else "")


def save_srt(
    subtitles: list[dict],
    output_path: str | Path,
) -> Path:
    """Salva o SRT em UTF-8 sem BOM."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    content = generate_srt(subtitles)

    destination.write_text(
        content,
        encoding="utf-8",
        newline="\n",
    )

    return destination.resolve()
