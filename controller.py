#!/usr/bin/env python
# -*- coding: cp1252 -*-

import view
import model
import viewCadastros
import viewListagem
import os
import sqlite3 as sql

def cria_banco():
    conexao = sql.connect('info.db')
    query = conexao.cursor()

    query.execute('''CREATE TABLE fornecedores (id integer PRIMARY KEY AUTOINCREMENT,nome text,dur_camp integer)''')

    query.execute('''CREATE TABLE pessoas (id integer PRIMARY KEY AUTOINCREMENT,nome text,email text, endereco text,
                                                            tel_cel text,tel_res text,tel_com text, tipo integer)''')

    query.execute('''CREATE TABLE comissoes (id integer PRIMARY KEY AUTOINCREMENT,vendedor_id integer,fornecedor_id integer,comissao integer)''')

    query.execute('''CREATE TABLE produtos (id integer PRIMARY KEY AUTOINCREMENT,codigo integer,
                                            forn_id integer,qnt integer,descr text, pcompra integer, pvenda integer)''')

    conexao.commit()

    conexao.close()

def verifica_banco():
        if not(os.path.isfile("info.db")):
                cria_banco()

def grava(tabela,dados):
    try:
        conexao = sql.connect('info.db')
        query = conexao.cursor()
        values = str(dados)
        values = values[1:len(values)-1]
        query.execute("INSERT INTO "+tabela+" VALUES (NULL, "+values+")" )
        conexao.commit()
        row_id = query.lastrowid
        conexao.close()
        return row_id
    except:
        view.popup_warning("Falha ao gravar dados!")
        return None

def altera(tabela,dados, condicao):
    try:
        conexao = sql.connect('info.db')
        query = conexao.cursor()
        query.execute("UPDATE "+tabela+" SET "+dados+" WHERE "+condicao )
        conexao.commit()
        row_id = query.lastrowid
        conexao.close()
        return row_id
    except:
        view.popup_warning("Falha ao alterar dados!")
        return None

def busca(selecao, tabela, condicoes, opcionais):
    try:
        conexao = sql.connect('info.db')
        conexao.text_factory = str
        query = conexao.cursor()
        query.execute("SELECT "+selecao+" FROM "+tabela+" "+condicoes+" "+opcionais)
        dados =  query.fetchall()
        conexao.commit()
        conexao.close()
        return dados
    except:
        view.popup_warning("Falha ao buscar dados!")
        return None

def exclui(tabela, condicao):
    try:
        conexao = sql.connect('info.db')
        query = conexao.cursor()
        query.execute("DELETE FROM "+tabela+" WHERE "+condicao)
        conexao.commit()
        row_id = query.lastrowid
        conexao.close()
        return row_id
    except:
        view.popup_warning("Falha ao excluir dados!")
        return None

def valida_numero(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if int(action) == 1:
        if text in '0123456789.,':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True

def excluir(retorno, pai, avo, dados):
    item = dados["classe"](dados)
    item.excluir(dados["id"])
    del item
    view.fecha_tela(pai)
    globals()[retorno](avo)                  #chamar funcao usando o conteudo de string, pq pode ser lista_clie,lista_forn,lista_prod, etc

def alterar(retorno, pai, avo, dados):
    item = dados["classe"](dados)
    item.alterar(dados["id"])
    del item
    view.fecha_tela(pai)
    globals()[retorno](avo)

def cadastrar(pai,dados):
    novo = dados["classe"](dados)
    novo.salvar()
    del novo
    view.limpa_entradas(pai)

def cad_forn(root):
    viewCadastros.tela_cad_forn(root)

def cad_clie(root):
    viewCadastros.tela_cad_clie(root)

def cad_vend(root):
    viewCadastros.tela_cad_vend(root)

def cad_prod(root):
    viewCadastros.tela_cad_prod(root)

def lista_forn(root):
    cabecalhos = ['ID', 'Nome', u'Duração Campanha']
    dados = busca('*','fornecedores','','')
    viewListagem.tela_lista_forn(root,cabecalhos, dados)

def lista_clie(root):
    cabecalhos = ['ID', 'Nome', 'Email', u'Endereço', 'Telefone Celular', u'Telefone residêncial', 'Telefone Comercial']
    dados = busca('id, nome, email, endereco, tel_cel, tel_res, tel_com','pessoas','WHERE tipo=0','')
    viewListagem.tela_lista_clie(root,cabecalhos, dados)

def lista_vend(root):
    cabecalhos = ['ID', 'Nome', 'Email', u'Endereço', 'Telefone Celular', u'Telefone residêncial', 'Telefone Comercial']
    dados = busca('id, nome, email, endereco, tel_cel, tel_res, tel_com', 'pessoas', 'WHERE tipo=1','')
    viewListagem.tela_lista_vend(root,cabecalhos, dados)



def main():
    verifica_banco()
    view.tela_principal()

if __name__ == "__main__":
    main()
