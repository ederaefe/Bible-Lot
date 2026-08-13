"""
================================================================================
LOT - A Sacred Scripture Draw (Offline CLI Edition)
================================================================================

Hello! If you are not a programmer, do not worry. This file is designed to be 
simple to use directly from your computer, acting as your personal, offline 
spiritual tool. 

WHAT IS THIS?
This is a minimalist program that mathematically draws a random, strictly 
verified Bible reference (Book, Chapter, or Verse). It works completely offline 
to give you the reference. If you happen to be connected to Wi-Fi, it will also 
fetch the verse text for you. If you are offline, it will simply invite you to 
open your physical Bible.

HOW TO RUN THIS PROGRAM:

Step 1: Install Python
- If you don't have Python, download and install it from https://www.python.org/
- (Windows users: Make sure to check the box "Add Python to PATH" during setup!)

Step 2: Open your Terminal or Command Prompt
- Windows: Press the Windows Start button, type "cmd", and hit Enter.
- Mac: Press Cmd + Space, type "Terminal", and hit Enter.

Step 3: Install the required visual libraries
- Type this exact command into your terminal window and hit Enter:
  pip install rich requests

Step 4: Run the file
- In your terminal, navigate to the folder where you saved this file. 
  (For example, type: cd Downloads)
- Type this command and hit Enter:
  python lot.py

(Alternatively, on some Windows computers, you can simply double-click this 
file once Python and the libraries are installed!)
================================================================================
"""

import os
import sys
import random
import time

# Safely check for required packages and pause if missing, making it easy for non-devs
try:
    import requests
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt
    from rich.text import Text
    from rich.align import Align
    from rich import box
    from rich.live import Live
except ImportError:
    print("\n[!] MISSING REQUIRED LIBRARIES [!]")
    print("Please install the required visual packages before running this script.")
    print("Open your terminal or command prompt and run the following command:\n")
    print("    pip install rich requests\n")
    
    # Wait command so the terminal doesn't close immediately if double-clicked
    if os.name == 'nt':
        os.system('pause')
    else:
        input("Press Enter to exit...")
    sys.exit(1)

console = Console()

# The exact same verified dataset from the web app. 
# Contains all chapters and verse counts to allow 100% offline reference drawing.
BIBLE = [
    ["Genesis","OT","Law",[31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,55,32,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26]],
    ["Exodus","OT","Law",[22,25,22,31,23,30,25,32,35,29,10,51,22,31,27,36,16,27,25,26,36,31,33,18,40,37,21,43,46,38,18,35,23,35,35,38,29,31,43,38]],
    ["Leviticus","OT","Law",[17,16,17,35,19,30,38,36,24,20,47,8,59,57,33,34,16,30,37,27,24,33,44,23,55,46,34]],
    ["Numbers","OT","Law",[54,34,51,49,31,27,89,26,23,36,35,16,33,45,41,50,13,32,22,29,35,41,30,25,18,65,23,31,40,16,54,42,56,29,34,13]],
    ["Deuteronomy","OT","Law",[46,37,29,49,33,25,26,20,29,22,32,32,18,29,23,22,20,22,21,20,23,30,25,22,19,19,26,68,29,20,30,52,29,12]],
    ["Joshua","OT","History",[18,24,17,24,15,27,26,35,27,43,23,24,33,15,63,10,18,28,51,9,45,34,16,33]],
    ["Judges","OT","History",[36,23,31,24,31,40,25,35,57,18,40,15,25,20,20,31,13,31,30,48,25]],
    ["Ruth","OT","History",[22,23,18,22]],
    ["1 Samuel","OT","History",[28,36,21,22,12,21,17,22,27,27,15,25,23,52,35,23,58,30,24,42,15,23,29,22,44,25,12,25,11,31,13]],
    ["2 Samuel","OT","History",[27,32,39,12,25,23,29,18,13,19,27,31,39,33,37,23,29,33,43,26,22,51,39,25]],
    ["1 Kings","OT","History",[53,46,28,34,18,38,51,66,28,29,43,33,34,31,34,34,24,46,21,43,29,53]],
    ["2 Kings","OT","History",[18,25,27,44,27,33,20,29,37,36,21,21,25,29,38,20,41,37,37,21,26,20,37,20,30]],
    ["1 Chronicles","OT","History",[54,55,24,43,26,81,40,40,44,14,47,40,14,17,29,43,27,17,19,8,30,19,32,31,31,32,34,21,30]],
    ["2 Chronicles","OT","History",[17,18,17,22,14,42,22,18,31,19,23,16,22,15,19,14,19,34,11,37,20,12,21,27,28,23,9,27,36,27,21,33,25,33,27,23]],
    ["Ezra","OT","History",[11,70,13,24,17,22,28,36,15,44]],
    ["Nehemiah","OT","History",[11,20,32,23,19,19,73,18,38,39,36,47,31]],
    ["Esther","OT","History",[22,23,15,17,14,14,10,17,32,3]],
    ["Job","OT","Wisdom",[22,13,26,21,27,30,21,22,35,22,20,25,28,22,35,22,16,21,29,29,34,30,17,25,6,14,23,28,25,31,40,22,33,37,16,33,24,41,30,24,34,17]],
    ["Psalms","OT","Wisdom",[6,12,8,8,12,10,17,9,20,18,7,8,6,7,5,11,15,50,14,9,13,31,6,10,22,12,14,9,11,12,24,11,22,22,28,12,40,22,13,17,13,11,5,26,17,11,9,14,20,23,19,9,6,7,23,13,11,11,17,12,8,12,11,10,13,20,7,35,36,5,24,20,28,23,10,12,20,72,13,19,16,8,18,12,13,17,7,18,52,17,16,15,5,23,11,13,12,9,9,5,8,28,22,35,45,48,43,13,31,7,10,10,9,8,18,19,2,29,176,7,8,9,4,8,5,6,5,6,8,8,3,18,3,3,21,26,9,8,24,13,10,7,12,15,21,10,20,14,9,6]],
    ["Proverbs","OT","Wisdom",[33,22,35,27,23,35,27,36,18,32,31,28,25,35,33,33,28,24,29,30,31,29,35,34,28,28,27,28,27,33,31]],
    ["Ecclesiastes","OT","Wisdom",[18,26,22,16,20,12,29,17,18,20,10,14]],
    ["Song of Solomon","OT","Wisdom",[17,17,11,16,16,13,13,14]],
    ["Isaiah","OT","Prophets",[31,22,26,6,30,13,25,22,21,34,16,6,22,32,9,14,14,7,25,6,17,25,18,23,12,21,13,29,24,33,9,20,24,17,10,22,38,22,8,31,29,25,28,28,25,13,15,22,26,11,23,15,12,17,13,12,21,14,21,22,11,12,19,12,25,24]],
    ["Jeremiah","OT","Prophets",[19,37,25,31,31,30,34,22,26,25,23,17,27,22,21,21,27,23,15,18,14,30,40,10,38,24,22,17,32,24,40,44,26,22,19,32,21,28,18,16,18,22,13,30,5,28,7,47,39,46,64,34]],
    ["Lamentations","OT","Prophets",[22,22,66,22,22]],
    ["Ezekiel","OT","Prophets",[28,10,27,17,17,14,27,18,11,22,25,28,23,23,8,63,24,32,14,49,32,31,49,27,17,21,36,26,21,26,18,32,33,31,15,38,28,23,29,49,26,20,27,31,25,24,23,35]],
    ["Daniel","OT","Prophets",[21,49,30,37,31,28,28,27,27,21,45,13]],
    ["Hosea","OT","Prophets",[11,23,5,19,15,11,16,14,17,15,12,14,16,9]],
    ["Joel","OT","Prophets",[20,32,21]],
    ["Amos","OT","Prophets",[15,16,15,13,27,14,17,14,15]],
    ["Obadiah","OT","Prophets",[21]],
    ["Jonah","OT","Prophets",[17,10,10,11]],
    ["Micah","OT","Prophets",[16,13,12,13,15,16,20]],
    ["Nahum","OT","Prophets",[15,13,19]],
    ["Habakkuk","OT","Prophets",[17,20,19]],
    ["Zephaniah","OT","Prophets",[18,15,20]],
    ["Haggai","OT","Prophets",[15,23]],
    ["Zechariah","OT","Prophets",[21,13,10,14,11,15,14,23,17,12,17,14,9,21]],
    ["Malachi","OT","Prophets",[14,17,18,6]],
    ["Matthew","NT","Gospels",[25,23,17,25,48,34,29,34,38,42,30,50,58,36,39,28,27,35,30,34,46,46,39,51,46,75,66,20]],
    ["Mark","NT","Gospels",[45,28,35,41,43,56,37,38,50,52,33,44,37,72,47,20]],
    ["Luke","NT","Gospels",[80,52,38,44,39,49,50,56,62,42,54,59,35,35,32,31,37,43,48,47,38,71,56,53]],
    ["John","NT","Gospels",[51,25,36,54,47,71,53,59,41,42,57,50,38,31,27,33,26,40,42,31,25]],
    ["Acts","NT","Acts",[26,47,26,37,42,15,60,40,43,48,30,25,52,28,41,40,34,28,41,38,40,30,35,27,27,32,44,31]],
    ["Romans","NT","Epistles",[32,29,31,25,21,23,25,39,33,21,36,21,14,23,33,27]],
    ["1 Corinthians","NT","Epistles",[31,16,23,21,13,20,40,13,27,33,34,31,13,40,58,24]],
    ["2 Corinthians","NT","Epistles",[24,17,18,18,21,18,16,24,15,18,33,21,14]],
    ["Galatians","NT","Epistles",[24,21,29,31,26,18]],
    ["Ephesians","NT","Epistles",[23,22,21,32,33,24]],
    ["Philippians","NT","Epistles",[30,30,21,23]],
    ["Colossians","NT","Epistles",[29,23,25,18]],
    ["1 Thessalonians","NT","Epistles",[10,20,13,18,28]],
    ["2 Thessalonians","NT","Epistles",[12,17,18]],
    ["1 Timothy","NT","Epistles",[20,15,16,16,25,21]],
    ["2 Timothy","NT","Epistles",[18,26,17,22]],
    ["Titus","NT","Epistles",[16,15,15]],
    ["Philemon","NT","Epistles",[25]],
    ["Hebrews","NT","Epistles",[14,18,19,16,14,20,28,13,28,39,40,29,25]],
    ["James","NT","Epistles",[27,26,18,17,20]],
    ["1 Peter","NT","Epistles",[25,25,22,19,14]],
    ["2 Peter","NT","Epistles",[21,22,18]],
    ["1 John","NT","Epistles",[10,29,24,21,21]],
    ["2 John","NT","Epistles",[13]],
    ["3 John","NT","Epistles",[14]],
    ["Jude","NT","Epistles",[25]],
    ["Revelation","NT","Prophecy",[20,29,22,11,14,17,17,13,21,11,19,17,18,20,8,21,18,24,21,15,27,21]]
]

def clear_screen():
    console.clear()

def print_header():
    header_text = Text()
    header_text.append("Lot. ", style="bold italic dark_goldenrod")
    header_text.append("A Sacred Scripture Draw\n", style="bold white")
    header_text.append("── Draw from the living text ──", style="dim")
    console.print(Panel(Align.center(header_text), box=box.ROUNDED, border_style="dark_goldenrod"))
    console.print()

def print_menu():
    menu_text = Text()
    menu_text.append("[1] ", style="bold dark_goldenrod")
    menu_text.append("Cast the Lot (Quick Verse)\n")
    menu_text.append("[2] ", style="bold dark_goldenrod")
    menu_text.append("Cast with Custom Filters\n")
    menu_text.append("[3] ", style="bold dark_goldenrod")
    menu_text.append("Close and depart")
    console.print(Panel(menu_text, title="Main Menu", title_align="left", box=box.MINIMAL, border_style="dim"))

def get_pool(testament_choice):
    if testament_choice == 2:
        return [b for b in BIBLE if b[1] == "OT"]
    elif testament_choice == 3:
        return [b for b in BIBLE if b[1] == "NT"]
    return BIBLE

def generate_draw(pool, depth):
    book_entry = random.choice(pool)
    name, test, genre, counts = book_entry
    chapter = random.randint(1, len(counts))
    verse_count = counts[chapter - 1]
    verse = random.randint(1, verse_count)
    
    return {
        "book": name,
        "testament": test,
        "genre": genre,
        "chapter": chapter,
        "verse": verse,
        "depth": depth
    }

def fetch_verse_text(result):
    book_fmt = result["book"].replace(" ", "+")
    ref = f"{book_fmt}+{result['chapter']}:{result['verse']}"
    url = f"https://bible-api.com/{ref}"
    
    try:
        response = requests.get(url, timeout=4) # Short timeout so offline users aren't left waiting
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "").strip()
    except requests.RequestException:
        return None
    return None

def build_ref_string(result):
    if result["depth"] == "book":
        return result["book"]
    elif result["depth"] == "chapter":
        return f"{result['book']} {result['chapter']}"
    else:
        return f"{result['book']} {result['chapter']}:{result['verse']}"

def animate_cast(pool):
    """Simulates the spinning reel deceleration of a physical lot."""
    console.print("\n[dim italic]Casting the lot...[/]")
    with Live(refresh_per_second=15, transient=True) as live:
        for i in range(25):
            fake_book = random.choice(pool)[0]
            fake_chap = random.randint(1, 150)
            fake_verse = random.randint(1, 100)
            
            # Create a rapid shuffling effect
            text = Text(f"> {fake_book} {fake_chap}:{fake_verse} <", style="dark_goldenrod")
            live.update(Align.center(text))
            
            # Decelerate smoothly
            time.sleep(0.02 + (i / 150))

def run_draw(pool, depth):
    animate_cast(pool)
    result = generate_draw(pool, depth)
    ref_str = build_ref_string(result)
    
    clear_screen()
    print_header()
    
    console.print(f"[dim]Reference secured from the {result['testament']} | Genre: {result['genre']}[/]", justify="center")
    
    if depth == "verse":
        with console.status("[dim]Retrieving ancient text...[/]", spinner="dots"):
            verse_text = fetch_verse_text(result)
        
        # Graceful handling for offline users!
        if verse_text:
            panel_content = f"[bold dark_goldenrod]{ref_str}[/]\n\n[italic white]\"{verse_text}\"[/]"
        else:
            panel_content = f"[bold dark_goldenrod]{ref_str}[/]\n\n[dim italic]You are currently offline.\nThe lot has been cast—open your physical Bible to read this passage.[/]"
    else:
        panel_content = f"\n[bold dark_goldenrod]{ref_str}[/]\n"
    
    console.print(Panel(Align.center(panel_content), box=box.DOUBLE_EDGE, padding=(1, 4), border_style="dark_goldenrod"))
    console.print()

def main():
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = Prompt.ask("\n[bold]Select an option[/]", choices=["1", "2", "3"], default="1")
        
        if choice == "3":
            console.print("\n[dim italic]Go in peace.[/]\n")
            sys.exit(0)
            
        elif choice == "1":
            # Quick Draw - All Bible, Verse depth
            pool = BIBLE
            depth = "verse"
            run_draw(pool, depth)
            
        elif choice == "2":
            # Custom Filters
            console.print("\n[bold]1. Select Testament[/]")
            console.print("  [dim][1][/] All Scripture")
            console.print("  [dim][2][/] Old Testament")
            console.print("  [dim][3][/] New Testament")
            t_choice = IntPrompt.ask("Choice", choices=["1", "2", "3"], default=1)
            
            console.print("\n[bold]2. Select Draw Scope[/]")
            console.print("  [dim][1][/] Verse [dim](Deepest)[/]")
            console.print("  [dim][2][/] Chapter")
            console.print("  [dim][3][/] Book [dim](Broadest)[/]")
            d_choice = IntPrompt.ask("Choice", choices=["1", "2", "3"], default=1)
            
            depth_map = {1: "verse", 2: "chapter", 3: "book"}
            depth = depth_map[d_choice]
            pool = get_pool(t_choice)
            
            run_draw(pool, depth)

        # Pause before looping back to main menu
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # If the user presses Ctrl+C to exit
        console.print("\n\n[dim italic]Go in peace.[/]\n")
        sys.exit(0)
