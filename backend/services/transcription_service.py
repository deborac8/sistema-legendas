from datetime import datetime
from pathlib import Path

from core.media.processor import get_media_info, extract_audio
from core.models.transcriber import Transcriber
from core.subtitles.segmenter import segment_transcription
from core.subtitles.srt_writer import save_srt


def process_media(
    input_path: str | Path,
    model_size: str = "base",
) -> dict:
    """
    Executa o processamento completo de um arquivo de m?dia.

    Etapas:
    1. Analisa o arquivo de entrada.
    2. Extrai o ?udio em WAV.
    3. Transcreve com o Whisper.
    4. Segmenta a transcri??o em legendas.
    5. Gera o arquivo SRT.
    """
    source = Path(input_path)

    if not source.is_file():
        raise FileNotFoundError(
            f"Arquivo de m?dia n?o encontrado: {source}"
        )

    media_info = get_media_info(source)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    base_name = f"{source.stem}_{timestamp}"

    audio_path = (
        Path("storage/temporary") / f"{base_name}.wav"
    )

    subtitle_path = (
        Path("storage/results") / f"{base_name}.srt"
    )

    audio_path.parent.mkdir(parents=True, exist_ok=True)
    subtitle_path.parent.mkdir(parents=True, exist_ok=True)

    extract_audio(source, audio_path)

    transcriber = Transcriber(
        model_size=model_size,
        device="cpu",
        compute_type="int8",
    )

    transcription = transcriber.transcribe(audio_path)

    subtitles = segment_transcription(
        transcription["segments"]
    )

    save_srt(subtitles, subtitle_path)

    return {
        "input_file": str(source.resolve()),
        "media_info": media_info,
        "language": transcription["language"],
        "language_probability": transcription["language_probability"],
        "transcription": transcription,
        "subtitles": subtitles,
        "audio_path": str(audio_path.resolve()),
        "subtitle_path": str(subtitle_path.resolve()),
        "subtitle_count": len(subtitles),
    }
