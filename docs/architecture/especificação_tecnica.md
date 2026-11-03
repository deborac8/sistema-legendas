# Especificação Técnica — Sistema de Transcrição e Geração Automática de Legendas

## 1. Identificação do projeto

**Nome provisório:** Sistema de Transcrição e Geração Automática de Legendas

**Linguagem principal:** Python

**Plataforma atual:** Aplicação web local

**Plataforma futura:** Aplicativo executável para Windows (`.exe`)

**Interface:** Streamlit

**Backend:** FastAPI

**Motor de processamento:** Python (Core)

**Formato de exportação:** SubRip (`.srt`)

**Modelo de reconhecimento:** Faster-Whisper, baseado em modelos Whisper pré-treinados

## 2. Objetivo geral

Desenvolver um sistema capaz de receber arquivos de áudio e vídeo, realizar o reconhecimento automático de fala, obter informações temporais das palavras reconhecidas, organizar o texto em blocos de legenda e gerar arquivos sincronizados em formato SRT.

O projeto prioriza o processamento local, a utilização de modelos pré-treinados, a modularidade do código e a compatibilidade dos arquivos gerados com programas especializados de edição de legendas.

A arquitetura também prevê futuras funcionalidades, como identificação de alternância entre idiomas, tradução das transcrições e geração de uma segunda legenda em idioma escolhido pelo usuário.

Essas funcionalidades futuras serão incorporadas e validadas separadamente, sem serem consideradas concluídas enquanto não estiverem implementadas e testadas.

## 3. Escopo e situação das funcionalidades

Para manter a documentação coerente com o código, as funcionalidades são classificadas em quatro categorias:

- **Implementado:** funcionalidade presente no código e disponível na versão atual.
- **Implementado parcialmente:** existe uma implementação, mas sua abrangência ou comportamento ainda possui limitações.
- **Planejado:** funcionalidade prevista para uma versão futura.
- **Não validado:** funcionalidade que depende de testes específicos antes de ser considerada comprovada.

### 3.1. Funcionalidades implementadas

- Recebimento de arquivos de áudio e vídeo pela interface Streamlit.
- Comunicação entre frontend e backend por meio de HTTP.
- Processamento de solicitações com FastAPI.
- Identificação de informações técnicas dos arquivos de mídia com FFmpeg e FFprobe.
- Extração de áudio de arquivos de vídeo.
- Preparação de áudio em WAV, mono e 16 kHz.
- Reconhecimento automático de fala com Faster-Whisper.
- Detecção automática de idioma pelo modelo.
- Obtenção de timestamps por palavra fornecidos pelo Whisper.
- Utilização de VAD durante a transcrição.
- Segmentação do texto em blocos de legenda.
- Limite de até duas linhas por bloco.
- Limite padrão de 42 caracteres por linha.
- Geração de arquivos SRT.
- Validação estrutural dos arquivos SRT.
- Disponibilização dos resultados para download pela interface.

### 3.2. Funcionalidades implementadas parcialmente ou com limitações

- **Detecção de idioma:** o modelo realiza detecção automática, mas isso não comprova a identificação independente de todos os idiomas presentes em um arquivo com alternância de falas.
- **Alinhamento temporal:** o Faster-Whisper fornece timestamps de palavras. A versão atual utiliza essas informações, mas não possui um módulo independente de alinhamento forçado.
- **Validação SRT:** existem verificações estruturais e temporais. A correção automática de qualquer tipo de inconsistência não está garantida.
- **Testes automatizados:** existem testes aprovados para segmentação e geração SRT, mas ainda não há cobertura automatizada completa de todos os módulos.

### 3.3. Funcionalidades planejadas

- Reconhecimento mais específico de trechos com alternância entre idiomas.
- Tradução contextual da transcrição para um idioma escolhido pelo usuário.
- Geração de um segundo arquivo SRT traduzido.
- Preservação da correspondência temporal entre a legenda original e a traduzida.
- Módulo independente de alinhamento temporal, caso os requisitos futuros justifiquem sua inclusão.
- Ampliação da cobertura de testes automatizados.
- Empacotamento do sistema em um aplicativo executável para Windows.

## 4. Fluxo de funcionamento da versão atual

### 4.1. Recebimento do arquivo

O usuário seleciona e envia um arquivo de áudio ou vídeo pela interface web.

A aplicação verifica a extensão permitida e encaminha o arquivo ao backend para processamento.

Os formatos aceitos pela aplicação incluem:

- Áudio: MP3, WAV, M4A, OGG e FLAC.
- Vídeo: MP4, MKV, MOV, WEBM e AVI.

A compatibilidade efetiva também depende da integridade do arquivo e dos recursos disponíveis no FFmpeg.

### 4.2. Identificação das características da mídia

O módulo de processamento de mídia utiliza FFmpeg e FFprobe para obter informações técnicas do arquivo.

São consideradas informações como duração, presença de áudio e vídeo e características necessárias à preparação do processamento.

### 4.3. Extração e preparação do áudio

Quando o arquivo recebido é um vídeo, o sistema extrai sua faixa de áudio.

O áudio é preparado em formato adequado ao reconhecimento de fala, utilizando WAV, canal mono e taxa de amostragem de 16 kHz.

A preparação deve preservar a referência temporal necessária para relacionar a transcrição ao arquivo original.

### 4.4. Reconhecimento automático de fala

O módulo de transcrição utiliza Faster-Whisper com modelos Whisper pré-treinados.

A configuração empregada na aplicação atual utiliza o modelo Tiny, execução em CPU e tipo de computação int8.

O processo inclui:

- Detecção automática do idioma.
- Reconhecimento do conteúdo falado.
- Obtenção dos segmentos de transcrição.
- Obtenção dos timestamps das palavras.
- Estimativas de probabilidade associadas às palavras.
- Utilização de VAD para auxiliar a identificação de trechos com fala.

A detecção automática de idioma não deve ser interpretada como identificação garantida de cada mudança de idioma dentro do mesmo arquivo.

### 4.5. Organização temporal

O sistema utiliza os tempos de início e término das palavras retornados pelo modelo.

Essas informações são utilizadas pelo módulo de segmentação para organizar o texto em blocos de legenda.

A versão atual não implementa um alinhador forçado independente. Portanto, a precisão temporal depende do comportamento e das estimativas do modelo de reconhecimento.

### 4.6. Segmentação das legendas

O módulo de segmentação organiza as palavras reconhecidas em blocos de legenda.

Os critérios incluem:

- Máximo de duas linhas por bloco.
- Limite padrão de 42 caracteres por linha.
- Preservação da integridade das palavras.
- Organização textual para facilitar a leitura.
- Utilização dos timestamps das palavras para determinar os intervalos dos blocos.

A implementação não deve inserir durações mínimas ou máximas artificiais de exibição sem justificativa técnica.

### 4.7. Geração do arquivo SRT

O módulo de escrita gera o arquivo SubRip com numeração sequencial, intervalos temporais e texto segmentado.

Os arquivos são armazenados na área de resultados e disponibilizados para download pela interface.

### 4.8. Validação

Antes da disponibilização, a estrutura do arquivo SRT deve ser verificada de acordo com as regras implementadas.

Inconsistências identificadas devem ser sinalizadas e corrigidas quando possível. Quando a correção não for possível, a limitação deve ser documentada, preservando os dados originais e evitando conclusões sem sustentação.

## 5. Requisitos técnicos de processamento

### 5.1. Arquivos de entrada

A aplicação atual aceita arquivos de áudio e vídeo nos formatos definidos na implementação.

A validação considera a extensão permitida e a possibilidade de processamento pela infraestrutura de mídia.

A arquitetura poderá ser ampliada para verificações adicionais de integridade, duração, resolução e características das faixas de áudio e vídeo.

### 5.2. Processamento de mídia

O FFmpeg e o FFprobe são utilizados para operações de mídia.

As responsabilidades atuais incluem:

- Obtenção de informações técnicas.
- Extração da faixa de áudio.
- Conversão para formato adequado ao reconhecimento.
- Preservação da referência temporal utilizada pelo processamento.

Tratamentos adicionais de deslocamento temporal e sincronização de fluxos deverão ser validados em testes específicos antes de serem considerados garantidos.

### 5.3. Preparação do áudio

A preparação do áudio utiliza:

- Formato WAV.
- Taxa de amostragem de 16 kHz.
- Canal mono.
- Codificação PCM de 16 bits, conforme a rotina de extração implementada.

Normalizações e ajustes adicionais de volume não devem ser aplicados sem justificativa técnica e avaliação de seus efeitos no reconhecimento.

### 5.4. Detecção de atividade vocal

O reconhecimento utiliza a opção de VAD disponibilizada pelo Faster-Whisper.

Essa funcionalidade auxilia a identificação de trechos com fala e períodos de silêncio.

Sua utilização não garante, por si só, a preservação de toda fala baixa ou palavra curta. Esse comportamento deve ser avaliado em amostras específicas.

### 5.5. Reconhecimento automático de fala

O reconhecimento é realizado localmente por modelos pré-treinados.

A arquitetura permite configurar o tamanho do modelo e os parâmetros de execução.

A escolha do modelo deve considerar:

- Qualidade da transcrição.
- Idiomas suportados.
- Memória disponível.
- Tempo de carregamento.
- Tempo de processamento.
- Relação entre qualidade e custo computacional.

A versão atual utiliza o modelo Tiny no fluxo da aplicação. Modelos de outros tamanhos podem ser avaliados experimentalmente, respeitando os recursos disponíveis no computador.

### 5.6. Informações temporais

Os timestamps retornados pelo modelo são utilizados para estabelecer os intervalos das palavras e dos blocos de legenda.

Os valores devem ser mantidos com precisão suficiente durante o processamento e convertidos para milissegundos na geração do SRT.

A qualidade dos tempos depende da estimativa fornecida pelo modelo e deve ser avaliada com áudio e referência adequados.

## 6. Arquitetura de software

O projeto utiliza uma arquitetura modular para separar a interface, a comunicação com o backend e os mecanismos de processamento.

### 6.1. Frontend — Streamlit

Responsável pela interação com o usuário.

Funções implementadas:

- Receber arquivos de áudio e vídeo.
- Encaminhar solicitações ao backend.
- Apresentar mensagens de processamento e erro.
- Exibir informações sobre o resultado.
- Disponibilizar o arquivo SRT para download.

A seleção de idioma de destino e a disponibilização de uma segunda legenda traduzida pertencem ao escopo futuro.

### 6.2. Backend — FastAPI

Responsável por receber solicitações e coordenar o processamento.

Rotas implementadas:

- `/health`: verificação de disponibilidade do serviço.
- `/process`: recebimento e processamento de arquivos.
- `/download/{filename}`: disponibilização dos arquivos gerados.

O backend encaminha o arquivo ao serviço de transcrição e organiza o retorno dos resultados.

### 6.3. Core — Núcleo de processamento

Concentra os mecanismos independentes da interface.

Os módulos atuais incluem:

- `core/media/processor.py`: identificação de informações da mídia e extração de áudio.
- `core/models/transcriber.py`: reconhecimento automático de fala com Faster-Whisper.
- `core/subtitles/segmenter.py`: segmentação do texto em blocos de legenda.
- `core/subtitles/srt_writer.py`: geração e validação dos arquivos SRT.

O Core não deve depender diretamente de Streamlit ou FastAPI, permitindo reutilização em outras interfaces.

### 6.4. Storage — Gerenciamento de arquivos

Organiza os arquivos utilizados durante o processamento.

A estrutura atual separa:

- `storage/uploads/`: arquivos enviados.
- `storage/temporary/`: arquivos temporários.
- `storage/processed/`: mídias processadas.
- `storage/results/`: resultados gerados.
- `storage/evaluation/`: arquivos de referência e materiais de avaliação experimental.

Arquivos temporários e resultados locais devem ser tratados adequadamente na preparação de uma distribuição do projeto.

### 6.5. Config — Configurações

A estrutura prevê um espaço para centralização de configurações gerais.

A implementação futura poderá concentrar parâmetros de processamento, caminhos de arquivos, seleção de modelos e preferências técnicas.

### 6.6. Tests — Testes automatizados

Os testes automatizados verificam o comportamento dos módulos implementados.

Na versão documentada, existem 12 testes aprovados, concentrados nos módulos de segmentação e geração de arquivos SRT.

A ampliação da cobertura deverá incluir:

- Processamento de mídia.
- Extração de áudio.
- Reconhecimento de fala.
- Rotas da API.
- Tratamento de erros.
- Validação dos resultados.
- Integração entre os módulos.

Testes de tradução e alinhamento independente serão adicionados quando essas funcionalidades forem implementadas.

### 6.7. Docs — Documentação

Armazena especificações técnicas, decisões arquiteturais, avaliações experimentais, fontes e licenças e instruções de utilização.

### 6.8. Independência entre plataformas

A separação do Core em relação à interface permite planejar a reutilização do processamento em outras plataformas.

A futura versão executável para Windows deverá reutilizar os mesmos módulos de processamento, evitando duplicação de regras e algoritmos.

## 7. Padrão de exportação e compatibilidade SRT

### 7.1. Formato de saída

A versão atual utiliza o formato SubRip (`.srt`) para exportação.

O resultado disponibilizado é a legenda da transcrição original.

A geração de uma segunda legenda traduzida está planejada e não faz parte das funcionalidades concluídas nesta versão.

### 7.2. Estrutura dos blocos

Cada bloco SRT contém:

1. Numeração sequencial.
2. Tempo inicial e final.
3. Texto da legenda.
4. Linha em branco separando o bloco seguinte.

### 7.3. Formato temporal

Os tempos seguem o padrão:

`HH:MM:SS,mmm --> HH:MM:SS,mmm`

Os valores representam os intervalos relativos à referência temporal da mídia processada.

### 7.4. Codificação e caracteres

Os arquivos utilizam codificação UTF-8, preferencialmente sem BOM.

Devem ser preservados:

- Acentos.
- Caracteres especiais.
- Pontuação.
- Caracteres de diferentes idiomas.

### 7.5. Organização textual

A segmentação respeita os critérios implementados:

- Máximo de duas linhas por bloco.
- Limite padrão de 42 caracteres por linha.
- Preservação da integridade das palavras.
- Organização textual para facilitar a leitura.
- Numeração sequencial.

### 7.6. Integridade temporal e estrutural

A validação deve verificar, conforme as regras implementadas:

- Validade dos tempos.
- Tempo final posterior ao inicial.
- Organização cronológica dos blocos.
- Estrutura dos blocos.
- Limites de linhas e caracteres.
- Numeração sequencial.

A ausência de uma inconsistência na validação estrutural não comprova, isoladamente, a precisão da transcrição ou a sincronização perfeita com o áudio.

### 7.7. Compatibilidade com programas externos

Os arquivos SRT podem ser utilizados em programas especializados, como:

- Subtitle Edit.
- Aegisub.

A compatibilidade deve ser verificada por importação e inspeção dos tempos, caracteres, quebras de linha e correspondência com a mídia original.

### 7.8. Tratamento de inconsistências

Arquivos que apresentarem inconsistências deverão ser sinalizados e corrigidos quando possível, antes de serem considerados resultados concluídos.

Quando a correção não for possível, a limitação deverá ser documentada.

Os dados originais e os resultados experimentais devem ser preservados para permitir rastreabilidade e reprodução.

## 8. Avaliação experimental

A avaliação dos modelos de reconhecimento é realizada separadamente do fluxo principal da aplicação.

O projeto utiliza métricas como:

- WER (Word Error Rate): taxa de erro por palavra.
- CER (Character Error Rate): taxa de erro por caractere.
- RTF (Real-Time Factor): relação entre tempo de processamento e duração do áudio.
- Tempo de carregamento do modelo.
- Tempo de transcrição.
- Probabilidade média das palavras reconhecidas.

Os resultados devem ser interpretados considerando a qualidade da transcrição de referência, as condições do áudio, os parâmetros de execução e as limitações do equipamento.

As execuções experimentais e seus resultados estão documentados em `experimentos/` e `docs/experiments/`.

Uma amostra isolada não deve ser utilizada para afirmar desempenho geral de um modelo em todos os idiomas e condições acústicas.

## 9. Limitações conhecidas

A versão atual possui as seguintes limitações:

- A detecção automática de idioma não comprova a identificação de cada mudança de idioma dentro de uma mídia.
- Os timestamps são estimativas do modelo de reconhecimento, não resultados de um alinhador forçado independente.
- A tradução contextual ainda não está implementada.
- A geração de duas legendas independentes ainda não está implementada.
- A cobertura de testes automatizados ainda não abrange todos os módulos.
- O desempenho depende dos recursos computacionais disponíveis.
- A reprodução de experimentos depende da disponibilidade do áudio, das referências, das dependências e dos modelos utilizados.

Essas limitações deverão ser consideradas na apresentação dos resultados e no planejamento das próximas etapas.

## 10. Critérios de conclusão da versão atual

A versão atual poderá ser considerada funcional dentro do escopo implementado quando:

- A interface receber arquivos compatíveis.
- O backend receber e encaminhar corretamente as solicitações.
- O processamento de mídia identificar as características necessárias.
- O áudio puder ser extraído e preparado.
- O modelo realizar a transcrição.
- Os timestamps retornados pelo modelo forem utilizados na segmentação.
- Os blocos respeitarem os limites definidos.
- O arquivo SRT for gerado e validado estruturalmente.
- O usuário conseguir baixar o resultado.
- Os testes automatizados existentes forem executados e aprovados.
- As limitações e inconsistências conhecidas estiverem documentadas.

Funcionalidades planejadas somente poderão ser promovidas à categoria de implementadas depois de incorporadas ao código e verificadas por testes apropriados.

## 11. Considerações finais

A arquitetura foi concebida para permitir evolução gradual, mantendo a separação entre interface, backend, núcleo de processamento e armazenamento.

A versão atual estabelece uma base funcional para reconhecimento automático de fala, segmentação temporal e geração de legendas SRT.

As próximas etapas deverão ampliar a capacidade multilíngue, implementar a tradução contextual, fortalecer a validação temporal e aumentar a cobertura de testes, sempre preservando a rastreabilidade dos resultados e a possibilidade de reprodução experimental.