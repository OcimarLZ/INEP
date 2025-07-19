import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tkinter import Tk, Listbox, Button, MULTIPLE, END, Label, StringVar
from tkinter.ttk import Combobox


# Função para carregar dados da tabela f_ies_dados_anuais
def load_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    query = 'SELECT * FROM f_ies_dados_anuais'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Função para criar gráfico dinâmico
def create_dynamic_plot(df, x_col, y_cols, plot_type):
    if plot_type == 'Linha':
        fig = go.Figure()
        for y_col in y_cols:
            fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines+markers', name=y_col, text=df[y_col]))
    elif plot_type == 'Barra':
        fig = go.Figure()
        for y_col in y_cols:
            fig.add_trace(go.Bar(x=df[x_col], y=df[y_col], name=y_col, text=df[y_col], textposition='auto'))

    fig.update_layout(title=f'Gráfico de {plot_type} para {", ".join(y_cols)}',
                      xaxis_title=x_col,
                      yaxis_title='Valores',
                      legend_title='Variáveis')
    fig.show()


# Função para aplicar filtros
def apply_filters(df, regiao, uf, municipio):
    if regiao != 'Todos':
        df = df[df['regiao'] == regiao]
    if uf != 'Todos':
        df = df[df['uf'] == uf]
    if municipio != 'Todos':
        df = df[df['municipio'] == municipio]
    elif municipio == 'Todos' and uf == 'Todos' and regiao != 'Todos':
        # Agrupar por região e somar os valores das colunas numéricas
        df = df.groupby(['ano', 'regiao']).sum().reset_index()
    return df


# Função para obter a seleção do usuário e criar o gráfico
def plot_selected_columns():
    selected_indices = listbox.curselection()
    selected_columns = [listbox.get(i) for i in selected_indices]
    plot_type = plot_type_var.get()
    if selected_columns:
        filtered_df = apply_filters(df, regiao_var.get(), uf_var.get(), municipio_var.get())
        create_dynamic_plot(filtered_df, 'ano', selected_columns, plot_type)


# Caminho do banco de dados
db_path = '../INEP.db'

# Carregar os dados
df = load_data_from_db(db_path)

# Criar interface gráfica
root = Tk()
root.title("Selecionar Colunas para o Gráfico")

# Combobox para selecionar o tipo de gráfico
Label(root, text="Tipo de Gráfico:").pack()
plot_type_var = StringVar()
plot_type_combobox = Combobox(root, textvariable=plot_type_var)
plot_type_combobox['values'] = ['Linha', 'Barra']
plot_type_combobox.current(0)
plot_type_combobox.pack()

# Combobox para selecionar Região
Label(root, text="Região:").pack()
regiao_var = StringVar()
regiao_combobox = Combobox(root, textvariable=regiao_var)
regiao_combobox['values'] = ['Todos'] + list(df['regiao'].unique())
regiao_combobox.current(0)
regiao_combobox.pack()

# Combobox para selecionar UF
Label(root, text="UF:").pack()
uf_var = StringVar()
uf_combobox = Combobox(root, textvariable=uf_var)
uf_combobox['values'] = ['Todos'] + list(df['uf'].unique())
uf_combobox.current(0)
uf_combobox.pack()

# Combobox para selecionar Município
Label(root, text="Município:").pack()
municipio_var = StringVar()
municipio_combobox = Combobox(root, textvariable=municipio_var)
municipio_combobox['values'] = ['Todos'] + list(df['municipio'].unique())
municipio_combobox.current(0)
municipio_combobox.pack()

# Listbox para selecionar múltiplas colunas
listbox = Listbox(root, selectmode=MULTIPLE, width=50, height=15)
listbox.pack()

# Preencher Listbox com nomes das colunas
for col in df.columns:
    if col != 'ano':
        listbox.insert(END, col)

# Botão para criar o gráfico
plot_button = Button(root, text="Plotar Gráfico", command=plot_selected_columns)
plot_button.pack()

# Iniciar o loop da interface gráfica
root.mainloop()