
from pathlib import Path
from faster_whisper import WhisperModel


class TranscriptionError(Exception):
    """Erro durante o reconhecimento de fala."""


class Transcriber:
    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def load_model(self):
        """Carrega o modelo Whisper localmente."""
        if self.model is not None:
            return

        try:
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )
        except Exception as error:
            raise TranscriptionError(
                f"Não foi possível carregar o modelo: {error}"
            ) from error

    def transcribe(self, audio_path: str | Path) -> dict:
        """Transcreve o áudio e retorna segmentos e palavras."""
        path = Path(audio_path)

        if not path.is_file():
            raise TranscriptionError(
                f"Arquivo de áudio não encontrado: {path}"
            )

        self.load_model()

        try:
            segments, info = self.model.transcribe(
                str(path),
                language=None,
                task="transcribe",
                beam_size=5,
                word_timestamps=True,
                vad_filter=True,
                condition_on_previous_text=True,
            )

            results = []

            for segment in segments:
                words = []

                if segment.words:
                    for word in segment.words:
                        words.append({
                            "start": float(word.start),
                            "end": float(word.end),
                            "text": word.word,
                            "probability": float(word.probability),
                        })

                results.append({
                    "start": float(segment.start),
                    "end": float(segment.end),
                    "text": segment.text.strip(),
                    "words": words,
                })

            return {
                "language": info.language,
                "language_probability": float(
                    info.language_probability
                ),
                "duration": float(info.duration),
                "segments": results,
            }

        except Exception as error:
            raise TranscriptionError(
                f"Falha durante a transcrição: {error}"
            ) from error
