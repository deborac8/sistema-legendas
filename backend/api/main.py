from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from backend.services.transcription_service import process_media


app = FastAPI(
    title="Sistema Automatizado de Legendas",
    description="API local para reconhecimento de fala e geração de legendas.",
    version="1.0.0",
)


UPLOAD_DIR = Path("storage/uploads")
RESULTS_DIR = Path("storage/results").resolve()

ALLOWED_EXTENSIONS = {
    ".mp3", ".wav", ".m4a", ".ogg", ".flac",
    ".mp4", ".mkv", ".mov", ".webm", ".avi",
}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Verifica se a API está funcionando."""
    return {
        "status": "online",
        "message": "API do Sistema de Legendas funcionando corretamente.",
    }


@app.post("/process")
def process_upload(file: UploadFile = File(...)) -> dict:
    """Recebe uma mídia e gera legendas no formato SRT."""
    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Formato de arquivo não suportado.",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = f"{uuid4().hex}{extension}"
    input_path = UPLOAD_DIR / safe_name

    try:
        with input_path.open("wb") as destination:
            while chunk := file.file.read(1024 * 1024):
                destination.write(chunk)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Falha no upload do arquivo: {error}",
        ) from error

    try:
        result = process_media(input_path, model_size="tiny")
        subtitle_filename = Path(result["subtitle_path"]).name

        return {
            "status": "success",
            "filename": file.filename,
            "language": result["language"],
            "subtitle_count": result["subtitle_count"],
            "subtitle_path": result["subtitle_path"],
            "audio_path": result["audio_path"],
            "download_url": f"/download/{subtitle_filename}",
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Falha no processamento: {error}",
        ) from error

    finally:
        file.file.close()


@app.get("/download/{filename}")
def download_subtitle(filename: str):
    """Disponibiliza o arquivo SRT para download."""
    if Path(filename).name != filename or not filename.lower().endswith(".srt"):
        raise HTTPException(
            status_code=400,
            detail="Nome de arquivo inválido.",
        )

    file_path = (RESULTS_DIR / filename).resolve()

    if file_path.parent != RESULTS_DIR or not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Arquivo de legenda não encontrado.",
        )

    return FileResponse(
        path=file_path,
        media_type="application/x-subrip",
        filename=filename,
    )