import os
import boto3
import json
from dotenv import load_dotenv
import PyPDF2

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do modelo Bedrock
class Settings:
    llm = boto3.client(
        'bedrock',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
    )

def extrair_texto_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() + "\n"
    return texto.strip()

def gerar_quiz_a_partir_pdf(pdf_content):
    prompt = (
        "Baseado no seguinte conteúdo de PDF, crie um quiz com 5 perguntas de múltipla escolha, "
        "cada uma com 4 opções de resposta. Inclua a resposta correta para cada pergunta:\n\n"
        f"{pdf_content}\n\n"
        "Formato de resposta: JSON."
    )

    try:
        response = Settings.llm.invoke_model(
            modelId='meta.llama3-1-70b-instruct-v1:0',  # ID do modelo que você deseja usar
            body={
                "prompt": prompt,
                "maxTokens": 300,
                "temperature": 0.1,  # Ajuste a temperatura conforme necessário
                "contextSize": 128   # Ajuste o tamanho do contexto
            }
        )
        
        return json.loads(response['body'])  # Retorna a resposta como dicionário
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

def main():
    # Caminho para o arquivo PDF
    pdf_path = "caminho/para/seu/arquivo.pdf"  # Substitua pelo caminho do seu PDF
    
    # Extrair o conteúdo do PDF
    pdf_content = extrair_texto_pdf(pdf_path)
    
    # Gerar o quiz
    quiz = gerar_quiz_a_partir_pdf(pdf_content)
    
    if quiz:
        print("Quiz gerado:", json.dumps(quiz, indent=2))

if __name__ == "__main__":
    main()
