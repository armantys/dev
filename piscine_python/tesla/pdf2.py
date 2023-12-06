import pdfplumber
import shutil
import requests
import re
# Chemin vers le fichier PDF


def read_pdf(local_filename):
    with pdfplumber.open(local_filename) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    return text

# Exemple d'utilisation
pdf_text = read_pdf(r'C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\piscine_python\tesla\report.pdf')
# print(pdf_text)
# # print(pdf_text)
# # Définition de l'expression régulière pour extraire les informations
date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
time_pattern = re.compile(r'(\d{2}:\d{2})')

# # Recherche de toutes les correspondances dans les chaînes
dates = date_pattern.findall(pdf_text)[4:]
times = time_pattern.findall(pdf_text)[:14]
times2 = time_pattern.findall(pdf_text)[-14:]

# # Combinaison des dates et heures correspondantes
combined_datetime = [f"{date} {time} {time2}" for date, time, time2 in zip(dates, times, times2)]

if combined_datetime:
    first_14_combined_datetime = combined_datetime
    print("Les 14 premières dates et heures combinées:", first_14_combined_datetime)
else:
    print("Aucune correspondance trouvée.")

# # columns = ["DATE", "START", "END", "ODOMETER", "DURATION", "kWh USAGE", "COST"]
# # df = pd.DataFrame(matches, columns=columns)

# # Affichage du DataFrame


