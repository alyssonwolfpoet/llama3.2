import os
import boto3
import json
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

# Exemplo de uso
if __name__ == "__main__":
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

    # Contexto para gerar o quiz
    context = (
        "A inteligência artificial (IA) refere-se à simulação de processos de inteligência humana "
        "por meio de sistemas computacionais. Isso inclui aprendizado, raciocínio e autocorreção. "
        "As aplicações de IA variam de assistentes virtuais a sistemas de recomendação."
    )

    # Gerando o quiz com base no contexto
    quiz = model.generate_quiz(context)

    if quiz:
        print("Quiz gerado:")
        print(json.dumps(quiz, indent=2))
