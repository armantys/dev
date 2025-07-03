import requests
import spacy

# Initialisation de l'API TMDb et du modèle spaCy pour le français
API_KEY = 'b7de48a5cda85973dba635c550c317a1'  # Remplacez par votre API Key TMDb
BASE_URL = 'https://api.themoviedb.org/3'
LANGUAGE = 'fr-FR'
nlp = spacy.load("fr_core_news_sm")

# Fonction pour récupérer la liste des genres disponibles
def fetch_genres():
    response = requests.get(f"{BASE_URL}/genre/movie/list", params={
        "api_key": API_KEY,
        "language": LANGUAGE
    })
    
    if response.status_code != 200:
        print(f"Erreur lors de la récupération des genres : {response.status_code}")
        return {}
    
    genres = response.json().get('genres', [])
    return {genre['id']: genre['name'] for genre in genres}

# Récupérer la liste des genres disponibles
genre_dict = fetch_genres()

def fetch_movie_details(movie_title):
    # Rechercher le film par son titre
    response = requests.get(f"{BASE_URL}/search/movie", params={
        "api_key": API_KEY,
        "query": movie_title,
        "language": LANGUAGE
    })
    
    # Vérification de la réponse API
    if response.status_code != 200:
        print(f"Erreur lors de la récupération du film : {response.status_code}")
        return None
    
    results = response.json().get('results', [])
    if not results:
        print(f"Aucun film trouvé pour le titre : {movie_title}")
        return None  # Aucun film trouvé
    
    movie = results[0]  # Prendre le premier film trouvé
    movie_id = movie['id']
    
    # Récupérer les détails du film, y compris les genres
    movie_details_response = requests.get(f"{BASE_URL}/movie/{movie_id}", params={
        "api_key": API_KEY,
        "language": LANGUAGE
    })
    
    if movie_details_response.status_code != 200:
        print(f"Erreur lors de la récupération des détails du film : {movie_details_response.status_code}")
        return None

    movie_details = movie_details_response.json()
    
    # Extraire le titre, résumé et genres
    title = movie_details['title']
    overview = movie_details['overview']
    genres = [genre['name'] for genre in movie_details.get('genres', [])]  # Vérification de l'existence de genres
    
    # Si aucun genre n'est trouvé, affecter un message par défaut
    if not genres:
        genres = ["Genres non disponibles"]
    
    return title, overview, genres, movie_id

def fetch_similar_movies(movie_title, top_n=5):
    # Récupérer les détails du film de base
    movie_details = fetch_movie_details(movie_title)
    
    if not movie_details:
        return f"Le film '{movie_title}' n'a pas été trouvé.", None
    
    title, overview, genres, movie_id = movie_details
    print(f"Film sélectionné : {title}\nRésumé : {overview}")
    print(f"Genres : {', '.join(genres)}")
    
    # Recherche de films similaires à partir de l'API
    similar_movies_response = requests.get(f"{BASE_URL}/movie/{movie_id}/similar", params={
        "api_key": API_KEY,
        "language": LANGUAGE
    })
    
    if similar_movies_response.status_code != 200:
        print(f"Erreur lors de la récupération des films similaires : {similar_movies_response.status_code}")
        return "Erreur lors de la récupération des films similaires.", None
    
    similar_movies = similar_movies_response.json().get('results', [])
    
    if not similar_movies:
        print(f"Aucun film similaire trouvé pour '{title}'.")
    
    similar_movies_list = []
    
    for movie in similar_movies[:top_n]:
        similar_movie_title = movie['title']
        similar_movie_overview = movie['overview']
        similar_movie_genre_ids = movie.get('genre_ids', [])
        
        # Convertir les genre_ids en noms de genres en utilisant le dictionnaire des genres
        similar_movie_genres = [genre_dict.get(genre_id, 'Genre inconnu') for genre_id in similar_movie_genre_ids]
        
        # Si aucun genre n'est trouvé, affecter un message par défaut
        if not similar_movie_genres:
            similar_movie_genres = ["Genres non disponibles"]
        
        # Journalisation pour débogage - Afficher les genres extraits
        print(f"Genres pour le film '{similar_movie_title}': {similar_movie_genres}")
        
        similar_movies_list.append({
            'title': similar_movie_title,
            'overview': similar_movie_overview,
            'genres': similar_movie_genres
        })
    
    return similar_movies_list

# Fonction d'extraction des entités avec spaCy
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def display_similar_movies(movie_title, top_n=5):
    print(f"\nRecherche des films similaires à '{movie_title}'...\n")
    
    # Extraire les entités du film recherché
    movie_details = fetch_movie_details(movie_title)
    if not movie_details:
        print(f"Le film '{movie_title}' n'a pas été trouvé.")
        return
    
    title, overview, genres, movie_id = movie_details
    print(f"Film sélectionné : {title}\nRésumé : {overview}")
    print(f"Genres : {', '.join(genres)}")
    entities = extract_entities(overview)
    print(f"Entités extraites du film '{title}' : {entities}\n")
    
    # Recherche des films similaires
    similar_movies = fetch_similar_movies(movie_title, top_n)
    
    if isinstance(similar_movies, str):  # Si une erreur est retournée (film non trouvé)
        print(similar_movies)
    else:
        print(f"Les {top_n} films les plus similaires à '{movie_title}' sont :\n")
        for idx, movie in enumerate(similar_movies, 1):
            print(f"{idx}. {movie['title']} (Genres: {', '.join(movie['genres'])})")
            print(f"   Description : {movie['overview']}\n")
            # Extraction et affichage des entités pour chaque film
            entities = extract_entities(movie['overview'])
            print(f"   Entités extraites : {entities}\n")

# Exemple d'utilisation
movie_title = "GoldenEye"  # Remplace par le film souhaité
top_n = 5  # Nombre de films similaires à retourner
display_similar_movies(movie_title, top_n)
