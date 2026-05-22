class Battle:

    def __init__(self):
        self.max_moves = 10
        self.rules = {}

    def load_file(self, filepath):
        current_color = None
        with open(filepath, "r") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue

                if line.startswith("MVS"):
                    parts = line.split()
                    self.max_moves = int(parts[1])

                elif line.startswith("["):
                    current_color = line[1]
                    self.rules[current_color] = []

                else:
                    left, right = line.split("=")
                    combo = left.strip()
                    points = int(right.strip())
                    self.rules[current_color].append((combo, points))

    def compute_points(self, col, arm, exp):
        total = 0
        rules = self.rules.get(col, [])
        for combo, points in rules:
            if "+" in combo:
                parts = combo.split("+")
                valid = True
                for part in parts:
                    if (part not in arm and part != exp):
                        valid = False

                if valid:
                    total += points

            elif "," in combo:
                parts = combo.split(",")
                valid = False
                for part in parts:
                    if (part in arm or part == exp):
                        valid = True

                if valid:
                    total += points
            else:
                if (combo in arm or combo == exp):
                    total += points

        return total

    def print_rules(self):
        print("=== RULES ===")
        print(f"MVS = {self.max_moves}")
        for color, rules in self.rules.items():
            print(f"\n[{color}]")
            for combo, points in rules:
                print(f"{combo} => {points}")