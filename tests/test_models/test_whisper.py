
from pathlib import Path
from faster_whisper import WhisperModel
from time import perf_counter
from statistics import mean


def main():
    audio_path = Path("storage/processed/diego_audio.wav")

    if not audio_path.exists():
        print(f"Arquivo não encontrado: {audio_path}")
        return

    # 1. Carregamento do modelo
    print("Carregando Faster-Whisper...")
    load_start = perf_counter()

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8",
    )

    load_time = perf_counter() - load_start

    print(f"Modelo carregado em {load_time:.2f} segundos")

    # 2. Transcrição
    print("\nIniciando transcrição...\n")
    transcription_start = perf_counter()

    segments, info = model.transcribe(
        str(audio_path),
        language=None,
        beam_size=5,
        vad_filter=True,
        word_timestamps=True,
        multilingual=True,
    )

    all_segments = []
    all_word_probabilities = []

    total_words = 0
    total_speech_duration = 0.0

    # 3. Processamento dos segmentos
    print("TRANSCRIÇÃO:\n")

    for segment in segments:
        words = segment.words or []

        word_count = len(words) if words else len(segment.text.split())
        duration = segment.end - segment.start

        total_words += word_count
        total_speech_duration += duration

        for word in words:
            if word.probability is not None:
                all_word_probabilities.append(word.probability)

        all_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
            "words": word_count,
            "duration": duration,
            "avg_logprob": segment.avg_logprob,
            "no_speech_prob": segment.no_speech_prob,
            "compression_ratio": segment.compression_ratio,
        })

        print(
            f"[{segment.start:.2f}s - {segment.end:.2f}s] "
            f"{segment.text.strip()}"
        )

    transcription_time = perf_counter() - transcription_start

    # 4. Métricas gerais
    audio_duration = info.duration
    rtf = transcription_time / audio_duration if audio_duration else 0
    processing_speed = (
        audio_duration / transcription_time
        if transcription_time > 0 else 0
    )

    avg_word_probability = (
        mean(all_word_probabilities)
        if all_word_probabilities else None
    )

    avg_logprob = mean(
        item["avg_logprob"] for item in all_segments
    ) if all_segments else None

    avg_no_speech = mean(
        item["no_speech_prob"] for item in all_segments
    ) if all_segments else None

    avg_compression = mean(
        item["compression_ratio"] for item in all_segments
    ) if all_segments else None

    # 5. Relatório
    print("\n" + "=" * 55)
    print("RELATÓRIO DE RECONHECIMENTO")
    print("=" * 55)

    print("\nIDENTIFICAÇÃO")
    print("Idioma inicial detectado:", info.language)
    print("Probabilidade do idioma inicial:",
          round(info.language_probability, 3))
    print("Modelo: small")
    print("Dispositivo: CPU")
    print("Precisão computacional: int8")

    print("\nVOLUME DE TRANSCRIÇÃO")
    print("Duração do áudio:", round(audio_duration, 2), "segundos")
    print("Total de segmentos:", len(all_segments))
    print("Total de palavras:", total_words)
    print("Tempo total de fala nos segmentos:",
          round(total_speech_duration, 2), "segundos")

    print("\nDESEMPENHO")
    print("Tempo de carregamento:", round(load_time, 2), "segundos")
    print("Tempo de transcrição:",
          round(transcription_time, 2), "segundos")
    print("RTF:", round(rtf, 3))
    print("Velocidade relativa:",
          round(processing_speed, 2), "x tempo real")

    print("\nINDICADORES DE QUALIDADE")

    if avg_word_probability is not None:
        print("Probabilidade média das palavras:",
              round(avg_word_probability, 3))
    else:
        print("Probabilidade das palavras: indisponível")

    if avg_logprob is not None:
        print("Log probability médio:", round(avg_logprob, 3))

    if avg_no_speech is not None:
        print("Probabilidade média de ausência de fala:",
              round(avg_no_speech, 3))

    if avg_compression is not None:
        print("Compression ratio médio:",
              round(avg_compression, 3))

    print("\n" + "=" * 55)
    print("ANÁLISE INDIVIDUAL DOS SEGMENTOS")
    print("=" * 55)

    for index, item in enumerate(all_segments, start=1):
        print(f"\nSegmento {index}")
        print(f"Tempo: {item['start']:.2f}s - {item['end']:.2f}s")
        print(f"Palavras: {item['words']}")
        print(f"Duração: {item['duration']:.2f}s")
        print(f"Log probability: {item['avg_logprob']:.3f}")
        print(f"No-speech probability: {item['no_speech_prob']:.3f}")
        print(f"Compression ratio: {item['compression_ratio']:.3f}")


if __name__ == "__main__":
    main()
