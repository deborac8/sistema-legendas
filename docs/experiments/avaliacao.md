# Avaliação Experimental dos Modelos de Reconhecimento de Fala

## 1. Objetivo

Avaliar o desempenho dos modelos pré-treinados Whisper Tiny e Whisper Base na tarefa de reconhecimento automático de fala (ASR), considerando precisão da transcrição e velocidade de processamento.

O experimento também registra a tentativa de execução do modelo Whisper Small e a limitação de memória encontrada.

## 2. Ambiente experimental

- Linguagem: Python
- Biblioteca de reconhecimento: faster-whisper
- Dispositivo: CPU
- Tipo de computação: int8
- Modelos avaliados: Whisper Tiny e Whisper Base
- Áudio de referência: Edward Snowden
- Duração do áudio: 53,291 segundos
- Idioma detectado: inglês (en)

Os modelos foram executados com configurações de transcrição equivalentes:

- Detecção automática de idioma.
- Tarefa de transcrição.
- beam_size = 5.
- word_timestamps = True.
- vad_filter = True.
- condition_on_previous_text = True.

Os modelos são pré-treinados. Portanto, este experimento avalia inferência, e não treinamento de épocas.

## 3. Dados de referência

Foi utilizada uma legenda em inglês disponibilizada no Wikimedia Commons como referência para comparação.

O arquivo de texto simples foi derivado da legenda para permitir o cálculo das métricas.

A referência possui aproximadamente 119 palavras após a preparação utilizada no experimento.

A fonte, os colaboradores e as informações de licenciamento estão documentados em:

[Fontes de dados e licenças](fontes_e_licencas.md)

A referência é material de terceiros e não foi transcrita pelo desenvolvedor.

## 4. Métricas utilizadas

### 4.1 Word Error Rate (WER)

O WER mede a proporção de erros de palavras em relação à transcrição de referência.

Considera substituições, inserções e exclusões de palavras.

Quanto menor o WER, maior a correspondência entre a transcrição gerada e a referência.

### 4.2 Character Error Rate (CER)

O CER mede a proporção de erros de caracteres em relação ao texto de referência.

Quanto menor o CER, maior a correspondência em nível de caracteres.

### 4.3 Real Time Factor (RTF)

O RTF relaciona o tempo de processamento à duração do áudio.

Valores abaixo de 1 indicam processamento mais rápido que o tempo real.

### 4.4 Velocidade de processamento

Expressa quantas vezes o processamento foi mais rápido que a duração do áudio.

### 4.5 Probabilidade média das palavras

Representa a média das probabilidades associadas às palavras reconhecidas pelo modelo.

É uma estimativa interna de confiança e não deve ser interpretada como uma medida direta de acurácia.

## 5. Resultados quantitativos

| Métrica | Whisper Tiny | Whisper Base |
|---|---:|---:|
| Dispositivo | CPU | CPU |
| Computação | int8 | int8 |
| Duração do áudio | 53,291 s | 53,291 s |
| Carregamento do modelo | 9,086 s | 9,931 s |
| Tempo de transcrição | 6,134 s | 10,850 s |
| RTF | 0,1151 | 0,2036 |
| Velocidade de processamento | 8,69x | 4,91x |
| Idioma detectado | Inglês | Inglês |
| Probabilidade do idioma | 0,9843 | 0,9661 |
| Quantidade de segmentos | 9 | 4 |
| Quantidade de palavras | 123 | 122 |
| Probabilidade média das palavras | 0,8087 | 0,8860 |
| WER | 15,97% | 10,08% |
| CER | 7,05% | 4,32% |

## 6. Análise comparativa

### 6.1 Precisão

O Whisper Base apresentou menores taxas de erro nesta amostra.

O WER foi reduzido de aproximadamente 15,97% no Tiny para 10,08% no Base.

O CER foi reduzido de aproximadamente 7,05% para 4,32%.

A diferença representa uma redução de aproximadamente 5,88 pontos percentuais no WER e 2,73 pontos percentuais no CER.

### 6.2 Velocidade

O Whisper Tiny apresentou tempo de transcrição de aproximadamente 6,13 segundos, enquanto o Base levou aproximadamente 10,85 segundos.

O Tiny apresentou velocidade de processamento de aproximadamente 8,69 vezes o tempo real, contra 4,91 vezes no Base.

Portanto, nesta execução, o Tiny apresentou menor custo de tempo de inferência.

### 6.3 Segmentação

O Tiny produziu 9 segmentos, enquanto o Base produziu 4.

Essa diferença mostra que os modelos organizaram a transcrição em quantidades distintas de segmentos.

A quantidade de segmentos, isoladamente, não representa maior precisão ou melhor qualidade das legendas.

### 6.4 Confiança

O Base apresentou probabilidade média das palavras de aproximadamente 0,8860, enquanto o Tiny apresentou aproximadamente 0,8087.

Esses valores representam estimativas internas dos modelos e não substituem a avaliação por WER e CER.

## 7. Tentativa de avaliação do Whisper Small

Foi realizada uma tentativa de execução do modelo Whisper Small.

A execução apresentou erro de alocação de memória:

`mkl_malloc: failed to allocate memory`

Por esse motivo, não foram obtidos resultados válidos de transcrição, WER ou CER para o Small.

A ocorrência foi registrada como limitação do ambiente computacional utilizado.

Não foram atribuídas métricas fictícias ao modelo.

## 8. Limitações experimentais

A avaliação possui limitações importantes:

1. Foi utilizada apenas uma amostra de áudio.
2. A duração do áudio foi de aproximadamente 53 segundos.
3. A qualidade da transcrição de referência influencia diretamente WER e CER.
4. A legenda de referência é material de terceiros.
5. O equipamento utilizado possui limitações de memória.
6. Os resultados representam uma execução experimental e não uma avaliação estatística de várias amostras.

Consequentemente, os resultados não devem ser generalizados para todos os idiomas, sotaques, condições acústicas ou durações de áudio.

## 9. Conclusão

Na amostra avaliada, o Whisper Tiny apresentou maior velocidade de processamento, enquanto o Whisper Base apresentou menores taxas de erro.

O Tiny pode ser considerado em cenários nos quais a velocidade de processamento é uma prioridade.

O Base apresentou melhor correspondência com a referência utilizada neste experimento, embora tenha exigido mais tempo de inferência.

A escolha entre os modelos depende, portanto, do equilíbrio desejado entre velocidade e precisão.

Para conclusões mais abrangentes, será necessário avaliar outros áudios, diferentes condições acústicas e mais amostras de referência.

## 10. Reprodutibilidade

Os resultados originais estão armazenados em:

- `experimentos/resultados/execucao_20261103_115625/`
- `experimentos/resultados/execucao_20261103_115737/`

Cada diretório contém métricas em CSV, resultados em JSON e gráficos da execução.

O script responsável pela avaliação está em:

`experimentos/avaliacao_modelos.py`

A reprodução depende da disponibilidade do áudio, da referência, das dependências Python e dos modelos pré-treinados utilizados.
