from datetime import datetime

import db
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func, select
from sqlalchemy.orm import column_property, relationship


class Cliente(db.Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    dtNascimento = Column(DateTime, nullable=False)
    dt_hr_manutencao = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    endereco = relationship("Endereco", cascade="all, delete-orphan", passive_deletes=True)
    compras = relationship("Venda", back_populates="cliente", cascade="all, delete-orphan")


class Endereco(db.Base):
    __tablename__ = "endereco"

    id = Column(Integer, primary_key=True)
    logradouro = Column(String, nullable=False)
    numero = Column(String)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id", ondelete="CASCADE"), nullable=False)
    dt_hr_manutencao = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Produto(db.Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    dt_hr_manutencao = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    itens = relationship("ItemVenda", back_populates="produto")


class ItemVenda(db.Base):
    __tablename__ = "itemvenda"

    venda_id = Column(Integer, ForeignKey("venda.id", ondelete="CASCADE"), primary_key=True)
    produto_id = Column(Integer, ForeignKey("produto.id"), primary_key=True)
    quantidade = Column(Float, nullable=False)
    valor = Column(Float, nullable=False)
    subtotal = column_property(quantidade * valor)
    dt_hr_manutencao = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")


class Venda(db.Base):
    __tablename__ = "venda"

    id = Column(Integer, primary_key=True)
    dt_venda = Column(DateTime, nullable=False, default=datetime.now)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    estado = Column(String(1), nullable=False, default="i")
    dt_hr_manutencao = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    cliente = relationship("Cliente", back_populates="compras")
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")
    valor_total = column_property(
        select(func.coalesce(func.sum(ItemVenda.subtotal), 0.0))
        .where(ItemVenda.venda_id == id)
        .correlate_except(ItemVenda)
        .scalar_subquery()
    )
