import xmlrpc.client
from datetime import datetime


class ClienteRPC:
    """Cliente leve para consumir o serviço XML-RPC de cadastro e vendas."""

    def __init__(self, url="http://localhost:7080"):
        self.server = xmlrpc.client.ServerProxy(url, allow_none=True)

    def addCliente(self, nome, dtNascimento, cpf, logradouro, num, bairro, cidade, estado):
        return self.server.addCliente(nome, dtNascimento, cpf, logradouro, num, bairro, cidade, estado)

    def getCliente(self, idCliente): return self.server.getCliente(idCliente)
    def getClientes(self): return self.server.getClientes()
    def getClientesPorNome(self, nome): return self.server.getClientesPorNome(nome)
    def delCliente(self, idCliente): return self.server.delCliente(idCliente)
    def addProduto(self, descricao): return self.server.addProduto(descricao)
    def getProduto(self, idProduto): return self.server.getProduto(idProduto)
    def getProdutos(self): return self.server.getProdutos()
    def iniciarVenda(self, idCliente): return self.server.iniciarVenda(idCliente)
    def addItemVenda(self, idVenda, idProduto, qtde, valor):
        return self.server.addItemVenda(idVenda, idProduto, qtde, valor)
    def getVrTotalVenda(self, idVenda): return self.server.getValorTotalVenda(idVenda)
    def finalizarVenda(self, idVenda): return self.server.finalizarVenda(idVenda)


if __name__ == "__main__":
    app = ClienteRPC()
    produto1 = app.addProduto("Produto 1")
    produto2 = app.addProduto("Produto 2")
    cliente = app.addCliente("Cliente 1", datetime(2003, 3, 20), "11122233344",
                             "Rua A", "0", "Centro", "Januária", "MG")
    venda = app.iniciarVenda(cliente)
    app.addItemVenda(venda, produto1, 1, 10.0)
    app.addItemVenda(venda, produto2, 3, 37.92)
    print(app.getVrTotalVenda(venda))
    app.finalizarVenda(venda)
