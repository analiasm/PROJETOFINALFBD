import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2 

# configuração da conexão com postgresql
def obter_conexao():
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    
    conn = psycopg2.connect(
        host="localhost",
        database="Sistemas_GE", 
        user="postgres",              
        password="senha123",        
        port="5432"                    
    )
    conn.set_client_encoding('LATIN1') 
    return conn

# funções - banco de dados

def listar_usuarios():
    for linha in tabela.get_children():
        tabela.delete(linha)
        
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        # adicionado data_nascimento no SELECT
        cursor.execute("SELECT id_usuario, nome_completo, email_institucional, matricula, senha, data_nascimento FROM Usuario ORDER BY id_usuario;")
        usuarios = cursor.fetchall()
        
        for usuario in usuarios:
            tabela.insert("", tk.END, values=usuario)
            
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar usuários: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def inserir_usuario():
    nome = user_nome_entry.get().strip()
    email = user_email_entry.get().strip()
    matricula = user_matr_entry.get().strip()
    senha = user_senha_entry.get().strip()
    data_nasc = user_data_entry.get().strip() # captura a data
    
    # validação incluindo a data de nascimento que é NOT NULL no banco
    if not nome or not email or not senha or not data_nasc:
        messagebox.showwarning("Aviso", "Nome, E-mail, Senha e Data de Nascimento são obrigatórios!")
        return

    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        
        # adicionada a coluna data_nascimento na query
        cursor.execute("""
            INSERT INTO Usuario (nome_completo, email_institucional, matricula, senha, data_nascimento) 
            VALUES (%s, %s, %s, %s, %s);
        """, (nome, email, matricula if matricula else None, senha, data_nasc))
        
        conn.commit() 
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        limpar_campos()
        listar_usuarios()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir usuário: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def editar_usuario():
    id_usuario = user_id_entry.get().strip()
    if not id_usuario:
        messagebox.showwarning("Aviso", "Selecione um usuário na lista para editar!")
        return
        
    nome = user_nome_entry.get().strip()
    email = user_email_entry.get().strip()
    matricula = user_matr_entry.get().strip()
    senha = user_senha_entry.get().strip()
    data_nasc = user_data_entry.get().strip()

    if not nome or not email or not senha or not data_nasc:
        messagebox.showwarning("Aviso", "Campos obrigatórios não podem ficar vazios!")
        return

    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        
        # atualizando também a data de nascimento
        cursor.execute("""
            UPDATE Usuario 
            SET nome_completo = %s, email_institucional = %s, matricula = %s, senha = %s, data_nascimento = %s
            WHERE id_usuario = %s;
        """, (nome, email, matricula if matricula else None, senha, data_nasc, int(id_usuario)))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
        limpar_campos()
        listar_usuarios()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar usuário: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def excluir_usuario():
    id_usuario = user_id_entry.get().strip()
    if not id_usuario:
        messagebox.showwarning("Aviso", "Selecione um usuário na lista para excluir!")
        return
        
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este usuário?"):
        try:
            conn = obter_conexao()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s;", (int(id_usuario),))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            limpar_campos()
            listar_usuarios()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir usuário: {e}")
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()

# funções aux da ineterface

def preencher_campos(event):
    item_selecionado = tabela.selection()
    if item_selecionado:
        valores = tabela.item(item_selecionado, "values")
        
        limpar_campos()
        user_id_entry.insert(0, valores[0])
        user_nome_entry.insert(0, valores[1])
        user_email_entry.insert(0, valores[2])
        user_matr_entry.insert(0, valores[3] if valores[3] != "None" else "")
        user_senha_entry.insert(0, valores[4])
        user_data_entry.insert(0, valores[5]) # preenche a data ao clicar na linha

def limpar_campos():
    user_id_entry.delete(0, tk.END)
    user_nome_entry.delete(0, tk.END)
    user_email_entry.delete(0, tk.END)
    user_matr_entry.delete(0, tk.END)
    user_senha_entry.delete(0, tk.END)
    user_data_entry.delete(0, tk.END)

# renderização da interface gráfica
root = tk.Tk()
root.title("Gerenciamento de Usuários")
root.geometry("800x480") # aumentado levemente para acomodar o novo campo

frame_form = tk.LabelFrame(root, text=" Dados do Usuário ", padx=10, pady=10)
frame_form.pack(fill="x", padx=10, pady=5)

tk.Label(frame_form, text="ID Usuário (Auto):").grid(row=0, column=0, sticky="w")
user_id_entry = tk.Entry(frame_form, width=10)
user_id_entry.grid(row=0, column=1, sticky="w")
user_id_entry.bind("<Key>", lambda e: "break") 

tk.Label(frame_form, text="Nome Completo:").grid(row=0, column=2, sticky="w", padx=10)
user_nome_entry = tk.Entry(frame_form, width=35)
user_nome_entry.grid(row=0, column=3, sticky="w")

tk.Label(frame_form, text="E-mail Inst.:").grid(row=1, column=0, sticky="w", pady=5)
user_email_entry = tk.Entry(frame_form, width=25)
user_email_entry.grid(row=1, column=1, columnspan=2, sticky="we", pady=5)

tk.Label(frame_form, text="Matrícula:").grid(row=1, column=3, sticky="e", padx=10)
user_matr_entry = tk.Entry(frame_form, width=15)
user_matr_entry.grid(row=1, column=4, sticky="w")

tk.Label(frame_form, text="Senha:").grid(row=2, column=0, sticky="w")
user_senha_entry = tk.Entry(frame_form, width=20) 
user_senha_entry.grid(row=2, column=1, sticky="w")

# novo campo: data de nascimento (Formato AAAA-MM-DD)
tk.Label(frame_form, text="Data Nasc. (AAAA-MM-DD):").grid(row=2, column=2, sticky="e", padx=10)
user_data_entry = tk.Entry(frame_form, width=15)
user_data_entry.grid(row=2, column=3, sticky="w")

# frame para os Botões de Ação
frame_botoes = tk.Frame(root)
frame_botoes.pack(fill="x", padx=10, pady=5)

tk.Button(frame_botoes, text="Inserir", bg="#d4edda", width=12, command=inserir_usuario).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Salvar Edição", bg="#cce5ff", width=12, command=editar_usuario).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Excluir", bg="#f8d7da", width=12, command=excluir_usuario).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Limpar Campos", width=12, command=limpar_campos).pack(side="left", padx=5)

# frame para a tabela de usuários
frame_tabela = tk.LabelFrame(root, text=" Usuários Cadastrados ")
frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)

colunas = ("id", "nome", "email", "matricula", "senha", "data_nasc")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

tabela.heading("id", text="ID")
tabela.heading("nome", text="Nome Completo")
tabela.heading("email", text="E-mail Institucional")
tabela.heading("matricula", text="Matrícula")
tabela.heading("senha", text="Senha")
tabela.heading("data_nasc", text="Data Nasc.")

tabela.column("id", width=40, anchor="center")
tabela.column("nome", width=160)
tabela.column("email", width=160)
tabela.column("matricula", width=80, anchor="center")
tabela.column("senha", width=80, anchor="center")
tabela.column("data_nasc", width=90, anchor="center")

tabela.pack(fill="both", expand=True, side="left")

scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

tabela.bind("<<TreeviewSelect>>", preencher_campos)

listar_usuarios()

root.mainloop()
