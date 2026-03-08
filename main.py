import streamlit as st
import time
import random
import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

# Configuração Profissional
st.set_page_config(page_title="Ciberv31 Shadow", page_icon="", layout="wide")

class Ciberv31Shadow:
    def __init__(self, proxy=None):
        # Lista manual de User-Agents para estabilidade total
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
        self.proxy = proxy
        self.cookie_file = "session_vault.json"

    def _set_options(self):
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument(f"--user-agent={random.choice(self.ua_list)}")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        
        # AJUSTE DE RESOLUÇÃO: Garante que o site renderize links e imagens
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--start-maximized")
        
        if self.proxy:
            try:
                ip, porta, user, pwd = self.proxy.split(':')
                opts.add_argument(f'--proxy-server={ip}:{porta}')
            except: pass
        return opts

    def run_session(self, url):
        driver = None
        try:
            opts = self._set_options()
            # Caminhos para o Chromium no Streamlit Cloud
            paths = ["/usr/bin/chromium", "/usr/bin/chromium-browser"]
            
            success = False
            for path in paths:
                try:
                    service = Service(path)
                    driver = webdriver.Chrome(service=service, options=opts)
                    success = True
                    break
                except: continue
            
            if not success:
                driver = webdriver.Chrome(options=opts)
            
            # Evasão de detecção (Stealth)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
            
            driver.get(url)
            
            # TEMPO DE ESPERA AUMENTADO: Para carregar conteúdos dinâmicos e links
            time.sleep(random.uniform(15, 25)) 
            
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file, 'r') as f:
                    for c in json.load(f):
                        try: driver.add_cookie(c)
                        except: pass
                driver.refresh()
                time.sleep(5)

            driver.save_screenshot("shadow_session.png")
            with open(self.cookie_file, 'w') as f:
                json.dump(driver.get_cookies(), f)
                
            return {"status": "Ativo", "img": "shadow_session.png", "url": driver.current_url}
        except WebDriverException as e:
            return {"status": "Erro", "msg": f"Erro no WebDriver: {str(e)}"}
        except Exception as e:
            return {"status": "Erro", "msg": str(e)}
        finally:
            if driver:
                try: driver.quit()
                except: pass

# --- UI INTERFACE ---
st.title(" Ciberv31 Shadow Framework")
target = st.text_input("URL Alvo:", value="https://superbet.bet.br")
proxy_addr = "91.123.10.151:6693:flashproxys718:nosindique777"

if st.button(" INICIAR SHADOW BYPASS"):
    shadow = Ciberv31Shadow(proxy_addr)
    with st.spinner("Executando Protocolo de Evasão Profunda..."):
        res = shadow.run_session(target)
        if res["status"] == "Ativo":
            st.success(f"Conexão Ativa em: {res['url']}")
            st.image(res["img"])
        else:
            st.error(f"Falha Técnica: {res['msg']}")

# Ferramentas de Auditoria
col1, col2 = st.columns(2)
with col1:
    if st.button(" SCAN HEADERS"):
        try:
            r = requests.get(target)
            st.json(dict(r.headers))
        except Exception as e:
            st.error(f"Erro ao scanear headers: {str(e)}")
with col2:
    if st.button(" CLEAN VAULT"):
        if os.path.exists("session_vault.json"):
            os.remove("session_vault.json")
            st.warning("Cookies removidos.")
