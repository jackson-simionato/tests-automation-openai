from openai import OpenAI
from src.tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_use_case():
    test_case_pattern = load_file('docs/test_case_pattern.txt')

    system_prompt = f"""
        Você é um especialista em descrever casos de uso. Você deve adotar o padrão abaixo para gerar seu caso de uso:
        {test_case_pattern}

        Considere os dados de entrada sugeridos pelo usuário.
    """

    user_prompt = f"""
        Gere um caso de uso para Ana que deseja realizar login na plataforma Acordelab.
    """

    response = cliente.chat.completions.create(
        model='gpt-4o-mini',
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content