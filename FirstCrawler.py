"""
    Esse exemplo cobre:
    * Download de páginas
    * Extração de dados (titulos)
    * Descoberta e Enfileiramento de novos links visitados
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class FirstCrawler:
    def __init__(self, start_url):
        self.visited = set()
        self.to_visit = [start_url]

    def extract_and_print_date(self, soup, base_url):
        # Extrair todos os titulos h1
        for h1 in soup.find_all('h1'):
            print(h1.get_text(f"Título encontrado: {h1.get_text(strip=True)}"))
    
    def enqueue_links(self, soup, base_url):
        # Pegar cada url do site, checar já se foi visitada e se ela não está dentro dos caminhos a serem visitados
        for link in soup.find_all('a'):
            abs_url = urljoin(base_url, link['href'])
            if abs_url not in self.visited and abs_url not in self.to_visit:
                self.to_visit.append(abs_url)
    
    def crawl(self):
        while self.to_visit:
            url = self.to_visit.pop(0)
            print(f"Visiting: {url}")
            try:
                # Envie a solicitação do site *visita
                response = requests.get(url, timeout=10)
                if response.status_code == 200: #Se conseguir acessar o site
                    soup = BeautifulSoup(response.text, 'html.parser') #Captura a html e separa em tags
                    self.extract_and_print_date(soup, url) #Imprime os titulos
                    self. enqueue_links(soup, url) #Procura por ancoras (links) no html
                else: print(f"Failed to retrive {url}")
            except Exception as ex:
                print(f"Error crawling {url}: {ex}")
            self.visited.add(url) # Se der tudo certo adiciona a varivel visitado

if __name__ == "__main__":  #https://scrapingcourse.com/
    crawler = FirstCrawler("https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal")
    crawler.crawl()
