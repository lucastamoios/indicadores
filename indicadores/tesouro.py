import arrow
import bs4
import datetime
import hashlib
import io
import math
import pandas
import requests
import vcr


TesouroVcr = vcr.VCR(
    cassette_library_dir='data/',
)


class Tesouro:

    URL_BASE = 'https://sisweb.tesouro.gov.br/apex/'
    URL_TESOURO = URL_BASE + 'f?p=2031:2'

    TRADUÇÃO = {
        'Dia': 'data',
        'Taxa Compra': 'taxa_compra',
        'Taxa Venda': 'taxa_venda',
        'PU Compra': 'preço_compra',
        'PU Venda': 'preço_venda',
        'PU Base': 'preço_base',
        'PU Extrato': 'preço_base',
    }

    def __init__(self, título, vencimento):
        self.título = self._valida_título(título)
        self.vencimento = self._valida_vencimento(vencimento)
        self._dados = None

    def atualiza(self, titulo=None):
        todas_urls = self._obtém_urls_tesouro()
        self._dados = {}
        for tipo_título, urls_anuais in todas_urls.items():
            self._dados[tipo_título] = self._atualiza_título(urls_anuais)

    def _valida_título(self, título):
        return título

    def _valida_vencimento(self, vencimento):
        return vencimento

    def _atualiza_título(self, urls_anuais):
        dados_por_ano = {}
        for ano, url in urls_anuais.items():
            excel_título_por_ano = self._obtém_arquivo_excel(url, ano)
            planilha_título_por_ano = self._extrai_planilhas_de_arquivo_excel(excel_título_por_ano)
            dados_por_ano[ano] = planilha_título_por_ano
        return self._organiza_informações(dados_por_ano)

    def _organiza_informações(self, dados_por_ano):
        """Organiza as informações sobre os títulos em séries temporais completas

        Os dados chegam até aqui fragmentados por ano, então é necessário
        emendar essas listas em uma única lista completa.
        """
        anos_dos_títulos = sorted(dados_por_ano)
        dados_título = {}
        for ano in anos_dos_títulos:
            dados_ano = dados_por_ano[ano]
            if not dados_título:
                # Preenche o primeiro ano
                dados_título = dados_ano
            else:
                # Preenche os demais anos
                for vencimento, dados_ in dados_ano.items():
                    # Novos vencimentos aparecem nos outros anos pois é normal
                    # que surjam novos títulos
                    if vencimento not in dados_título.keys():
                        # É um vencimento novo deste título
                        dados_título[vencimento] = dados_
                    else:
                        # São dados e uma série temporal já existente, então é
                        # necessário apenas estender a série
                        for key in dados_título[vencimento].keys():
                            dados_título[vencimento][key].extend(dados_[key])
        return dados_título

    def _obtém_arquivo_excel(self, url, ano):
        """Obtém informações do servidor do governo

        Caso essa informação seja de anos antigos, verifica-se se existe um
        cassete salvo.
        """
        if ano == str(arrow.now().year):
            r = requests.get(url, verify=False)
        else:
            nome_cassete = hashlib.sha256(bytes(url, 'utf8')).hexdigest()[:12]
            with TesouroVcr.use_cassette(nome_cassete):
                r = requests.get(url, verify=False)
        arquivo_excel = io.BytesIO(r.content)
        return arquivo_excel

    def _extrai_planilhas_de_arquivo_excel(self, arquivo_excel):
        data_frames = pandas.read_excel(arquivo_excel, sheet_name=None)
        planilhas = {}
        for data_frame in data_frames.values():
            vencimento = self._valida_data_vencimento_da_planilha(data_frame.columns[1])
            planilhas[vencimento] = self._obtém_colunas_da_planilha(data_frame)
        return planilhas

    def _valida_data_vencimento_da_planilha(self, vencimento):
        if isinstance(vencimento, datetime.datetime):
            vencimento = vencimento.strftime('%d/%m/%Y')
        return vencimento

    def _obtém_colunas_da_planilha(self, df):
        planilha = {}
        for coluna in df.columns:
            cabeçalho = df[coluna][0]
            corpo = df[coluna][1:]
            if self._cabeçalho_inválido(cabeçalho):
                continue
            nome_coluna = self._infere_nome_coluna(cabeçalho)
            planilha[nome_coluna] = corpo.values.tolist()
        return planilha

    def _cabeçalho_inválido(self, cabeçalho):
        return isinstance(cabeçalho, float) and math.isnan(cabeçalho)

    def _infere_nome_coluna(self, nome_encontrado):
        for nome_catalogado, nome_desejado in self.TRADUÇÃO.items():
            if nome_catalogado in nome_encontrado:
                return nome_desejado
        raise Exception('Coluna {coluna} tem um nome não esperado.'.format(coluna=nome_encontrado))

    def _obtém_urls_tesouro(self):
        """Retorna as URLs para as planilhas de títulos do tesouro

        A hierarquia de dados é
            Nome do título > Ano das informações > URL para planilha
        """
        tags = self._extrai_tags_úteis()
        urls = {}
        ano = None
        for tag in tags:
            if tag.name == 'span':
                ano = tag.text.strip('\n\t -')
            else:
                tipo_título = tag.text.strip()
                urls[tipo_título] = urls.get(tipo_título, {})
                urls[tipo_título][ano] = self.URL_BASE + tag['href']
        return urls

    def _extrai_tags_úteis(self):
        """Extrai tags de ano e de links para as planilhas """
        r = requests.get(self.URL_TESOURO, verify=False)
        página = bs4.BeautifulSoup(r.text, 'html.parser')
        div = página.find(id='R152792803134912015')
        tabela = div.find(class_='bl-body')
        tags_úteis = tabela.find_all(['a', 'span'])
        return tags_úteis
