import PyPDF2


def cortar_pdf(input_path, output_path, ponto_corte):
    try:
        # Abrir o arquivo PDF original
        with open(input_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            page = reader.pages[0]

            # Converter os valores do mediabox para float antes de multiplicar
            upper_right_x = float(page.mediabox.right)
            upper_right_y = float(page.mediabox.top) * ponto_corte

            # Ajustar o mediabox
            page.mediabox.upper_right = (upper_right_x, upper_right_y)

            # Adicionar a página cortada ao novo PDF
            writer.add_page(page)

            # Salvar o novo PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            print(f"PDF cortado com sucesso e salvo em: {output_path}")

    except Exception as e:
        print(f"Erro ao cortar o pdf :( \nErro: {e}")