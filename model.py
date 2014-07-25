#!/usr/bin/env python

import controller

#TODO verificar duplicata de dados antes de salvar (todas as classes)
#TODO verificar dados antes de salvar(vazio, preenchimento incorreto, etc)

def apaga(string, rep_set):
    for car in rep_set:
        string = string.replace(car,"")
    return string

class fornecedor:
    nome = ''
    campanha = 0
    def __init__(self,dados):
        self.nome = dados["nome_forn"]
        self.campanha = dados["dur_camp"]


    def salvar(self):
        controller.grava('fornecedores',[self.nome, self.campanha])

    def alterar(self,ident):
        controller.altera('fornecedores','nome = "'+self.nome+'", dur_camp='+str(self.campanha),' id='+str(ident))
        

    def excluir(self,ident):
        controller.exclui('fornecedores',' id='+str(ident))
    
class pessoa:
    nome = ''
    tel_cel = 0
    tel_res = 0
    tel_com = 0
    email = ''
    endereco = ''
    tipo = 0
    def __init__(self,dados):
        self.nome       = dados["nome_pessoa"]
        self.email      = dados["email"]
        self.endereco   = dados["endereco"]
        self.tel_cel    = dados["tel_cel"]
        self.tel_res    = dados["tel_res"]
        self.tel_com    = dados["tel_com"]
        self.tipo       = dados["tipo"]

    def salvar(self):
        return controller.grava('pessoas',[self.nome, self.email, self.endereco, self.tel_cel, self.tel_res, self.tel_com, self.tipo])

class vendedor(pessoa):
    comissoes = []

    def __init__(self,dados):
        pessoa.__init__(self,dados)
        self.comissoes = dados["comissoes"]

    def salvar(self):
        pessoa_id = pessoa.salvar(self)
        for comissao in self.comissoes:
                controller.grava('comissoes',[pessoa_id,comissao[0], comissao[1]])


class produto():
    codigo = 0
    forn_id = 0
    qnt = 0
    desc = ''
    pcompra = 0
    pvenda = 0

    def __init__(self,dados):
        self.codigo = dados["codigo"]
        temp = dados["fornecedor"]
        temp = apaga(temp,"(),")
        dado = controller.busca("id", "fornecedores", "WHERE nome = "+temp, "")
        dado = str(dado)
        dado = apaga(dado,"[](),")
        self.forn_id = dado[0]
        self.qnt = dados["qnt"]
        self.desc = dados["desc"]
        self.pcompra = dados["pcompra"]
        self.pvenda = dados["pvenda"]

    def salvar(self):
            controller.grava('produtos',[self.codigo, self.forn_id, self.qnt, self.desc, self.pcompra, self.pvenda])
    
