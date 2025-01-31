from openai import OpenAI
from src.tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_test_case_script(use_case, test_case):
    company_doc = load_file('docs/acorde_lab.txt')

    system_prompt = f"""
        Você é um especialista em gerar scripts de teste para validar casos de uso e cenários de teste.
        Considere o contexto da empresa disponível em: {company_doc}

        Você deve fornecer um script em Python + Selenium e deve utilizar o chromium como driver. 
        Não use headless. Use time.sleep(3) antes de fechar o script.
        Devem ser usadas apenas as bibliotecas em destaque abaixo:

        # Bibliotecas
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        import time
    """

    user_prompt = f"""
        Considere o caso de uso {use_case} e o cenário de teste {test_case}.

        Crie um script para gerar um teste automatizado.
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