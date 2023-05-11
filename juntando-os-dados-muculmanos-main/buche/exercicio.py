from bs4 import BeautifulSoup    
import requests
import pandas as pd
import streamlit as st

def pegarDadosBuche():
    url = "https://imobiliariaperez.com.br/alugar" # site para extrair
    response = requests.get(url) #request html
    soup = BeautifulSoup(response.content, 'html.parser') #configurao beautifulsoup
    myInfoArray = []
    progress_text = "Carrgando dados, porfavor aguarde."
    my_bar = st.progress(0, text=progress_text)

    links = soup.find_all('a',class_="slide-home-btn")

    progress = 1    

    for link in links:
        
        pushHref = link['href']
        newResponse = requests.get(pushHref)
        newSoup = BeautifulSoup(newResponse.content, 'html.parser') #configurao beautifulsoup
        titleA = newSoup.find('h1', class_= "elementor-heading-title").get_text()
        value = newSoup.find('h2', class_= "elementor-heading-title").get_text() 
        description = newSoup.find_all('p')[3].get_text()
        arrayInfo =  newSoup.find_all('div', class_= "col-6")

        valueArea = arrayInfo[-1].text

        area = valueArea.split()[0] +""+ valueArea.split()[2]

        if value != 'Sob Consulta':
            value += ",00"

        title = titleA.split()[0]   

        aux = [title, value, area.strip(), description]
        myInfoArray.append(aux)

        
        progress_percent = (progress / len(links))
        my_bar.progress(progress_percent, text=progress_text)     
        progress += 1
    
    df = pd.DataFrame(myInfoArray, columns=['Título', 'Aluguel', 'Área', 'Descrição'])
    return df

def gerarCsv(df):
    df.to_csv('scrapImobiliaria.csv', index=False)
