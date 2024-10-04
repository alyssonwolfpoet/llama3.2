import os
import requests
import json
import boto3
import PyPDF2
import io
from dotenv import load_dotenv
from llama_index import Document, GPTSimpleVectorIndex

class BedrockModel:
    def __init__(self, model_id, aws_access_key, aws_secret_key, region, temperature=0.1):
        # Inicializa o modelo Bedrock com os parâmetros fornecidos
        self.model_id = model_id
        self.temperature = temperature
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

    def generate(self, prompt):
        # Gera uma resposta com base no prompt fornecido
        body = {
            "prompt": prompt,
            "temperature": self.temperature,
        }

        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            return json.loads(response['body'].read())
        except Exception as e:
            print(f"Erro ao invocar o modelo {self.model_id}: {str(e)}")
            return None

    def read_pdf_from_url(self, url):
        # Lê o conteúdo de um PDF a partir de uma URL
        response = requests.get(url)
        if response.status_code == 200:
            pdf_file = io.BytesIO(response.content)
            texto = ""
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                # Extrai o texto de cada página do PDF
                texto += page.extract_text() + "\n" if page.extract_text() else "Página vazia ou texto não extraível.\n"
            return texto.strip()  # Remove espaços em branco desnecessários
        else:
            print(f"Erro ao acessar o PDF {url}: {response.status_code}")
            return ""

def main():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    region = os.getenv('AWS_REGION')

    # Inicializa o modelo Bedrock
    model = BedrockModel(
        model_id="meta.llama3-1-70b-instruct-v1:0",
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key,
        region=region
    )

    # Lista de URLs dos PDFs a serem lidos
    urls = [
        # "https://squad7.s3.amazonaws.com/1.pdf",
        # "https://squad7.s3.amazonaws.com/2.pdf",
        "https://squad7.s3.amazonaws.com/3.pdf",
        # Adicione mais URLs conforme necessário
    ]

    documentos = []

    for url in urls:
        # Lendo o conteúdo do PDF a partir da URL
        contexto = model.read_pdf_from_url(url)

        if contexto:
            # Cria um documento LlamaIndex a partir do conteúdo extraído
            documentos.append(Document(text=contexto))

    # Cria um índice a partir dos documentos
    index = GPTSimpleVectorIndex(documents)

    # Exemplo de consulta ao índice
    while True:
        pergunta = input("Digite sua pergunta ou 'sair' para encerrar: ")
        if pergunta.lower() == 'sair':
            break

        # Busca a resposta utilizando o índice
        resposta = index.query(pergunta)
        print(f"Resposta: {resposta}")

if __name__ == "__main__":
    main()
