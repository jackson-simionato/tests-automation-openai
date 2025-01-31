from openai import OpenAI
from src.tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def delete_assistant(assistant_id):
    return cliente.beta.assistants.delete(assistant_id)

def delete_thread(thread_id):
    return cliente.beta.threads.delete(thread_id)

def delete_openai_files(list_files_ids):
    for id in list_files_ids:
        cliente.files.delete(id=id)

def create_thread():
    return cliente.beta.threads.create()

def create_assistant(list_files_ids=[], model=STANDARD_MODEL):
    assistant = cliente.beta.assistants.create(
        name='AcordeLab - QA Automation',
        instructions=f"""
            Assuma que você é um assistente virtual que auxilia um especialista em testes de software a gerar casos de uso e cenários de teste para uma aplicação web.
            Você utiliza a linguagem Python e o pacote Selenium.

            Você deve oferecer suporte abrangente, desde o setup inicial do ambiente de desenvolvimento até a implementação 
            de testes complexos, adotando e consultando principalmente os documentos de sua
            base (para identificar padrões e formas de estruturar os scripts solicitados).

            Consulte sempre os arquivos html, css e js do projeto para elaborar um teste.
            
            Adicionalmente, você deve ser capaz de explicar conceitos chave de 
            testes automatizados e Selenium, fornecer templates de código personalizáveis, e oferecer feedback sobre scripts de teste escritos pelo usuário. 

            O objetivo é facilitar o aprendizado e a aplicação de testes automatizados, 
            melhorando a qualidade e a confiabilidade das aplicações web desenvolvidas.

            Caso solicitado a gerar um script, apenas gere ele sem outros comentários adicionais.

            Você também é um especialista em casos de uso, seguindo os templates indicados.
            E também é um especialista em gerar cenários de teste.
        """,
        tools = [{'type': 'file_search'}],
        file_ids = list_files_ids,
        model=model
    )

    return assistant

def create_file_list_app(folder='AcordeLab'):
    list_files = []
    list_ids = []
    dict_ids = {}

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.css','.js','.html')):
                list_files.append(file)
                
    for file in list_files:
        with open(f'{folder}/{file}', 'rb') as f:
            file_openai = cliente.files.create(
                file=f,
                purpose='assistant'
            )
            list_ids.append(file_openai.id)
            dict_ids[file] = file_openai.id

    use_case_example = 'docs/exemplo_caso_uso.txt'
    
    with open(use_case_example, 'rb') as f:
        file_openai = cliente.files.create(
            file=f,
            purpose='assistant'
        )

    list_ids.append(file_openai.id)
    dict_ids['exemplo_caso_uso.txt'] = file_openai.id 

    return list_ids, dict_ids
