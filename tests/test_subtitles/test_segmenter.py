import pytest

from core.subtitles.segmenter import segment_transcription


def make_word(start, text):
    return {
        "start": start,
        "end": start + 0.3,
        "text": text,
    }


def test_combines_words_and_preserves_timestamps():
    words = [
        make_word(0.0, "Ol\u00e1"),
        make_word(0.3, "mundo!"),
    ]

    result = segment_transcription([{"words": words}])

    assert len(result) == 1
    assert result[0]["text"] == "Ol\u00e1 mundo!"
    assert result[0]["start"] == 0.0
    assert result[0]["end"] == 0.6


def test_respects_line_and_character_limits():
    texts = [
        "Esta", "e\u0301", "uma", "legenda", "com", "mais",
        "de", "quarenta", "caracteres", "adicionais", "aqui",
    ]
    words = [
        make_word(index * 0.3, text)
        for index, text in enumerate(texts)
    ]

    result = segment_transcription([{"words": words}])

    assert result
    for subtitle in result:
        assert len(subtitle["lines"]) <= 2
        assert all(len(line) <= 42 for line in subtitle["lines"])

    reconstructed = " ".join(
        line for subtitle in result for line in subtitle["lines"]
    )
    assert reconstructed == " ".join(texts)


def test_preserves_unicode_exactly():
    text = "Ol\u00e1"
    result = segment_transcription([{
        "words": [make_word(0.0, text)]
    }])

    assert result[0]["text"] == text


def test_rejects_word_longer_than_42_characters():
    words = [make_word(0.0, "A" * 43)]

    with pytest.raises(ValueError, match="maior que 42"):
        segment_transcription([{"words": words}])


def test_rejects_segment_without_word_timestamps():
    with pytest.raises(ValueError, match="sem timestamps"):
        segment_transcription([{"words": []}])
