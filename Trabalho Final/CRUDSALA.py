import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2 

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

#FUNÇÕES DO CRUD

def listar_reservas():
    for row in tabela.get_children():
        tabela.delete(row)
        
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_reserva, data_reserva, id_sala, id_grupo FROM Reserva ORDER BY id_reserva;")
        linhas = cursor.fetchall()
        
        for linha in linhas:
            tabela.insert("", tk.END, values=linha)
            
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar reservas: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def reservar_sala():
    data = reserva_data_entry.get().strip()
    id_sala = reserva_sala_entry.get().strip()
    id_grupo = reserva_grupo_entry.get().strip()
    
    if not data or not id_sala:
        messagebox.showwarning("Aviso", "Data e ID da Sala são obrigatórios!")
        return
    
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Reserva (data_reserva, id_sala, id_grupo) 
            VALUES (%s, %s, %s);
        """, (data, id_sala, id_grupo if id_grupo else None))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Sala reservada com sucesso!")
        limpar_campos()
        listar_reservas() # Atualiza a tabela
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao reservar sala: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def editar_reserva():
    # Verifica se tem alguma linha selecionada
    item_selecionado = tabela.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma reserva na tabela para editar!")
        return
        
    id_reserva = tabela.item(item_selecionado)['values'][0]
    data = reserva_data_entry.get().strip()
    id_sala = reserva_sala_entry.get().strip()
    id_grupo = reserva_grupo_entry.get().strip()
    
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Reserva 
            SET data_reserva = %s, id_sala = %s, id_grupo = %s 
            WHERE id_reserva = %s;
        """, (data, id_sala, id_grupo if id_grupo else None, id_reserva))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Reserva atualizada com sucesso!")
        limpar_campos()
        listar_reservas()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def excluir_reserva():
    item_selecionado = tabela.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma reserva na tabela para excluir!")
        return
        
    id_reserva = tabela.item(item_selecionado)['values'][0]
    
    if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir a reserva ID {id_reserva}?"):
        try:
            conn = obter_conexao()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Reserva WHERE id_reserva = %s;", (id_reserva,))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Reserva excluída com sucesso!")
            limpar_campos()
            listar_reservas()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()

def obter_linha_selecionada(event):
    item_selecionado = tabela.selection()
    if item_selecionado:
        valores = tabela.item(item_selecionado)['values']
        
        limpar_campos()
        reserva_data_entry.insert(0, valores[1])
        reserva_sala_entry.insert(0, valores[2])
        reserva_grupo_entry.insert(0, valores[3] if valores[3] != "None" and valores[3] is not None else "")

def limpar_campos():
    reserva_data_entry.delete(0, tk.END)
    reserva_sala_entry.delete(0, tk.END)
    reserva_grupo_entry.delete(0, tk.END)


