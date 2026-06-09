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
                    line_cleaned = line.strip()
                    movement_number = int(line_cleaned[:-1])
                    direction = line_cleaned[-1]
                    movements.append((movement_number,direction))
        return movements

    def getAct(self):
        acts_by_color = {}
        can_read=False
        with open(self.filepath, "r") as file:
            for line in file:
                if line.startswith("SEQ"):
                    continue
                if can_read == True:
                    acts_by_color[line.split()[0]] = line.split()[1:]
                elif line.startswith("ACT"):
                    can_read = True
        print(acts_by_color)
        return acts_by_color
                    

                    