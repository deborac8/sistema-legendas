
from pathlib import Path
import json
import shutil
import subprocess


class MediaProcessingError(Exception):
    """Erro durante a análise ou conversão de um arquivo de mídia."""


def _find_executable(name: str) -> str:
    """Localiza um executável no PATH do sistema."""
    executable = shutil.which(name)

    if executable is None:
        raise MediaProcessingError(
            f"{name} não foi encontrado. Verifique a instalação do FFmpeg "
            "e se a pasta bin está no PATH."
        )

    return executable


def get_media_info(file_path: str | Path) -> dict:
    """Obtém informações do arquivo usando o FFprobe."""
    path = Path(file_path)

    if not path.is_file():
        raise MediaProcessingError(f"Arquivo não encontrado: {path}")

    ffprobe = _find_executable("ffprobe")

    command = [
        ffprobe,
        "-v", "error",
        "-show_format",
        "-show_streams",
        "-of", "json",
        str(path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise MediaProcessingError(
            f"Não foi possível analisar o arquivo: {result.stderr}"
        )

    try:
        info = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise MediaProcessingError(
            f"Falha ao decodificar a saída do FFprobe: {error}"
        )
    streams = info.get("streams", [])
    audio_streams = [
        stream for stream in streams
        if stream.get("codec_type") == "audio"
    ]
    video_streams = [
        stream for stream in streams
        if stream.get("codec_type") == "video"
    ]

    if not audio_streams:
        raise MediaProcessingError(
            "O arquivo não contém uma faixa de áudio."
        )

    duration = info.get("format", {}).get("duration")

    return {
        "path": str(path.resolve()),
        "duration": float(duration) if duration else None,
        "has_audio": bool(audio_streams),
        "has_video": bool(video_streams),
        "audio_streams": audio_streams,
        "video_streams": video_streams,
        "format": info.get("format", {}),
    }


def extract_audio(
    input_path: str | Path,
    output_path: str | Path,
) -> Path:
    """
    Extrai o áudio para WAV mono, 16 kHz, PCM 16 bits.

    Essa configuração será usada como entrada do modelo de transcrição.
    """
    source = Path(input_path)
    destination = Path(output_path)

    if not source.is_file():
        raise MediaProcessingError(
            f"Arquivo de entrada não encontrado: {source}"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg = _find_executable("ffmpeg")

    command = [
        ffmpeg,
        "-y",
        "-i", str(source),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        str(destination),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise MediaProcessingError(
            f"Falha ao extrair o áudio: {result.stderr}"
        )

    if not destination.is_file() or destination.stat().st_size == 0:
        raise MediaProcessingError(
            "O FFmpeg não gerou um arquivo de áudio válido."
        )

    return destination.resolve()
