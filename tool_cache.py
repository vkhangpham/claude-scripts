#!/usr/bin/env python3
"""
Shared caching system for French language tools
Provides persistent caching with size management and cleanup commands
"""

import json
import os
import hashlib
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

class ToolCache:
    def __init__(self, cache_name, cache_dir=None, max_age_days=30):
        """Initialize cache with name and optional directory"""
        if cache_dir is None:
            cache_dir = Path.home() / '.cache' / 'french-tools'
        
        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / f'{cache_name}.json'
        self.max_age = max_age_days * 24 * 3600  # Convert days to seconds
        
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing cache
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from file"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            else:
                self.cache = {}
        except (json.JSONDecodeError, IOError):
            self.cache = {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except IOError as e:
            console.print(f"[yellow]Warning: Could not save cache: {e}[/yellow]")
    
    def _generate_key(self, *args):
        """Generate cache key from arguments"""
        key_string = '|'.join(str(arg) for arg in args)
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()
    
    def _is_expired(self, timestamp):
        """Check if cache entry is expired"""
        return time.time() - timestamp > self.max_age
    
    def get(self, *args):
        """Get cached result"""
        key = self._generate_key(*args)
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Check if entry is expired
            if self._is_expired(entry['timestamp']):
                del self.cache[key]
                self._save_cache()
                return None
            
            return entry['data']
        
        return None
    
    def set(self, data, *args):
        """Set cache entry"""
        key = self._generate_key(*args)
        
        self.cache[key] = {
            'data': data,
            'timestamp': time.time(),
            'args': args  # Store original args for debugging
        }
        
        self._save_cache()
    
    def clear(self):
        """Clear all cache entries"""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
    
    def cleanup_expired(self):
        """Remove expired entries"""
        expired_keys = []
        current_time = time.time()
        
        for key, entry in self.cache.items():
            if current_time - entry['timestamp'] > self.max_age:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self._save_cache()
        
        return len(expired_keys)
    
    def get_stats(self):
        """Get cache statistics"""
        if not self.cache:
            return {
                'total_entries': 0,
                'file_size': 0,
                'expired_entries': 0
            }
        
        file_size = self.cache_file.stat().st_size if self.cache_file.exists() else 0
        current_time = time.time()
        expired_count = sum(1 for entry in self.cache.values() 
                          if current_time - entry['timestamp'] > self.max_age)
        
        return {
            'total_entries': len(self.cache),
            'file_size': file_size,
            'expired_entries': expired_count
        }

def format_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    size_index = 0
    
    while size_bytes >= 1024 and size_index < len(size_names) - 1:
        size_bytes /= 1024
        size_index += 1
    
    return f"{size_bytes:.1f} {size_names[size_index]}"

def show_all_cache_stats():
    """Show statistics for all caches"""
    console.print(f"\n🗄️  [bold blue]French Tools Cache Statistics[/bold blue]")
    
    cache_dir = Path.home() / '.cache' / 'french-tools'
    
    if not cache_dir.exists():
        console.print("[dim]No cache directory found[/dim]")
        return
    
    table = Table(box=box.ROUNDED, show_header=True)
    table.add_column("Tool", style="cyan", width=20)
    table.add_column("Entries", style="green", width=12)
    table.add_column("Size", style="yellow", width=12)
    table.add_column("Expired", style="red", width=12)
    
    total_size = 0
    total_entries = 0
    total_expired = 0
    
    # Check each possible cache file
    cache_files = {
        'wordreference': 'WordReference',
        'conjugation': 'Conjugation',
        'verbecc': 'VerbECC'
    }
    
    for cache_name, display_name in cache_files.items():
        cache = ToolCache(cache_name)
        stats = cache.get_stats()
        
        if stats['total_entries'] > 0:
            table.add_row(
                display_name,
                str(stats['total_entries']),
                format_size(stats['file_size']),
                str(stats['expired_entries'])
            )
            
            total_size += stats['file_size']
            total_entries += stats['total_entries']
            total_expired += stats['expired_entries']
    
    if total_entries > 0:
        console.print(table)
        console.print(f"\n[bold]Total:[/bold] {total_entries} entries, {format_size(total_size)}")
        if total_expired > 0:
            console.print(f"[dim]💡 Use 'cj --clear-cache' or 'wr --clear-cache' to clean up expired entries[/dim]")
    else:
        console.print("[dim]No cached data found[/dim]")

def clear_all_caches():
    """Clear all caches"""
    cache_dir = Path.home() / '.cache' / 'french-tools'
    
    if not cache_dir.exists():
        console.print("[dim]No cache directory found[/dim]")
        return
    
    cleared_count = 0
    cache_files = ['wordreference', 'conjugation', 'verbecc']
    
    for cache_name in cache_files:
        cache = ToolCache(cache_name)
        if cache.cache:
            cache.clear()
            cleared_count += 1
    
    if cleared_count > 0:
        console.print(f"[green]✅ Cleared {cleared_count} cache(s)[/green]")
    else:
        console.print("[dim]No caches to clear[/dim]")

def cleanup_expired_all():
    """Clean up expired entries from all caches"""
    cache_dir = Path.home() / '.cache' / 'french-tools'
    
    if not cache_dir.exists():
        console.print("[dim]No cache directory found[/dim]")
        return
    
    total_removed = 0
    cache_files = ['wordreference', 'conjugation', 'verbecc']
    
    for cache_name in cache_files:
        cache = ToolCache(cache_name)
        removed = cache.cleanup_expired()
        total_removed += removed
    
    if total_removed > 0:
        console.print(f"[green]✅ Removed {total_removed} expired entries[/green]")
    else:
        console.print("[dim]No expired entries found[/dim]")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'stats':
            show_all_cache_stats()
        elif command == 'clear':
            clear_all_caches()
        elif command == 'cleanup':
            cleanup_expired_all()
        else:
            console.print(f"[red]Unknown command: {command}[/red]")
            console.print("Available commands: stats, clear, cleanup")
    else:
        show_all_cache_stats()