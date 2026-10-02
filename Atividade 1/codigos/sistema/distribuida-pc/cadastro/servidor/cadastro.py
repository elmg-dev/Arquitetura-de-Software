import json
from datetime import datetime

import db
from db import addRegisters, saveSession, startDatabase
from model import Cliente, Endereco, ItemVenda, Produto, Venda


class CadastroCTRL:
    """Fachada da aplicação exposta pelo servidor XML-RPC."""

    @staticmethod
    def _parse_date(value):
        if isinstance(value, datetime):
            return value
        text = str(value)
        for fmt in ("%Y%m%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                pass
        raise ValueError("dtNascimento deve estar no formato YYYYMMDDTHH:MM:SS")

    def addCliente(self, nome, dtNascimento, cpf, logradouro, num, bairro, cidade, estado):
        cliente = Cliente(nome=nome, dtNascimento=self._parse_date(dtNascimento), cpf=cpf)
        cliente.endereco.append(Endereco(logradouro=logradouro, numero=num, bairro=bairro,
                                         cidade=cidade, estado=estado))
        addRegisters([cliente])
        saveSession()
        return cliente.id

    def _doGetCliente(self, id_cliente):
        cliente = db.session.query(Cliente).filter_by(id=id_cliente).first()
        if not cliente:
            raise ValueError(f"Cliente {id_cliente} não encontrado")
        return cliente

    @staticmethod
    def _cliente_dict(cliente):
        return {"id": cliente.id, "nome": cliente.nome, "cpf": cliente.cpf,
                "dtNascimento": cliente.dtNascimento.strftime("%Y%m%dT%H:%M:%S")}

    def getCliente(self, idCliente):
        return json.dumps(self._cliente_dict(self._doGetCliente(idCliente)), indent=4)

    def getClientes(self):
        return json.dumps({c.id: self._cliente_dict(c) for c in db.session.query(Cliente).all()}, indent=4)

    def getClientesPorNome(self, nome):
        clientes = db.session.query(Cliente).filter(Cliente.nome.ilike(f"%{nome}%")).all()
        return json.dumps({c.id: self._cliente_dict(c) for c in clientes}, indent=4)

    def delCliente(self, idCliente):
        db.session.delete(self._doGetCliente(idCliente))
        saveSession()

    def addProduto(self, descricao):
        if not descricao or not str(descricao).strip():
            raise ValueError("A descrição do produto é obrigatória")
        produto = Produto(descricao=str(descricao).strip())
        addRegisters([produto])
        saveSession()
        return produto.id

    def getProdutos(self):
        return json.dumps({p.id: {"descricao": p.descricao} for p in db.session.query(Produto).all()}, indent=4)

    def getProduto(self, idProduto):
        produto = db.session.query(Produto).filter_by(id=idProduto).first()
        if not produto:
            raise ValueError(f"Produto {idProduto} não encontrado")
        return json.dumps({produto.id: {"descricao": produto.descricao}}, indent=4)

    def iniciarVenda(self, idCliente):
        self._doGetCliente(idCliente)
        venda = Venda(cliente_id=idCliente, dt_venda=datetime.now(), estado="i")
        addRegisters([venda])
        saveSession()
        return venda.id

    def _doGetVenda(self, idVenda):
        venda = db.session.query(Venda).filter_by(id=idVenda).first()
        if not venda:
            raise ValueError(f"Venda {idVenda} não encontrada")
        return venda

    def addItemVenda(self, idVenda, idProduto, quantidade, valor):
        venda = self._doGetVenda(idVenda)
        if venda.estado != "i":
            raise ValueError("Só é possível alterar uma venda iniciada")
        produto = db.session.query(Produto).filter_by(id=idProduto).first()
        if not produto:
            raise ValueError(f"Produto {idProduto} não encontrado")
        quantidade, valor = float(quantidade), float(valor)
        if quantidade <= 0 or valor < 0:
            raise ValueError("Quantidade deve ser positiva e valor não pode ser negativo")
        item = db.session.query(ItemVenda).filter_by(venda_id=idVenda, produto_id=idProduto).first()
        if item:
            item.quantidade += quantidade
            item.valor = valor
        else:
            item = ItemVenda(venda_id=idVenda, produto_id=idProduto, quantidade=quantidade, valor=valor)
            addRegisters([item])
        saveSession()

    def getValorTotalVenda(self, idVenda):
        venda = self._doGetVenda(idVenda)
        db.session.refresh(venda)
        return json.dumps({"valor": float(venda.valor_total or 0.0)}, indent=4)

    def finalizarVenda(self, idVenda):
        venda = self._doGetVenda(idVenda)
        if not venda.itens:
            raise ValueError("Não é possível finalizar uma venda sem itens")
        venda.estado = "f"
        saveSession()
