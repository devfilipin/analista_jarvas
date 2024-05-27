import tkinter as tk  # Importa a biblioteca Tkinter para criar a interface gráfica
from tkinter import scrolledtext, filedialog, messagebox  # Importa componentes específicos do Tkinter
import threading  # Importa a biblioteca de threading para permitir execução paralela
from talking_llm import TalkingLLM  # Importa a classe TalkingLLM do módulo talking_llm

class JarvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvas - Assistente de Voz")  # Define o título da janela

        self.talking_llm = TalkingLLM()  # Instancia a classe TalkingLLM
        self.talking_llm.set_display_callback(self.display_response)  # Define o callback para atualizar a GUI

        # Cria uma área de texto rolável para exibir as conversas
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15, font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10)

        # Cria um campo de entrada de texto para o usuário digitar mensagens
        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", self.send_text)  # Define o evento de pressionar Enter para enviar texto

        # Cria um botão para gravar áudio
        self.record_button = tk.Button(root, text="Gravar", command=self.toggle_recording, font=("Arial", 14))
        self.record_button.pack(pady=10)

        # Cria um botão para carregar um novo arquivo CSV
        self.load_file_button = tk.Button(root, text="Carregar CSV", command=self.load_file, font=("Arial", 14))
        self.load_file_button.pack(pady=10)

        self.is_recording = False  # Inicializa o estado de gravação como False

        # Inicia a thread de gravação
        self.talking_llm.start_recording_thread()

    def toggle_recording(self):
        # Alterna o estado de gravação e atualiza o texto do botão
        if self.is_recording:
            self.is_recording = False
            self.record_button.config(text="Gravar")
        else:
            self.is_recording = True
            self.record_button.config(text="Parar")
        self.talking_llm.start_or_stop_recording()  # Chama o método para iniciar ou parar a gravação

    def send_text(self, event):
        user_input = self.entry.get()  # Obtém o texto do campo de entrada
        self.text_area.insert(tk.END, "Você: " + user_input + "\n")  # Insere o texto do usuário na área de texto
        self.entry.delete(0, tk.END)  # Limpa o campo de entrada
        response = self.talking_llm.agent.invoke(user_input)  # Obtém a resposta do agente
        self.text_area.insert(tk.END, "Jarvas: " + response['output'] + "\n")  # Insere a resposta do Jarvas na área de texto
        self.talking_llm.llm_queue.put(response['output'])  # Adiciona a resposta à fila de TTS

    def load_file(self):
        # Abre um diálogo para selecionar um arquivo CSV
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.talking_llm.load_new_dataframe(file_path)  # Carrega o novo dataframe
                messagebox.showinfo("Sucesso", f"Arquivo {file_path} carregado com sucesso!")  # Exibe uma mensagem de sucesso
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")  # Exibe uma mensagem de erro

    def display_response(self, user_input, jarvas_response):
        # Exibe o texto do usuário e a resposta do Jarvas na área de texto
        self.text_area.insert(tk.END, f"Você: {user_input}\n")
        self.text_area.insert(tk.END, f"Jarvas: {jarvas_response}\n")

if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal
    app = JarvasApp(root)  # Instancia a aplicação JarvasApp
    root.mainloop()  # Inicia o loop principal da GUI
