import random 
import time 
from datetime import datetime , timedelta 
from rich.console import Console 
from rich.panel import Panel 
from rich.table import Table 
from rich.columns import Columns 
from rich.prompt import Prompt 
from rich import box 

console = Console()

FIRST_NAMES = ["Orpheus" , "Heidi" , "Zach" , "Max" ,"Ada", "Linus", "Grace","Leo", "Maya", "Kai"] 
LAST_NAMES = ["Dinasour", "Raccoon", "Latta", "Wottford","Lovelace", "Torvalds", "Hopper", "Chen","Patel","Tanaka" ]
COUNTRIES =  ["Dino Island","United States","Qatar","Japan","Germany","Canada","Brazil","India"]
EVENTS = ["Apex","Counterspell","Boreal","Outernet","Apocalypse","Arcade"]
VALID_STAMPS = ["EMBASSY-2026","ORPHEUS-OK","YSWS-VERIFIED",]
FAKE_STAMPS = ["EMBASSY-2025","ORPHEUS-NO","FAKE-STAMP","PENDING-99"]


def get_daily_rules(day: int) -> dict:
    return {
        "min_commits": 15 if day >= 2 else 1,
        "banned_country": "Dino Island" if day >= 3 else None,
    }


def generate_entrant(day: int) -> dict:
    rules = get_daily_rules(day)
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    allowed_countries = [c for c in COUNTRIES if c != rules["banned_country"]]
    country = random.choice(allowed_countries)
    event = random.choice(EVENTS)
    slack_id = f"U0{random.randint(1000000,9999999)}"
    github_commits = random.randint(rules["min_commits"] + 5, 120)

    today = datetime.now() + timedelta(days=day - 1)
    exp_date = today + timedelta(days=random.randint(30, 365))
    stamp = random.choice(VALID_STAMPS) 

    is_valid = random.choice([True, False])
    reason = "All documents verified."
    statement = f"Im flying rom {country} to build a project for hack club {event}!"
    if not is_valid:
        possible_flaws = ["expired", "bad slack", "fake stamp", "low_commits", "lie"]
        if rules["banned_country"]:
            possible_flaws.append("banned_country")

        flaw = random.choice(possible_flaws)
        if flaw == "expired":
            exp_date = today - timedelta(days=random.randint(1,60))
            reason = f"Passport expired on {exp_date.strftime('%Y-%m-%d')}."
        elif flaw == "bad slack":
            slack_id = f"X9{random.randint(1000000,9999999)}"
            reason = "invalid Slack ID prefix (it shld start with 'U0')."
        elif flaw == "fake stamp":
            stamp = random.choice(FAKE_STAMPS)
            reason = f"Unrecognized Embassy stamp: {stamp}."
        elif flaw == "low_commits":
            github_commits = 0 if day == 1 else random.randint(5, rules["min_commits"] - 1)
            reason = f"Only {github_commits} Github commits logged (need {rules['min_commits']} today)!"
        elif flaw == "banned_country":
            country = rules["banned_country"]
            statement = f"Im flying rom {country} to build a project for hack club {event}!"
            reason = f"Travelers from {country} are restricted starting Day 3!"
        elif flaw == "lie":
            github_commits = random.randint(1,4)
            fake_event = random.choice ([e for e in EVENTS if e != event])
            statement = f"erm im super excited ig to attend hack club {fake_event}!"
            reason = f"lied during interrogation u scammer! passport says {event} but they said {fake_event}" 
        
    return {
        "name": name,
        "country": country,
        "event": event,
        "slack_id": slack_id,
        "commits": github_commits,
        "expiritation date": exp_date.strftime("%Y-%m-%d"),
        "stamp": stamp,
        "is_valid": is_valid,
        "reason": reason,
        "statement": statement,
        "current_date": today.strftime("%Y-%m-%d"),
    }


def render_desk (entrant: dict , score: int, citations: int, day:int):
    console.clear()
    rules_data = get_daily_rules(day)

    header = Panel(
        f"[bold cyan]HACK CLUB EMBASSY CHECKPOINT[/bold cyan]  |  "
        f"Date: [yellow]{entrant['current_date']}[/yellow]  |  "
        f"Day: [bold]{day}[/bold]  |  "
        f"Approved/Caught: [green]{score}[/green]  |  "
        f"Citations: [red]{citations}/3[/red]",
        box=box.DOUBLE,
        style="white on black"
    )
    console.print(header)

    rule_text = (
        "[bold underline]todays entry requirments[/bold underline]\n"
        "1. passport must [bold green]NOT be expired[/bold green] (check Date above).\n"
        "2. slack id must start with [bold cyan]U0[/bold cyan].\n"
        "3. stamp must be: [bold]EMBASSY-2026[/bold], [bold]ORPHEUS-OK[/bold], or [bold]YSWS-VERIFIED[/bold].\n"
        f"4. hacker should have [bold yellow]at least {rules_data['min_commits']} github commit(s)[/bold yellow].\n"
        "5. press [bold magenta]I[/bold magenta] to interrogate a person if they seem sus."
    )
    if rules_data["banned_country"]:
        rule_text += f"\n[bold red]6. NEW: deny all travelers from {rules_data['banned_country']}![/bold red]"

    rules = Panel(
        rule_text,
        title="[bold yellow]official rulebook[/bold yellow]",
        border_style="yellow",
        width=50
    )

    passport_table = Table(show_header=False,box=box.SIMPLE)
    passport_table.add_row("[bold]NAME:[/bold]", entrant["name"])
    passport_table.add_row("[bold]ORIGIN:[/bold]", entrant["country"])  
    passport_table.add_row("[bold]DESTINATION:[/bold]", f"Hack Club {entrant['event']}")
    passport_table.add_row("[bold]EXPIRES:[/bold]", f"[bold]{entrant['expiritation date']}[/bold]")
    passport_table.add_row("[bold]VISA STAMP:[/bold]", f"[bold magenta]{entrant['stamp']}[/bold magenta]")

    passport = Panel (
        passport_table,
        title="[bold cyan]hack club passport[/bold cyan]",
        border_style="cyan",
        width=45
    )

    system_table = Table(show_header=False, box=box.SIMPLE)
    system_table.add_row("[bold]slack id:[/bold]", entrant["slack_id"])
    system_table.add_row("[bold]hackatime commits:[/bold]", str(entrant["commits"]))
    system_table.add_row("[bold]status:[/bold]", "waiting for border decision..")

    system_panel = Panel(
        system_table,
        title="[bold green]EMBASSY DATABASE LOOKUP[/bold green]",
        border_style="green",
        width=48
    )

    console.print(Columns([rules, passport, system_panel]))


def main():
    score = 0 
    citations = 0 
    day = 1 
    processed_today = 0 
    interrogations_left = 2 

    console.print("[bold cyan]startin hack club embassy checkpoint[/bold cyan]")
    time.sleep(1)

    while citations < 3:
        entrant = generate_entrant(day)
        interrogated = False

        while True:
            render_desk(entrant,score,citations,day)

            if interrogated:
                console.print(Panel(
                    f"[bold italic]\"{entrant['statement']}\"[/bold italic]",
                    title=f"[bold magenta]{entrant['name']} says:[/bold magenta]",
                    border_style="magenta"
                ))

            decision = Prompt.ask(
              f"\n[bold white]Action[/bold white] ([bold green]A[/bold green]pprove / [bold red]D[/bold red]eny / [bold magenta]I[/bold magenta]nterrogte [{interrogations_left} left] / [bold dim]Q[/bold dim]uit)",
               choices=["a","d","i","q","A","D","I","Q"],
               show_choices=False
               ).lower()

            if decision == "i":
              if interrogated:
                  console.print("\n[yellow]You already interrogated this hacker![/yellow]")
                  time.sleep(1.2)
              elif interrogations_left > 0:
                  interrogations_left -= 1
                  interrogated = True 
              else:
                  console.print("\n[red]no interrogation remaining for u buddy![/red]")
                  time.sleep(1.2)
            else:
                break
        
        if decision == "q":
            console.print("\n[yellow]Shift ended early. Glory to Hack Club![/yellow]")
            break

        approved = decision == "a"

        if approved == entrant["is_valid"]:
            score += 1
            console.print("\n[bold green]✓ CORRECT DECISION![/bold green] Next hacker approaching...")
        else:
            citations += 1
            if "lied during interrogation" in entrant["reason"].lower() and not interrogated:
                console.print("\n[bold red]✗ EMBASSY CITATION ISSUED![/bold red] Their documents were valid, but you didn't interrogate them to catch their lie!")
            else:
                console.print(f"\n[bold red]✗ EMBASSY CITATION ISSUED![/bold red] {entrant['reason']}")

        processed_today += 1
        if processed_today >= 4:
            day += 1
            processed_today = 0
            interrogations_left = 2
            console.print(f"\n[bold cyan]--- SHIFT COMPLETE! Advancing to Day {day} (New Rules Active!) ---[/bold cyan]")

        time.sleep(2.2)

    if citations >= 3:
        console.print(Panel(
            f"[bold red]YOU HAVE BEEN FIRED FROM THE EMBASSY![/bold red]\n"
            f"Final Score: [bold]{score}[/bold] hackers processed across [bold]{day}[/bold] days.",
            border_style="red"
        ))
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()