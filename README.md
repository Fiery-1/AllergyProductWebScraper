# Allergen Product Webscraper  

A Python web scraper that identifies allergen-safe products based on a given list of allergies. This tool helps users filter out products that may contain allergens by scraping sites like **boots.com**. Future plans include integrating a web frontend to make it accessible for a wider audience.  

---

## Features  
- ✅ Web scraping using Python to find allergen-safe products.  
- ✅ Customizable input: provide a list of allergens to filter products.  
- 🔄 Future enhancement: Web-based frontend for user-friendly access.  

---

## Installation  

1. Clone the repository:  
```bash
git clone https://github.com/your-username/allergen-product-webscraper.git
cd allergen-product-webscraper
```
   
2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv env  
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install beautifulsoup4 requests
```

## Usage

**!!!THIS DOESN'T WORK YET!!!**

Provide a list of allergens in a text file or directly as input.

Run the script:
```bash
python allergen_finder.py --allergens "allergen1, allergen2, allergen3"
```

Review the output, which includes a list of products that are safe based on the specified allergens.


## Acknowledgments

Special thanks to the developers of the libraries used in this project:

- BeautifulSoup
- Requests
