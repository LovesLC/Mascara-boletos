import pdfkit
import PyPDF2
import re
import os

#Convertendo a página HTML para PDF usando pdfkit
def htmlto_pdf(arquivo_html):
    try:
        pdfkit.from_file(arquivo_html, './Arquivos/header.pdf')
        print("Arquivo HTML Convertido com sucesso!")
    except Exception as e:
        print(f"Não foi possível converter o HTML em PDF. \n Erro: {e}")

 
def extrair_cpf_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text()

            linhas = texto_completo.split('\n')
            linha = linhas[4]
            print(linha)
            padrao_numero = r'([0-9]+)$'
            match2 = re.search(padrao_numero, linha)
            print(f"CPF: {match2.group(1)}")
            return match2.group(1)
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None

def extrair_dados_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text()

            linhas = texto_completo.split('\n')
            
            dados = {
                'nome': None,
                'cod_barra': None,
                'data': None,
                'n_doc': None,
                'especie': None,
                'aceite': None,
                'dt_proc': None,
                'nnum': None,
                'ref': None,
                'valor': None
            }

            # Definir as linhas específicas a serem extraídas
            linha_nome = linhas[2] if len(linhas) > 2 else ''
            linha_cod_barra = linhas[12] if len(linhas) > 12 else ''
            linha_data = linhas[6] if len(linhas) > 6 else ''
            linha_n_doc = linhas[14] if len(linhas) > 14 else ''
            linha_especie = linhas[16] if len(linhas) > 16 else ''
            linha_aceite = linhas[18] if len(linhas) > 18 else ''
            linha_dt_proc = linhas[20] if len(linhas) > 20 else ''
            linha_nnum = linhas[22] if len(linhas) > 22 else ''
            linha_ref = linhas[24] if len(linhas) > 24 else ''
            linha_valor = linhas[10] if len(linhas) > 10 else ''
            
            padrao_nome = r'^([^0-9]+)'
            match_nome = re.match(padrao_nome, linha_nome)
            if match_nome:
                dados['nome'] = match_nome.group(1).strip()

            dados['cod_barra'] = linha_cod_barra.strip()

            dados['data'] = linha_data.strip()
            
            padrao_n_doc = r'([0-9]+)$'
            match_n_doc = re.search(padrao_n_doc, linha_n_doc)
            if match_n_doc:
                dados['n_doc'] = match_n_doc.group(1).strip()

            dados['especie'] = linha_especie.strip()

            dados['aceite'] = linha_aceite.strip()

            dados['dt_proc'] = linha_dt_proc.strip()

            dados['nnum'] = linha_nnum.strip()

            dados['ref'] = linha_ref.strip()
            
            dados['valor'] = linha_valor.strip()

            print(dados)

            return dados
    except Exception as e:
        print(f"Erro ao extrair dados do PDF: {e}")
        return None

def replace_dados_no_html(html_path, dados, novo_html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            content = file.read()
            substituicoes = {
                '{NOME}': dados.get('nome', ''),
                '{COD_BARRA}': dados.get('cod_barra', ''),
                '{DATA}': dados.get('data', ''),
                '{NDOC}': dados.get('n_doc', ''),
                '{ESP}': dados.get('especie', ''),
                '{ACEITE}': dados.get('aceite', ''),
                '{DATAPROC}': dados.get('dt_proc', ''),
                '{NNUM}': dados.get('nnum', ''),
                '{REF}': dados.get('ref', ''),
                '{NVALOR}': dados.get('valor', '')
            }
            for placeholder, valor in substituicoes.items():
                content = content.replace(placeholder, valor)
            
            with open(novo_html_path, 'w', encoding='utf-8') as new_file:
                new_file.write(content)
        print(f"Substituição realizada com sucesso! Novo arquivo: {novo_html_path}")
    except Exception as e:
        print(f"Não foi possível alterar os dados no documento HTML. \n Erro: {e}")

def atualizar_html_com_dados_do_boleto(boleto_pdf_path, html_path):
    try:
        dados_extraidos = extrair_dados_pdf(boleto_pdf_path)
        
        if dados_extraidos:
            novo_html_path = os.path.join(os.path.dirname(html_path), "boletoNomeado.html")
            replace_dados_no_html(html_path, dados_extraidos, novo_html_path)
        else:
            print("Não foi possível extrair os dados do boleto PDF.")
    except Exception as e:
        print(f"Erro ao atualizar o novo html com dados do boleto :( \n Erro: {e} ")

# html = r'C:/Users/administrator/Desktop/Mascara-de-Boletos/teste.html'
# htmlto_pdf(html)
# pdf = r'./Arquivos/Boleto-teste.pdf'
# extrair_cpf_pdf(pdf)

