from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

@app.route('/SefazEntry', methods=['POST'])
def criar_nota():
    data = request.json
    if not data:
        return jsonify({'message': 'Bad request, missing form'}), 400

    # Lógica para criar a nota usando o Selenium
    try:
        SefazEntry(data)
        return jsonify({'message': 'Nota criada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao criar nota: {str(e)}'}), 500


def SefazEntry(data):
    options = Options()
    options.binary_location = "/opt/firefox/firefox"
    service = Service('/usr/local/bin/geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get('https://www.sefaz.rs.gov.br/nfa/nfe-nfa-mei.aspx')
    time.sleep(2)

    wait = WebDriverWait(driver, 30)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

    cpf_field = wait.until(EC.presence_of_element_located((By.NAME, "cpf")))
    cpf_field.send_keys(data['cpf'])

    data_field = wait.until(EC.presence_of_element_located((By.NAME, "datanasc")))
    data_field.send_keys(data['datanasc'])

    CNPJ_field = wait.until(EC.presence_of_element_located((By.NAME, "cnpj")))
    CNPJ_field.send_keys(data['cnpj'])

    name_check = wait.until(EC.presence_of_element_located((By.ID, "rdNomeMae")))
    name_check.click()

    nome_mae_field = wait.until(EC.presence_of_element_located((By.NAME, "nomemae")))
    nome_mae_field.send_keys(data['nomemae'])

    next_check = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
    next_check.click()

    time.sleep(5)

    main_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    try:
        alert = wait.until(EC.alert_is_present())
        alert.accept()
    except:
        pass

    try:
        alert = wait.until(EC.alert_is_present())
        alert.accept()
    except:
        pass

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "frmDados")))
    time.sleep(2)
    try:
        ok_check = wait.until(EC.presence_of_element_located((By.ID, "btSim")))
        ok_check.click()
    except:
        pass

if __name__ == '__main__':
    app.run(debug=True)
