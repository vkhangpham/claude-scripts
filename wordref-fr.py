#!/usr/bin/env python3
"""
WordReference French-English CLI Tool
Usage: python wordref-fr.py [word] [direction]
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
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_translation(word, direction='fr'):
    """Get translation from WordReference with clean formatting"""
    if direction == 'fr':
        url = f"https://www.wordreference.com/fren/{word}"
        print(f"\n{word}")
    else:
        url = f"https://www.wordreference.com/enfr/{word}"
        print(f"\n{word}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
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
        print("-" * 75)
        
        if direction == 'fr':
            print(f"{'Français':<25} {'Contexte':<25} {'Anglais':<25}")
        else:
            print(f"{'Anglais':<25} {'Contexte':<25} {'Français':<25}")
        print("-" * 75)
        
        # Extract translations from table rows
        rows = main_table.find_all('tr')
        count = 0
        
        for row in rows:
            if count >= 6:  # Limit to main translations
                break
                
            cells = row.find_all('td')
            if len(cells) >= 3:  # Need at least 3 columns: French | Explanation | English
                # Column 1: French term + type
                french_cell = cells[0]
                french_term = ""
                french_type = ""
                
                # Get the main French term (usually in bold/strong)
                french_strong = french_cell.find('strong')
                if french_strong:
                    french_term = clean_text(french_strong.get_text())
                
                # Get the grammatical type (usually in italic/em)
                french_em = french_cell.find('em')
                if french_em:
                    french_type = clean_text(french_em.get_text())
                
                # Column 2: French explanation (in parentheses)
                explanation_cell = cells[1]
                explanation = clean_text(explanation_cell.get_text())
                
                # Column 3: English translations
                english_cell = cells[2]
                english_text = clean_text(english_cell.get_text())
                
                # Only show if we have the essential parts
                if french_term and english_text:
                    # Format the French side with distinct grammatical type
                    if french_type:
                        french_display = f"{french_term} [{french_type}]"
                    else:
                        french_display = french_term
                    
                    # Extract and format English grammatical type
                    english_parts = english_text.split()
                    english_term = ""
                    english_type = ""
                    
                    # Look for grammatical type in English (usually the last word if it's a type)
                    if english_parts:
                        # Common grammatical types
                        gram_types = ['interj', 'n', 'v', 'adj', 'adv', 'expr', 'prep', 'conj', 'det']
                        if english_parts[-1] in gram_types:
                            english_type = english_parts[-1]
                            english_term = ' '.join(english_parts[:-1])
                        else:
                            english_term = english_text
                    
                    # Format English with distinct type
                    if english_type:
                        english_display = f"{english_term} [{english_type}]"
                    else:
                        english_display = english_text
                    
                    # Show the main row
                    print(f"{french_display:<25} {explanation:<25} {english_display}")
                    
                    # Look for example sentences in the next row or additional cells
                    # Examples are usually in a separate row or additional cells
                    next_row = row.find_next_sibling('tr')
                    if next_row:
                        example_cells = next_row.find_all('td')
                        if len(example_cells) >= 2:
                            # Check if this looks like an example row
                            example_text = clean_text(example_cells[0].get_text())
                            if example_text and len(example_text) > 15 and not any(tag in example_text.lower() for tag in ['interj', 'expr', 'nm', 'nf']):
                                print(f"    {example_text}")
                                # English example
                                if len(example_cells) > 1:
                                    eng_example = clean_text(example_cells[1].get_text())
                                    if eng_example:
                                        print(f"    {eng_example}")
                    
                    count += 1
                    print()
        
        # Look for inflections
        try:
            inflection_div = soup.find(string=re.compile(r"Inflections"))
            if inflection_div:
                parent = inflection_div.parent
                if parent:
                    inflection_text = clean_text(parent.get_text())
                    if "fpl:" in inflection_text or "mpl:" in inflection_text:
                        print(f"Inflections: {inflection_text}")
        except:
            pass
        
    except requests.RequestException as e:
        print(f"❌ Error accessing WordReference: {e}")
    except Exception as e:
        print(f"❌ Error parsing results: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python wordref-fr.py [word] [direction]")
        print("Direction: fr (French to English, default) or en (English to French)")
        print("Example: python wordref-fr.py bonjour")
        print("Example: python wordref-fr.py hello en")
        sys.exit(1)
    
    word = sys.argv[1]
    direction = sys.argv[2] if len(sys.argv) > 2 else 'fr'
    
    if direction not in ['fr', 'en']:
        print("Direction must be 'fr' (French to English) or 'en' (English to French)")
        sys.exit(1)
    
    get_translation(word, direction)

if __name__ == "__main__":
    main()