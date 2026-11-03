
import re

MAX_LINES = 2
MAX_CHARS_PER_LINE = 42


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def segment_transcription(segments: list[dict]) -> list[dict]:
    """
    Organiza palavras em legendas de até duas linhas.

    Usa os timestamps individuais das palavras para calcular
    o intervalo real de cada legenda.
    """
    subtitles = []

    for segment in segments:
        words = segment.get("words", [])

        if not words:
            raise ValueError(
                "Segmento sem timestamps de palavras. "
                "Não é possível dividir a fala com precisão."
            )

        current_lines = []
        current_line = ""
        cue_words = []

        def finish_cue():
            nonlocal current_lines, current_line, cue_words

            if not cue_words:
                return

            lines = current_lines + (
                [current_line] if current_line else []
            )

            subtitles.append({
                "start": float(cue_words[0]["start"]),
                "end": float(cue_words[-1]["end"]),
                "text": "\n".join(lines),
                "lines": lines,
            })

            current_lines = []
            current_line = ""
            cue_words = []

        for word in words:
            token = word["text"].strip()

            if not token:
                continue

            if len(token) > MAX_CHARS_PER_LINE:
                raise ValueError(
                    f"Palavra maior que {MAX_CHARS_PER_LINE} "
                    f"caracteres: {token}"
                )

            candidate = (
                f"{current_line} {token}".strip()
                if current_line else token
            )

            if len(candidate) <= MAX_CHARS_PER_LINE:
                current_line = candidate
                cue_words.append(word)
                continue

            if len(current_lines) < MAX_LINES - 1:
                current_lines.append(current_line)
                current_line = token
                cue_words.append(word)
            else:
                finish_cue()
                current_line = token
                cue_words.append(word)

        finish_cue()

    return subtitles
