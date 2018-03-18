Indicadores
=============

Biblioteca com dados de índices brasileiros, até agora suporta apenas os dados do Tesouro Direto.

> Preste atenção na acentuação das palavras desta API.

Uso
----

Sempre que um objeto do `Tesouro` é inicializado ele atualiza as informações
faltantes. Mas caso seja necessário, é possível forçar que essa atualização
ocorra com:

```
>>> from indicadores import Tesouro
>>> Tesouro().atualizar()
```

Para obter informações de um título específico, é necessário utilizar a classe Tesouro.

```
>>> from indicadores import Tesouro
>>> título = Tesouro(título='IPCA+', vencimento='2045')
>>> título
<indicadores.tesouro.Título at 0x7feb728b7472>
```

Algumas outras funcionalidades

```
>>> from indicadores import Tesouro
>>> título = Tesouro(título='IPCA+', vencimento='2045')
>>> titulo.preço_compra(data='24/02/2018')
31.89
>>> titulo.taxa_venda(data='24/02/2018')
0.052
```

Título suporta ainda os métodos `preço_venda()`, `taxa_compra()`,
`preço_base()`, e os atributos `nome`, `vencimento`.

Caso queira toda a série temporal, basta passar o intervalo ou nenhum parâmetro:

```
>>> titulo.preco_compra()
[31.89, ...]
>>> titulo.taxa_venda(inicio='24/02/2018', fim='16/03/2018')
[0.052, ...]
```

A biblioteca é inteligente na tradução dos diversos nomes que um mesmo título
pode ter. Todos os construtures abaixo geram um objeto com as mesmas
características.

```
>>> from indicadores import Tesouro
>>> título = Tesouro(título='IPCA+ com Juros Semestrais', vencimento='2045')
>>> título = Tesouro(título='IPCA+ juros semestrais', vencimento='2045')
>>> título = Tesouro(título='IPCA+ semestral', vencimento='2045')
>>> título = Tesouro(título='IPCA semestral', vencimento='15/05/2045')
>>> título = Tesouro(título='NTN-B', vencimento='2045')
```

Tradução de alguns nomes de títulos:
- LFT = Tesouro Selic
- LTN = Tesouro Prefixado
- NTN-C = Tesouro IGPM+ com Juros Semestrais
- NTN-B = Tesouro IPCA+ com Juros Semestrais 2020
- NTN-B Principal = Tesouro IPCA+
- NTN-F = Tesouro Prefixado com Juros Semestrais
