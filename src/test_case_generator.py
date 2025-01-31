from openai import OpenAI
from src.tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
STATUS_COMPLETED = 'completed'
STATUS_FAILED = 'failed'

def generate_test_case(test_case, document, dict_files, assistant, thread, model=STANDARD_MODEL):
    question = f"""
        Você é um especialista de desenvolvercenários de teste para validar uma aplicação web, quanto a sua navegação e usabilidade.
        Para isso, considere o caso de uso abaixo:
        {test_case}

        Você deve também utilizar os documentos enviados pelo usuário para elaborar o cenário de teste.
        Consulte a base de arquivos interna buscando: {dict_files[document]}.html, {dict_files[document]}.css e {dict_files[document]}.js.

        Seu caso de teste deve fornecer dados suficientes para validar uma aplicação web, considerando implementação com Python e Selenium.
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