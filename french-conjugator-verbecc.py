#!/usr/bin/env python3
"""
French Conjugation Tool - Using verbecc library
Three modes: All, Person, Person+Tense
Usage: 
  cj [verb]                    # All conjugations
  cj [person] [verb]           # All tenses for a person  
  cj [person] [verb] [tense]   # Specific person+tense
"""

import sys
from verbecc import Conjugator
from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
from rich.panel import Panel
from tool_cache import ToolCache, show_all_cache_stats, clear_all_caches, cleanup_expired_all

console = Console()

# Initialize conjugation cache
conj_cache = ToolCache('conjugation', max_age_days=30)  # Cache for 30 days

# Initialize French conjugator
cg = Conjugator(lang='fr')

# Predefined persons and their variations
PERSONS = {
    'je': ['je', "j'", 'j'],
    'tu': ['tu'],
    'il': ['il', 'elle', 'on'],
    'nous': ['nous'],
    'vous': ['vous'],
    'ils': ['ils', 'elles']
}

# Predefined tenses with aliases and their verbecc mappings
TENSES = {
    # Indicatif
    'présent': {
        'aliases': ['présent', 'present', 'p'],
        'mood': 'indicatif',
        'tense': 'présent'
    },
    'imparfait': {
        'aliases': ['imparfait', 'imperfect', 'i'],
        'mood': 'indicatif',
        'tense': 'imparfait'
    },
    'passé simple': {
        'aliases': ['passé simple', 'passé-simple', 'simple', 'ps'],
        'mood': 'indicatif',
        'tense': 'passé-simple'
    },
    'futur simple': {
        'aliases': ['futur simple', 'futur-simple', 'futur', 'future', 'f'],
        'mood': 'indicatif',
        'tense': 'futur-simple'
    },
    'passé composé': {
        'aliases': ['passé composé', 'passé-composé', 'passe-compose', 'pc'],
        'mood': 'indicatif',
        'tense': 'passé-composé'
    },
    'plus-que-parfait': {
        'aliases': ['plus-que-parfait', 'pluperfect', 'pqp'],
        'mood': 'indicatif',
        'tense': 'plus-que-parfait'
    },
    'passé antérieur': {
        'aliases': ['passé antérieur', 'passé-antérieur', 'passe-anterieur', 'pa'],
        'mood': 'indicatif',
        'tense': 'passé-antérieur'
    },
    'futur antérieur': {
        'aliases': ['futur antérieur', 'futur-antérieur', 'futur-anterieur', 'fa'],
        'mood': 'indicatif',
        'tense': 'futur-antérieur'
    },
    
    # Conditionnel
    'conditionnel présent': {
        'aliases': ['conditionnel présent', 'conditionnel', 'conditional', 'c'],
        'mood': 'conditionnel',
        'tense': 'présent'
    },
    'conditionnel passé': {
        'aliases': ['conditionnel passé', 'conditionnel-passe', 'cond-passe', 'cp'],
        'mood': 'conditionnel',
        'tense': 'passé'
    },
    
    # Subjonctif
    'subjonctif présent': {
        'aliases': ['subjonctif présent', 'subjonctif', 'subjunctive', 's'],
        'mood': 'subjonctif',
        'tense': 'présent'
    },
    'subjonctif imparfait': {
        'aliases': ['subjonctif imparfait', 'subj-imp', 'si'],
        'mood': 'subjonctif',
        'tense': 'imparfait'
    },
    'subjonctif passé': {
        'aliases': ['subjonctif passé', 'subj-passe', 'sp'],
        'mood': 'subjonctif',
        'tense': 'passé'
    },
    'subjonctif plus-que-parfait': {
        'aliases': ['subjonctif plus-que-parfait', 'subj-pqp', 'spqp'],
        'mood': 'subjonctif',
        'tense': 'plus-que-parfait'
    },
    
    # Impératif
    'impératif présent': {
        'aliases': ['impératif présent', 'imperatif', 'imperative', 'impér', 'im'],
        'mood': 'imperatif',
        'tense': 'imperatif-présent'
    },
    'impératif passé': {
        'aliases': ['impératif passé', 'impér-passé', 'imperatif-passe', 'imp'],
        'mood': 'imperatif',
        'tense': 'imperatif-passé'
    },
    
    # Infinitif
    'infinitif présent': {
        'aliases': ['infinitif présent', 'infinitif', 'infinitive', 'inf'],
        'mood': 'infinitif',
        'tense': 'infinitif-présent'
    },
    'infinitif passé': {
        'aliases': ['infinitif passé', 'inf-passe', 'inf-passé'],
        'mood': 'infinitif',
        'tense': 'infinitif-passé'
    },
    
    # Participe
    'participe présent': {
        'aliases': ['participe présent', 'part-pres', 'participle', 'part', 'gérondif', 'ger'],
        'mood': 'participe',
        'tense': 'participe-présent'
    },
    'participe passé': {
        'aliases': ['participe passé', 'part-passe', 'part-passé', 'pp'],
        'mood': 'participe',
        'tense': 'participe-passé'
    }
}

# Person mappings for verbecc
PERSON_MAPPING = {
    'je': '1s',
    'tu': '2s', 
    'il': '3s',
    'nous': '1p',
    'vous': '2p',
    'ils': '3p'
}

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
    for standard, tense_info in TENSES.items():
        if tense_input in tense_info['aliases']:
            return standard
    return None

def get_conjugation(verb, mood, tense, person=None):
    """Get conjugation using verbecc"""
    try:
        conjugation = cg.conjugate(verb)
        
        if mood in conjugation and tense in conjugation[mood]:
            if person:
                person_key = PERSON_MAPPING.get(person)
                if person_key in conjugation[mood][tense]:
                    return conjugation[mood][tense][person_key]
                return None
            else:
                return conjugation[mood][tense]
        return None
    except Exception as e:
        console.print(f"[bold red]❌ Error conjugating '{verb}': {e}[/bold red]")
        return None

def display_all_conjugations(verb):
    """Display all conjugations for a verb"""
    # Check cache first
    cached_result = conj_cache.get(verb, 'all')
    if cached_result:
        result = cached_result
    else:
        try:
            result = cg.conjugate(verb)
            
            # Cache the result
            if result:
                conj_cache.set(result, verb, 'all')
        except Exception as e:
            console.print(f"[bold red]❌ Error conjugating '{verb}': {e}[/bold red]")
            return
    
    try:
        
        if not result or 'moods' not in result:
            console.print("[bold red]❌ No conjugations found[/bold red]")
            return
        
        conjugation = result['moods']
        
        # Display each mood and tense
        for mood_name, mood_data in conjugation.items():
            if isinstance(mood_data, dict):
                console.print(f"\n[bold magenta]═══ {mood_name.upper()} ═══[/bold magenta]")
                
                for tense_name, tense_data in mood_data.items():
                    if isinstance(tense_data, list) and tense_data:
                        table = Table(title=f"[bold cyan]{tense_name}[/bold cyan]", 
                                     box=box.ROUNDED, show_header=True)
                        table.add_column("Personne", style="cyan", width=15)
                        table.add_column("Conjugaison", style="green", width=30)
                        
                        # Standard person order for French
                        persons = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
                        
                        # Handle different cases based on tense type
                        if 'imperatif' in tense_name:
                            # Imperative has only 3 forms: tu, nous, vous
                            imp_persons = ['tu', 'nous', 'vous']
                            for i, conjugated_form in enumerate(tense_data):
                                if i < len(imp_persons):
                                    table.add_row(imp_persons[i], conjugated_form)
                        elif 'infinitif' in tense_name or 'participe' in tense_name:
                            # Infinitive and participle forms
                            for conjugated_form in tense_data:
                                table.add_row("—", conjugated_form)
                        else:
                            # Regular conjugation with 6 persons
                            for i, conjugated_form in enumerate(tense_data):
                                if i < len(persons):
                                    table.add_row(persons[i], conjugated_form)
                        
                        console.print(table)
        
        # Display verb info if available
        if 'verb' in result:
            verb_info = result['verb']
            info_text = f"[dim]Infinitif: {verb_info.get('infinitive', verb)}"
            if 'translation_en' in verb_info:
                info_text += f" | EN: {verb_info['translation_en']}"
            console.print(f"\n{info_text}[/dim]")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error processing conjugations: {e}[/bold red]")

def display_person_conjugations(verb, person):
    """Display all tenses for a specific person"""
    # Check cache first  
    cached_result = conj_cache.get(verb, 'person', person)
    if cached_result:
        result = cached_result
    else:
        try:
            result = cg.conjugate(verb)
            
            # Cache the result
            if result:
                conj_cache.set(result, verb, 'person', person)
        except Exception as e:
            console.print(f"[bold red]❌ Error conjugating '{verb}': {e}[/bold red]")
            return
    
    try:
        
        if not result or 'moods' not in result:
            console.print("[bold red]❌ No conjugations found[/bold red]")
            return
        
        conjugation = result['moods']
        
        table = Table(box=box.ROUNDED, show_header=True)
        table.add_column("Temps", style="magenta", width=30)
        table.add_column("Conjugaison", style="green", width=25)
        
        persons = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
        person_index = persons.index(person) if person in persons else -1
        found_any = False
        
        for mood_name, mood_data in conjugation.items():
            if isinstance(mood_data, dict):
                for tense_name, tense_data in mood_data.items():
                    if isinstance(tense_data, list) and tense_data:
                        conjugated_form = None
                        
                        if 'imperatif' in tense_name:
                            # Imperative: tu=0, nous=1, vous=2
                            imp_persons = ['tu', 'nous', 'vous']
                            if person in imp_persons:
                                imp_index = imp_persons.index(person)
                                if imp_index < len(tense_data):
                                    conjugated_form = tense_data[imp_index]
                        elif 'infinitif' in tense_name or 'participe' in tense_name:
                            # Skip infinitive/participle for person-specific display
                            continue
                        else:
                            # Regular 6-person conjugation
                            if person_index != -1 and person_index < len(tense_data):
                                conjugated_form = tense_data[person_index]
                        
                        if conjugated_form:
                            full_tense_name = f"{mood_name} {tense_name}"
                            table.add_row(full_tense_name, conjugated_form)
                            found_any = True
        
        if found_any:
            console.print(table)
        else:
            console.print(f"[bold red]❌ No conjugations found for person '{person}'[/bold red]")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error processing conjugations: {e}[/bold red]")

def display_specific_conjugation(verb, person, tense):
    """Display specific conjugation for person and tense"""
    # Get tense info
    tense_info = TENSES.get(tense)
    if not tense_info:
        console.print(f"[bold red]❌ Unknown tense: '{tense}'[/bold red]")
        return
    
    # Check cache first
    cached_result = conj_cache.get(verb, 'specific', person, tense)
    if cached_result:
        result = cached_result
    else:
        try:
            result = cg.conjugate(verb)
            
            # Cache the result
            if result:
                conj_cache.set(result, verb, 'specific', person, tense)
        except Exception as e:
            console.print(f"[bold red]❌ Error conjugating '{verb}': {e}[/bold red]")
            return
    
    try:
        
        if not result or 'moods' not in result:
            console.print("[bold red]❌ No conjugations found[/bold red]")
            return
        
        conjugation = result['moods']
        mood = tense_info['mood']
        tense_key = tense_info['tense']
        
        # Find the conjugation
        conjugated_form = None
        
        if mood in conjugation and tense_key in conjugation[mood]:
            tense_data = conjugation[mood][tense_key]
            
            if isinstance(tense_data, list) and tense_data:
                # Handle different types of conjugations
                if 'infinitif' in tense_key or 'participe' in tense_key:
                    # Infinitive and participle forms don't have persons
                    conjugated_form = tense_data[0] if tense_data else None
                    # Update title to not show person for these forms
                    result_panel = Panel(
                        f"[bold green]{conjugated_form}[/bold green]",
                        title=f"[bold magenta]{tense}[/bold magenta]",
                        border_style="green"
                    )
                    console.print(result_panel)
                    return
                elif 'imperatif' in tense_key:
                    # Imperative: tu=0, nous=1, vous=2
                    imp_persons = ['tu', 'nous', 'vous']
                    if person in imp_persons:
                        imp_index = imp_persons.index(person)
                        if imp_index < len(tense_data):
                            conjugated_form = tense_data[imp_index]
                else:
                    # Regular 6-person conjugation
                    persons = ['je', 'tu', 'il', 'nous', 'vous', 'ils']
                    person_index = persons.index(person) if person in persons else -1
                    if person_index != -1 and person_index < len(tense_data):
                        conjugated_form = tense_data[person_index]
        
        if conjugated_form:
            result_panel = Panel(
                f"[bold green]{conjugated_form}[/bold green]",
                title=f"[bold cyan]{person}[/bold cyan] + [bold magenta]{tense}[/bold magenta]",
                border_style="green"
            )
            console.print(result_panel)
        else:
            console.print(f"[bold red]❌ No conjugation found for '{person}' in '{tense}'[/bold red]")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")

def display_impersonal_conjugation(verb, tense):
    """Display conjugation for forms that don't use persons (participles, infinitives)"""
    # Get tense info
    tense_info = TENSES.get(tense)
    if not tense_info:
        console.print(f"[bold red]❌ Unknown tense: '{tense}'[/bold red]")
        return
    
    # Check cache first
    cached_result = conj_cache.get(verb, 'impersonal', tense)
    if cached_result:
        result = cached_result
    else:
        try:
            result = cg.conjugate(verb)
            
            # Cache the result
            if result:
                conj_cache.set(result, verb, 'impersonal', tense)
        except Exception as e:
            console.print(f"[bold red]❌ Error conjugating '{verb}': {e}[/bold red]")
            return
    
    try:
        
        if not result or 'moods' not in result:
            console.print("[bold red]❌ No conjugations found[/bold red]")
            return
        
        conjugation = result['moods']
        mood = tense_info['mood']
        tense_key = tense_info['tense']
        
        # Find the conjugation
        conjugated_form = None
        
        if mood in conjugation and tense_key in conjugation[mood]:
            tense_data = conjugation[mood][tense_key]
            
            if isinstance(tense_data, list) and tense_data:
                conjugated_form = tense_data[0] if tense_data else None
        
        if conjugated_form:
            result_panel = Panel(
                f"[bold green]{conjugated_form}[/bold green]",
                title=f"[bold magenta]{verb} - {tense}[/bold magenta]",
                border_style="green"
            )
            console.print(result_panel)
        else:
            console.print(f"[bold red]❌ No conjugation found for '{tense}'[/bold red]")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")

def show_help():
    """Display help information"""
    help_text = """
[bold cyan]French Conjugation Tool[/bold cyan]

[bold]Usage (Original Format):[/bold]
  cj [verb]                    # Show all conjugations
  cj [person] [verb]           # Show all tenses for a person
  cj [person] [verb] [tense]   # Show specific conjugation
  cj [verb] [tense]            # Show participle/infinitive (no person needed)

[bold]Usage (Flag Format):[/bold]
  cj -[tense] [person] [verb]  # Show specific conjugation
  cj -[tense] [verb]           # Show participle/infinitive (no person needed)

[bold]Special Commands:[/bold]
  cj --help, cj -h             # Show this help
  cj --aliases                 # Show all tense aliases
  cj --cache-stats             # Show cache statistics
  cj --clear-cache             # Clear cache
  cj --cleanup-cache           # Remove expired entries

[bold]Persons:[/bold] je, tu, il/elle/on, nous, vous, ils/elles

[bold]Common Tenses (with short aliases):[/bold]
  présent (p) | imparfait (i) | futur simple (f) 
  passé composé (pc) | conditionnel présent (c) | subjonctif présent (s)
  impératif présent (im) | passé simple (ps)
  participe passé (pp) | participe présent (part) | infinitif (inf)

[bold]Examples (Original Format):[/bold]
  cj être                      # All conjugations of être
  cj je suivre                 # All tenses of suivre for 'je'
  cj tu manger p               # Present: "tu manges"
  cj il avoir f                # Future: "il aura"
  cj nous finir im             # Imperative: "finissons"
  cj manger pp                 # Participe passé: "mangé"

[bold]Examples (Flag Format):[/bold]
  cj -p tu manger              # Present: "tu manges"
  cj -f il avoir               # Future: "il aura"
  cj -im nous finir            # Imperative: "finissons"
  cj -pp manger                # Participe passé: "mangé"
"""
    console.print(Panel(help_text, border_style="blue"))

def show_aliases():
    """Display all tense aliases"""
    console.print(f"\n🇫🇷 [bold blue]All Tense Aliases[/bold blue]")
    
    table = Table(box=box.ROUNDED, show_header=True)
    table.add_column("Tense", style="magenta", width=25)
    table.add_column("Aliases", style="green", width=40)
    
    for tense, tense_info in TENSES.items():
        aliases = ", ".join([f"[cyan]{alias}[/cyan]" for alias in tense_info['aliases'][1:]])  # Skip the first one (full name)
        if aliases:
            table.add_row(tense, aliases)
    
    console.print(table)
    
    console.print(f"\n[dim]💡 Tip: Use any alias in place of the full tense name[/dim]")
    console.print(f"[dim]Example: 'cj je avoir fut' instead of 'cj je avoir futur simple'[/dim]")

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    args = sys.argv[1:]
    
    if args[0] in ['-h', '--help', 'help']:
        show_help()
        return
    
    if args[0] in ['--aliases', '-a', 'aliases']:
        show_aliases()
        return
    
    # Handle cache management commands
    if args[0] == '--cache-stats':
        show_all_cache_stats()
        return
    elif args[0] == '--clear-cache':
        conj_cache.clear()
        console.print("[green]✅ Conjugation cache cleared[/green]")
        return
    elif args[0] == '--cleanup-cache':
        removed = conj_cache.cleanup_expired()
        if removed > 0:
            console.print(f"[green]✅ Removed {removed} expired entries[/green]")
        else:
            console.print("[dim]No expired entries found[/dim]")
        return
    
    # Check for flag format: cj -<tense> <person> <verb>
    if args[0].startswith('-') and len(args[0]) > 1:
        # Flag format detected
        tense_flag = args[0][1:]  # Remove the '-' prefix
        tense = normalize_tense(tense_flag)
        
        if not tense:
            console.print(f"[bold red]❌ Unknown tense flag: '-{tense_flag}'[/bold red]")
            console.print("Use 'cj --aliases' to see available tense aliases")
            return
        
        if len(args) == 2:
            # cj -<tense> <verb> (for participles/infinitives)
            verb = args[1]
            tense_info = TENSES.get(tense)
            if tense_info and ('participe' in tense_info['mood'] or 'infinitif' in tense_info['mood']):
                display_impersonal_conjugation(verb, tense)
            else:
                console.print(f"[bold red]❌ Tense '{tense}' requires a person. Use: cj -{tense_flag} <person> <verb>[/bold red]")
            return
        
        elif len(args) == 3:
            # cj -<tense> <person> <verb>
            person_input, verb = args[1], args[2]
            person = normalize_person(person_input)
            
            if not person:
                console.print(f"[bold red]❌ Unknown person: '{person_input}'[/bold red]")
                console.print("Valid persons: je, tu, il/elle/on, nous, vous, ils/elles")
                return
            
            # Check if this tense doesn't need a person
            tense_info = TENSES.get(tense)
            if tense_info and ('participe' in tense_info['mood'] or 'infinitif' in tense_info['mood']):
                display_impersonal_conjugation(verb, tense)
            else:
                display_specific_conjugation(verb, person, tense)
            return
        
        else:
            console.print(f"[bold red]❌ Invalid flag format. Use: cj -{tense_flag} <person> <verb> or cj -{tense_flag} <verb> (for participles)[/bold red]")
            return
    
    # Original format parsing
    if len(args) == 1:
        # Mode 1: All conjugations
        verb = args[0]
        display_all_conjugations(verb)
    
    elif len(args) == 2:
        # Mode 2: Person + verb OR verb + tense (for participles/infinitives)
        person_input, verb = args
        person = normalize_person(person_input)
        tense = normalize_tense(verb)  # Check if second arg is a tense
        
        if not person and tense:
            # This is probably: verb + tense (participle/infinitive)
            tense_info = TENSES.get(tense)
            if tense_info and ('participe' in tense_info['mood'] or 'infinitif' in tense_info['mood']):
                verb_name = person_input  # First arg is actually the verb
                display_impersonal_conjugation(verb_name, tense)
                return
        
        if not person:
            console.print(f"[bold red]❌ Unknown person: '{person_input}'[/bold red]")
            console.print("Valid persons: je, tu, il/elle/on, nous, vous, ils/elles")
            return
        
        display_person_conjugations(verb, person)
    
    elif len(args) == 3:
        # Mode 3: Person + verb + tense OR verb + tense (for participles/infinitives)
        person_input, verb, tense_input = args
        person = normalize_person(person_input)
        tense = normalize_tense(tense_input)
        
        # Check if first argument might be a verb instead of person (for participles/infinitives)
        if not person and tense:
            tense_info = TENSES.get(tense)
            if tense_info and ('participe' in tense_info['mood'] or 'infinitif' in tense_info['mood']):
                # This is probably: verb + tense (participle/infinitive)
                verb = person_input  # First arg is actually the verb
                display_impersonal_conjugation(verb, tense)
                return
        
        if not person:
            console.print(f"[bold red]❌ Unknown person: '{person_input}'[/bold red]")
            return
        
        if not tense:
            console.print(f"[bold red]❌ Unknown tense: '{tense_input}'[/bold red]")
            console.print("Use 'cj --help' to see available tenses")
            return
        
        # Check if this tense doesn't need a person
        tense_info = TENSES.get(tense)
        if tense_info and ('participe' in tense_info['mood'] or 'infinitif' in tense_info['mood']):
            display_impersonal_conjugation(verb, tense)
        else:
            display_specific_conjugation(verb, person, tense)
    
    else:
        console.print("[bold red]❌ Too many arguments[/bold red]")
        show_help()

if __name__ == "__main__":
    main()