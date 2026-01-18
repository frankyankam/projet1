from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO,
                    filename='france.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

        
def criterias(page, url):
    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )
    try:
        page.wait_for_selector("xpath=//div[@class='pecookies']//pe-cookies-main[button[@id='pecookies-continue-btn']]", timeout=10000)
        page.locator("xpath=//div[@class='pecookies']//pe-cookies-main[button[@id='pecookies-continue-btn']]//button[@id='pecookies-continue-btn']").click()
    except PlaywrightTimeoutError as e:
        logging.info(f"Pas de gestion des cookies nécessaire. {e}")
    
    return page


def loop(page):
    #affichage du nombre d'offres de la page actuelle
    page.mouse.wheel(0, 1200)
    page.wait_for_timeout(2000)
    df=[]
    items= page.locator('xpath=//li[@data-id-offre]').all()
    #current_page= page.locator('xpath=').text_content().strip()
    logging.info(f"Page actuelle avec {len(items)} offres")
    
    #extraire les offres de la page actuelle
    for item in items:
        titre= item.locator('xpath=.//a[@id]//h2[@data-intitule-offre]').text_content().strip() 
        Entreprise=item.locator('xpath=.//div[@class="media-body"]//p[@class="subtext"]').inner_text().strip()
        #adresse=item.locator('xpath=.').text_content().strip()
        lien= item.locator('xpath=.//a').first.get_attribute('href')
        
        emploi={
        'offre': titre,
        'entreprise': Entreprise.split("-")[0].strip(),
        'adresse': Entreprise.split("-",1)[1].strip(),
        'lien de description': lien
        }
        
        df.append(emploi)
    logging.info(f"{len(df)} offres extraites de la page")
        
    return df


def convert_csv(df, output_file):
    df=pd.DataFrame(df)
    df.to_csv(output_file, index=False)
    
def pagination(page):
    
    #cette focton permet de passer a la page suivante pour extraire les offres
    
    try:
        page.wait_for_selector("xpath=//div[@id='zoneAfficherPlus']//a[@data-async-trigger='true']", timeout=10000)
        page.locator("xpath=//div[@id='zoneAfficherPlus']//a[@data-async-trigger='true']").click(force=True)
        #page.wait_for_selector("xpath=")
        page.wait_for_timeout(10000)
        return True
    except PlaywrightTimeoutError as e:
        logging.info(f"Fin de la pagination ou erreur de chargement de la page. page {e}")
        return False
    
def scrappe_france(url = "https://candidat.francetravail.fr/offres/recherche?lieux=01P&motsCles=data+engineer+&offresPartenaires=true&rayon=10&tri=0", output_file='france_jobs.csv'):
    count=0
    offer=[]
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="france_session",
            headless=True,
            slow_mo=80
        )
        

        page = context.new_page()
        
        page_crite = criterias(page, url)
        
        #boucle pour extraire les offres de toutes les pages
        while count<10 :
            
            pagination(page_crite)
    
            emploi= loop(page_crite)
            count=count+1
        #offer.extend(emploi)
                
        
        convert_csv(emploi, output_file)   
        
        
        context.close()
