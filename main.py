import requests
from bs4 import BeautifulSoup
import os

# Fonction pour télécharger les images d'une page web
def get_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")
    
    if not os.path.exists("scraping_images"):
        os.makedirs("scraping_images")
    
    for image in images:
        image_url = image.get("src")
        if image_url:
            if not image_url.startswith(('http://', 'https://')):
                image_url = requests.compat.urljoin(url, image_url)
            
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                filename = os.path.join("scraping_images", image_url.split('/')[-1])
                with open(filename, "wb") as f:
                    f.write(image_response.content)
                print(f"Image téléchargée : {filename}")
            else:
                print(f"Échec du téléchargement de l'image : {image_url}")

url = "https://books.toscrape.com/catalogue/page-1.html"
get_images(url)
