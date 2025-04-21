import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk
from faker import Faker
import random

def conectar():
    return psycopg2.connect(
        user="postgres",
        password="7474",
        host="localhost",
        port="5432",
        database="projetonotas"
    )

def criar_tabela():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            matricula VARCHAR(20) UNIQUE NOT NULL,
            nota NUMERIC(5,2) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()



def criar_tabela():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            matricula VARCHAR(20) UNIQUE NOT NULL,
            nota NUMERIC(5,2) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def popular_alunos_fake(qtd=10):
    fake = Faker("pt_BR")
    conn = conectar()
    cur = conn.cursor()
    inseridos = 0

    for _ in range(qtd):
        nome = fake.name()
        matricula = fake.unique.numerify("2025####")
        nota = round(random.uniform(0.0, 10.0), 2)

        try:
            cur.execute("INSERT INTO alunos (nome, matricula, nota) VALUES (%s, %s, %s)",
                        (nome, matricula, nota))
            inseridos += 1
        except Exception as e:
            print("Erro ao inserir:", e)

    conn.commit()
    cur.close()
    conn.close()
    listar_alunos()
    messagebox.showinfo("Sucesso", f"{inseridos} alunos fictícios inseridos.")

# Funções CRUD - tema 5 
def adicionar_aluno():
    nome = entry_nome.get()
    matricula = entry_matricula.get()
    nota = entry_nota.get()

    if nome and matricula and nota:
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO alunos (nome, matricula, nota) VALUES (%s, %s, %s)",
                        (nome, matricula, nota))
            conn.commit()
            cur.close()
            conn.close()
            listar_alunos()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

def listar_alunos():
    for row in tree.get_children():
        tree.delete(row)

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM alunos ORDER BY id")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    cur.close()
    conn.close()

def atualizar_aluno():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Atenção", "Selecione um aluno para atualizar.")
        return

    aluno_id = tree.item(selected)["values"][0]
    nome = entry_nome.get()
    matricula = entry_matricula.get()
    nota = entry_nota.get()

    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE alunos SET nome=%s, matricula=%s, nota=%s WHERE id=%s",
                (nome, matricula, nota, aluno_id))
    conn.commit()
    cur.close()
    conn.close()
    listar_alunos()
    limpar_campos()

def deletar_aluno():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Atenção", "Selecione um aluno para excluir.")
        return

    aluno_id = tree.item(selected)["values"][0]

    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM alunos WHERE id=%s", (aluno_id,))
    conn.commit()
    cur.close()
    conn.close()
    listar_alunos()
    limpar_campos()

def preencher_campos(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected)["values"]
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, values[1])
        entry_matricula.delete(0, tk.END)
        entry_matricula.insert(0, values[2])
        entry_nota.delete(0, tk.END)
        entry_nota.insert(0, values[3])

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_matricula.delete(0, tk.END)
    entry_nota.delete(0, tk.END)

janela = tk.Tk()
janela.title("Projeto Sistema de Notas  by Alunos de TI ")
janela.geometry("900x400")


tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

tk.Label(janela, text="Matrícula:").grid(row=1, column=0, padx=10, pady=5)
entry_matricula = tk.Entry(janela)
entry_matricula.grid(row=1, column=1, padx=10, pady=5)

tk.Label(janela, text="Nota:").grid(row=2, column=0, padx=10, pady=5)
entry_nota = tk.Entry(janela)
entry_nota.grid(row=2, column=1, padx=10, pady=5)


tk.Button(janela, text="Adicionar", command=adicionar_aluno).grid(row=0, column=2, padx=10)
tk.Button(janela, text="Atualizar", command=atualizar_aluno).grid(row=1, column=2, padx=10)
tk.Button(janela, text="Excluir", command=deletar_aluno).grid(row=2, column=2, padx=10)
tk.Button(janela, text="Popular aleatório", command=lambda: popular_alunos_fake(10)).grid(row=3, column=2, padx=10, pady=5)


tree = ttk.Treeview(janela, columns=("ID", "Nome", "Matrícula", "Nota"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Matrícula", text="Matrícula")
tree.heading("Nota", text="Nota")
tree.bind("<ButtonRelease-1>", preencher_campos)
tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)


criar_tabela()
listar_alunos()
janela.mainloop()
