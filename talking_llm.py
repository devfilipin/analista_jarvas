import openai  # Importa a biblioteca OpenAI para interagir com os modelos de linguagem da OpenAI
from dotenv import load_dotenv, find_dotenv  # Importa funções para carregar variáveis de ambiente de um arquivo .env
from pynput import keyboard  # Importa a biblioteca pynput para monitorar eventos de teclado
import sounddevice as sd  # Importa a biblioteca sounddevice para gravar e reproduzir áudio
import wave  # Importa a biblioteca wave para manipular arquivos WAV
import os  # Importa a biblioteca os para interagir com o sistema operacional
import numpy as np  # Importa a biblioteca NumPy para manipulação de arrays numéricos
import whisper  # Importa a biblioteca Whisper para transcrição de áudio
from langchain_openai import ChatOpenAI  # Importa a classe ChatOpenAI do módulo langchain_openai
from queue import Queue  # Importa a classe Queue para manipulação de filas
import io  # Importa o módulo io para manipulação de streams de entrada e saída
import soundfile as sf  # Importa a biblioteca soundfile para manipulação de arquivos de áudio
import threading  # Importa a biblioteca threading para execução de tarefas em paralelo
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent  # Importa função para criar agentes que interagem com dataframes pandas
import pandas as pd  # Importa a biblioteca pandas para manipulação de dataframes
from langchain.agents.agent_types import AgentType  # Importa a enumeração AgentType para especificar o tipo de agente

# Carrega variáveis de ambiente de um arquivo .env
load_dotenv(find_dotenv())

# Inicializa o cliente da OpenAI
client = openai.Client()

class TalkingLLM():
    def __init__(self, model="gpt-3.5-turbo-0613", whisper_size="small"):
        self.is_recording = False  # Inicializa o estado de gravação como False
        self.audio_data = []  # Inicializa a lista para armazenar dados de áudio
        self.samplerate = 44100  # Define a taxa de amostragem do áudio
        self.channels = 1  # Define o número de canais do áudio (1 para mono)
        self.dtype = 'int16'  # Define o tipo de dados do áudio
        self.display_callback = None  # Inicializa o callback para atualização da GUI como None

        # Carrega o modelo Whisper para transcrição de áudio
        self.whisper = whisper.load_model(whisper_size)
        # Inicializa o modelo de linguagem ChatOpenAI
        self.llm = ChatOpenAI(model=model)
        # Inicializa a fila para armazenamento de respostas para TTS
        self.llm_queue = Queue()
        # Cria o agente para interagir com o dataframe
        self.create_agent()

        # Inicia a thread para conversão de texto em fala e reprodução do áudio
        threading.Thread(target=self.convert_and_play, daemon=True).start()

    def set_display_callback(self, callback):
        # Define o callback para atualizar a GUI com as respostas
        self.display_callback = callback

    def start_or_stop_recording(self):
        # Alterna o estado de gravação e chama a função apropriada
        if self.is_recording:
            self.is_recording = False
            self.save_and_transcribe()  # Salva e transcreve o áudio quando a gravação é interrompida
            self.audio_data = []  # Reseta os dados de áudio
        else:
            print("Starting record")
            self.audio_data = []  # Reseta os dados de áudio
            self.is_recording = True

    def create_agent(self, df_path="df_rent.csv"):
        # Define o prefixo do prompt do agente
        agent_prompt_prefix = """
            Você se chama Jarvas, e está trabalhando com dataframe pandas no Python. O nome do Dataframe é `df`.
        """

        try:
            # Carrega o dataframe a partir de um arquivo CSV
            df = pd.read_csv(df_path)
        except FileNotFoundError:
            print("Arquivo df_rent.csv não encontrado.")
            return

        # Cria um agente para interagir com o dataframe usando o modelo de linguagem
        self.agent = create_pandas_dataframe_agent(
            self.llm,
            df,
            prefix=agent_prompt_prefix,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

    def load_new_dataframe(self, df_path):
        # Carrega um novo dataframe e atualiza o agente
        self.create_agent(df_path)

    def save_and_transcribe(self):
        print("Saving the recording...")
        if "test.wav" in os.listdir():
            os.remove("test.wav")  # Remove qualquer arquivo de teste anterior
        # Abre um novo arquivo WAV para escrita
        wav_file = wave.open("test.wav", 'wb')
        wav_file.setnchannels(self.channels)  # Define o número de canais
        wav_file.setsampwidth(2)  # Define a largura de amostra (bytes por amostra)
        wav_file.setframerate(self.samplerate)  # Define a taxa de amostragem
        # Escreve os dados de áudio no arquivo
        wav_file.writeframes(np.array(self.audio_data, dtype=self.dtype))
        wav_file.close()  # Fecha o arquivo WAV

        try:
            # Transcreve o áudio usando o modelo Whisper
            result = self.whisper.transcribe("test.wav", fp16=False)
            user_text = result["text"]  # Obtém o texto transcrito
            print("Usuário:", user_text)

            # Obtém a resposta do agente para o texto transcrito
            response = self.agent.invoke(user_text)
            jarvas_response = response['output']  # Obtém a resposta do agente
            print("AI:", jarvas_response)
            self.llm_queue.put(jarvas_response)  # Adiciona a resposta à fila de TTS

            # Chama o callback para atualizar a GUI, se definido
            if self.display_callback:
                self.display_callback(user_text, jarvas_response)
        except FileNotFoundError as e:
            print(f"Erro: {e}. Certifique-se de que o FFmpeg está instalado e no PATH do sistema.")

    def convert_and_play(self):
        tts_text = ''
        while True:
            tts_text += self.llm_queue.get()  # Obtém a próxima resposta da fila

            if '.' in tts_text or '?' in tts_text or '!' in tts_text:
                print(tts_text)
                
                # Converte o texto em fala usando a API da OpenAI
                spoken_response = client.audio.speech.create(model="tts-1",
                                                             voice='alloy', 
                                                             response_format="opus",
                                                             input=tts_text)

                buffer = io.BytesIO()
                for chunk in spoken_response.iter_bytes(chunk_size=4096):
                    buffer.write(chunk)  # Escreve os dados de áudio no buffer
                buffer.seek(0)

                # Reproduz o áudio usando a biblioteca soundfile e sounddevice
                with sf.SoundFile(buffer, 'r') as sound_file:
                    data = sound_file.read(dtype='int16')
                    sd.play(data, sound_file.samplerate)
                    sd.wait()
                tts_text = ''  # Reseta o texto TTS

    def start_recording_thread(self):
        # Inicia a thread de gravação
        threading.Thread(target=self.run_recording, daemon=True).start()

    def run_recording(self):
        def callback(indata, frame_count, time_info, status):
            if self.is_recording:
                self.audio_data.extend(indata.copy())  # Armazena os dados de áudio gravados

        # Configura o stream de entrada de áudio
        with sd.InputStream(samplerate=self.samplerate, 
                            channels=self.channels, 
                            dtype=self.dtype, 
                            callback=callback):
            def on_activate():
                self.start_or_stop_recording()  # Alterna a gravação quando a tecla é pressionada

            def for_canonical(f):
                return lambda k: f(l.canonical(k))

            # Configura o hotkey para iniciar/parar a gravação
            hotkey = keyboard.HotKey(
                keyboard.HotKey.parse('<cmd>'),
                on_activate)
            with keyboard.Listener(
                    on_press=for_canonical(hotkey.press),
                    on_release=for_canonical(hotkey.release)) as l:
                l.join()  # Inicia o listener de teclado

if __name__ == "__main__":
    talking_llm = TalkingLLM()
    talking_llm.start_recording_thread()  # Inicia a thread de gravação
