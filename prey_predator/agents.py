from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        We consider that if the sheep moved and is out of energy, but eats immediately after, it can stay alive.
        Moving reduces the sheep's energy by 1.
        """

        self.random_move()
        # self.eat_grass()
        self.reproduce()
        self.exhaustion_death()

    def random_move(self):
        super().random_move()
        self.energy -= 1

    def eat_grass(self):
        cell = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=0, include_center=True
        )
        if cell:
            for thing in cell:
                if type(thing) == GrassPatch:
                    self.energy += self.model.wolf_gain_from_food
                    thing.gets_eaten()
                    break

    def reproduce(self):
        # le 2 est arbitraire, on pourrait le mettre en paramètre
        if (self.energy > 2) and (self.model.random.random() <= self.model.sheep_reproduce):
            # Si le mouton a assez d'énergie, on crée un agent enfant, qu'on ajoute à la grille et au schedule.
            kid = Sheep(self.model.next_id(), self.pos,
                        self.model, self.moore, energy=10)
            self.model.schedule.add(kid)
            self.model.grid.place_agent(kid, self.pos)

            self.energy -= 2

    def exhaustion_death(self):
        if self.energy and (self.energy <= 0):
            self.dies()


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    We consider that if the wolf moved and is out of energy, but eats immediately after, it can stay alive.
    Moving reduces the wolf's energy by 1.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        # self.eat_sheep()
        self.reproduce()
        self.exhaustion_death()

    def random_move(self):
        super().random_move()
        self.energy -= 1

    def eat_sheep(self):
        cell = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=0, include_center=True
        )
        if cell:
            for thing in cell:
                if type(thing) == Sheep:
                    self.energy += self.model.wolf_gain_from_food
                    thing.dies()
                    break

    def reproduce(self):
        # le 2 est arbitraire, on pourrait le mettre en paramètre
        if (self.energy > self.model.wolf_reproduce) and (self.model.random.random() <= self.model.wolf_reproduce):
            # Si le loup a assez d'énergie, on crée un agent enfant, qu'on ajoute à la grille et au schedule.
            kid = Wolf(self.model.next_id(), self.pos,
                       self.model, self.moore, energy=10)
            self.model.schedule.add(kid)
            self.model.grid.place_agent(kid, self.pos)

    def exhaustion_death(self):
        if self.energy and (self.energy <= 0):
            self.dies()


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.grown = fully_grown
        # on initialisera avec la valeur self.model.grass_regrowth_time
        self.countdown = countdown

    def step(self):
        self.countdown -= 1
        self.update_growth()

    def update_growth(self):
        if (not self.grown) and (self.countdown <= 0):
            self.grown = True

    def gets_eaten(self):
        self.countdown = self.model.grass_regrowth_time
        self.grown = False
