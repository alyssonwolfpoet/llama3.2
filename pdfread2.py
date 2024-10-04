import requests
from PyPDF2 import PdfReader
import io

def ler_pdf_da_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Cria um objeto de arquivo em memória a partir do conteúdo do PDF
        pdf_file = io.BytesIO(response.content)
        reader = PdfReader(pdf_file)
        
        print(f"\nConteúdo do PDF {url}:")
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                print(texto)
            else:
                print("Página vazia ou texto não extraível.")
    else:
        print(f"Erro ao acessar o PDF {url}: {response.status_code}")

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

    for url in urls:
        ler_pdf_da_url(url)

if __name__ == "__main__":
    main()
