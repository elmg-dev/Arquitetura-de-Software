import json
import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "servidor"))

import db
from cadastro import CadastroCTRL


def setup_function():
    db.session.close()
    db.engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    db.Session.configure(bind=db.engine)
    db.session = db.Session()
    db.Base.metadata.create_all(bind=db.engine)


def test_fluxo_completo_de_venda():
    ctrl = CadastroCTRL()
    cliente = ctrl.addCliente("Ana", datetime(1990, 1, 2), "12345678900", "Rua A", "10", "Centro", "Januária", "MG")
    produto_a = ctrl.addProduto("Café")
    produto_b = ctrl.addProduto("Pão")
    venda = ctrl.iniciarVenda(cliente)
    ctrl.addItemVenda(venda, produto_a, 2, 10.5)
    ctrl.addItemVenda(venda, produto_b, 3, 4.0)

    assert json.loads(ctrl.getValorTotalVenda(venda))["valor"] == 33.0
    ctrl.finalizarVenda(venda)
    assert db.session.get(__import__("model").Venda, venda).estado == "f"


def test_item_repetido_soma_quantidade():
    ctrl = CadastroCTRL()
    cliente = ctrl.addCliente("Bruno", datetime(1991, 2, 3), "12345678901", "Rua B", "20", "Centro", "Januária", "MG")
    produto = ctrl.addProduto("Caneta")
    venda = ctrl.iniciarVenda(cliente)
    ctrl.addItemVenda(venda, produto, 1, 5)
    ctrl.addItemVenda(venda, produto, 2, 5)
    assert json.loads(ctrl.getValorTotalVenda(venda))["valor"] == 15.0


def test_nao_finaliza_venda_sem_itens():
    ctrl = CadastroCTRL()
    cliente = ctrl.addCliente("Carla", datetime(1992, 3, 4), "12345678902", "Rua C", "30", "Centro", "Januária", "MG")
    venda = ctrl.iniciarVenda(cliente)
    try:
        ctrl.finalizarVenda(venda)
        assert False, "deveria rejeitar venda sem itens"
    except ValueError as exc:
        assert "sem itens" in str(exc)
