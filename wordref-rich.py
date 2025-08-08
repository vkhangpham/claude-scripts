#!/usr/bin/env python3
"""
WordReference French-English CLI Tool - Rich Version
Beautiful terminal output with colors and tables
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

# Initialize WordReference cache
wr_cache = ToolCache('wordreference', max_age_days=7)  # Cache for 7 days

def clean_text(text):
    """Clean and format text from HTML"""
    if not text:
        return ""
    # Remove arrow symbols that link to conjugation pages
    text = text.replace('⇒', '')
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_translation(word, direction='fr'):
    """Get translation from WordReference with beautiful Rich formatting"""
    if direction == 'fr':
        url = f"https://www.wordreference.com/fren/{word}"
        flag = "🇫🇷→🇬🇧"
        title = f"French to English: [bold blue]{word}[/bold blue]"
    else:
        url = f"https://www.wordreference.com/enfr/{word}"
        flag = "🇬🇧→🇫🇷"
        title = f"English to French: [bold blue]{word}[/bold blue]"
    
    # Check cache first
    cached_result = wr_cache.get(word, direction)
    if cached_result:
        soup = BeautifulSoup(cached_result, 'html.parser')
    else:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Cache the HTML content
            wr_cache.set(response.text, word, direction)
            soup = BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            console.print(f"[bold red]❌ Error accessing WordReference: {e}[/bold red]")
            return
        except Exception as e:
            console.print(f"[bold red]❌ Error parsing results: {e}[/bold red]")
            return
    
    try:
        # Find the main translation table
        main_table = soup.find('table', class_='WRD')
        
        if not main_table:
            console.print(f"[bold red]❌ No translations found for '{word}'[/bold red]")
            return
        
        # Create a beautiful table
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
        
        if direction == 'fr':
            table.add_column("Français", style="cyan", width=25)
            table.add_column("Contexte", style="dim white", width=25)  
            table.add_column("Anglais", style="green", width=30)
        else:
            table.add_column("Anglais", style="cyan", width=25)
            table.add_column("Contexte", style="dim white", width=25)
            table.add_column("Français", style="green", width=30)
        
        # Extract translations from table rows
        rows = main_table.find_all('tr')
        count = 0
        examples = []
        
        for row in rows:
            if count >= 8:  # Limit to main translations
                break
                
            cells = row.find_all('td')
            if len(cells) >= 3:
                # Column 1: Source term + type
                source_cell = cells[0]
                source_term = ""
                source_type = ""
                
                # Get the main source term
                source_strong = source_cell.find('strong')
                if source_strong:
                    source_term = clean_text(source_strong.get_text())
                
                # Get the grammatical type - handle multi-word types like "loc adv"
                source_em = source_cell.find('em')
                if source_em:
                    source_type = clean_text(source_em.get_text())
                
                # Column 2: Context/explanation
                explanation_cell = cells[1]
                explanation = clean_text(explanation_cell.get_text())
                
                # Column 3: Target translations
                target_cell = cells[2]
                target_text = clean_text(target_cell.get_text())
                
                # Only show if we have essential parts
                if source_term and target_text:
                    # Format source term with type
                    if source_type:
                        source_display = Text(f"{source_term} ", style="bold cyan")
                        source_display.append(f"[{source_type}]", style="dim cyan")
                    else:
                        source_display = Text(source_term, style="bold cyan")
                    
                    # Format target with type - extract grammatical types from end
                    target_parts = target_text.split()
                    target_term = ""
                    target_type = ""
                    
                    # Look for grammatical type at the end
                    if target_parts:
                        # Common grammatical types that appear at the end
                        gram_types = ['interj', 'n', 'v', 'adj', 'adv', 'expr', 'prep', 'conj', 'det', 'nm', 'nf', 'npl', 'nmpl', 'nfpl']
                        if target_parts[-1] in gram_types:
                            target_type = target_parts[-1]
                            target_term = ' '.join(target_parts[:-1])
                        else:
                            target_term = target_text
                    
                    # Format target with Rich styling
                    if target_type:
                        target_display = Text(f"{target_term} ", style="bold green")
                        target_display.append(f"[{target_type}]", style="dim green")
                    else:
                        target_display = Text(target_text, style="bold green")
                    
                    # Format explanation
                    explanation_display = Text(explanation, style="italic dim white")
                    
                    # Add row to table - source is always first column, target is always third
                    table.add_row(source_display, explanation_display, target_display)
                    
                    count += 1
        
        # Display the beautiful table
        console.print(table)
        
        # Look for inflections
        try:
            inflection_div = soup.find(string=re.compile(r"Inflections"))
            if inflection_div:
                parent = inflection_div.parent
                if parent:
                    inflection_text = clean_text(parent.get_text())
                    if "fpl:" in inflection_text or "mpl:" in inflection_text:
                        inflection_panel = Panel(
                            f"[italic]{inflection_text}[/italic]",
                            title="[bold blue]Inflections[/bold blue]",
                            border_style="blue"
                        )
                        console.print("\n", inflection_panel)
        except:
            pass
    
    except Exception as e:
        console.print(f"[bold red]❌ Error processing results: {e}[/bold red]")

def main():
    if len(sys.argv) < 2:
        console.print("[bold yellow]Usage:[/bold yellow] python wordref-rich.py [word] [direction]")
        console.print("[dim]Direction: fr (French to English, default) or en (English to French)[/dim]")
        console.print("[dim]Example: python wordref-rich.py bonjour[/dim]")
        console.print("[dim]Example: python wordref-rich.py hello en[/dim]")
        console.print("\n[bold yellow]Cache Commands:[/bold yellow]")
        console.print("[dim]--cache-stats    Show cache statistics[/dim]")
        console.print("[dim]--clear-cache    Clear cache[/dim]")
        console.print("[dim]--cleanup-cache  Remove expired entries[/dim]")
        sys.exit(1)
    
    # Handle cache management commands
    if sys.argv[1] == '--cache-stats':
        show_all_cache_stats()
        return
    elif sys.argv[1] == '--clear-cache':
        wr_cache.clear()
        console.print("[green]✅ WordReference cache cleared[/green]")
        return
    elif sys.argv[1] == '--cleanup-cache':
        removed = wr_cache.cleanup_expired()
        if removed > 0:
            console.print(f"[green]✅ Removed {removed} expired entries[/green]")
        else:
            console.print("[dim]No expired entries found[/dim]")
        return
    
    word = sys.argv[1]
    direction = sys.argv[2] if len(sys.argv) > 2 else 'fr'
    
    if direction not in ['fr', 'en']:
        console.print("[bold red]Direction must be 'fr' (French to English) or 'en' (English to French)[/bold red]")
        sys.exit(1)
    
    get_translation(word, direction)

if __name__ == "__main__":
    main()