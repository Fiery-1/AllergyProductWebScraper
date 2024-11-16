import time

from bs4 import BeautifulSoup
import re
import requests
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
}
url = "https://www.boots.com/batiste-dry-shampoo-original-350ml-10297620"
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_data = response.text
    print("Successfully Read Data!")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    time.sleep(1)

# Open and parse the HTML file

soup = BeautifulSoup(html_data, 'html.parser')
def most_frequent(List):
    return max(set(List), key=List.count)
# Find the ingredients section
ingredientsLabelId = "product_ingredients"
try:
    tagIngredients = soup.find('h3', id=ingredientsLabelId).find_next('p')
except AttributeError as e:
    print("Couldn't find ingredients on this page!")
    exit()
# print(tagIngredients)
# Extract and clean the ingredients text
textIngredients = tagIngredients.text

textIngredients = re.sub(r'\s+', ' ', textIngredients).strip().upper()
print(textIngredients)
delimiterCount = []
# textIngredients = """1199524 C, Aqua / Water, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Dimethicone, Sodium Chloride, Parfum / Fragrance, CI 77891 / Titanium Dioxide, Guar Hydroxypropyltrimonium Chloride, Niacinamide, Ricinus Communis Seed Oil / Castor Seed Oil, Mica, Coco Betaine, Sodium Benzoate, Sodium Hydroxide, Hydroxycitronellal, Hydrolyzed Corn Protein, Hydrolyzed Soy Protein, Hydrolyzed Wheat Protein, Hydroxypropyltrimonium Hydrolyzed Wheat Protein, Phenoxyethanol, Steareth-6, Acetic Acid, PEG-100 Stearate, Trideceth-10, Trideceth-3, Salicylic Acid, Limonene, Fumaric Acid, Panthenol, Benzyl Salicylate, Linalool, Benzyl Alcohol, Amodimethicone, Alpha-Isomethyl Ionone, Carbomer, Geraniol, Citric Acid, Citronellol, Coumarin, Hexylene Glycol, Hexyl Cinnamal, Glycerin, Glycol Distearate, (F.I.L. C215722/2)"""
for i, letter in enumerate(textIngredients):
    if letter.isalnum() or letter.isspace():
        continue
    else:
        before = textIngredients[i - 1] if i > 0 else None  # Check if there's a previous letter
        after = textIngredients[i + 1] if i < len(textIngredients) - 1 else None  # Check if there's a next letter
        # print(f"'{letter}' is not alphanum. Before: '{before}', After: '{after}'")
        if before is not None and after == ' ':
            # print(f"Delimiter should be {letter}.")
            delimiterCount.append(letter)

delimiter = most_frequent(delimiterCount)
print(f"Delimiter is: {delimiter}")
listIngredients = [
    re.sub(r'\\+', '/', re.sub(r'\s*/\s*', '/', item.strip()))  # Replace \ with / and clean spaces around /
    for item in textIngredients.split(delimiter) if item.strip()
]
# print(textIngredients)
# print(listIngredients)
# Normalize the ingredients for allergy detection
normalizedIngredients = {}
for ingredient in listIngredients:
    components = ingredient.split('/')  # Split combined ingredients like "AQUA/WATER"
    for comp in components:
        normalizedIngredients[comp.strip().upper()] = ingredient  # Map each component to its original ingredient

# Ask the user for allergies
allergyList = []
allergy = ""
while allergy.upper() not in ["EXIT", "STOP"]:
    allergy = input("Enter allergy (EXIT/STOP): ")
    if allergy.upper() not in ["EXIT", "STOP"]:
        allergyList.append(allergy.upper())

# Check for allergies
print("\nIngredients List:", listIngredients)
print("Allergy List:", allergyList)

safe = True
for allergy in allergyList:
    if allergy in normalizedIngredients:
        print(f"Allergy Found! Contains: {normalizedIngredients[allergy]}")
        safe = False

if safe:
    print("\nProduct is SAFE for you to use! :)")
else:
    print("\nProduct is UNSAFE for you to use!")
