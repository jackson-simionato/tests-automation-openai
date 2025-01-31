### Observações:
#1. **Substitua os seletores**: As localizações de elementos (como `By.NAME`, `By.ID`, `By.LINK_TEXT`, etc.) devem ser ajustadas de acordo com a estrutura real da página do AcordeLab.
#2. **Caminho do ChromeDriver**: Certifique-se de fornecer o caminho correto para o seu executável do ChromeDriver.
#3. **Validação de Erros**: Para validar cenários de erro, você pode adicionar testes adicionais que inserem credenciais inválidas e verificam as mensagens de erro.
#4. **Responsividade**: Para verificar a responsividade, você pode alterar o tamanho da janela do navegador durante o teste e verificar se os elementos ainda são acessíveis.

# Bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without GUI (necessary in WSL)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1. Acessar o Aplicativo
    driver.get('https://almsantana.github.io/')  # Substitua pela URL correta do AcordeLab
    time.sleep(3)  # Aguardar o carregamento da página

    # 2. Localizar a Tela de Login
    # Verifica se a página inicial é carregada corretamente
    assert "AcordeLab" in driver.title  # Verifique se o título da página contém "AcordeLab"
    print(driver.title)

    # 3. Inserir Credenciais
    # Na tela de login, localizar o campo para inserir o e-mail
    email_field = driver.find_element(By.ID, 'email')  # Ajuste o nome do campo conforme necessário
    email_field.send_keys('email@acordelab.com.br')  # E-mail de teste

    # Localizar o campo para inserir a senha
    password_field = driver.find_element(By.ID, 'senha')  # Ajuste o nome do campo conforme necessário
    password_field.send_keys('123senha')  # Senha de teste

    # 4. Clicar no Botão "Entrar"
    login_submit_button = driver.find_element(By.CLASS_NAME, 'botao-login')  # Ajuste o XPath conforme necessário
    login_submit_button.click()
    time.sleep(3)

    # 5. Verificar a Autenticação
    # Aguardar o redirecionamento após o clique no botão "Entrar"
    assert "Home - AcordeLab" in driver.title  # Verifique se o título da página inicial é exibido
    print(driver.title)

    # 6. Visualizar Informações Personalizadas
    # Verificar se os projetos de Ana estão visíveis na página inicial
    projects_section = driver.find_element(By.CLASS_NAME, 'course-grid')  # Ajuste o ID conforme necessário
    assert projects_section.is_displayed()  # Verifica se a seção de projetos está visível

    # Confirmar a presença de elementos que indicam que Ana está logada
    user_name = driver.find_element(By.CLASS_NAME, 'meu-perfil')  # Ajuste o ID conforme necessário

finally:
    # Espera antes de fechar o navegador
    time.sleep(3)
    driver.quit()

