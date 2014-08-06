#!/usr/bin/env python
# -*- coding: cp1252 -*-

import controller
import model
import view
from Tkinter import *

#TODO colocar valores padroes em campos

#==============================================================================================================================================#

def inclui_comissao(comissoes,novo):
    tela = Toplevel()
    tela.title("Gerenciador - Comissões")
    dados = controller.busca("id, nome", "fornecedores","","")
    if (novo > 0) :
            valores_antigos = controller.busca("comissao","comissoes"," WHERE vendedor_id ="+str(novo),"")
    x = 0
    entradas = []
    for dado in dados:
        label = Label(tela, text = dado[1]+": ")
        label.grid(row = x, column = 0, sticky=W)
        comissoes.append([dado[0]])
        valida_num = (tela.register(controller.valida_numero),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        entradas.append(Entry(tela,width=20,validate = 'key', validatecommand = valida_num))
        if (novo > 0):
            valor = str(valores_antigos[x][0])
            for index in range(len(valor)):                                 #necessario por causa da validacao do campo 'duracao campanha'
                entradas[x].insert(index, valor[index]) 
        else:
            entradas[x].insert(0,"0")
        entradas[x].grid(row = x, column =1)
        label2= Label(tela, text="%")
        label2.grid(row = x , column = 2, sticky=W)
        x+=1
    botao_limpar = Button(tela,text="Limpar", command=lambda: view.limpa_entradas(tela))
    botao_limpar.grid(row=x,column=2)
    botao_ok = Button(tela,text="Finalizar", command=lambda: view.get_entradas(tela, entradas,comissoes))
    botao_ok.grid(row = x , column = 3)


#==============================================================================================================================================#

def tela_cad_forn(root):
    view.limpa_tela(root)

    frame_cad_forn = LabelFrame(root, text="Cadastro Fornecedores", padx=5, pady=5)
    frame_cad_forn.grid(padx=10, pady=10)


    campo1 = Label(frame_cad_forn, text="Nome:")
    campo1.grid(row = 0, column = 1,padx = 10, sticky=E)

    nome_forn = Entry(frame_cad_forn, width=50)
    nome_forn.grid(row=0, column = 2, columnspan=3)

    campo2 = Label(frame_cad_forn, text="Duração da campanha:")
    campo2.grid(row = 1, column = 0,padx = 10, columnspan=2)

    valida_num = (root.register(controller.valida_numero),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W') #permitir apenas numero no duracao da campanha

    dur_camp_forn = Entry(frame_cad_forn, width=50, validate = 'key', validatecommand = valida_num)
    dur_camp_forn.grid(row=1, column = 2, columnspan=3)

    botao_enviar = Button(frame_cad_forn,text="Cadastrar", command=lambda: controller.cadastrar(frame_cad_forn,{"classe":model.fornecedor,"nome_forn":nome_forn.get(), "dur_camp":dur_camp_forn.get()})) #passo os dados do formulario em um dicionario
    botao_enviar.grid(row=2,column=4, columnspan=2, sticky=W, pady=10)
    
    botao_limpar = Button(frame_cad_forn,text="Limpar", command=lambda: view.limpa_entradas(frame_cad_forn))
    botao_limpar.grid(row=2,column=3, sticky=E, pady=10)

#==============================================================================================================================================#

def tela_cad_clie(root):
    view.limpa_tela(root)

    frame_cad_clie = LabelFrame(root, text="Cadastro Clientes", padx=5, pady=5)
    frame_cad_clie.grid(padx=10, pady=10)


    campo1 = Label(frame_cad_clie, text="Nome Completo:")
    campo1.grid(row = 0, column = 1,padx = 10, sticky=E)

    nome_clie = Entry(frame_cad_clie, width=50)
    nome_clie.grid(row=0, column = 2, columnspan=3)

    campo2 = Label(frame_cad_clie, text="Telefone Res:")
    campo2.grid(row = 1, column = 0,padx = 10, columnspan=2)

    tel_res = Entry(frame_cad_clie, width=50)
    tel_res.grid(row=1, column = 2, columnspan=3)

    campo3 = Label(frame_cad_clie, text="Telefone Cel:")
    campo3.grid(row = 2, column = 0,padx = 10, columnspan=2)

    tel_cel = Entry(frame_cad_clie, width=50)
    tel_cel.grid(row=2, column = 2, columnspan=3)

    campo4 = Label(frame_cad_clie, text="Telefone Com:")
    campo4.grid(row = 3, column = 0,padx = 10, columnspan=2)

    tel_com = Entry(frame_cad_clie, width=50)
    tel_com.grid(row=3, column = 2, columnspan=3)

    campo5 = Label(frame_cad_clie, text="Email:")
    campo5.grid(row = 4, column = 0,padx = 10, columnspan=2)

    email = Entry(frame_cad_clie, width=50)
    email.grid(row=4, column = 2, columnspan=3)

    campo6 = Label(frame_cad_clie, text="Endereço:")
    campo6.grid(row = 5, column = 0,padx = 10, columnspan=2)

    endereco = Entry(frame_cad_clie, width=50)
    endereco.grid(row=5, column = 2, columnspan=3)

    botao_enviar = Button(frame_cad_clie,text="Cadastrar", command=lambda: controller.cadastrar(frame_cad_clie,{"classe": model.pessoa, "nome_pessoa": nome_clie.get(),
                                                                "email": email.get(),"endereco": endereco.get(),"tel_cel": tel_cel.get(),
                                                                 "tel_res": tel_res.get(),"tel_com": tel_com.get(),"tipo": 0}))
    
    botao_enviar.grid(row=7,column=4, columnspan=2, sticky=W, pady=10)
    
    botao_limpar = Button(frame_cad_clie,text="Limpar", command=lambda: view.limpa_entradas(frame_cad_clie))
    botao_limpar.grid(row=7,column=3, sticky=E, pady=10)

#==============================================================================================================================================#

def tela_cad_vend(root):
    view.limpa_tela(root)

    frame_cad_vend = LabelFrame(root, text="Cadastro Vendedores", padx=5, pady=5)
    frame_cad_vend.grid(padx=10, pady=10)


    campo1 = Label(frame_cad_vend, text="Nome Completo:")
    campo1.grid(row = 0, column = 1,padx = 10, sticky=E)

    nome_vend= Entry(frame_cad_vend, width=50)
    nome_vend.grid(row=0, column = 2, columnspan=3)

    campo2 = Label(frame_cad_vend, text="Telefone Res:")
    campo2.grid(row = 1, column = 0,padx = 10, columnspan=2)

    tel_res = Entry(frame_cad_vend, width=50)
    tel_res.grid(row=1, column = 2, columnspan=3)

    campo3 = Label(frame_cad_vend, text="Telefone Cel:")
    campo3.grid(row = 2, column = 0,padx = 10, columnspan=2)

    tel_cel = Entry(frame_cad_vend, width=50)
    tel_cel.grid(row=2, column = 2, columnspan=3)

    campo4 = Label(frame_cad_vend, text="Telefone Com:")
    campo4.grid(row = 3, column = 0,padx = 10, columnspan=2)

    tel_com = Entry(frame_cad_vend, width=50)
    tel_com.grid(row=3, column = 2, columnspan=3)

    campo5 = Label(frame_cad_vend, text="Email:")
    campo5.grid(row = 4, column = 0,padx = 10, columnspan=2)

    email = Entry(frame_cad_vend, width=50)
    email.grid(row=4, column = 2, columnspan=3)

    campo6 = Label(frame_cad_vend, text="Endereço:")
    campo6.grid(row = 5, column = 0,padx = 10, columnspan=2)

    endereco = Entry(frame_cad_vend, width=50)
    endereco.grid(row=5, column = 2, columnspan=3)

    campo7 = Label(frame_cad_vend, text="Comissões:")
    campo7.grid(row = 6, column = 0,padx = 10, columnspan=2)

    comissoes = []
    botao_incluir_comis = Button(frame_cad_vend, text="Incluir", command= lambda: inclui_comissao(comissoes,0)) #segundo par. de inclui_comissao indica novo registro ou nao (0 = novo, id_vendedor = antigo)
    botao_incluir_comis.grid(row=6, column = 2, sticky = W)

    botao_enviar = Button(frame_cad_vend,text="Cadastrar", command=lambda: controller.cadastrar(frame_cad_vend,{"classe": model.vendedor, "nome_pessoa": nome_vend.get(),
                                                                "email": email.get(),"endereco": endereco.get(),"tel_cel": tel_cel.get(),
                                                                 "tel_res": tel_res.get(),"tel_com": tel_com.get(),"tipo": 1,"comissoes":comissoes}))
    
    botao_enviar.grid(row=7,column=4, columnspan=2, sticky=W, pady=10)
    
    botao_limpar = Button(frame_cad_vend,text="Limpar", command=lambda: view.limpa_entradas(frame_cad_vend))
    botao_limpar.grid(row=7,column=3, sticky=E, pady=10)

#==============================================================================================================================================#

def tela_cad_prod(root):
    view.limpa_tela(root)

    frame_cad_prod = LabelFrame(root, text="Cadastro Produtos", padx=5, pady=5)
    frame_cad_prod.grid(padx=10, pady=10)

    valida_num = (root.register(controller.valida_numero),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W') #permitir apenas numero no duracao da campanha

    campo1 = Label(frame_cad_prod, text="Código:")
    campo1.grid(row = 0, column = 1,padx = 10, sticky=E)

    cod_prod = Entry(frame_cad_prod, width=50, validate = 'key', validatecommand = valida_num)
    cod_prod.grid(row=0, column = 2, columnspan=3)

    campo2 = Label(frame_cad_prod, text="Fornecedor:")
    campo2.grid(row = 1, column = 0,padx = 10, columnspan=2)

    try:
            dados = controller.busca("nome", "fornecedores","","")
            var_forn = StringVar(frame_cad_prod)
            var_forn.set(dados[0])
            forn_prod = apply(OptionMenu, (frame_cad_prod,var_forn) + tuple(dados))
    except:
            var_forn.set("")
            forn_prod = OptionMenu(frame_cad_prod,var_forn,"")
    
    forn_prod.grid(row = 1 , column = 2, columnspan = 3, sticky = W+E )    

    campo3 = Label(frame_cad_prod, text="Quantidade:")
    campo3.grid(row = 2, column = 0,padx = 10, columnspan=2)

    qnt_prod = Entry(frame_cad_prod, width=50, validate = 'key', validatecommand = valida_num)
    qnt_prod.grid(row=2, column = 2, columnspan=3)

    campo4 = Label(frame_cad_prod, text="Descrição:")
    campo4.grid(row = 3, column = 0,padx = 10, columnspan=2)

    desc_prod = Entry(frame_cad_prod, width=50)
    desc_prod.grid(row=3, column = 2, columnspan=3)

    campo5 = Label(frame_cad_prod, text="Preço compra:")
    campo5.grid(row = 4, column = 0,padx = 10, columnspan=2)

    pcompra = Entry(frame_cad_prod, width=50)
    pcompra.grid(row=4, column = 2, columnspan=3)

    campo6 = Label(frame_cad_prod, text="Preço venda:")
    campo6.grid(row = 5, column = 0,padx = 10, columnspan=2)

    pvenda = Entry(frame_cad_prod, width=50)
    pvenda.grid(row=5, column = 2, columnspan=3)

    botao_enviar = Button(frame_cad_prod,text="Cadastrar", command=lambda: controller.cadastrar(frame_cad_prod,{"classe": model.produto, "codigo": cod_prod.get(),
                                                                "fornecedor": var_forn.get(),"qnt": qnt_prod.get(),"desc": desc_prod.get(),
                                                                 "pcompra": pcompra.get(),"pvenda": pvenda.get()}))
    
    botao_enviar.grid(row=7,column=4, columnspan=2, sticky=W, pady=10)
    
    botao_limpar = Button(frame_cad_prod,text="Limpar", command=lambda: view.limpa_entradas(frame_cad_prod))
    botao_limpar.grid(row=7,column=3, sticky=E, pady=10)

