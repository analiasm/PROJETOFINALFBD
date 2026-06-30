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

