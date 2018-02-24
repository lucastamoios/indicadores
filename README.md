Indicadores
=============

Biblioteca com dados de índices brasileiros, até agora suporta apenas os dados do Tesouro Direto.

Uso
----

Para obter os dados mais atualizados de todos os títulos, é necessário fazer:

```
>>> from indicadores import Tesouro
>>> Tesouro().atualizar()
True
```

Caso queira atualizar apenas um título, por questões de performance:

```
>>> from indicadores import Tesouro
>>> Tesouro(titulo='Tesouro IPCA+ 2045', vencimento='15/05/2045').atualizar()
True
```

O retorno da função informa se foi ou não necessário atualizar.

Obtendo o dados de uma data para um determinado título:

```
>>> from indicadores import Titulos
>>> titulo = Titulos(nome='Tesouro IPCA+ 2045', vencimento='15/05/2045')
>>> titulo.preco_compra(data='24/02/2018')
31.89
>>> titulo.taxa_venda(data='24/02/2018')
0.052
```

Caso queira toda a série temporal, basta passar o intervalo ou nenhum parâmetro:

```
>>> titulo.preco_compra(data='24/02/2018')
31.89
>>> titulo.taxa_venda(data='24/02/2018')
0.052
```
