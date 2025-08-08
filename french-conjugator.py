#!/usr/bin/env python3
"""
French Conjugation Tool - Using la-conjugaison.nouvelobs.com
Three modes: All, Person, Person+Tense
Usage: 
  cj [verb]                    # All conjugations
  cj [person] [verb]           # All tenses for a person  
  cj [person] [verb] [tense]   # Specific person+tense
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

console = Console()

# Predefined persons and their variations
PERSONS = {
    'je': ['je', "j'", 'j'],
    'tu': ['tu'],
    'il': ['il', 'elle', 'on'],
    'nous': ['nous'],
    'vous': ['vous'],
    'ils': ['ils', 'elles']
}

# Predefined tenses with aliases
TENSES = {
    # Indicatif
    'présent': ['présent', 'pres', 'present'],
    'imparfait': ['imparfait', 'imp', 'imperfect'],
    'passé simple': ['passé simple', 'ps', 'simple', 'passé-simple'],
    'futur simple': ['futur simple', 'futur', 'fut', 'future', 'futur-simple'],
    'passé composé': ['passé composé', 'pc', 'passe-compose', 'passé-composé'],
    'plus-que-parfait': ['plus-que-parfait', 'pqp', 'pluperfect'],
    'passé antérieur': ['passé antérieur', 'pa', 'passe-anterieur'],
    'futur antérieur': ['futur antérieur', 'fa', 'futur-anterieur'],
    
    # Conditionnel
    'conditionnel présent': ['conditionnel présent', 'cond', 'conditionnel', 'conditional'],
    'conditionnel passé': ['conditionnel passé', 'cond-passe', 'conditionnel-passe'],
    
    # Subjonctif
    'subjonctif présent': ['subjonctif présent', 'subj', 'subjonctif', 'subjunctive'],
    'subjonctif imparfait': ['subjonctif imparfait', 'subj-imp'],
    'subjonctif passé': ['subjonctif passé', 'subj-passe'],
    'subjonctif plus-que-parfait': ['subjonctif plus-que-parfait', 'subj-pqp'],
    
    # Impératif
    'impératif présent': ['impératif présent', 'imp-pres', 'imperatif', 'imperative'],
    'impératif passé': ['impératif passé', 'imp-passe'],
    
    # Infinitif et Participe
    'infinitif présent': ['infinitif présent', 'inf', 'infinitive'],
    'infinitif passé': ['infinitif passé', 'inf-passe'],
    'participe présent': ['participe présent', 'part-pres', 'participle'],
    'participe passé': ['participe passé', 'part-passe'],
    'gérondif': ['gérondif', 'ger', 'gerund']
}

def clean_text(text):
    """Clean and format text from HTML"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_person(person_input):
    """Normalize person input to standard form"""
    person_input = person_input.lower().strip()
    for standard, variations in PERSONS.items():
        if person_input in variations:
            return standard
    return None

def normalize_tense(tense_input):
    """Normalize tense input to standard form"""
    tense_input = tense_input.lower().strip()
    for standard, variations in TENSES.items():
        if tense_input in variations:
            return standard
    return None

def get_conjugation_url(verb):
    """Generate URL for the verb conjugation page"""
    # Remove accents and clean verb
    verb_clean = verb.lower().strip()
    return f"https://la-conjugaison.nouvelobs.com/du/verbe/{verb_clean}.php"

def scrape_conjugations(verb):
    """Scrape all conjugations for a verb from la-conjugaison.nouvelobs.com"""
    url = get_conjugation_url(verb)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        with console.status(f"[bold green]Conjugating '{verb}'..."):
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find conjugation tables
        conjugations = {}
        
        # Look for different table structures that might contain conjugations
        # This is a general approach - may need adjustment based on actual HTML structure
        tables = soup.find_all('table')
        
        for table in tables:
            # Try to identify tense from nearby headings or table attributes
            tense_header = None
            
            # Look for preceding heading
            prev_elements = table.find_previous_siblings(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if prev_elements:
                tense_header = clean_text(prev_elements[0].get_text())
            
            # Look for tense in table class or id
            if not tense_header:
                table_class = table.get('class', [])
                table_id = table.get('id', '')
                if table_class or table_id:
                    tense_header = ' '.join(table_class) + ' ' + table_id
            
            # Extract conjugation data from table
            rows = table.find_all('tr')
            if rows:
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        person_cell = cells[0]
                        conj_cell = cells[1]
                        
                        person = clean_text(person_cell.get_text())
                        conjugation = clean_text(conj_cell.get_text())
                        
                        if person and conjugation:
                            # Normalize person
                            norm_person = None
                            for std_person in PERSONS:
                                if person.lower().startswith(std_person):
                                    norm_person = std_person
                                    break
                            
                            if norm_person:
                                if tense_header not in conjugations:
                                    conjugations[tense_header] = {}
                                conjugations[tense_header][norm_person] = conjugation
        
        return conjugations
        
    except requests.RequestException as e:
        console.print(f"[bold red]❌ Error accessing conjugation site: {e}[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red]❌ Error parsing conjugations: {e}[/bold red]")
        return None

def display_all_conjugations(verb, conjugations):
    """Display all conjugations for a verb"""
    console.print(f"\n🇫🇷 [bold blue]Conjugaisons de '{verb}'[/bold blue]")
    
    if not conjugations:
        console.print("[bold red]❌ No conjugations found[/bold red]")
        return
    
    for tense, persons in conjugations.items():
        if persons:  # Only show tenses that have conjugations
            table = Table(title=f"[bold magenta]{tense}[/bold magenta]", 
                         box=box.ROUNDED, show_header=True)
            table.add_column("Personne", style="cyan", width=15)
            table.add_column("Conjugaison", style="green", width=25)
            
            for person in ['je', 'tu', 'il', 'nous', 'vous', 'ils']:
                if person in persons:
                    table.add_row(person, persons[person])
            
            console.print(table)
            console.print()

def display_person_conjugations(verb, person, conjugations):
    """Display all tenses for a specific person"""
    console.print(f"\n🇫🇷 [bold blue]Conjugaisons de '{verb}' pour '{person}'[/bold blue]")
    
    if not conjugations:
        console.print("[bold red]❌ No conjugations found[/bold red]")
        return
    
    table = Table(box=box.ROUNDED, show_header=True)
    table.add_column("Temps", style="magenta", width=25)
    table.add_column("Conjugaison", style="green", width=25)
    
    found_any = False
    for tense, persons in conjugations.items():
        if person in persons:
            table.add_row(tense, persons[person])
            found_any = True
    
    if found_any:
        console.print(table)
    else:
        console.print(f"[bold red]❌ No conjugations found for person '{person}'[/bold red]")

def display_specific_conjugation(verb, person, tense, conjugations):
    """Display specific conjugation for person and tense"""
    console.print(f"\n🇫🇷 [bold blue]Conjugaison de '{verb}' - {person} - {tense}[/bold blue]")
    
    if not conjugations:
        console.print("[bold red]❌ No conjugations found[/bold red]")
        return
    
    found = False
    for conj_tense, persons in conjugations.items():
        # Try to match tense (exact or partial)
        if tense.lower() in conj_tense.lower() or conj_tense.lower() in tense.lower():
            if person in persons:
                result_panel = Panel(
                    f"[bold green]{persons[person]}[/bold green]",
                    title=f"[bold cyan]{person}[/bold cyan] + [bold magenta]{conj_tense}[/bold magenta]",
                    border_style="green"
                )
                console.print(result_panel)
                found = True
                break
    
    if not found:
        console.print(f"[bold red]❌ No conjugation found for '{person}' in '{tense}'[/bold red]")

def show_help():
    """Display help information"""
    help_text = """
[bold cyan]French Conjugation Tool[/bold cyan]

[bold]Usage:[/bold]
  cj [verb]                    # Show all conjugations
  cj [person] [verb]           # Show all tenses for a person
  cj [person] [verb] [tense]   # Show specific conjugation

[bold]Persons:[/bold] je, tu, il/elle/on, nous, vous, ils/elles

[bold]Common Tenses (with aliases):[/bold]
  présent (pres) | imparfait (imp) | futur (fut) 
  passé composé (pc) | conditionnel (cond) | subjonctif (subj)
  impératif (imp-pres) | infinitif (inf) | participe (part)

[bold]Examples:[/bold]
  cj être                      # All conjugations of être
  cj je suivre                 # All tenses of suivre for 'je'
  cj tu manger présent         # Present tense of manger for 'tu'
  cj il avoir fut              # Future tense of avoir for 'il'
"""
    console.print(Panel(help_text, border_style="blue"))

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    args = sys.argv[1:]
    
    if args[0] in ['-h', '--help', 'help']:
        show_help()
        return
    
    # Parse arguments based on number
    if len(args) == 1:
        # Mode 1: All conjugations
        verb = args[0]
        conjugations = scrape_conjugations(verb)
        if conjugations:
            display_all_conjugations(verb, conjugations)
    
    elif len(args) == 2:
        # Mode 2: Person + verb
        person_input, verb = args
        person = normalize_person(person_input)
        
        if not person:
            console.print(f"[bold red]❌ Unknown person: '{person_input}'[/bold red]")
            console.print("Valid persons: je, tu, il/elle/on, nous, vous, ils/elles")
            return
        
        conjugations = scrape_conjugations(verb)
        if conjugations:
            display_person_conjugations(verb, person, conjugations)
    
    elif len(args) == 3:
        # Mode 3: Person + verb + tense
        person_input, verb, tense_input = args
        person = normalize_person(person_input)
        tense = normalize_tense(tense_input)
        
        if not person:
            console.print(f"[bold red]❌ Unknown person: '{person_input}'[/bold red]")
            return
        
        if not tense:
            # Use original input if normalization fails
            tense = tense_input
        
        conjugations = scrape_conjugations(verb)
        if conjugations:
            display_specific_conjugation(verb, person, tense, conjugations)
    
    else:
        console.print("[bold red]❌ Too many arguments[/bold red]")
        show_help()

if __name__ == "__main__":
    main()