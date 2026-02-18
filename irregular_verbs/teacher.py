#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# ---------------- Data ----------------
# Format: (base, past, past participle, german)
VERBS: List[Tuple[str, str, str, str]] = [
    ("be", "was/were", "been", "sein"),
    ("beat", "beat", "beaten", "schlagen; besiegen"),
    ("become", "became", "become", "werden"),
    ("begin", "began", "begun", "beginnen; anfangen"),
    ("bet", "bet", "bet", "wetten"),
    ("bite", "bit", "bitten", "beißen"),
    ("blow", "blew", "blown", "blasen; pusten"),
    ("break", "broke", "broken", "(zer)brechen; kaputt machen"),
    ("bring", "brought", "brought", "(mit)bringen"),
    ("build", "built", "built", "bauen"),
    ("burn", "burnt/burned", "burnt/burned", "(ver)brennen"),
    ("buy", "bought", "bought", "kaufen"),
    ("catch", "caught", "caught", "fangen"),
    ("choose", "chose", "chosen", "(aus)wählen"),
    ("come", "came", "come", "kommen"),
    ("cost", "cost", "cost", "kosten"),
    ("cut", "cut", "cut", "schneiden"),
    ("deal (with)", "dealt (with)", "dealt (with)", "sich befassen (mit); umgehen (mit)"),
    ("do", "did", "done", "machen; tun"),
    ("draw", "drew", "drawn", "zeichnen; ziehen"),
    ("dream", "dreamt/dreamed", "dreamt/dreamed", "träumen"),
    ("drink", "drank", "drunk", "trinken"),
    ("drive", "drove", "driven", "fahren"),
    ("eat", "ate", "eaten", "essen"),
    ("fall", "fell", "fallen", "(hin)fallen"),
    ("feed", "fed", "fed", "füttern; ernähren"),
    ("feel", "felt", "felt", "fühlen"),
    ("fight", "fought", "fought", "kämpfen; (sich) streiten"),
    ("find", "found", "found", "finden"),
    ("fit", "fit/fitted", "fit/fitted", "passen"),
    ("fly", "flew", "flown", "fliegen"),
    ("forget", "forgot", "forgotten", "vergessen"),
    ("forgive", "forgave", "forgiven", "vergeben; verzeihen"),
    ("freeze", "froze", "frozen", "gefrieren; erstarren"),
    ("get", "got", "got", "bekommen; erhalten"),
    ("give", "gave", "given", "geben"),
    ("go", "went", "gone", "gehen; fahren"),
    ("grow", "grew", "grown", "wachsen; anbauen; züchten"),
    ("hang", "hung", "hung", "hängen"),
    ("have", "had", "had", "haben"),
    ("hear", "heard", "heard", "hören"),
    ("hide", "hid", "hidden", "(sich) verstecken"),
    ("hit", "hit", "hit", "schlagen; treffen"),
    ("hold", "held", "held", "(fest)halten"),
    ("hurt", "hurt", "hurt", "verletzen; sich weh tun"),
    ("keep", "kept", "kept", "(auf)bewahren; behalten"),
    ("know", "knew", "known", "kennen; wissen"),
    ("lead", "led", "led", "(an)führen"),
    ("learn", "learnt/learned", "learnt/learned", "lernen"),
    ("leave", "left", "left", "(ver)lassen"),
    ("lend", "lent", "lent", "(ver)leihen"),
    ("let", "let", "let", "lassen"),
    ("lie", "lay", "lain", "liegen"),
    ("lose", "lost", "lost", "verlieren"),
    ("make", "made", "made", "machen; tun"),
    ("mean", "meant", "meant", "bedeuten; meinen"),
    ("meet", "met", "met", "treffen"),
    ("pay", "paid", "paid", "(be)zahlen"),
    ("put", "put", "put", "legen; setzen; stellen"),
    ("read", "read", "read", "lesen"),
    ("ride", "rode", "ridden", "fahren; reiten"),
    ("ring", "rang", "rung", "klingeln; läuten"),
    ("rise", "rose", "risen", "steigen; sich erheben"),
    ("run", "ran", "run", "laufen; rennen"),
    ("say", "said", "said", "sagen"),
    ("see", "saw", "seen", "sehen"),
    ("sell", "sold", "sold", "verkaufen"),
    ("send", "sent", "sent", "senden; verschicken"),
    ("set up", "set up", "set up", "erbauen; errichten"),
    ("shine", "shone", "shone", "scheinen; glänzen"),
    ("shoot", "shot", "shot", "schießen"),
    ("show", "showed", "shown", "zeigen"),
    ("sing", "sang", "sung", "singen"),
    ("sink", "sank", "sunk", "untergehen; sinken"),
    ("sit", "sat", "sat", "sitzen"),
    ("sleep", "slept", "slept", "schlafen"),
    ("smell", "smelt/smelled", "smelt/smelled", "riechen; duften"),
    ("speak", "spoke", "spoken", "sprechen"),
    ("spell", "spelt/spelled", "spelt/spelled", "buchstabieren"),
    ("spend", "spent", "spent", "ausgeben; verbringen"),
    ("spill", "spilt/spilled", "spilt/spilled", "verschütten; auslaufen"),
    ("stand", "stood", "stood", "stehen"),
    ("steal", "stole", "stolen", "stehlen"),
    ("sting", "stung", "stung", "stechen"),
    ("swim", "swam", "swum", "schwimmen"),
    ("take", "took", "taken", "nehmen"),
    ("teach", "taught", "taught", "unterrichten; lehren; beibringen"),
    ("tell", "told", "told", "erzählen"),
    ("think", "thought", "thought", "(nach)denken; glauben"),
    ("throw", "threw", "thrown", "werfen"),
    ("understand", "understood", "understood", "verstehen"),
    ("wake up", "woke up", "woken up", "(auf)wachen; (auf)wecken"),
    ("wear", "wore", "worn", "anhaben; tragen"),
    ("win", "won", "won", "gewinnen; siegen"),
    ("write", "wrote", "written", "schreiben"),
]

# ---------------- Settings ----------------
CASE_INSENSITIVE = False       # If True: ignore case
WEIGHTED_RANDOM = True         # If True: verbs you miss more often show up more
MIN_WEIGHT = 1.0
WEIGHT_PER_WRONG = 0.75
SHOW_HINT_AFTER_FAIL = True    # Show allowed variants after a mistake

STATE_PATH = os.path.join(os.path.expanduser("~"), ".irregular_verbs_trainer_state.json")

# ---------------- ANSI colors ----------------
RED = "\033[0;31m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
YELLOW = "\033[0;33m"
NC = "\033[0m"


@dataclass(frozen=True)
class Verb:
    base: str
    past: str
    pp: str
    german: str


def normalize(s: str) -> str:
    s = s.strip()
    return s.lower() if CASE_INSENSITIVE else s


def split_options(allowed: str) -> List[str]:
    # "burnt/burned" -> ["burnt", "burned"]
    return [opt.strip() for opt in allowed.split("/")]


def is_correct(user_input: str, allowed: str) -> bool:
    u = normalize(user_input)
    for opt in split_options(allowed):
        if u == normalize(opt):
            return True
    return False


def colorize(ok: bool, text: str) -> str:
    return f"{GREEN if ok else RED}{text}{NC}"


def load_state() -> Dict[str, int]:
    if not os.path.exists(STATE_PATH):
        return {}
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {str(k): int(v) for k, v in data.items()}
    except Exception:
        pass
    return {}


def save_state(wrong_counts: Dict[str, int]) -> None:
    try:
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(wrong_counts, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"{YELLOW}Warning: Could not save progress: {e}{NC}")


def reset_state() -> None:
    try:
        if os.path.exists(STATE_PATH):
            os.remove(STATE_PATH)
    except Exception as e:
        print(f"{YELLOW}Warning: Could not delete progress file: {e}{NC}")


def print_stats(wrong_counts: Dict[str, int], verbs: List[Verb]) -> None:
    print()
    print(f"{CYAN}Stats (only verbs with mistakes). File: {STATE_PATH}{NC}")
    items = [(k, v) for k, v in wrong_counts.items() if v > 0]
    items.sort(key=lambda x: x[1], reverse=True)
    if not items:
        print("  (no mistakes saved yet)")
        return

    de_map = {v.base: v.german for v in verbs}
    for base, cnt in items[:30]:
        print(f"  {base:<15} {cnt:>3}  {de_map.get(base, '')}")
    if len(items) > 30:
        print(f"  ... ({len(items) - 30} more)")
    print()


def choose_verb(verbs: List[Verb], wrong_counts: Dict[str, int]) -> Verb:
    if not WEIGHTED_RANDOM:
        return random.choice(verbs)

    weights = []
    for v in verbs:
        w = MIN_WEIGHT + WEIGHT_PER_WRONG * float(wrong_counts.get(v.base, 0))
        weights.append(max(MIN_WEIGHT, w))
    return random.choices(verbs, weights=weights, k=1)[0]


def read_answer(prompt: str) -> Optional[str]:
    try:
        s = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if not s:
        return ""  # allow empty input (counts as wrong)
    if s.lower() == "q":
        return None
    return s


def main() -> int:
    verbs = [Verb(*t) for t in VERBS]
    wrong_counts = load_state()

    print(f"{CYAN}Irregular Verbs Trainer{NC}")
    print("Type 'q' to quit at any prompt.")
    print("Commands: ':stats' (show stats), ':reset' (delete saved progress)")
    print(f"Mode: weighted_random={WEIGHTED_RANDOM}, case_insensitive={CASE_INSENSITIVE}")
    print()

    while True:
        v = choose_verb(verbs, wrong_counts)

        print(f"{YELLOW}German meaning:{NC} {v.german}")

        a1 = read_answer("Infinitive (base form): ")
        if a1 is None:
            break
        if a1 == ":stats":
            print_stats(wrong_counts, verbs)
            continue
        if a1 == ":reset":
            reset_state()
            wrong_counts = {}
            print(f"{CYAN}Progress deleted.{NC}\n")
            continue

        a2 = read_answer("Simple Past: ")
        if a2 is None:
            break

        a3 = read_answer("Past Participle: ")
        if a3 is None:
            break

        ok1 = is_correct(a1, v.base)
        ok2 = is_correct(a2, v.past)
        ok3 = is_correct(a3, v.pp)

        any_wrong = not (ok1 and ok2 and ok3)
        if any_wrong:
            wrong_counts[v.base] = wrong_counts.get(v.base, 0) + 1
            save_state(wrong_counts)

        print()
        print("Correct forms:")
        print("  " + colorize(ok1, v.base) + " | " + colorize(ok2, v.past) + " | " + colorize(ok3, v.pp))

        if any_wrong and SHOW_HINT_AFTER_FAIL:
            def fmt_opts(s: str) -> str:
                opts = split_options(s)
                return ", ".join(opts) if len(opts) > 1 else opts[0]

            print(f"Allowed variants: base={fmt_opts(v.base)}; past={fmt_opts(v.past)}; pp={fmt_opts(v.pp)}")

        print(f"Mistakes for '{v.base}': {wrong_counts.get(v.base, 0)}")
        print("-" * 60)
        print()

    print()
    print(f"{CYAN}Goodbye.{NC} (progress file: {STATE_PATH})")
    print_stats(wrong_counts, verbs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
