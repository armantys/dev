from pdfminer.high_level import extract_text
import re

# Chemin vers le fichier PDF
pdf_path = 'report.pdf'

# Extraction du texte du PDF
pdf_text = extract_text(pdf_path)

# Définition de l'expression régulière pour extraire les informations
date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
time_pattern = re.compile(r'(\d{2}:\d{2})')
print (time_pattern)
# Diviser le texte du PDF en pages
pages = pdf_text.split('\x0c')  # '\x0c' est le caractère de saut de page

# Initialiser une liste pour stocker les résultats
combined_datetime = []

# Parcourir chaque page et extraire les dates et heures
for page_text in pages:
    # Recherche de toutes les correspondances dans les chaînes
    # dates = date_pattern.findall(page_text)[4:]
    times = time_pattern.findall(page_text)
    # times2 = time_pattern.findall(page_text)[-23:]

    # Combinaison des dates et heures correspondantes
    combined_datetime.extend([f"{date} {time} {time2}" for date, time, time2 in zip(dates, times, times2)])

# Imprimer les résultats
if combined_datetime:
    print("Dates et heures combinées (en excluant la dernière ligne de chaque page):", combined_datetime)
else:
    print("Aucune correspondance trouvée.")
# columns = ["DATE", "START", "END", "ODOMETER", "DURATION", "kWh USAGE", "COST"]
# df = pd.DataFrame(matches, columns=columns)

# Affichage du DataFrame


