```markdown
# Jarvas - Assistente de Voz

Jarvas é um assistente de voz inteligente desenvolvido em Python que utiliza a API da OpenAI.
Ele permite que você interaja com seus dados de forma fácil e intuitiva.
Com o Jarvas, você pode usar comandos de voz ou texto para fazer perguntas e obter respostas sobre os dados que você
carrega no sistema.

Imagine poder conversar com seu computador para analisar uma planilha de dados, sem precisar escrever códigos complicados.
Jarvas escuta seus comandos de voz, os transcreve para texto, processa a solicitação usando a API da OpenAI e fornece uma
resposta imediata.
Ele pode ler arquivos CSV, responder perguntas sobre os dados e até mesmo falar as respostas para você.

### Principais Funcionalidades:
- Interação por Voz: Fale com Jarvas para fazer perguntas sobre seus dados.
- Interação por Texto: Digite perguntas diretamente na interface gráfica.
- Análise de Dados: Carregue arquivos CSV e obtenha respostas inteligentes sobre seus dados.
- Geração de Gráficos: Gere gráficos de barras para visualizar a relação entre duas colunas de dados.

### Exemplos de Uso:
- Perguntar sobre o número de linhas em uma tabela de dados.
- Calcular a média de uma coluna de preços.
- Identificar possíveis anomalias em um conjunto de dados.
- Gerar um gráfico de barras para visualizar a relação entre duas colunas.

## Requisitos

- Python 3.7+
- FFmpeg

## Instruções de Instalação

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/devfilipin/analista_jarvas.git
cd analista_jarvas
```

### Passo 2: Crie um Ambiente Virtual

Crie e ative um ambiente virtual para o projeto:

```bash
python -m venv .venv
# No Windows
.venv\Scripts\activate
# No MacOS/Linux
source .venv/bin/activate
```

### Passo 3: Instale as Dependências

Instale as dependências necessárias a partir do arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Passo 4: Instale o FFmpeg

#### Windows

1. Baixe o FFmpeg de [ffmpeg.org](https://ffmpeg.org/download.html).
2. Extraia o conteúdo do arquivo zip em um diretório, por exemplo, `C:\ffmpeg`.
3. Adicione o caminho `C:\ffmpeg\bin` às variáveis de ambiente do sistema.

#### MacOS

Use Homebrew para instalar o FFmpeg:

```bash
brew install ffmpeg
```

#### Linux

Use o gerenciador de pacotes do seu sistema para instalar o FFmpeg. Por exemplo, no Ubuntu:

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### Passo 5: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais da OpenAI. O arquivo `.env` deve conter:

```
OPENAI_API_KEY='seu_token_openai_aqui'
```

### Passo 6: Execute o Projeto

Execute a interface gráfica do Jarvas:

```bash
python talking_llm_gui.py
```

## Uso

1. **Carregar um Arquivo CSV**: Use o botão "Carregar CSV" para selecionar um arquivo CSV.
2. **Gravar Comandos de Voz**: Use o botão "Gravar" para iniciar e parar a gravação de comandos de voz.
3. **Enviar Comandos de Texto**: Digite comandos na caixa de entrada e pressione Enter para enviar.

## Estrutura do Projeto

```
.
├── .env.example            # Exemplo de arquivo .env
├── README.md               # Este arquivo
├── requirements.txt        # Dependências do projeto
├── talking_llm.py          # Código principal do assistente de voz
├── talking_llm_gui.py      # Interface gráfica do assistente de voz
└── df_rent.csv             # Exemplo de arquivo CSV (se necessário)
```

## Contribuição

Sinta-se à vontade para contribuir com o projeto através de pull requests. Antes de começar, por favor, abra uma issue para discutir o que você gostaria de mudar.
