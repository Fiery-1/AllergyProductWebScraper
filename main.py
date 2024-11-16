from bs4 import BeautifulSoup
import requests
import re
# Set Parser and Headers
parser = 'html.parser'
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
}

# Choose URL:
url = "https://www.boots.com/plantur-21-long-hair-shampoo-200ml-10307642"
# -----------------------------------------------------------------------


# TODO: Make it automatically detect this domain.
website_name = "boots.com"

# Getting HTML data
def get_required_tag(soup_obj,domain_name):
    try:
        if domain_name == "boots.com":
            tag = soup_obj.find('h3', id="product_ingredients").find_next('p')

            return tag
        else:
            print("Please use a compatible website.")

    except AttributeError as e:
        print(f"Couldn't find ingredients on {domain_name}!")
        print(f"Error: {e}")
        exit()
def most_frequent(arr):
    return max(set(arr), key=arr.count)
def get_html_txt(address):
    try:
        response = requests.get(address, headers=headers)
        response.raise_for_status()  # checks for http error if occurred.
        html_data = response.text
        print(f"[DEBUG] Successfully read data from {address}!")
        return html_data
    except requests.exceptions.RequestException as e:
        print(f"Error reading data: from {address}\nError:{e}")

# Data cleaning
def clean_up(string):
    return re.sub(r'\s+', ' ', string).strip().upper()
def normalise_list(array):
    normalised_list = {}
    for item in array:
        components = item.split('/')  # Split combined values like "AQUA/WATER"
        for comp in components:
            normalised_list[comp.strip().upper()] = item  # Map each component to its original values
    return normalised_list

# Detects all possible delimiters in a string of text
def detect_delimiters(string):
    delimiter_list = []
    for i, letter in enumerate(string):
        if letter.isalnum() or letter.isspace():
            continue
        else:
            before = string[i - 1] if i > 0 else None  # Check if there's a previous letter
            after = string[i + 1] if i < len(string) - 1 else None  # Check if there's a next letter
            # print(f"'{letter}' is not alphanum. Before: '{before}', After: '{after}'")
            if before is not None and after == ' ':
                # print(f"Delimiter should be {letter}.")
                delimiter_list.append(letter)
    return delimiter_list


# Create soup object using html.parser
html = get_html_txt(url)
soup = BeautifulSoup(html, parser)

# Find the ingredients section
ingredientsTag = get_required_tag(soup, website_name)

#Get text only from the tag
textIngredients = ingredientsTag.text
# Clean text for using in algorithm
textIngredients = clean_up(textIngredients)

print(f"[DEBUG] Cleaned up text: {textIngredients}")



delimiters_found = detect_delimiters(textIngredients)
delimiter = most_frequent(delimiters_found)
print(f"[DEBUG] Delimiter is: {delimiter}\n")

listIngredients = [
    re.sub(r'\\+', '/', re.sub(r'\s*/\s*', '/', item.strip()))  # Replace \ with / and clean spaces around /
    # has to happen after delimiter check incase it was a delimiter
    for item in textIngredients.split(delimiter) if item.strip()
]

# Normalise the ingredients for allergy detection
productAllergenList = normalise_list(listIngredients)

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
detectedAllergens = []
safe = True
for allergy in allergyList:
    if allergy in productAllergenList:
        ingredient = productAllergenList[allergy].title()
        print(f"Allergy Found! Contains: {ingredient}")
        detectedAllergens.append(ingredient)
        safe = False

if safe:
    print("\nProduct is SAFE for you to use! :)")

else:
    print("\nProduct is UNSAFE for you to use!")
    print("Contains: " + str(detectedAllergens))
