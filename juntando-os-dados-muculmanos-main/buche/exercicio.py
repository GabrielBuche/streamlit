from bs4 import BeautifulSoup    
import requests
import pandas as pd
import streamlit as st

import re

from geopy.geocoders import Nominatim

def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="my-geocode-addres")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    if location is not None:
        return location.address
    else:
        return None

def pegarDadosBuche():
    regex = r'q=(-?\d+\.\d+),(-?\d+\.\d+)'
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
        div_element = newSoup.find('div', class_="elementor-custom-embed")

        if div_element:
            iframe_element = div_element.find('iframe') 
            if iframe_element and 'src' in iframe_element.attrs:
                iframe_src = iframe_element['src']  
                match = re.search(regex, iframe_src)
                if match:
                    latitude = match.group(1)
                    longitude = match.group(2)  


        valueArea = arrayInfo[-1].text

        area = valueArea.split()[0] +""+ valueArea.split()[2]

        if value != 'Sob Consulta':
            value += ",00"

        title = titleA.split()[0]   

        endereco = get_address(latitude, longitude)

        aux = [title, value, endereco, area.strip(), description, latitude, longitude]
        myInfoArray.append(aux)

        
        progress_percent = (progress / len(links))
        my_bar.progress(progress_percent, text=progress_text)     
        progress += 1
    
    df = pd.DataFrame(myInfoArray, columns=['Título', 'Aluguel', 'Endereco', 'Área', 'Descrição', 'Latitude', 'Longitude'])
    return df

def gerarCsv(df):
    df.to_csv('scrapImobiliaria.csv', index=False)
