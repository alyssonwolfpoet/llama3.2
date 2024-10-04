import requests
from PyPDF2 import PdfReader

def baixar_pdf(url, nome_arquivo):
    response = requests.get(url)
    if response.status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            f.write(response.content)
        print(f"PDF {nome_arquivo} baixado com sucesso!")
    else:
        print(f"Erro ao baixar o PDF {nome_arquivo}: {response.status_code}")

def ler_pdf(caminho):
    try:
        with open(caminho, 'rb') as f:
            reader = PdfReader(f)
            print(f"\nConteúdo do PDF {caminho}:")
            for page in reader.pages:
                texto = page.extract_text()
                if texto:
                    print(texto)
                else:
                    print("Página vazia ou texto não extraível.")
    except Exception as e:
        print(f"Erro ao ler o PDF {caminho}: {e}")

def main():
    urls = [
        "https://squad7.s3.amazonaws.com/1.pdf",
        "https://squad7.s3.amazonaws.com/2.pdf",
        "https://squad7.s3.amazonaws.com/3.pdf",
        "https://squad7.s3.amazonaws.com/5.pdf",
        "https://squad7.s3.amazonaws.com/6.pdf",
        "https://squad7.s3.amazonaws.com/7.pdf",
        "https://squad7.s3.amazonaws.com/8.pdf",
        "https://squad7.s3.amazonaws.com/9.pdf",
        "https://squad7.s3.amazonaws.com/10.pdf",
        "https://squad7.s3.amazonaws.com/13.pdf",
        "https://squad7.s3.amazonaws.com/Fechamento.pdf",
        "https://squad7.s3.amazonaws.com/MiniMundoBiblioteca.pdf",
        "https://squad7.s3.amazonaws.com/MiniMundoOS.pdf",
        "https://squad7.s3.amazonaws.com/Minimundo.pdf",
        "https://squad7.s3.amazonaws.com/MinimundoCatalogosdeprodutos.pdf",
        "https://squad7.s3.amazonaws.com/transcript0.pdf",
        "https://squad7.s3.amazonaws.com/transcript1.pdf",
        "https://squad7.s3.amazonaws.com/transcript2.pdf",
        "https://squad7.s3.amazonaws.com/transcript3.pdf",
        "https://squad7.s3.amazonaws.com/transcript4.pdf",
        "https://squad7.s3.amazonaws.com/transcript5.pdf",
        "https://squad7.s3.amazonaws.com/transcript6.pdf",
        "https://squad7.s3.amazonaws.com/transcript7.pdf",
        "https://squad7.s3.amazonaws.com/transcript8.pdf",
        "https://squad7.s3.amazonaws.com/transcript9.pdf",
        "https://squad7.s3.amazonaws.com/transcript10.pdf",
        "https://squad7.s3.amazonaws.com/transcript11.pdf",
        "https://squad7.s3.amazonaws.com/transcript12.pdf",
        "https://squad7.s3.amazonaws.com/transcript13.pdf"
    ]

    for index, url in enumerate(urls, start=1):
        nome_arquivo = f'documento_{index}.pdf'
        baixar_pdf(url, nome_arquivo)
        ler_pdf(nome_arquivo)

if __name__ == "__main__":
    main()
