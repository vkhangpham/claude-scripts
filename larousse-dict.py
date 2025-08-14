#!/usr/bin/env python3
"""
Larousse French-French Dictionary CLI Tool
Beautiful terminal output with comprehensive French definitions
"""

import sys
import requests
from bs4 import BeautifulSoup
import re
from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
from rich.panel import Panel
from tool_cache import ToolCache, show_all_cache_stats, clear_all_caches, cleanup_expired_all

console = Console()

# Initialize Larousse cache
lr_cache = ToolCache('larousse', max_age_days=14)  # Cache for 14 days

def clean_text(text):
    """Clean and format text from HTML"""
    if not text:
        return ""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove unwanted symbols
    text = text.replace('⇒', '').replace('▷', '')
    return text

def highlight_larousse_indicators(text):
    """Highlight common Larousse dictionary indicators and markers"""
    # Style and register markers
    style_markers = [
        'Littéraire', 'littéraire',
        'Familier', 'familier', 
        'Populaire', 'populaire',
        'Soutenu', 'soutenu',
        'Vieilli', 'vieilli',
        'Argotique', 'argotique',
        'Péjoratif', 'péjoratif',
        'Ironique', 'ironique',
        'Plaisant', 'plaisant',
        'Vulgaire', 'vulgaire'
    ]
    
    # Semantic relationship indicators
    semantic_markers = [
        'Synonymes', 'synonymes', 'Synonyme', 'synonyme',
        'Contraires', 'contraires', 'Contraire', 'contraire',
        'Antonymes', 'antonymes', 'Antonyme', 'antonyme'
    ]
    
    # Domain and field markers (comprehensive list)
    domain_markers = [
        'Botanique', 'botanique',
        'Zoologie', 'zoologie', 
        'Médecine', 'médecine',
        'Anatomie', 'anatomie',
        'Physiologie', 'physiologie',
        'Psychologie', 'psychologie',
        'Philosophie', 'philosophie',
        'Religion', 'religion',
        'Théologie', 'théologie',
        'Liturgie', 'liturgie',
        'Histoire', 'histoire',
        'Géographie', 'géographie',
        'Politique', 'politique',
        'Économie', 'économie',
        'Droit', 'droit',
        'Juridique', 'juridique',
        'Militaire', 'militaire',
        'Marine', 'marine',
        'Aviation', 'aviation',
        'Automobile', 'automobile',
        'Technique', 'technique',
        'Technologie', 'technologie',
        'Informatique', 'informatique',
        'Physique', 'physique',
        'Chimie', 'chimie',
        'Mathématiques', 'mathématiques',
        'Géométrie', 'géométrie',
        'Astronomie', 'astronomie',
        'Astrologie', 'astrologie',
        'Météorologie', 'météorologie',
        'Géologie', 'géologie',
        'Minéralogie', 'minéralogie',
        'Agriculture', 'agriculture',
        'Horticulture', 'horticulture',
        'Cuisine', 'cuisine',
        'Gastronomie', 'gastronomie',
        'Mode', 'mode',
        'Couture', 'couture',
        'Arts', 'arts',
        'Peinture', 'peinture',
        'Sculpture', 'sculpture',
        'Musique', 'musique',
        'Danse', 'danse',
        'Théâtre', 'théâtre',
        'Cinéma', 'cinéma',
        'Littérature', 'littérature',
        'Poésie', 'poésie',
        'Architecture', 'architecture',
        'Héraldique', 'héraldique',
        'Topographie', 'topographie',
        'Cartographie', 'cartographie',
        'Sports', 'sports',
        'Jeux', 'jeux',
        'Échecs', 'échecs',
        'Cartes', 'cartes',
        'Photographie', 'photographie',
        'Typographie', 'typographie',
        'Linguistique', 'linguistique',
        'Grammaire', 'grammaire',
        'Rhétorique', 'rhétorique'
    ]
    
    # Apply highlighting
    # Style markers in italic yellow
    for marker in style_markers:
        pattern = r'\b(' + re.escape(marker) + r')\b'
        text = re.sub(pattern, r'[italic yellow]\1[/italic yellow]', text)
    
    # Semantic markers in bold cyan  
    for marker in semantic_markers:
        pattern = r'\b(' + re.escape(marker) + r')\s*:'
        text = re.sub(pattern, r'[bold cyan]\1[/bold cyan]:', text)
    
    # Domain markers already handled by field indicator logic, but highlight standalone ones
    for marker in domain_markers:
        # Only highlight if not already processed by field indicator logic
        if f'[bold magenta]{marker}.[/bold magenta]' not in text:
            pattern = r'\b(' + re.escape(marker) + r')\.'
            text = re.sub(pattern, r'[bold magenta]\1.[/bold magenta]', text)
    
    return text

def extract_definitions(soup):
    """Extract numbered definitions from the page"""
    definitions = []
    
    # Remove navigation and header elements to focus on content
    for nav in soup.find_all(['nav', 'header', 'footer']):
        nav.decompose()
    for elem in soup.find_all(class_=re.compile(r'nav|menu|header|footer|sidebar')):
        elem.decompose()
    
    # Look for the main content area first
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|entry|definition'))
    if main_content:
        soup = main_content
    
    # Find ordered/unordered lists that contain numbered definitions
    def_lists = soup.find_all(['ol', 'ul'])
    
    for def_list in def_lists:
        items = def_list.find_all('li')
        for item in items:
            text = clean_text(item.get_text())
            # Filter out navigation items and short content
            if (text and len(text) > 20 and 
                not re.search(r'Newsletter|Toggle|LAROUSSE|DICTIONNAIRE|EN ES DE IT', text, re.IGNORECASE)):
                
                # Look for synonyms in the same item
                synonyms = []
                syn_elements = item.find_all(['span', 'em'], class_=re.compile(r'syn|synonym'))
                for syn in syn_elements:
                    syn_text = clean_text(syn.get_text())
                    if syn_text and syn_text not in synonyms:
                        synonyms.append(syn_text)
                
                definitions.append({
                    'text': text,
                    'synonyms': synonyms
                })
    
    # If no lists found, look for numbered paragraphs
    if not definitions:
        all_paragraphs = soup.find_all(['p', 'div'])
        for para in all_paragraphs:
            text = clean_text(para.get_text())
            if (text and len(text) > 20 and
                re.match(r'^\d+\.', text.strip()) and  # Starts with number
                not re.search(r'Newsletter|Toggle|LAROUSSE|DICTIONNAIRE', text, re.IGNORECASE)):
                definitions.append({
                    'text': text,
                    'synonyms': []
                })
    
    return definitions[:8]  # Limit to 8 main definitions

def extract_etymology(soup):
    """Extract etymology information"""
    # Search for etymology patterns in parentheses (common Larousse format)
    all_text = soup.get_text()
    
    # Look for etymology in parentheses, typically after grammatical info
    etym_patterns = [
        r'\(([^)]*latin[^)]*)\)',  # (latin ...)
        r'\(([^)]*grec[^)]*)\)',   # (grec ...)
        r'\(([^)]*du [^)]*)\)',    # (du ...)
        r'\(([^)]*de [^)]*)\)',    # (de ...)
        r'étymologie[:\s]+([^.]+)', # étymologie: ...
    ]
    
    for pattern in etym_patterns:
        match = re.search(pattern, all_text, re.IGNORECASE)
        if match:
            etym_text = clean_text(match.group(1) if match.lastindex else match.group())
            # Filter out non-etymology content
            if etym_text and not re.search(r'Newsletter|Toggle|LAROUSSE', etym_text, re.IGNORECASE):
                return etym_text
    
    return None

def extract_expressions(soup):
    """Extract expressions and examples"""
    expressions = []
    
    # Look for expression sections
    expr_containers = soup.find_all(['div', 'section'], class_=re.compile(r'express|example|phrase'))
    
    for container in expr_containers:
        items = container.find_all(['li', 'div', 'span'])
        for item in items:
            text = clean_text(item.get_text())
            if text and len(text) > 5 and len(text) < 200:  # Reasonable length expressions
                expressions.append(text)
    
    return expressions[:6]  # Limit to 6 expressions

def extract_grammatical_info(soup):
    """Extract grammatical information (nom féminin, adj., etc.)"""
    # Look for French grammatical terms (Larousse format)
    page_text = soup.get_text()
    
    gram_patterns = [
        r'nom féminin',    # noun feminine
        r'nom masculin',   # noun masculine
        r'adjectif',       # adjective  
        r'verbe',          # verb
        r'adverbe',        # adverb
        r'préposition',    # preposition
        r'conjonction',    # conjunction
        r'interjection',   # interjection
        r'pronom',         # pronoun
        r'n\.f\.',         # abbrev noun feminine
        r'n\.m\.',         # abbrev noun masculine
        r'adj\.',          # abbrev adjective
        r'v\.',            # abbrev verb
        r'adv\.',          # abbrev adverb
    ]
    
    for pattern in gram_patterns:
        match = re.search(pattern, page_text, re.IGNORECASE)
        if match:
            # Clean up the match
            gram_info = match.group().lower()
            # Return standardized format
            if 'féminin' in gram_info or 'n.f.' in gram_info:
                return 'n.f.'
            elif 'masculin' in gram_info or 'n.m.' in gram_info:
                return 'n.m.'
            elif 'adjectif' in gram_info or 'adj.' in gram_info:
                return 'adj.'
            elif 'verbe' in gram_info or 'v.' in gram_info:
                return 'v.'
            elif 'adverbe' in gram_info or 'adv.' in gram_info:
                return 'adv.'
            else:
                return gram_info
    
    return None

def get_definition(word):
    """Get French definition from Larousse with beautiful Rich formatting"""
    url = f"https://www.larousse.fr/dictionnaires/francais/{word.lower()}"
    
    # Check cache first
    cached_result = lr_cache.get(word.lower())
    if cached_result:
        soup = BeautifulSoup(cached_result, 'html.parser')
    else:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Cache the HTML content
            lr_cache.set(response.text, word.lower())
            soup = BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            console.print(f"[bold red]❌ Erreur d'accès à Larousse: {e}[/bold red]")
            return
        except Exception as e:
            console.print(f"[bold red]❌ Erreur d'analyse: {e}[/bold red]")
            return
    
    # Check if the word was found
    if "Page non trouvée" in soup.get_text() or "404" in soup.get_text():
        console.print(f"[bold red]❌ Mot '{word}' non trouvé dans le dictionnaire Larousse[/bold red]")
        return
    
    try:
        # Extract information
        definitions = extract_definitions(soup)
        etymology = extract_etymology(soup)
        expressions = extract_expressions(soup)
        grammatical_info = extract_grammatical_info(soup)
        
        if not definitions:
            console.print(f"[bold red]❌ Aucune définition trouvée pour '{word}'[/bold red]")
            return
        
        # Create header panel
        title = f"🇫🇷 Larousse: [bold cyan]{word}[/bold cyan]"
        if grammatical_info:
            title += f" [yellow]({grammatical_info})[/yellow]"
        
        header_content = title
        if etymology:
            header_content += f"\n[bright_black]Étymologie: {etymology}[/bright_black]"
        
        console.print(Panel(header_content, box=box.ROUNDED, border_style="cyan"))
        
        # Create definitions table with better formatting
        table = Table(box=box.SIMPLE, show_header=False, pad_edge=False)
        table.add_column("Définition", style="bright_white", min_width=60)
        
        for definition in definitions:
            def_text = definition['text'].strip()  # Remove leading/trailing whitespace
            
            # Clean up definition text and improve formatting
            # Handle field indicators that appear mid-text (e.g., "Physique4. Text")
            # First, try to separate field names that are attached to numbers
            field_pattern = r'(Botanique|Héraldique|Liturgie|Littéraire|Familier|Populaire|Physique|Topographie|Mathématiques|Médecine|Droit|Histoire|Géographie|Économie|Informatique)(\d+)\.\s*(.*)'
            field_match = re.search(field_pattern, def_text)
            
            if field_match:
                field, number, rest = field_match.groups()
                # Replace the field+number pattern with proper formatting
                before_field = def_text[:field_match.start()].strip()
                if before_field:
                    def_text = f"{before_field} [bold green]{number}.[/bold green] [bold magenta]{field}.[/bold magenta] {rest.strip()}"
                else:
                    def_text = f"[bold green]{number}.[/bold green] [bold magenta]{field}.[/bold magenta] {rest.strip()}"
            
            # Ensure numbered definitions are clearly visible
            if re.match(r'^\d+\.', def_text):
                # Extract number and definition
                match = re.match(r'^(\d+\.)\s*(.*)', def_text)
                if match:
                    number, text = match.groups()
                    def_text = f"[bold green]{number}[/bold green] {text}"
            
            # Highlight common Larousse indicators and markers
            def_text = highlight_larousse_indicators(def_text)
            
            if definition['synonyms']:
                def_text += f"\n[cyan]Synonymes: {', '.join(definition['synonyms'])}[/cyan]"
            table.add_row(def_text)
        
        console.print(table)
        
        # Show expressions if available
        if expressions:
            console.print("\n[bold cyan]Expressions:[/bold cyan]")
            for expr in expressions:
                console.print(f"  [yellow]•[/yellow] {expr}")
        
    except Exception as e:
        console.print(f"[bold red]❌ Erreur lors de l'analyse de la page: {e}[/bold red]")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        console.print("[bold blue]Usage:[/bold blue] lr <mot_français>")
        console.print("\n[bold blue]Exemples:[/bold blue]")
        console.print("  lr maison")
        console.print("  lr courage")
        console.print("  lr --cache-stats")
        console.print("  lr --clear-cache")
        return
    
    # Handle cache management commands
    if sys.argv[1] == '--cache-stats':
        show_all_cache_stats()
        return
    elif sys.argv[1] == '--clear-cache':
        clear_all_caches()
        return
    elif sys.argv[1] == '--cleanup-cache':
        cleanup_expired_all()
        return
    
    word = sys.argv[1].strip()
    if not word:
        console.print("[bold red]❌ Veuillez fournir un mot à chercher[/bold red]")
        return
    
    get_definition(word)

if __name__ == "__main__":
    main()