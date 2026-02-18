import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# =========================
# Data set (infinitive, simple_past, past_participle, german)
# =========================
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


# =========================
# Helpers: normalization & checking
# =========================
def normalize(s: str) -> str:
    return " ".join(s.strip().lower().split())


def accepted_answers(correct: str) -> List[str]:
    return [normalize(x) for x in correct.split("/")]


def is_correct(user_input: str, correct: str) -> bool:
    return normalize(user_input) in accepted_answers(correct)


def format_mmss(seconds: float) -> str:
    total = int(round(seconds))
    minutes = total // 60
    secs = total % 60
    return f"{minutes:02d}:{secs:02d}"


def verb_key(v: Tuple[str, str, str, str]) -> str:
    inf, _, _, german = v
    return f"{german}||{inf}"


# =========================
# Progress persistence (JSON)
# =========================
def load_progress(progress_path: Path) -> Dict:
    if progress_path.exists():
        try:
            return json.loads(progress_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_progress(progress_path: Path, progress: Dict) -> None:
    progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_progress_shape(progress: Dict) -> Dict:
    progress.setdefault("meta", {})
    progress.setdefault("sessions", [])
    progress.setdefault("verbs", {})
    return progress


def update_per_verb(progress: Dict, v: Tuple[str, str, str, str], correct_count: int, time_s: float) -> None:
    k = verb_key(v)
    pv = progress["verbs"].setdefault(
        k,
        {
            "german": v[3],
            "infinitive": v[0],
            "times_asked": 0,
            "total_fields": 0,
            "total_correct_fields": 0,
            "total_time_s": 0.0,
            "last_seen": None,
        },
    )
    pv["times_asked"] += 1
    pv["total_fields"] += 3
    pv["total_correct_fields"] += int(correct_count)
    pv["total_time_s"] += float(time_s)
    pv["last_seen"] = datetime.now().isoformat(timespec="seconds")


def print_progress_summary(progress: Dict) -> None:
    sessions = progress.get("sessions", [])
    if not sessions:
        return

    total_sessions = len(sessions)
    total_fields = sum(s["total_questions"] for s in sessions)
    total_correct = sum(s["total_correct"] for s in sessions)
    total_time_s = sum(s["total_time_s"] for s in sessions)
    overall_acc = (total_correct / total_fields * 100.0) if total_fields else 0.0

    last_n = 5
    recent = sessions[-last_n:]
    recent_fields = sum(s["total_questions"] for s in recent)
    recent_correct = sum(s["total_correct"] for s in recent)
    recent_time_s = sum(s["total_time_s"] for s in recent)
    recent_acc = (recent_correct / recent_fields * 100.0) if recent_fields else 0.0

    per = progress.get("verbs", {})
    tough = []
    for pv in per.values():
        asked = pv["times_asked"]
        if asked < 3:
            continue
        acc = (pv["total_correct_fields"] / pv["total_fields"]) if pv["total_fields"] else 0.0
        tough.append((acc, asked, pv["german"], pv["infinitive"]))
    tough.sort(key=lambda x: (x[0], -x[1]))

    print("\n==============================")
    print("PROGRESS STATISTICS")
    print("==============================")
    print(f"Sessions completed: {total_sessions}")
    print(f"Overall accuracy: {overall_acc:.1f}%")
    print(f"Overall total time: {format_mmss(total_time_s)}")
    print(f"Average time per session: {format_mmss(total_time_s / total_sessions)}")

    print("\nLast 5 sessions:")
    print(f"  Accuracy: {recent_acc:.1f}%")
    print(f"  Total time: {format_mmss(recent_time_s)}")

    if tough:
        print("\nTough verbs (lowest accuracy, asked ≥ 3 times):")
        for acc, asked, german, inf in tough[:10]:
            print(f"  - {german} ({inf}) — {acc*100:.1f}% over {asked} asks")
    else:
        print("\nTough verbs: not enough history yet (need a verb asked at least 3 times).")


# =========================
# Raw input (space-blocking + backspace supported)
# =========================
def beep() -> None:
    # Terminal bell (works in many terminals)
    sys.stdout.write("\a")
    sys.stdout.flush()


def read_line_no_spaces(prompt: str, allow_space: bool = False) -> str:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    user_input = sys.stdin.readline().rstrip("\n")
    
    if not allow_space:
        user_input = user_input.replace(" ", "")
        
    return user_input.strip()


def allow_space_for_field(correct_value: str) -> bool:
    # Allow spaces ONLY when the correct answer(s) contains a space (e.g., "wake up", "set up")
    # If there are alternatives, allow if any alternative has a space.
    for alt in correct_value.split("/"):
        if " " in alt.strip():
            return True
    return False


# =========================
# Quiz interaction
# =========================
def ask_one(v: Tuple[str, str, str, str], log_lines: List[str]) -> Tuple[int, float, List[Tuple[str, str, str]]]:
    """
    Returns:
      correct_count (0-3),
      duration_seconds,
      wrong_fields: list of (field_name, user_value, correct_value)
    """
    inf, past, part, german = v
    print(f"German meaning: {german}")

    log_lines.append(f"German meaning: {german}\n")

    # Space rule is applied per field based on whether the correct value needs spaces.
    allow_inf_space = allow_space_for_field(inf)
    allow_past_space = allow_space_for_field(past)
    allow_part_space = allow_space_for_field(part)

    start = time.time()
    user_inf = read_line_no_spaces("Infinitive: ", allow_space=allow_inf_space)
    user_past = read_line_no_spaces("Simple Past: ", allow_space=allow_past_space)
    user_part = read_line_no_spaces("Past Participle: ", allow_space=allow_part_space)
    duration = time.time() - start

    c_inf = is_correct(user_inf, inf)
    c_past = is_correct(user_past, past)
    c_part = is_correct(user_part, part)

    correct_count = int(c_inf) + int(c_past) + int(c_part)

    wrong_fields = []
    if not c_inf:
        wrong_fields.append(("Infinitive", user_inf, inf))
    if not c_past:
        wrong_fields.append(("Simple Past", user_past, past))
    if not c_part:
        wrong_fields.append(("Past Participle", user_part, part))

    print(f"Time: {format_mmss(duration)} | Correct: {correct_count}/3")

    log_lines.append(f"Your answers: inf='{user_inf}', past='{user_past}', part='{user_part}'\n")
    log_lines.append(f"Correct:      inf='{inf}', past='{past}', part='{part}'\n")
    log_lines.append(f"Result: {correct_count}/3 | Time: {duration:.2f}s ({format_mmss(duration)})\n")

    if wrong_fields:
        print("Correct forms:")
        print(f"  {inf} | {past} | {part}")
        log_lines.append("Mistakes:\n")
        for field, u, corr in wrong_fields:
            log_lines.append(f"  - {field}: user='{u}' -> correct='{corr}'\n")

    log_lines.append("\n")
    return correct_count, duration, wrong_fields


def main():
    print("\nIrregular Verbs Trainer")
    print("------------------------")
    print("You will see the German base meaning.")
    print("Enter the English infinitive, simple past, and past participle.")
    print("Typing spaces is blocked (beep) unless the correct answer needs spaces (e.g., 'wake up').")
    print("Backspace works normally.\n")

    N = 20

    # Paths
    base_dir = Path.home() / "irregular_verbs_logs"
    base_dir.mkdir(parents=True, exist_ok=True)
    progress_path = base_dir / "progress.json"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_log_path = base_dir / f"session_{timestamp}.txt"

    # Load progress
    progress = ensure_progress_shape(load_progress(progress_path))

    # Show progress at start
    if progress.get("sessions"):
        print_progress_summary(progress)
        print()

    # Prepare session
    selected = random.sample(VERBS, N)

    total_correct = 0
    total_questions = N * 3
    total_time_s = 0.0

    wrong_verbs: List[Tuple[str, str, str, str]] = []
    mistakes_detail = []

    log_lines: List[str] = []
    log_lines.append("Irregular Verbs Trainer Session Log\n")
    log_lines.append(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}\n")
    log_lines.append(f"Sample size: {N}\n")
    log_lines.append("=" * 60 + "\n\n")

    # Round 1
    for idx, v in enumerate(selected, 1):
        print(f"\nVerb {idx}/{N}")
        log_lines.append(f"Verb {idx}/{N}\n")

        correct_count, dur, wrong_fields = ask_one(v, log_lines)
        total_correct += correct_count
        total_time_s += dur

        update_per_verb(progress, v, correct_count, dur)

        if wrong_fields:
            wrong_verbs.append(v)
            mistakes_detail.append(
                {
                    "german": v[3],
                    "inf": v[0],
                    "past": v[1],
                    "part": v[2],
                    "wrong_fields": wrong_fields,
                    "time_s": dur,
                }
            )

    # Automatic repetition
    max_rounds = 3
    round_num = 0
    while wrong_verbs and round_num < max_rounds:
        round_num += 1
        print("\n" + "=" * 30)
        print(f"REPEAT ROUND {round_num}")
        print("=" * 30)
        log_lines.append("=" * 60 + "\n")
        log_lines.append(f"REPEAT ROUND {round_num}\n\n")

        random.shuffle(wrong_verbs)
        still_wrong = []
        for idx, v in enumerate(wrong_verbs, 1):
            print(f"\nRepeat {idx}/{len(wrong_verbs)}")
            log_lines.append(f"Repeat {idx}/{len(wrong_verbs)}\n")

            correct_count, dur, wrong_fields = ask_one(v, log_lines)
            total_correct += correct_count
            total_questions += 3
            total_time_s += dur

            update_per_verb(progress, v, correct_count, dur)

            if wrong_fields:
                still_wrong.append(v)

        wrong_verbs = still_wrong

    # Final summary
    accuracy = (total_correct / total_questions) * 100.0 if total_questions else 0.0
    avg_time_per_prompt = total_time_s / (total_questions / 3) if total_questions else 0.0

    print("\n==============================")
    print("FINAL RESULT")
    print("==============================")
    print(f"Total correct answers: {total_correct}/{total_questions}")
    print(f"Accuracy: {accuracy:.1f}%")
    print(f"Total time: {format_mmss(total_time_s)}")
    print(f"Average time per verb prompt: {format_mmss(avg_time_per_prompt)}")
    print(f"Session log saved to: {session_log_path}")
    print(f"Progress file: {progress_path}")

    log_lines.append("\n" + "=" * 60 + "\n")
    log_lines.append("FINAL RESULT\n")
    log_lines.append(f"Total correct answers: {total_correct}/{total_questions}\n")
    log_lines.append(f"Accuracy: {accuracy:.1f}%\n")
    log_lines.append(f"Total time: {format_mmss(total_time_s)}\n")
    log_lines.append(f"Average time per verb prompt: {format_mmss(avg_time_per_prompt)}\n")
    if wrong_verbs:
        log_lines.append(f"Still wrong after repetitions (max {max_rounds} rounds): {len(wrong_verbs)}\n")
    else:
        log_lines.append("All repeated verbs were answered correctly.\n")

    # Mistakes recap (first round)
    if mistakes_detail:
        print("\nMistakes recap (from the first round):")
        print("-------------------------------------")
        for m in mistakes_detail:
            print(f"- German: {m['german']}")
            print(f"  Correct: {m['inf']} | {m['past']} | {m['part']}")
            for field, u, corr in m["wrong_fields"]:
                print(f"  {field}: you='{u}' -> correct='{corr}'")
            print(f"  Time: {format_mmss(m['time_s'])}\n")

        log_lines.append("\nMISTAKES RECAP (first round)\n")
        log_lines.append("-" * 60 + "\n")
        for m in mistakes_detail:
            log_lines.append(f"German: {m['german']}\n")
            log_lines.append(f"Correct: {m['inf']} | {m['past']} | {m['part']}\n")
            for field, u, corr in m["wrong_fields"]:
                log_lines.append(f"  {field}: user='{u}' -> correct='{corr}'\n")
            log_lines.append(f"Time: {m['time_s']:.2f}s ({format_mmss(m['time_s'])})\n\n")
    else:
        print("\nPerfect first round! No mistakes!")
        log_lines.append("\nPerfect first round. No mistakes.\n")

    # Store session into progress.json
    progress["sessions"].append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "base_sample_size": N,
            "total_questions": total_questions,
            "total_correct": total_correct,
            "accuracy_percent": round(accuracy, 2),
            "total_time_s": float(total_time_s),
            "total_time_mmss": format_mmss(total_time_s),
        }
    )

    # Save files
    session_log_path.write_text("".join(log_lines), encoding="utf-8")
    save_progress(progress_path, progress)

    # Show updated progress
    print("\n")
    print_progress_summary(progress)


if __name__ == "__main__":
    main()
