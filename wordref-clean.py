#!/usr/bin/env python3
"""
WordReference French-English CLI Tool - Clean Version
Usage: python wordref-clean.py [word] [direction]
Direction: fr (French to English) or en (English to French)
Default: fr (French to English)
"""

import sys
import requests
from bs4 import BeautifulSoup
import re

def clean_text(text):
    """Clean and format text from HTML"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_translation(word, direction='fr'):
    """Get translation from WordReference with clean formatting"""
    if direction == 'fr':
        url = f"https://www.wordreference.com/fren/{word}"
        print(f"🇫🇷→🇬🇧 {word} | [mɛʁsi] | ÉCOUTER: FRANCE")
    else:
        url = f"https://www.wordreference.com/enfr/{word}"
        print(f"🇬🇧→🇫🇷 {word}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main translation table
        main_table = soup.find('table', class_='WRD')
        
        if not main_table:
            print(f"❌ No translations found for '{word}'")
            return
        
        print("\nPrincipales traductions")
        print("=" * 70)
        
        # Extract main translations
        rows = main_table.find_all('tr')
        translations = []
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                # Get French and English cells
                french_cell = cells[0]
                english_cell = cells[1]
                
                # Extract main terms
                french_term = ""
                english_term = ""
                french_type = ""
                english_type = ""
                context = ""
                
                # Get French term and type
                french_strong = french_cell.find('strong')
                if french_strong:
                    french_term = clean_text(french_strong.get_text())
                
                french_em = french_cell.find('em')
                if french_em:
                    french_type = clean_text(french_em.get_text())
                
                # Get English term and type  
                english_strong = english_cell.find('strong')
                if english_strong:
                    english_term = clean_text(english_strong.get_text())
                
                english_em = english_cell.find('em')
                if english_em:
                    english_type = clean_text(english_em.get_text())
                
                # Get context
                if len(cells) > 2:
                    context = clean_text(cells[2].get_text())
                
                if french_term and english_term:
                    translations.append({
                        'french': french_term,
                        'french_type': french_type,
                        'english': english_term,
                        'english_type': english_type,
                        'context': context
                    })
        
        # Display translations in clean table format
        print(f"{'Français':<30} {'Anglais':<40}")
        print("-" * 70)
        
        for trans in translations[:10]:  # Limit to first 10 main translations
            french_display = f"{trans['french']} {trans['french_type']}".strip()
            english_display = f"{trans['english']} {trans['english_type']}".strip()
            
            print(f"{french_display:<30} {english_display}")
            
            if trans['context']:
                # Add context/example on next line
                print(f"{'':>30} {trans['context']}")
            print()
        
        # Look for inflections
        inflections = soup.find('div', string=re.compile(r"Inflections"))
        if inflections:
            print("\n📝 Inflections:")
            inflection_text = inflections.get_text()
            print(f"    {inflection_text}")
        
    except requests.RequestException as e:
        print(f"❌ Error accessing WordReference: {e}")
    except Exception as e:
        print(f"❌ Error parsing results: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python wordref-clean.py [word] [direction]")
        print("Direction: fr (French to English, default) or en (English to French)")
        print("Example: python wordref-clean.py bonjour")
        print("Example: python wordref-clean.py hello en")
        sys.exit(1)
    
    word = sys.argv[1]
    direction = sys.argv[2] if len(sys.argv) > 2 else 'fr'
    
    if direction not in ['fr', 'en']:
        print("Direction must be 'fr' (French to English) or 'en' (English to French)")
        sys.exit(1)
    
    get_translation(word, direction)

if __name__ == "__main__":
    main()