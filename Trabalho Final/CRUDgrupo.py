# --- CRUD ----
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2 

# --- conexão com o postgreSQL ---- 
def obtener_conexao():
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
# --- CRUD -----
# --- inserir ---
def inserir_grupo():
    nome = grupo_nome_entry.get().strip()
    id_adm = grupo_idadm_entry.get().strip()
    descricao = grupo_desc_entry.get().strip()
    status = grupo_status_entry.get().strip()
    qtd = grupo_qtd_entry.get().strip()
    
    if not nome or not id_adm:
        messagebox.showwarning("Aviso", "Nome do Grupo e ID do Administrador são obrigatórios!")
        return
    try:
        id_adm_tratado = int(id_adm)
        descricao_tratada = descricao if descricao else None
        qtd_tratada = int(qtd) if qtd else None
        
        conn = obtener_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Grupo (nome_grupo, id_adm, descricao, status, qtd_participantes) 
            VALUES (%s, %s, %s, %s, %s);
        """, (nome, id_adm_tratado, descricao_tratada, status, qtd_tratada))
        
        conn.commit() 
        messagebox.showinfo("Sucesso", "Grupo criado com sucesso!")
        limpar_campos()
        listar_grupos()
        
# ---- Excluir ---
def excluir_grupo():
    id_grupo = grupo_id_entry.get().strip()
    if not id_grupo:
        messagebox.showwarning("Aviso", "Selecione um grupo na lista para excluir!")
        return
        
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este grupo?"):
        try:
            conn = obtener_conexao()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Grupo WHERE id_grupo = %s;", (int(id_grupo),))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Grupo excluído com sucesso!")
            limpar_campos()
            listar_grupos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir grupo: {e}")
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()

# --- listar ---
def listar_grupos():
    # Limpa a tabela visual antes de recarregar
    for linha in tabela.get_children():
        tabela.delete(linha)
        
    try:
        conn = obtener_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_grupo, nome_grupo, id_adm, descricao, status, qtd_participantes FROM Grupo ORDER BY id_grupo;")
        grupos = cursor.fetchall()
        
        for grupo in grupos:
            tabela.insert("", tk.END, values=grupo)
            
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar grupos: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            
# --- editar ---
def editar_grupo():
    id_grupo = grupo_id_entry.get().strip()
    if not id_grupo:
        messagebox.showwarning("Aviso", "Selecione um grupo na lista para editar!")
        return
        
    nome = grupo_nome_entry.get().strip()
    id_adm = grupo_idadm_entry.get().strip()
    descricao = grupo_desc_entry.get().strip()
    status = grupo_status_entry.get().strip()
    qtd = grupo_qtd_entry.get().strip()

    try:
        conn = obtener_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Grupo 
            SET nome_grupo = %s, id_adm = %s, descricao = %s, status = %s, qtd_participantes = %s
            WHERE id_grupo = %s;
        """, (nome, int(id_adm), descricao if descricao else None, status, int(qtd) if qtd else None, int(id_grupo)))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Grupo atualizado com sucesso!")
        limpar_campos()
        listar_grupos()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar grupo: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

# --- INTERFACE ---
# -- funções auxiliares da inteerface --
def preencher_campos(event):
    """ Preenche os campos de texto ao clicar em uma linha da tabela """
    item_selecionado = tabela.selection()
    if item_selecionado:
        valores = tabela.item(item_selecionado, "values")
        
        # Limpa e insere os novos valores nos campos
        limpar_campos()
        grupo_id_entry.insert(0, valores[0])
        grupo_nome_entry.insert(0, valores[1])
        grupo_idadm_entry.insert(0, valores[2])
        grupo_desc_entry.insert(0, valores[3] if valores[3] != "None" else "")
        grupo_status_entry.insert(0, valores[4])
        grupo_qtd_entry.insert(0, valores[5] if valores[5] != "None" else "")

def limpar_campos():
    grupo_id_entry.delete(0, tk.END)
    grupo_nome_entry.delete(0, tk.END)
    grupo_idadm_entry.delete(0, tk.END)
    grupo_desc_entry.delete(0, tk.END)
    grupo_status_entry.delete(0, tk.END)
    grupo_qtd_entry.delete(0, tk.END)

# --- interface gráfica ---
root = tk.Tk()
root.title("Gerenciamento de Grupos de Estudo")
root.geometry("750x450")

# Frame para o formulário (Campos de entrada)
frame_form = tk.LabelFrame(root, text=" Dados do Grupo ", padx=10, pady=10)
frame_form.pack(fill="x", padx=10, pady=5)

# ID do Grupo (Campo oculto ou desabilitado apenas para controle do SQL)
tk.Label(frame_form, text="ID Grupo (Auto):").grid(row=0, column=0, sticky="w")
grupo_id_entry = tk.Entry(frame_form, width=10)
grupo_id_entry.grid(row=0, column=1, sticky="w")
# Deixamos desabilitado para o usuário não alterar manualmente o ID do banco
grupo_id_entry.bind("<Key>", lambda e: "break") 

# --- campos ---
tk.Label(frame_form, text="Nome Grupo:").grid(row=0, column=2, sticky="w", padx=10)
grupo_nome_entry = tk.Entry(frame_form, width=30)
grupo_nome_entry.grid(row=0, column=3, sticky="w")

tk.Label(frame_form, text="ID Adm:").grid(row=1, column=0, sticky="w", pady=5)
grupo_idadm_entry = tk.Entry(frame_form, width=10)
grupo_idadm_entry.grid(row=1, column=1, sticky="w", pady=5)

tk.Label(frame_form, text="Status:").grid(row=1, column=2, sticky="w", padx=10)
grupo_status_entry = tk.Entry(frame_form, width=15)
grupo_status_entry.grid(row=1, column=3, sticky="w")

tk.Label(frame_form, text="Descrição:").grid(row=2, column=0, sticky="w")
grupo_desc_entry = tk.Entry(frame_form, width=40)
grupo_desc_entry.grid(row=2, column=1, columnspan=3, sticky="we")

tk.Label(frame_form, text="Qtd Part.:").grid(row=2, column=4, sticky="w", padx=10)
grupo_qtd_entry = tk.Entry(frame_form, width=10)
grupo_qtd_entry.grid(row=2, column=5, sticky="w")

# Frame para os Botões de Ação
frame_botoes = tk.Frame(root)
frame_botoes.pack(fill="x", padx=10, pady=5)

tk.Button(frame_botoes, text="Inserir", bg="#d4edda", width=12, command=inserir_grupo).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Salvar Edição", bg="#cce5ff", width=12, command=editar_grupo).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Excluir", bg="#f8d7da", width=12, command=excluir_grupo).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Limpar Campos", width=12, command=limpar_campos).pack(side="left", padx=5)


# Frame para a Listagem Visual (Tabela Treeview)
frame_tabela = tk.LabelFrame(root, text=" Grupos Cadastrados ")
frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)

colunas = ("id", "nome", "adm", "descricao", "status", "qtd")
tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

# Definição dos cabeçalhos da tabela
tabela.heading("id", text="ID")
tabela.heading("nome", text="Nome do Grupo")
tabela.heading("adm", text="ID Adm")
tabela.heading("descricao", text="Descrição")
tabela.heading("status", text="Status")
tabela.heading("qtd", text="Qtd Part.")

# Ajuste da largura das colunas
tabela.column("id", width=50, anchor="center")
tabela.column("nome", width=150)
tabela.column("adm", width=60, anchor="center")
tabela.column("descricao", width=200)
tabela.column("status", width=80, anchor="center")
tabela.column("qtd", width=80, anchor="center")

tabela.pack(fill="both", expand=True, side="left")

# Scrollbar para a tabela
scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Evento de clique na tabela para carregar os dados nos inputs
tabela.bind("<<TreeviewSelect>>", preencher_campos)

# Inicializa listando os dados já existentes no banco
listar_grupos()

root.mainloop()
