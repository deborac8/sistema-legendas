# Sistema de Transcrição e Geração Automática de Legendas

Sistema local desenvolvido em Python para transcrição automática de áudio e vídeo, segmentação temporal e geração de legendas no formato SubRip (`.srt`).

O projeto utiliza modelos pré-treinados de reconhecimento de fala e uma arquitetura modular composta por Streamlit, FastAPI e um núcleo de processamento independente.

## 1. Objetivo

Desenvolver uma aplicação capaz de receber arquivos de áudio e vídeo, extrair o áudio quando necessário, reconhecer a fala, utilizar os timestamps fornecidos pelo modelo e gerar legendas sincronizadas.

O processamento prioriza ferramentas locais e modelos gratuitos, sem dependência obrigatória de APIs pagas.

## 2. Funcionalidades da versão atual

- Envio de arquivos de áudio e vídeo pela interface web.
- Identificação de informações técnicas da mídia.
- Extração de áudio utilizando FFmpeg.
- Preparação do áudio em WAV, mono e 16 kHz.
- Transcrição automática com Faster-Whisper.
- Detecção automática do idioma pelo modelo.
- Obtenção de timestamps por palavra.
- Utilização de VAD durante o reconhecimento.
- Segmentação em blocos de até duas linhas.
- Limite padrão de 42 caracteres por linha.
- Geração de arquivos SRT.
- Validação estrutural das legendas.
- Download do resultado pela interface web.

## 3. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal |
| Streamlit | Interface web |
| FastAPI | Backend e API |
| Faster-Whisper | Reconhecimento automático de fala |
| FFmpeg / FFprobe | Processamento de mídia |
| pysubs2 | Dependência para operações com legendas |
| pytest | Testes automatizados |
| jiwer | Métricas de avaliação |
| Matplotlib | Gráficos experimentais |

## 4. Arquitetura

O sistema está organizado em módulos independentes:

- **Frontend:** interface desenvolvida com Streamlit.
- **Backend:** API desenvolvida com FastAPI.
- **Core:** processamento de mídia, transcrição, segmentação e geração SRT.
- **Storage:** armazenamento de arquivos enviados, temporários, processados e resultados.
- **Experimentos:** scripts e resultados de avaliação dos modelos.
- **Tests:** testes automatizados.
- **Docs:** documentação técnica, avaliação experimental e fontes.

### Principais módulos

```text
backend/
    api/
        main.py
    services/
        transcription_service.py

core/
    media/
        processor.py
    models/
        transcriber.py
    subtitles/
        segmenter.py
        srt_writer.py

frontend/
experimentos/
docs/
storage/
tests/
```

## 5. Requisitos

- Windows 10 ou superior.
- Python instalado.
- FFmpeg e FFprobe instalados e disponíveis no PATH.
- Memória RAM e espaço em disco suficientes para os modelos escolhidos.
- Conexão com a internet na primeira obtenção dos modelos, caso ainda não estejam disponíveis localmente.

O desempenho depende do hardware, do tamanho do modelo e das características do arquivo processado.

## 6. Instalação

Clone o repositório:

```powershell
git clone URL_DO_REPOSITORIO
cd sistema_legendas
```

Crie um ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Atualize o instalador de pacotes:

```powershell
python -m pip install --upgrade pip
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Instale o FFmpeg e configure o PATH do Windows para que os comandos `ffmpeg` e `ffprobe` sejam reconhecidos.

## 7. Execução

### 7.1. Iniciar o backend

Abra um terminal PowerShell na raiz do projeto e execute:

```powershell
python -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000
```

A documentação interativa da API estará disponível em:

http://127.0.0.1:8000/docs

### 7.2. Iniciar a interface

Abra um segundo terminal PowerShell, ative o mesmo ambiente virtual e execute:

```powershell
streamlit run app.py
```

A interface estará disponível no endereço local informado pelo Streamlit, normalmente:

http://localhost:8501

### 7.3. Utilizar o sistema

1. Acesse a interface no navegador.
2. Selecione um arquivo de áudio ou vídeo compatível.
3. Envie o arquivo para processamento.
4. Aguarde a conclusão da transcrição.
5. Baixe o arquivo SRT gerado.
6. Abra o resultado em um editor de legendas para inspeção.

## 8. Testes automatizados

Para executar os testes:

```powershell
python -m pytest -v
```

Na versão documentada, existem 12 testes automatizados aprovados, concentrados nos módulos de segmentação e geração de arquivos SRT.

A cobertura dos demais módulos deverá ser ampliada nas próximas etapas.

## 9. Avaliação experimental

O projeto possui um script específico para avaliação de modelos:

```text
experimentos/avaliacao_modelos.py
```

Os resultados originais das execuções estão armazenados em:

```text
experimentos/resultados/
```

Foram avaliados experimentalmente os modelos Whisper Tiny e Base em CPU com int8, utilizando uma amostra de áudio e uma transcrição de referência.

Entre as métricas utilizadas estão:

- WER: taxa de erro por palavra.
- CER: taxa de erro por caractere.
- RTF: relação entre tempo de processamento e duração do áudio.
- Tempo de carregamento.
- Tempo de transcrição.
- Probabilidade média das palavras reconhecidas.

Os resultados, configurações, limitações e interpretações estão descritos em `docs/experiments/avaliacao.md`.

A reprodução dos experimentos depende da disponibilidade do áudio, da referência, das dependências Python e dos modelos utilizados.

## 10. Limitações conhecidas

A versão atual possui algumas limitações:

- A detecção automática de idioma não garante a identificação de cada mudança de idioma dentro de uma mesma mídia.
- Os timestamps são fornecidos pelo modelo de reconhecimento, não por um alinhador forçado independente.
- A tradução contextual ainda não está implementada.
- A geração de uma segunda legenda traduzida ainda não está implementada.
- A cobertura de testes automatizados ainda não abrange todos os módulos.
- O desempenho depende dos recursos computacionais disponíveis.

## 11. Próximas etapas

As próximas etapas deverão:

- Ampliar a capacidade multilíngue.
- Implementar a tradução contextual.
- Fortalecer a validação temporal.
- Aumentar a cobertura de testes.
- Preservar a rastreabilidade dos resultados e a possibilidade de reprodução experimental.
- Avaliar a criação de uma versão executável para Windows.

## 12. Documentação adicional

A documentação complementar está organizada em `docs/`.

Principais arquivos:

- `docs/architecture/especificação_tecnica.md`: especificação técnica e arquitetura.
- `docs/experiments/avaliacao.md`: avaliação dos modelos.
- `docs/experiments/fontes_e_licencas.md`: fontes utilizadas e informações de licenciamento.

## 13. Licenciamento e atribuição

Os materiais de terceiros utilizados na avaliação experimental devem manter suas respectivas atribuições e condições de licença.

Consulte `docs/experiments/fontes_e_licencas.md` antes de redistribuir materiais de referência.

## 14. Status do projeto

A versão atual implementa um fluxo funcional de transcrição automática, processamento local de mídia, segmentação temporal e geração de legendas SRT.

As funcionalidades planejadas estão identificadas separadamente para evitar confusão entre recursos disponíveis e melhorias futuras.
