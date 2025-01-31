from openai import OpenAI
from src.tools import *
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
STATUS_COMPLETED = 'completed'
STATUS_FAILED = 'failed'

def generate_use_case(user_prompt, assistant, thread, model=STANDARD_MODEL):
    question = f"""
        Gere um caso de uso para: {user_prompt}

        Busque nos arquivos associados a você o conteúdo de exemplo de casos de uso (arquivo exemplos_casos_uso.txt).

        Adote o seguinte template para gerar o caso de uso:        

        # Formato de Saída
        *Nome da Persona*, em *contexto do app*, precisa realizar *tarefa* no aplicativo. Logo, *benefício esperado*, para isso ela *descrição detalhada da tarefa realizada*.
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