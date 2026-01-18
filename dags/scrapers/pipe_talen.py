from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO,
                    filename='talent.log',
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
    items= page.locator('xpath=//div[@class="sc-8e83a395-0 cuSEPQ"]//section[@data-testid]').all()
    current_page= page.locator('xpath=//nav[@aria-label="Pagination"]//a[@class="sc-fcd630a4-5 sc-fcd630a4-6 sc-9939acc6-1 kLmScU hTALns gSKnXL"]').text_content().strip()
    logging.info(f"Page actuelle: {current_page} avec {len(items)} offres")
    
    #extraire les offres de la page actuelle
    for item in items:
        titre= item.locator('xpath=.//div[@data-testid="JobCardContainer"]//h2').text_content().strip() 
        Entreprise=item.locator('xpath=.//div[@data-testid="JobCardContainer"]//span[@color="#691F74"]').text_content().strip()
        adresse=item.locator('xpath=.//div[@data-testid="JobCardContainer"]//span[@color="#222222"]').text_content().strip()
        lien= item.locator('xpath=.//div[@data-testid="JobCardContainer"]//a').first.get_attribute('href')
        
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
        page.wait_for_selector('xpath=//nav[@aria-label="Pagination"]//a[@class="sc-fcd630a4-5 sc-fcd630a4-6 sc-9939acc6-1 kLmScU hTALns gSKnXL"]/following-sibling::a[1]', timeout=10000)
        page.locator('xpath=//nav[@aria-label="Pagination"]//a[@class="sc-fcd630a4-5 sc-fcd630a4-6 sc-9939acc6-1 kLmScU hTALns gSKnXL"]/following-sibling::a[1]').click()
        page.wait_for_selector('xpath=//div[@class="sc-8e83a395-0 cuSEPQ"]//section[@data-testid]')
        page.wait_for_timeout(10000)
        return True
    except PlaywrightTimeoutError as e:
        logging.info(f"Fin de la pagination ou erreur de chargement de la page. page {e}")
        return False

    
def scrappe_talen (url = "https://fr.talent.com/jobs?k=data&l=France&id=f5d5829db967", output_file='talent.csv'):
    offer=[]
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="talent_session",
            headless=True,
            slow_mo=80
        )
        
        #//button[@id='hw-cc-notice-accept-btn']
        #//button[@aria-label="Fermer la fenêtre modale"]

        page = context.new_page()
        
        page_crite = criterias(page, url)
        
        #boucle pour extraire les offres de toutes les pages
        for i in range(4):
            
            emploi= loop(page_crite)
            offer.extend(emploi)
            
    
            if not pagination(page_crite):
                break
        
        convert_csv(offer, output_file)   
        
        context.close()