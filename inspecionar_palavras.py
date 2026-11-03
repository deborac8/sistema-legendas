
from core.models.transcriber import Transcriber

transcriber = Transcriber()

result = transcriber.transcribe(
    "storage/processed/entrevista_01.wav"
)

for segment in result["segments"][:2]:
    print("\nSEGMENTO:")
    print("Início:", segment["start"])
    print("Fim:", segment["end"])

    print("\nTEMPOS DAS PALAVRAS:")

    for word in segment["words"]:
        print(
            f"{word['start']:.3f} --> "
            f"{word['end']:.3f} | {word['text']}"
        )
