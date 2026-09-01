# Cadastro RPC — vendas

Esta versão amplia o exemplo XML-RPC da disciplina com o fluxo de venda. O banco SQLite é criado automaticamente pelo servidor e contém as tabelas `produto`, `venda` e `itemvenda`, além das tabelas de clientes já existentes.

## Operações disponíveis

| Operação | Finalidade |
| --- | --- |
| `addProduto(descricao)` | Cadastra um produto e retorna seu identificador. |
| `getProduto(idProduto)` / `getProdutos()` | Consulta um produto ou a lista de produtos. |
| `iniciarVenda(idCliente)` | Cria uma venda no estado iniciada e retorna seu identificador. |
| `addItemVenda(idVenda, idProduto, quantidade, valor)` | Adiciona um item; se o produto já estiver na venda, soma a quantidade. |
| `getValorTotalVenda(idVenda)` | Retorna o total calculado a partir de quantidade × valor. |
| `finalizarVenda(idVenda)` | Finaliza a venda, exigindo que ela tenha pelo menos um item. |

O servidor rejeita clientes, produtos ou vendas inexistentes, valores negativos, quantidades não positivas, alterações após a finalização e vendas sem itens. Os erros são propagados pelo XML-RPC para o cliente.

## Execução

No diretório `servidor`, instale as dependências e execute:

```bash
pip install -r requirements_server.txt
python run.py
```

Em outro terminal, execute o exemplo do cliente:

```bash
python cliente/cliente.py
```

Os testes de integração podem ser executados a partir do diretório `cadastro` com:

```bash
python -m pytest -q tests
```
