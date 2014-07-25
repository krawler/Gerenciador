#!/usr/bin/env python
# -*- coding: cp1252 -*-

import controller
import model
from Tkinter import *

#==============================================================================================================================================#

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    try:
        data = [(float(tree.set(child, col)), child) for child in tree.get_children('')]
    except:
        data = [(tree.set(child, col), child) for child in tree.get_children('')]

    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))
    
#==============================================================================================================================================#

def limpa_entradas(pai):    #funcao generica para limpar entradas
        for filho in pai.winfo_children():
                if filho.winfo_class() == 'Entry':  #quando existirem novos tipos para limpar, copiar esse if
                        if filho.cget("validate") == "key":     #por causa da funcao de validacao, as entrys que aceitam so numeros nao podem ser simplesmente deletadas
                            filho.insert(len(filho.get()),0)    #insiro zero no final e limpo o comeco
                            filho.delete(0,len(filho.get())-1)
                        else:
                            filho.delete(0,len(filho.get()))
                            
#==============================================================================================================================================#

def limpa_tela(pai):
    for filho in pai.winfo_children():
        if filho.winfo_class() == 'Labelframe':
            filho.grid_forget()
            filho.destroy()
            
#==============================================================================================================================================#

def fecha_tela(pai):
    pai.destroy()
            
#==============================================================================================================================================#            

def get_entradas(pai, lista_entries, dados):
    x = 0
    for entry in lista_entries:
        dados[x].append(int(entry.get()))
        x+=1
    pai.destroy()

#==============================================================================================================================================#
    
def popup_warning(texto):
    popup = Toplevel()
    popup.title("Gerenciador - Alerta!")
    msg = Message(popup, text=texto, width = 200)
    msg.pack(expand = 1, fill=X)
    ok = Button(popup, text="Fechar", command=popup.destroy)
    ok.pack()

#==============================================================================================================================================#

def tela_principal(): #define elementos basicos que devem aparecer na tela principal
    
    #inicia o controlador do tkinter - janela principal
    root = Tk()         
    root.wm_title("Gerenciador")
    root.wm_minsize(width=800,height=600)

    #menu do topo da aplicacao
    menu_principal = Menu(root)

    #tres menus dropdown a seguir, arquivo, cadastro e listagem.
    #futuros menus no menu principal devem ser colocados aqui
    menu_arquivo = Menu(menu_principal, tearoff=0)
    menu_arquivo.add_command(label="Importar Banco")
    menu_arquivo.add_command(label="Exportar Banco")
    menu_principal.add_cascade(label="Arquivo", menu = menu_arquivo)

    menu_cadastro = Menu(menu_principal, tearoff=0)
    menu_cadastro.add_command(label="Fornecedores", command = lambda: controller.cad_forn(root) )
    menu_cadastro.add_command(label="Produtos", command = lambda: controller.cad_prod(root))
    menu_cadastro.add_command(label="Vendedores", command = lambda: controller.cad_vend(root))
    menu_cadastro.add_command(label="Clientes", command = lambda: controller.cad_clie(root))
    menu_principal.add_cascade(label="Cadastro", menu = menu_cadastro)

    menu_lista = Menu(menu_principal, tearoff=0)
    menu_lista.add_command(label="Fornecedores", command = lambda: controller.lista_forn(root))
    menu_lista.add_command(label="Produtos")
    menu_lista.add_command(label="Vendedores")
    menu_lista.add_command(label="Clientes", command = lambda: controller.lista_clie(root))
    menu_principal.add_cascade(label="Listagem", menu = menu_lista)

    root.config(menu=menu_principal) #define qual eh o menu da aplicacao principal

    root.mainloop()

