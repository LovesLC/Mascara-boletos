## Automatização de Processamento de Boletos
Este script Python automatiza o processamento de boletos bancários em PDF. Ele realiza várias operações para transformar um boleto bancário em um formato específico, pronto para ser utilizado em um sistema de processamento.

Funcionalidades
Extração e Atualização de Dados:

Extrai dados específicos do boleto bancário para inserção em um arquivo HTML.
Atualiza o HTML com os dados extraídos, preparando-o para conversão em PDF.
Conversão de Formatos:

Converte o HTML atualizado para um arquivo PDF.
Manipulação de PDF:

Corta o PDF original do boleto em seções específicas conforme necessário.
Processamento de Imagens:

Converte os PDFs (boleto e cabeçalho) em imagens.
Concatena as imagens geradas para formar uma única imagem combinada.
Conversão de Imagem para PDF:

Transforma a imagem concatenada de volta em PDF, mantendo a formatação e dados essenciais.
Organização e Movimentação de Arquivos:

Move os arquivos processados para uma pasta de saída específica, organizada por data.
Dependências
Bibliotecas Python
os
shutil
schedule
time
datetime
Módulos Personalizados
Conversor (funções: pdf_to_image, concatenate_images, image_to_pdf)
CortePdf (função: cortar_pdf)
ConversorHtml (funções: htmlto_pdf, atualizar_html_com_dados_do_boleto, extrair_cpf_pdf)
Ferramentas Necessárias
wkhtmltopdf
ImageMagick
Ghostscript
Configuração do Ambiente
Instale as ferramentas listadas acima.
Adicione os diretórios de instalação das ferramentas ao PATH do sistema.
Configuração de Caminhos
Atualize os caminhos dos arquivos e diretórios conforme necessário no script para refletir sua estrutura de diretórios local.
Execução
Execute o script.
Coloque arquivos de boletos na pasta de entrada designada (./Entrada).
Os arquivos processados serão encontrados na pasta de saída (./Saida), organizados por data.
Considerações
Ajuste o valor de ponto_corte conforme necessário para obter o corte correto dos PDFs.
Monitore logs e mensagens de erro para resolver quaisquer problemas durante a execução do script.
Certifique-se de que todos os caminhos fornecidos para arquivos e diretórios existem e são acessíveis.
Este script oferece uma solução automatizada para processamento de boletos bancários, ideal para ambientes que lidam com grandes volumes de documentos financeiros de forma eficiente e organizada.
