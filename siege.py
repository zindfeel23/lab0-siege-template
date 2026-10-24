import sys


def parse_shot(line):
    parts = line.split("|")
    if len(parts) < 3:
        return None

    head = parts[0].strip()
    if not head.startswith("[") or "]" not in head:
        return None
    end = head.index("]")
    tag = head[1:end]
    name = head[end + 1:].strip()

    base = float(parts[1].strip())

    state = parts[2].strip().lower()
    if state == "active":
        mult = 1.5
    elif state == "broken":
        mult = 0.5
    else:
        mult = 1.0

    buffs = 0
    if len(parts) > 3 and parts[3].strip() != "":
        buffs = float(parts[3].strip())

    damage = base * mult * (1 + 0.15 * buffs)
    return name, tag, damage


def main(path: str) -> None:
    with open(path, encoding="utf-8") as log:
        for line in log:
            line = line.rstrip("\n")
            if line.strip() == "" or line.lstrip().startswith("#"):
                continue
            try:
                shot = parse_shot(line)
            except ValueError:
                continue
            if shot is None:
                continue
            name, tag, damage = shot
            print(f"Игрок {name} из гильдии {tag} нанес {damage:.2f} по воротам.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "siege_log.txt")
