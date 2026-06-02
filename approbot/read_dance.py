class ReadDance:
    def __init__(self, filepath):
        self.filepath=filepath

    def getMovement(self):
        movements = []
        with open(self.filepath, "r") as file:
            for line in file:
                if line.startswith("SEQ"):
                    continue
                elif line.startswith("ACT"):
                    break
                else:
                    direction = int(line.split()[0][0])
                    movement = line.split()[0][1]
                    movements.append((direction,movement))
        print(movements)





