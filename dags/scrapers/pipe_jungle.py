from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO,
                    filename='jungle.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def criterias(page, url):
    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )
    page.wait_for_timeout(5000)
    
    #//button[@id='axeptio_btn_acceptAll']
    return page
   
def loop(page):
    #affichage du nombre d'offres de la page actuelle
    page.mouse.wheel(0, 1200)
    page.wait_for_timeout(2000)
    df=[]
    items= page.locator('xpath=//li[@data-testid="search-results-list-item-wrapper"]').all()
    current_page= page.locator('xpath=//li[a[@aria-current="true"]]').text_content().strip()
    logging.info(f"Page actuelle: {current_page} avec {len(items)} offres")
    
    #extraire les offres de la page actuelle
    for item in items:
        titre= item.locator('xpath=.//div[a[@role]]//h2').text_content().strip() 
        Entreprise=item.locator('xpath=.//div[span[@class="sc-izXThL fFdRYJ sc-jkYWRr ewxOXb wui-text"]]').text_content().strip()
        adresse=item.locator('xpath=.//div[@variant]//span[@class="sc-hzawhJ jggXUx"]').text_content().strip()
        lien= item.locator('xpath=.//div[@data-role="jobs:thumb"]//a[@role]').first.get_attribute('href')
        
        emploi={
        'offre': titre,
        'entreprise': Entreprise,
        'adresse': adresse,
        'lien de description': lien
        }
        
        df.append(emploi)
    logging.info(f"{len(df)} offres extraites de la page {current_page}")
        
    return df
   
def convert_csv(df, output_file):
    df=pd.DataFrame(df)
    df.to_csv(output_file, index=False)
    
def pagination(page):
    
    #cette focton permet de passer a la page suivante pour extraire les offres
    
    try:
        page.wait_for_selector("xpath=//li[a[@aria-current='true']]/following-sibling::li[1]/a", timeout=20000)
        page.locator("xpath=//li[a[@aria-current='true']]/following-sibling::li[1]/a").click()
        page.wait_for_selector('xpath=//li[@data-testid="search-results-list-item-wrapper"]')
        page.wait_for_timeout(10000)
        return True
    except PlaywrightTimeoutError as e:
        logging.info(f"Fin de la pagination ou erreur de chargement de la page. page {e}")
        return False

def scrappe_jungle(url ="https://www.welcometothejungle.com/fr/jobs?query=Data%20Engineer&aroundQuery=France", output_file='jungle_jobs.csv'):
    
    offer=[]
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="jungle.session",
            headless= True,
            slow_mo=80
        )
        

        page = context.new_page()
        page_jung =criterias(page, url)
         #boucle pour extraire les offres de toutes les pages
        for i in range(15):
            
            emploi= loop(page_jung)
            offer.extend(emploi)
            
    
            if not pagination(page_jung):
                break
        
        convert_csv(offer, output_file)   
        
        context.close()