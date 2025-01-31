from openai import OpenAI
from src.tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_test_case(test_case):
    system_prompt = f"""
        Você é um especialista de desenvolvercenários de teste para validar uma aplicação web, quanto a sua navegação e usabilidade.
        Para isso, considere o caso de uso abaixo:
        {test_case}

        Seu caso de teste deve fornecer dados suficientes para validar uma aplicação HTML, CSS e JS. Retringa-se apenas ao passo a passo do cenário de teste.
    """

    response = cliente.chat.completions.create(
        model='gpt-4o-mini',
        messages = [
            {'role': 'system', 'content': system_prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content