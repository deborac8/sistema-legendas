
from core.models.transcriber import Transcriber
from core.subtitles.segmenter import segment_transcription
from core.subtitles.srt_writer import save_srt


print("Iniciando transcrição...")

transcriber = Transcriber()

result = transcriber.transcribe(
    "storage/processed/entrevista_01.wav"
)

print("Organizando legendas...")

subtitles = segment_transcription(result["segments"])

print("Gerando arquivo SRT...")

output = save_srt(
    subtitles,
    "storage/results/entrevista_01.srt",
)

print("\nARQUIVO GERADO:", output)
print("TOTAL DE LEGENDAS:", len(subtitles))
print("IDIOMA:", result["language"])
print("\nTESTE CONCLUÍDO!")
