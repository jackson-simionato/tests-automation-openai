from openai import OpenAI
from src.tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
STATUS_COMPLETED = 'completed'
STATUS_FAILED = 'failed'

def generate_test_case_script(test_case, document, dict_files, assistant, thread, model=STANDARD_MODEL):
    question = f"""
        Você é um especialista em gerar scripts de teste para validar casos de uso e cenários de teste.
        
        Você deve fornecer um script em Python + Selenium e deve utilizar o chromium como driver. 
        Use time.sleep(3) antes de fechar o script.
        Devem ser usadas apenas as bibliotecas em destaque abaixo:

        # Bibliotecas
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        import time

        Consulte a base de arquivos interna buscando: {dict_files[document]}.html, {dict_files[document]}.css e {dict_files[document]}.js.
        Além disso, considere o cenário de teste {test_case} para elaborar o script.

        # Saída
        Script python com comentários em português, objetivos e claros para auxiliar a pessoa desenvolvedora.
    """

    cliente.beta.threads.messages.create(
        thread_id=thread.id,
        role = 'user',
        content = question
    )

    run = cliente.beta.threads.runs.create(
        model=model,
        thread_id=thread.id,
        assistant_id=assistant.id,
        tools=[{'type':'file_search'}]
    )
    
    while run.status != STATUS_COMPLETED:
        run = cliente.beta.threads.runs.retrieve(run.id, thread_id=thread.id)
        print(run.status)

        if run.status == STATUS_FAILED:
            raise Exception('Erro ao gerar caso de uso')
    
    messages = cliente.beta.threads.messages.list(thread_id=thread.id)
    
    return messages.data[0].content[0].text.value