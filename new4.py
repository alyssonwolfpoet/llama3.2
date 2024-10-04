import os
import boto3
import json
import PyPDF2
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
            f"junto com suas respectivas respostas:\n\n"
            f"Contexto: {context}\n"
        )
        return self.generate(prompt)

    def read_pdf(self, pdf_path):
        texto = ""
        with open(pdf_path, "rb") as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
        return texto.strip()  # Remove espaços em branco desnecessários

def main():
    load_dotenv()

    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    region = os.getenv('AWS_REGION')
    pdf_path = "pdf.pdf"  # Substitua pelo caminho do seu PDF

    model = BedrockModel(
        model_id="meta.llama3-1-70b-instruct-v1:0",
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key,
        region=region
    )

    # Lendo o conteúdo do PDF
    contexto = model.read_pdf(pdf_path)

    # Gerando o quiz com base no contexto extraído do PDF
    quiz = model.generate_quiz(contexto)

    if quiz:
        print("Quiz gerado:")
        print(json.dumps(quiz, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
