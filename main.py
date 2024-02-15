import requests
from bs4 import BeautifulSoup
import phonenumbers 
from phonenumbers import geocoder, carrier, timezone
import re
import json

# fonction
def pseudo_osint(pseudo):
    # GitHub
    url_github = f"https://github.com/{pseudo}"
    try:
        response_github = requests.get(url_github)
        if response_github.status_code == 200:
            print(f"Le profil GitHub pour '{pseudo}' existe : {url_github}")
        else:
            print(f"[x] : Aucun profil GitHub trouvé pour '{pseudo}'.")
    except Exception as e:
        print(f"Erreur lors de la tentative d'accès à GitHub pour '{pseudo}': {e}")
    # twitter(x)
    url_twitter = f"https://twitter.com/{pseudo}"
    try:
        response_twitter = requests.get(url_twitter)
        if response_twitter.status_code == 200:
            print(f"Le profil twitter pour '{pseudo}' existe : {url_twitter}")
            target_tag = "span"
            target_class = "css-1qaijid r-bcqeeo r-qvutc0 r-poiln3"
            url = url_twitter
            infos = get_info_from_webpage(url, target_tag, target_class)
            if infos:
                for info in infos:
                    print("a rejoint twitter en  :" + info)
        else:
            print(f"[x] : Aucun profil twitter trouvé pour '{pseudo}'.")
    except Exception as e:
        print(f"Erreur lors de la tentative d'accès à twitter pour '{pseudo}': {e}")
    # speedrun.com 
    url_speedrun = f"https://www.speedrun.com/users/{pseudo}"
    try:
        response_speedrun = requests.get(url_speedrun)
        if response_speedrun.status_code == 200:
            print(f"Le profil speedrun.com pour '{pseudo}' existe : {url_speedrun}")
            target_tag = "div"
            target_class = "inline-flex flex-row items-center justify-start gap-1 text-sm font-normal text-foreground"
            url = url_speedrun
            infos = get_info_from_webpage(url, target_tag, target_class)
            if infos:
                for info in infos:
                    print("info lie a speedrun.com : ")
                    print("loc_speedrun.com :" + info + "\n")
        else:
            print(f"[x] : Aucun profil speedrun.com trouvé pour '{pseudo}'.")
    except Exception as e:
        print(f"Erreur lors de la tentative d'accès à speedrun.com pour '{pseudo}': {e}")
    print("test de masse : \n")
    file_path = 'sites.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
        urls = data['urls']
    userId = pseudo
    email = mail
    # Expression régulière pour chercher nom, prenom, et email
    regex_patterns = [
        re.compile(re.escape(nom), re.IGNORECASE),
        re.compile(re.escape(prenom), re.IGNORECASE),
        re.compile(re.escape(email), re.IGNORECASE)
    ]
    # Parcourir chaque URL, insérer la variable et envoyer la requête GET
    for url in urls:
        # Format l'URL avec la variable userId
        formatted_url = url.format(userId)
        
        try:
            # Envoi de la requête GET
            response = requests.get(formatted_url)
            
            # Vérifier si la requête a réussi
            if response.status_code == 200:
                print(f"Requête réussie à {formatted_url}")
                # Utiliser BeautifulSoup pour parser le contenu HTML
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Convertir le soup en texte pour une recherche simplifiée
                text = soup.get_text()
                # Parcourir chaque pattern et chercher dans le texte
                for pattern in regex_patterns:
                    if pattern.search(text):
                        print(f"        L'info : '{pattern.pattern}' a etait trouver dans le contenu de la page.")
                        
        except requests.RequestException as e:
            print(f"Erreur de requête à {formatted_url}: {e}")

def get_info_from_webpage(url, target_tag, target_class):
    # Récupérer le contenu HTML de la page
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # Trouver tous les éléments correspondant à la balise et à la classe cibles
        target_elements = soup.find_all(target_tag, class_=target_class)
        # Récupérer les informations souhaitées
        info_list = []
        for element in target_elements:
            info_list.append(element.text.strip())
        return info_list
    else:
        print("Erreur lors de la récupération de la page :", response.status_code)
        return None

def analyze_phone_number(num):
    # Parse le numéro de téléphone
    number = phonenumbers.parse(num)
    
    # Obtient le pays du numéro
    country = geocoder.description_for_number(number, "fr")
    
    # Obtient l'opérateur du numéro
    operator = carrier.name_for_number(number, "fr")
    
    # Obtient le fuseau horaire du numéro
    tz = timezone.time_zones_for_number(number)
    
    return {
        "phone_number": num,
        "country": country,
        "operator": operator,
        "time_zone": tz
    }

def check_websites(company_name):
    available_websites = []
    
    for tld in tlds:
        url = f"http://{company_name}{tld}"
        try:
            response = requests.get(url, timeout=5)
            # Si le code de statut est inférieur à 400, le site est considéré comme disponible
            if response.status_code < 400:
                available_websites.append(url)
        except requests.RequestException as e:
            # Gère les exceptions pour les requêtes échouées (site inaccessible, etc.)
            print(f"Erreur lors de la vérification de {url}: {e}")
    
    return available_websites

def entreprise_osint(entreprise):
    url_xing = f"https://www.xing.com/pages/{entreprise}"
    try:
        response_xing = requests.get(url_xing)
        if response_xing.status_code == 200:
            print(f"L'entreprise pour '{entreprise}' existe : {url_xing}")
        else:
            print(f"[x] : Aucune entreprise trouvé pour '{entreprise}'.")
    except Exception as e:
        print(f"Erreur lors de la tentative d'accès à GitHub pour '{pseudo}': {e}")

# Program :
# Liste des domaines de premier niveau à tester
tlds = ['.com', '.fr', '.tv', '.ru', '.ch']
print("demande d'info :\n")
nom = input("nom : ")
prenom = input("prenom : ")
adresse = input("adresse : ")
pseudo = input("pseudo : ")
mail = input("mail : ")
num = input("num: ")
entreprise = input("entreprise: ")
company_name = entreprise
websites = check_websites(company_name)
print("\nSites web disponibles au nom de l'entreprise :\n")
for website in websites:
    print(website)
url = f"https://www.speedrun.com/users/{pseudo}"
print("")
print("site atacher au pseudo : \n")
pseudo_osint(pseudo)
print()
print("information de num : \n") 
info_num = analyze_phone_number(num)
print(info_num)
print()
print("informatioon sur l'entreprise : \n")
entreprise_osint(entreprise)
print("\n")
print("site recomande :\n")
print("https://whatsmyname.app/")
print("https://www.numlookup.com/")
