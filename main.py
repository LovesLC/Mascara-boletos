import os
from pathlib import Path
import shutil
import schedule
import time
from datetime import datetime
from Conversor import pdf_to_image, concatenate_images, image_to_pdf
from CortePdf import cortar_pdf
from ConversorHtml import htmlto_pdf, atualizar_html_com_dados_do_boleto, extrair_cpf_pdf

# Função para criar diretório se não existir
def criar_diretorio_se_nao_existir(diretorio):
    try:
        if not diretorio.exists():
            diretorio.mkdir(parents=True)
    except Exception as e:
        print(f"Erro ao criar diretório {diretorio}: {e}")

# Função para criar pasta do dia atual
def criar_pasta_dia_atual(diretorio_base):
    try:
        data_atual = datetime.now()
        nome_pasta = data_atual.strftime("%d-%m-%Y")
        caminho_pasta = os.path.join(diretorio_base, nome_pasta)
        if not os.path.exists(caminho_pasta):
            os.mkdir(caminho_pasta)
        return caminho_pasta
    except Exception as e:
        print(f"Erro ao criar pasta do dia atual: {e}")
        return None

# Função para mover arquivos
def mover_arquivos(origem, destino):
    try:
        arquivos = os.listdir(origem)
        for arquivo in arquivos:
            caminho_origem = os.path.join(origem, arquivo)
            shutil.copy(caminho_origem, destino)
    except Exception as e:
        print(f"Erro ao mover arquivos de {origem} para {destino}: {e}")

def processar_boletos():
    # Caminho dos arquivos
    html_path_header = './Arquivos/html/boletoOrig.html' # Seu arquivo html (Pasta arquivos)
    header_path = './Arquivos/header.pdf' # Seu arquivo header (Html transformado em PDF)
    ponto_corte = 0.54  # Ajuste este valor conforme necessário
    boletoEntrada_path = Path(r'./Entrada') # Pasta Entradas
    output_folder_path = Path(r'./Saida') # Pasta saída
    arquivos_folder_path = Path(r'./Arquivos') # Pasta Arquivos

    criar_diretorio_se_nao_existir(boletoEntrada_path)
    criar_diretorio_se_nao_existir(output_folder_path)

    
    pdf_files = list(boletoEntrada_path.glob("*.pdf")) # Lista todos os arquivos na pasta de entrada com extensão .pdf

    if pdf_files:
        print("------------------Arquivo Encontrado------------------")
        
        for file_path in pdf_files:
            
            output_file_path = arquivos_folder_path / f"boleto_cortado" # Define o caminho de saída com base no nome do arquivo

            print(f"Processando arquivo: {file_path}")

            try:
                senhaChaveamento = extrair_cpf_pdf(file_path)

                atualizar_html_com_dados_do_boleto(file_path, html_path_header)
                htmlto_pdf("./Arquivos/html/boletoNomeado.html")

                #Corta o PDF
                cortar_pdf(file_path, output_file_path, ponto_corte)


                # Transformar PDFs em imagens
                image1_path = pdf_to_image(header_path, './Arquivos/images/header.png')
                image2_path = pdf_to_image(output_file_path, './Arquivos/images/boleto.png')

                # Concatenar imagens
                concatenated_image_path = concatenate_images(image1_path, image2_path, './Arquivos/images/concatenated.png')

                # Transformar imagem concatenada em PDF
                concatenated_pdf_path = output_folder_path / f"{file_path.stem}.pdf"
                image_to_pdf(concatenated_image_path, concatenated_pdf_path, senhaChaveamento[:3])

                print(f"Arquivo {file_path.name} processado e salvo em {concatenated_pdf_path}")

                # Exclui o arquivo original após o processamento
                os.remove(file_path)
                print(f"Arquivo original {file_path.name} excluído.")

            except Exception as e:
                print(f"Erro ao processar o arquivo {file_path.name}: {e}")

        # Verifica se a pasta de saída contém arquivos
        output_files = list(output_folder_path.glob("*.pdf"))
        if output_files:
            print("Arquivos processados com sucesso. Verifique a pasta de saída.")
        else:
            print("Nenhum arquivo foi processado ou salvo. Verifique se há algum problema.")

    diretorio_base = r"./Boletos Gerados"
    pasta_dia_atual = criar_pasta_dia_atual(diretorio_base)
    pasta_origem = r"./Saida"
    mover_arquivos(pasta_origem, pasta_dia_atual)

# Agenda a execução da função a cada 'x' minutos
schedule.every(1).minutes.do(processar_boletos)

# Loop infinito para manter o script em execução e verificar o agendamento
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
