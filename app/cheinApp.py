from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgbox
import mysql.connector as mysql

entryFields = {}

colunas_tabelas = {
    'cliente': [
        ('idCliente', 'ID'),
        ('nome', 'Nome'),
        ('email', 'E-mail'),
        ('usuario', 'Usuário'),
        ('senha', 'Senha')
    ],
    'produto': [
        ('idProduto', 'ID'),
        ('nome', 'Nome'),
        ('descricao', 'Descrição'),
        ('preco', 'Preço'),
        ('estoque', 'Estoque')
    ],
    'compra': [
        ('idCompra', 'ID'),
        ('fkIdCliente', 'ID Cliente'),
        ('dataCompra', 'Data da Compra'),
        ('valorTotal', 'Valor Total')
    ],
    'produtoCompra': [
        ('idProdutoCompra', 'ID'),
        ('fkIdCompra', 'ID Compra'),
        ('fkIdProduto', 'ID Produto'),
        ('quantidade', 'Quantidade'),
        ('subtotal', 'SubTotal')
    ]
}



def connectChein():
    return mysql.connect(
        host='localhost',
        user='root',
        password='3214',
        database='Chein'
    )

## ====================
##         CRUD
## ====================

def create(tabela):
    dados = {k: v.get() for k, v in entryFields.items()}
    
    con = connectChein()
    cursor = con.cursor()

    if tabela == 'cliente':
        if not dados['idCliente'] or not dados['usuario'] or not dados['senha']:
            msgbox.showinfo("Alerta", "Os campos ID, Usuario e Senha são obrigatórios.")
            return

        insert = f"INSERT INTO cliente VALUES (%s, %s, %s, %s, MD5(%s))"
        valores = (dados['idCliente'], dados['nome'], dados['email'], dados['usuario'], dados['senha'])
        cursor.execute(insert, valores)
        
    elif tabela == 'produto':
        if not dados['idProduto'] or not dados['nome'] or not dados['preco']:
            msgbox.showinfo("Alerta", "Os campos ID, Nome e Preço são obrigatórios.")
            return

        insert = f"INSERT INTO produto (idProduto, nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s, %s)"
        valores = (dados['idProduto'], dados['nome'], dados['descricao'], dados['preco'], dados['estoque'] or 100)
        cursor.execute(insert, valores)
        
    elif tabela == 'compra':
        if not dados['idCompra'] or not dados['fkIdCliente']:
            msgbox.showinfo("Alerta", "O campo ID e ID Cliente são obrigatórios.")
            return

        if dados['dataCompra'].strip():  # if user provided a value
            insert = f"INSERT INTO compra (idCompra, fkIdCliente, dataCompra) VALUES (%s, %s, %s)"
            valores = (dados['idCompra'], dados['fkIdCliente'], dados['dataCompra'])
        else:  # omit dataCompra so MySQL uses default
            insert = f"INSERT INTO compra (idCompra, fkIdCliente) VALUES (%s, %s)"
            valores = (dados['idCompra'], dados['fkIdCliente'])
            
        cursor.execute(insert, valores)
        
    elif tabela == 'produtoCompra':
        if not dados['idProdutoCompra'] or not dados['fkIdCompra'] or not dados['fkIdProduto']:
            msgbox.showinfo("Alerta", "Os campos ID Compra e ID Produto são obrigatórios.")
            return
        
        if not dados['quantidade'].strip():
            dados['quantidade'] = 1

        insert = f"INSERT INTO produtoCompra (idProdutoCompra, fkIdCompra, fkIdProduto, quantidade) VALUES (%s, %s, %s, %s)"
        valores = (dados['idProdutoCompra'], dados['fkIdCompra'], dados['fkIdProduto'], dados['quantidade'])
        cursor.execute(insert, valores)

    con.commit()
    cursor.close()
    con.close()
    
    read(tabela)



def read(tabela):
    
    tree.delete(*tree.get_children())
    tree["show"] = "headings"

    campos = colunas_tabelas.get(tabela, [])

    colunas_visiveis = [t for k, t in campos if k != 'senha']
    campos_query = [k for k, t in campos if k != 'senha']

    tree["columns"] = colunas_visiveis

    for col in colunas_visiveis:
        tree.heading(col, text=col)
        tree.column(col, anchor=CENTER, width=100)

    select = f"SELECT {', '.join(campos_query)} FROM {tabela}"

    con = connectChein()
    cursor = con.cursor()
    cursor.execute(select)
    result = cursor.fetchall()

    for row in result:
        tree.insert("", END, values=row)

    cursor.close()
    con.close()

    atualizaLabels(tabela)



def update(tabela):
    dados = {k: v.get() for k, v in entryFields.items()}

    con = connectChein()
    cursor = con.cursor()

    if tabela == 'cliente':
        id = dados['idCliente']
        cursor.execute("UPDATE cliente SET nome=%s, email=%s, usuario=%s, senha=MD5(%s) WHERE idCliente=%s", 
                       (dados['nome'], dados['email'], dados['usuario'], dados['senha'], id))

    elif tabela == 'produto':
        id = dados['idProduto']
        cursor.execute("UPDATE produto SET nome=%s, descricao=%s, preco=%s, estoque=%s WHERE idProduto=%s", 
                       (dados['nome'], dados['descricao'], dados['preco'], dados['estoque'], id))

    elif tabela == 'compra':
        id = dados['idCompra']
        cursor.execute("UPDATE compra SET fkIdCliente=%s, dataCompra=%s WHERE idCompra=%s", 
                       (dados['fkIdCliente'], dados['dataCompra'], id))

    elif tabela == 'produtoCompra':
        id = dados['idProdutoCompra']
        cursor.execute("UPDATE produtoCompra SET fkIdCompra=%s, fkIdProduto=%s, quantidade=%s WHERE idProdutoCompra=%s", 
                       (dados['fkIdCompra'], dados['fkIdProduto'], dados['quantidade'], id))

    con.commit()
    cursor.close()
    con.close()
    
    read(tabela)



def delete(tabela):
    dados = {k: v.get() for k, v in entryFields.items()}
    
    con = connectChein()
    cursor = con.cursor()

    if tabela == 'cliente':
        id = dados['idCliente']
        cursor.execute("DELETE FROM cliente WHERE idCliente=%s;",(id,))
        
    elif tabela =='produto':
        id = dados['idProduto']
        cursor.execute("DELETE FROM produto WHERE idProduto=%s;",(id,))
        
    elif tabela == 'compra':
        id = dados['idCompra']
        cursor.execute("DELETE FROM compra WHERE idCompra=%s;",(id,))
        
    elif tabela == 'produtoCompra':
        id = dados['idProdutoCompra']
        cursor.execute("DELETE FROM produtoCompra WHERE idProdutoCompra=%s;",(id,))

    con.commit()
    cursor.close()
    con.close()

    read(tabela)



# === OUTRAS FUNCOES ===

def atualizaLabels(tabela):
    global frameEntry, entryFields
    
    try:
        frameEntry.destroy()
    except:
        pass

    entryFields.clear()
    frameEntry = Frame(root, bg='#d3bab4')
    frameEntry.place(x=20, y=420)

    campos = colunas_tabelas.get(tabela, [])

    for i, (chave, texto) in enumerate(campos):
        label = Label(frameEntry, text=texto, bg='#d3bab4', fg='#434343')
        label.grid(row=i, column=0, sticky='w', padx=5, pady=2)
        ent = Entry(frameEntry, width=30)
        ent.grid(row=i, column=1, padx=5, pady=2)
        entryFields[chave] = ent
        
def on_tree_select(evento):
    selected_item = tree.focus()
    if not selected_item:
        return

    valores = tree.item(selected_item)['values']
    campos = colunas_tabelas.get(tabela.get(), [])

    campos = [k for k, t in campos if k != 'senha']

    for i, chave in enumerate(campos):
        entryFields[chave].delete(0, END)
        entryFields[chave].insert(0, valores[i])

def clearEntry():
    for entry in entryFields.values():
        entry.delete(0, END)



# WIDGET
root = Tk()
root.geometry("1000x600")
root.title("Chein")
root.configure(background='#d3bab4')



# STYLES
style = ttk.Style()
style.configure('b.TButton', 
      font=('consolas', 10), 
      bg="#bf9e9e", 
      fg="#343434",
      width=15
)

style = ttk.Style()
style.configure('texto.TLabel',
      fg="#434343",
      bg='#d3bab4'
)

style = ttk.Style()
style.configure('e.TEntry', 
      font=('verdana', 12), 
      fg="#434343"
)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
    background="#ddd1ce",
    foreground='#434343',
    fieldbackground='#ddd1ce')
style.map('Treeview',
    background=[('selected', "#a9938e")])



# TITULO CHEIN
titulo = Label(root, text="C H E I N", font=('verdana', 25, 'bold'), bg='#d3bab4')
titulo.place(relx=0.5, y=30, anchor='center')

# DROPDOWN P ESCOLHER A TABELA
tabela = StringVar()
tabDropdown = ttk.Combobox(root, textvariable=tabela, state='readonly')
tabDropdown['values'] = ('cliente', 'produto', 'compra', 'produtoCompra')
tabDropdown.set("Selecione uma tabela")
tabDropdown.place(x=20, y=60, width=150)

# TREEVIEW P MOSTRAR AS TABELAS
tree = ttk.Treeview(root)
tree.place(x=20, y=100, width=950, height=300)
tree.bind("<ButtonRelease-1>", on_tree_select)

## BOTAO SELECT
btnRead = ttk.Button(root, text="READ", command=lambda: read(tabela.get()), style='b.TButton')
btnRead.place(x=200, y=58)

# BOTOES 
frameCrud = Frame(root, bg='#d3bab4')
frameCrud.place(x=320, y=420)

btnCreate = ttk.Button(frameCrud, text="INSERT", width=12, command=lambda: create(tabela.get()), style='b.TButton')
btnCreate.grid(row=0, column=0, sticky='w', padx=5, pady=2)

btnUpdate = ttk.Button(frameCrud, text="UPDATE", width=12, command=lambda: update(tabela.get()), style='b.TButton')
btnUpdate.grid(row=1, column=0, sticky='w', padx=5, pady=2)

btnDelete = ttk.Button(frameCrud, text="DELETE", width=12, command=lambda: delete(tabela.get()), style='b.TButton')
btnDelete.grid(row=2, column=0, sticky='w', padx=5, pady=2)

btnClear = ttk.Button(frameCrud, text="CLEAR", width=12, command=clearEntry, style='b.TButton')
btnClear.grid(row=3, column=0, sticky='w', padx=5, pady=2)

root.mainloop()