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
                    

                    