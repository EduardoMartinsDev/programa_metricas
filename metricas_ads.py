import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Frame, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MetricsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Acompanhamento de Métricas de Ads")
        
        # Estrutura de dados inicial
        self.metrics = ["Alcance", "Impressões", "Frequência", "Cliques", "Custo por clique", 
                        "Quantidade de Leads", "Quantidade de vendas", "Custo por Lead", 
                        "Custo por venda (CAC)", "Investimento"]
        self.months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", 
                       "Junho", "Julho", "Agosto", "Setembro", "Outubro", 
                       "Novembro", "Dezembro"]
        self.data = {metric: {month: None for month in self.months} for metric in self.metrics}

        # Configuração de notebook com abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.create_input_tab()
        self.create_graph_tab()

    def create_input_tab(self):
        input_tab = Frame(self.notebook)
        self.notebook.add(input_tab, text="Inserir Dados")
        
        Label(input_tab, text="Métrica / Mês", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5)
        for j, month in enumerate(self.months):
            Label(input_tab, text=month, font=("Arial", 10)).grid(row=0, column=j+1, padx=5, pady=5)

        # Campos de entrada para cada métrica
        self.entries = {}
        for i, metric in enumerate(self.metrics):
            Label(input_tab, text=metric, font=("Arial", 10)).grid(row=i+1, column=0, padx=5, pady=5, sticky="w")
            self.entries[metric] = {}
            for j, month in enumerate(self.months):
                entry = Entry(input_tab, width=8)
                entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                self.entries[metric][month] = entry

        # Botão para salvar dados
        Button(input_tab, text="Salvar Dados", command=self.save_data, font=("Arial", 10, "bold")).grid(row=len(self.metrics)+1, columnspan=len(self.months)+1, pady=20)

    def create_graph_tab(self):
        self.graph_tab = Frame(self.notebook)
        self.notebook.add(self.graph_tab, text="Visualizar Gráficos")
        
        Label(self.graph_tab, text="Painel de Gráficos", font=("Arial", 14)).pack(pady=10)

    def save_data(self):
        # Salvar dados da tabela em `self.data`
        for metric in self.metrics:
            for month in self.months:
                value = self.entries[metric][month].get()
                if value:
                    try:
                        self.data[metric][month] = float(value)
                    except ValueError:
                        messagebox.showerror("Erro de Entrada", f"Valor inválido para {metric} em {month}.")
                        return
                else:
                    self.data[metric][month] = None
        messagebox.showinfo("Dados Salvos", "Os dados foram salvos com sucesso.")
        
        # Atualizar os gráficos automaticamente
        self.plot_all_metrics()

    def plot_all_metrics(self):
        # Limpar gráficos anteriores
        for widget in self.graph_tab.winfo_children():
            widget.destroy()

        Label(self.graph_tab, text="Painel de Gráficos", font=("Arial", 14)).pack(pady=10)

        # Criar DataFrame e configurar layout de subplots
        df = pd.DataFrame(self.data)
        df.fillna(0, inplace=True)  # Substituir valores None ou NaN por 0

        total_metrics = len(self.metrics)
        cols = 3  # Configurar 3 colunas para os gráficos
        rows = (total_metrics + cols - 1) // cols  # Calcular o número de linhas necessário
        figure, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(15, 10), squeeze=False)
        figure.tight_layout(pad=3.0)

        # Plotar cada métrica em um subplot com cores distintas
        colors = plt.cm.Paired(range(total_metrics))
        for i, (metric, color) in enumerate(zip(df.columns, colors)):
            row, col = divmod(i, cols)
            ax = axes[row][col]
            df[metric].plot(kind='line', marker='o', color=color, ax=ax, title=metric)
            ax.set_ylabel(metric)
            ax.set_xlabel("Meses")
            ax.set_xticks(range(len(self.months)))
            ax.set_xticklabels(self.months, rotation=45, fontsize=8)

        # Desabilitar eixos vazios (se houver)
        for j in range(i + 1, rows * cols):
            row, col = divmod(j, cols)
            axes[row][col].axis("off")
        
        # Embutir o gráfico na interface tkinter
        canvas = FigureCanvasTkAgg(figure, master=self.graph_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

# Inicializar a aplicação
root = Tk()
app = MetricsApp(root)
root.mainloop()













