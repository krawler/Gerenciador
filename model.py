#!/usr/bin/env python

import controller
import datetime

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
        controller.grava('fornecedores',[self.nome, self.campanha,"FALSE"])

    def alterar(self,ident):
        controller.altera('fornecedores','nome = "'+self.nome+'", dur_camp='+str(self.campanha),' id='+str(ident))
        

    def excluir(self,ident):
        controller.altera('fornecedores', "del='true'",' id='+str(ident))

class campanha:
    forn_id = 0
    data_inic = ''
    data_fim = ''
    itens = []

    def __init__(self,dados):
        temp = dados["fornecedor"]
        temp = apaga(temp,"(),")
        dado = controller.busca("id", "fornecedores", "WHERE nome = "+temp, "")         #busca id fornecedor
        dado = str(dado)
        dado = apaga(dado,"[](),")                                                      #consulta retorna com caracteres especiais
        self.forn_id = dado[0]
        
        dur_camp = controller.busca('dur_camp','fornecedores','WHERE id = '+self.forn_id,'')        #calculo do fim da data de fim da campanha
        dur_camp = apaga(str(dur_camp),"[](),")
        auxDate = datetime.datetime.strptime(dados["data_inic"], "%d/%m/%Y")

        self.data_fim = auxDate + datetime.timedelta(days=int(dur_camp))
        self.data_inic = auxDate
        self.data_fim = self.data_fim.strftime('%d/%m/%Y')
        self.data_inic = self.data_inic.strftime('%d/%m/%Y')
        self.itens = dados["produtos"]

    def salvar(self):
        camp_id = controller.grava('campanhas',[self.forn_id,self.data_inic,self.data_fim])
        for item in self.itens:
            controller.grava('itens_campanha',[camp_id,item[0],item[1]]) # item[0] = cod_prod, item[1] = desconto
    
class pessoa:
    nome = ''
    cpf = 0
    tel_cel = 0
    tel_res = 0
    tel_com = 0
    email = ''
    endereco = ''
    tipo = 0
    def __init__(self,dados):
        self.nome       = dados["nome_pessoa"]
        self.cpf       = dados["cpf"]
        self.email      = dados["email"]
        self.endereco   = dados["endereco"]
        self.tel_cel    = dados["tel_cel"]
        self.tel_res    = dados["tel_res"]
        self.tel_com    = dados["tel_com"]
        self.tipo       = dados["tipo"]

    def salvar(self):
        return controller.grava('pessoas',[self.nome, self.cpf, self.email, self.endereco, self.tel_cel, self.tel_res, self.tel_com, self.tipo])

    def alterar(self,ident):
        controller.altera('pessoas','nome = "'+self.nome+'", email="'+str(self.email)+'", endereco="'+str(self.endereco)+'", tel_cel="'+str(self.tel_cel)+
                                    '", tel_res="'+str(self.tel_res)+'", tel_com="'+str(self.tel_com)+'"','  id='+str(ident))
        
    def excluir(self,ident):
        controller.exclui('pessoas',' id='+str(ident))

class vendedor(pessoa):
    comissoes = []

    def __init__(self,dados):
        pessoa.__init__(self,dados)
        self.comissoes = dados["comissoes"]

    def salvar(self):
        pessoa_id = pessoa.salvar(self)
        for comissao in self.comissoes:
                controller.grava('comissoes',[pessoa_id,comissao[0], comissao[1]])

    def alterar(self,ident):
        pessoa_id = pessoa.alterar(self,ident)
        for comissao in self.comissoes:
                controller.altera('comissoes','comissao = '+str(comissao[1]),' vendedor_id = '+str(ident)+' AND fornecedor_id = '+str(comissao[0]))


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
    
