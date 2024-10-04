import os
import requests
import json
import boto3
import PyPDF2
import io
from dotenv import load_dotenv

class BedrockModel:
    def __init__(self, model_id, aws_access_key, aws_secret_key, region, temperature=0.1):
        self.model_id = model_id
        self.temperature = temperature
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )

    def generate(self, prompt):
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

    def generate_quiz(self, context, num_questions=5):
        prompt = (
            f"Baseado no seguinte contexto, gere {num_questions} perguntas de quiz "
            f"junto com suas respectivas respostas em formato JSON:\n\n"
            f"Contexto: {context}\n"
        )
        return self.generate(prompt)

    def read_pdf_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            pdf_file = io.BytesIO(response.content)
            texto = ""
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                texto += page.extract_text() + "\n" if page.extract_text() else "Página vazia ou texto não extraível.\n"
            return texto.strip()
        else:
            print(f"Erro ao acessar o PDF {url}: {response.status_code}")
            return ""

def main():
    load_dotenv()

    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    region = os.getenv('AWS_REGION')

    model = BedrockModel(
        model_id="meta.llama3-1-70b-instruct-v1:0",
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key,
        region=region
    )

    urls = [
        "https://squad7.s3.amazonaws.com/3.pdf",
    ]

    for url in urls:
        contexto = model.read_pdf_from_url(url)

        if contexto:
            quiz = model.generate_quiz(contexto)

            if quiz:
                # Quiz já é um dicionário, apenas o imprimimos diretamente
                print(f"Quiz gerado a partir do PDF {url}:")
                print(json.dumps(quiz, indent=2, ensure_ascii=False))
            else:
                print(f"Não foi possível gerar um quiz a partir do PDF {url}.")

if __name__ == "__main__":
    main()
