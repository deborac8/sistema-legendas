import pytest

from core.subtitles.srt_writer import (
    format_timestamp,
    generate_srt,
    save_srt,
)


def test_formats_timestamps():
    assert format_timestamp(0) == "00:00:00,000"
    assert format_timestamp(1.5) == "00:00:01,500"
    assert format_timestamp(3661.234) == "01:01:01,234"


def test_generates_srt_content():
    subtitles = [
        {
            "start": 0.0,
            "end": 1.5,
            "text": "Ol\u00e1 mundo!",
        },
        {
            "start": 2.0,
            "end": 3.75,
            "text": "Teste de legendas.",
        },
    ]

    expected = (
        "1\n"
        "00:00:00,000 --> 00:00:01,500\n"
        "Ol\u00e1 mundo!\n"
        "\n"
        "2\n"
        "00:00:02,000 --> 00:00:03,750\n"
        "Teste de legendas.\n"
    )

    assert generate_srt(subtitles) == expected


def test_saves_utf8_without_bom_and_creates_directory(tmp_path):
    subtitles = [{
        "start": 0.0,
        "end": 1.0,
        "text": "Ol\u00e1 mundo!",
    }]
    destination = tmp_path / "subfolder" / "teste.srt"

    saved_path = save_srt(subtitles, destination)
    content = saved_path.read_bytes()

    assert saved_path.is_file()
    assert content.decode("utf-8").startswith("1\n")
    assert not content.startswith(b"\xef\xbb\xbf")
    assert "\u00e1" in content.decode("utf-8")


def test_rejects_negative_start_time():
    subtitles = [{
        "start": -1.0,
        "end": 1.0,
        "text": "Teste",
    }]

    with pytest.raises(ValueError, match="Intervalo de tempo inv\u00e1lido"):
        generate_srt(subtitles)


def test_rejects_end_time_not_after_start():
    subtitles = [{
        "start": 1.0,
        "end": 1.0,
        "text": "Teste",
    }]

    with pytest.raises(ValueError, match="Intervalo de tempo inv\u00e1lido"):
        generate_srt(subtitles)


def test_rejects_more_than_two_lines():
    subtitles = [{
        "start": 0.0,
        "end": 2.0,
        "text": "Linha um\nLinha dois\nLinha tres",
    }]

    with pytest.raises(ValueError, match="mais de duas linhas"):
        generate_srt(subtitles)


def test_rejects_line_longer_than_42_characters():
    subtitles = [{
        "start": 0.0,
        "end": 2.0,
        "text": "A" * 43,
    }]

    with pytest.raises(ValueError, match="mais de 42 caracteres"):
        generate_srt(subtitles)
