
from core.models.transcriber import Transcriber
from core.subtitles.segmenter import segment_transcription


transcriber = Transcriber()

print("Transcrevendo áudio...")

result = transcriber.transcribe(
    "storage/processed/entrevista_01.wav"
)

print("Organizando legendas...")

subtitles = segment_transcription(result["segments"])

print("\nRESULTADO DA SEGMENTAÇÃO:\n")

for number, subtitle in enumerate(subtitles, start=1):
    print(f"{number}")
    print(
        f"{subtitle['start']:.3f} --> "
        f"{subtitle['end']:.3f}"
    )
    print(subtitle["text"])
    print()

    for line in subtitle["lines"]:
        if len(line) > 42:
            print("ERRO: linha ultrapassou 42 caracteres!")

    if len(subtitle["lines"]) > 2:
        print("ERRO: legenda ultrapassou duas linhas!")

print("TOTAL DE LEGENDAS:", len(subtitles))
print("TESTE DE SEGMENTAÇÃO CONCLUÍDO!")
