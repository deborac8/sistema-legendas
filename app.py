import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Sistema Automatizado de Legendas",
    page_icon="🎬",
    layout="wide",
)


st.title("🎬 Sistema Automatizado de Legendas")

st.write(
    "Envie um arquivo de áudio ou vídeo para gerar "
    "legendas automaticamente."
)

st.divider()


uploaded_file = st.file_uploader(
    "Selecione um arquivo de áudio ou vídeo",
    type=[
        "mp3", "wav", "m4a", "ogg", "flac",
        "mp4", "mkv", "mov", "webm", "avi",
    ],
)


if uploaded_file is not None:

    st.success(f"Arquivo selecionado: {uploaded_file.name}")

    if st.button("Gerar legendas", type="primary"):

        with st.spinner(
            "Processando mídia... Aguarde."
        ):

            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type or "application/octet-stream",
                    )
                }

                response = requests.post(
                    f"{API_URL}/process",
                    files=files,
                    timeout=(10, 3600),
                )

                response.raise_for_status()

                result = response.json()

                st.success("Legendas geradas com sucesso!")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Idioma detectado",
                        result["language"].upper(),
                    )

                with col2:
                    st.metric(
                        "Quantidade de legendas",
                        result["subtitle_count"],
                    )

                download_url = (
                    API_URL + result["download_url"]
                )

                subtitle_response = requests.get(
                    download_url,
                    timeout=60,
                )

                subtitle_response.raise_for_status()

                st.download_button(
                    label="⬇️ Baixar legendas (.srt)",
                    data=subtitle_response.content,
                    file_name=(
                        result["download_url"].split("/")[-1]
                    ),
                    mime="application/x-subrip",
                )

            except requests.exceptions.RequestException as error:
                st.error(f"Erro na comunicação com a API: {error}")

                if error.response is not None:
                    st.code(error.response.text)

            except Exception as error:
                st.error(
                    f"Erro durante o processamento: {error}"
                )


st.divider()

st.caption(
    "Sistema Automatizado de Legendas — "
    "Reconhecimento de fala e geração de arquivos SRT."
)