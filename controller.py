#!/usr/bin/env python
# -*- coding: cp1252 -*-

import view
import model
import viewCadastros
import viewListagem
import os
import sqlite3 as sql
import atexit

def cria_banco():
    conexao = sql.connect('info.db')
    query = conexao.cursor()

    query.execute('''CREATE TABLE fornecedores (id integer PRIMARY KEY AUTOINCREMENT,nome text,dur_camp integer, del boolean default false)''')

    query.execute('''CREATE TABLE pessoas (id integer PRIMARY KEY AUTOINCREMENT,nome text,cpf integer, email text, endereco text,
                                                            tel_cel text,tel_res text,tel_com text, tipo integer)''')

    query.execute('''CREATE TABLE comissoes (id integer PRIMARY KEY AUTOINCREMENT,vendedor_id integer,fornecedor_id integer,comissao integer)''')

    query.execute('''CREATE TABLE produtos (id integer PRIMARY KEY AUTOINCREMENT,codigo integer,
                                            forn_id integer,qnt integer,descr text, pcompra real, pvenda real)''')

    query.execute('''CREATE TABLE campanhas (id integer PRIMARY KEY AUTOINCREMENT, forn_id integer, data_inic text, data_fim text)''')

    query.execute('''CREATE TABLE itens_campanha (id integer PRIMARY KEY AUTOINCREMENT, campanha_id integer, cod_prod integer, desconto real)''')

    query.execute('''CREATE TABLE vendas (id integer PRIMARY KEY AUTOINCREMENT, clie_id integer, vendor_id integer,
                                            data text, status integer, t_pag integer)''')

    query.execute('''CREATE TABLE produtos_venda (id integer PRIMARY KEY AUTOINCREMENT, venda_id integer, cod_prod integer, quant integer,val_t real)''')

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
        command = "INSERT INTO "+tabela+" VALUES (NULL, "+values+")"
        print command
        query.execute(command)
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
        command = "UPDATE "+tabela+" SET "+dados+" WHERE "+condicao
        print command
        query.execute(command)
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
        command = "SELECT "+selecao+" FROM "+tabela+" "+condicoes+" "+opcionais # debug
        query.execute(command)
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
        command = "DELETE FROM "+tabela+" WHERE "+condicao
        query.execute(command)
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

def cad_vendas(root):
    viewCadastros.tela_cad_vendas(root)

def cad_forn(root):
    viewCadastros.tela_cad_forn(root)

def cad_camp(root):
    viewCadastros.tela_cad_camp(root)

def cad_clie(root):
    viewCadastros.tela_cad_clie(root)

def cad_vend(root):
    viewCadastros.tela_cad_vend(root)

def cad_prod(root):
    viewCadastros.tela_cad_prod(root)

def lista_forn(root):
    cabecalhos = ['ID', 'Nome', u'Dura��o Campanha']
    dados = busca('id, nome, dur_camp','fornecedores','WHERE not(del)','')
    viewListagem.tela_lista_forn(root,cabecalhos, dados)

def lista_prod(root):
    cabecalhos = ['ID', u'C�digo', 'Fornecedor', 'Quantidade', u'Descri��o' ,u'Pre�o Compra', u'Pre�o Venda']   #pego o nome do fornecedor usando inner join no forn_id
    dados = busca('produtos.id, produtos.codigo, fornecedores.nome, produtos.qnt, produtos.descr, produtos.pcompra, produtos.pvenda','produtos',
                  '',' INNER JOIN fornecedores ON produtos.forn_id = fornecedores.id')
    viewListagem.tela_lista_prod(root,cabecalhos, dados)

def lista_clie(root):
    cabecalhos = ['ID', 'Nome','CPF', 'Email', u'Endere�o', 'Telefone Celular', u'Telefone residencial', 'Telefone Comercial']
    dados = busca('id, nome, cpf, email, endereco, tel_cel, tel_res, tel_com','pessoas','WHERE tipo=0','')
    viewListagem.tela_lista_clie(root,cabecalhos, dados)

def lista_vend(root):
    cabecalhos = ['ID', 'Nome', 'CPF', 'Email', u'Endere�o', 'Telefone Celular', u'Telefone residencial', 'Telefone Comercial']
    dados = busca('id, nome, cpf, email, endereco, tel_cel, tel_res, tel_com', 'pessoas', 'WHERE tipo=1','')
    viewListagem.tela_lista_vend(root,cabecalhos, dados)



def verifica_deletados(): # TODO: ver se existem outras dependencias no banco.
    for fornecedor in busca('id','fornecedores',"where del='true'",''):
        #print fornecedor[0]
        usos = busca('id','produtos','where forn_id="'+str(fornecedor[0])+'"','')
        if usos is None:
            exclui('fornecedores', ' id="'+str(fornecedor[0])+'"')
            for comissao in busca('id','comissoes','where fornecedor_id="'+str(fornecedor[0])+'"',''):
                exclui('comissoes',' id="'+str(comissao[0])+'"')

def busca_cpf(event,pai,cpf,index):
    nome = busca("nome","pessoas","WHERE cpf = "+cpf,"")
    nome = model.apaga(str(nome),"[]()'',")
    viewCadastros.mostra_nome(pai,nome,index)

def busca_preco(prod):
    retorno1 = busca("descr,pvenda","produtos","WHERE codigo = "+prod,"")
    retorno2 = busca("desconto","itens_campanha","WHERE cod_prod="+prod,"")
    if retorno2 == []:
        return retorno1[0]
    else:
        valor = retorno1[0][1] - (retorno1[0][1]*(retorno2[0][0]/100))
        return (retorno1[0][0],valor)
    
def main():
    # registra a funcao verifica_deletados para ser executada ao fim do programa.
    # https://docs.python.org/2/library/atexit.html
    atexit.register(verifica_deletados)
    
    verifica_banco()
    view.tela_principal()

if __name__ == "__main__":
    main()
