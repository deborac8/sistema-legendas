
from core.models.transcriber import Transcriber

print("Iniciando transcrição...")

transcriber = Transcriber()

result = transcriber.transcribe(
    "storage/processed/entrevista_01.wav"
)

print("\nIDIOMA:", result["language"])
print("CONFIANÇA:", round(result["language_probability"], 3))
print("DURAÇÃO:", round(result["duration"], 2), "segundos")

print("\nTRANSCRIÇÃO:")

for segment in result["segments"]:
    print(
        f"[{segment['start']:.2f} - {segment['end']:.2f}] "
        f"{segment['text']}"
    )

print("\nTOTAL DE SEGMENTOS:", len(result["segments"]))

total_words = sum(
    len(segment["words"])
    for segment in result["segments"]
)

print("TOTAL DE PALAVRAS:", total_words)
print("\nTESTE CONCLUÍDO!")
