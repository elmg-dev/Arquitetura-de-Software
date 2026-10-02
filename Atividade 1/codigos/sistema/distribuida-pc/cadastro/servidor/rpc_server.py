from twisted.web import xmlrpc

import db
from cadastro import CadastroCTRL


class ServerRPC(xmlrpc.XMLRPC):
    """Adaptador RPC fino para a fachada de cadastro."""

    def __init__(self, allowNone=True):
        super().__init__(allowNone=allowNone)
        db.startDatabase()
        self.fachada = CadastroCTRL()

    def xmlrpc_addCliente(self, *args):
        return self.fachada.addCliente(*args)

    def xmlrpc_getCliente(self, idCliente):
        return self.fachada.getCliente(idCliente)

    def xmlrpc_getClientes(self):
        return self.fachada.getClientes()

    def xmlrpc_getClientesPorNome(self, nome):
        return self.fachada.getClientesPorNome(nome)

    def xmlrpc_delCliente(self, idCliente):
        return self.fachada.delCliente(idCliente)

    def xmlrpc_addProduto(self, descricao):
        return self.fachada.addProduto(descricao)

    def xmlrpc_getProduto(self, idProduto):
        return self.fachada.getProduto(idProduto)

    def xmlrpc_getProdutos(self):
        return self.fachada.getProdutos()

    def xmlrpc_iniciarVenda(self, idCliente):
        return self.fachada.iniciarVenda(idCliente)

    def xmlrpc_addItemVenda(self, idVenda, idProduto, qtde, valor):
        return self.fachada.addItemVenda(idVenda, idProduto, qtde, valor)

    def xmlrpc_getValorTotalVenda(self, idVenda):
        return self.fachada.getValorTotalVenda(idVenda)

    def xmlrpc_finalizarVenda(self, idVenda):
        return self.fachada.finalizarVenda(idVenda)
