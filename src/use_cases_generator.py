from openai import OpenAI
from src.tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_use_case(user_prompt, model = REFINED_MODEL):
    system_prompt = f"""
        Você é um especialista em descrever casos de uso. Você deve adotar o padrão abaixo para gerar seu caso de uso:
        
        # Formato de Saída
        *Nome da Persona*, em *contexto do app*, precisa realizar *tarefa* no aplicativo. Logo, *benefício esperado*, para isso ela *descrição detalhada da tarefa realizada*.

        Considere os dados de entrada sugeridos pelo usuário e gere caso de uso no formato adequado.
    """

    response = cliente.chat.completions.create(
        model=model,
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content