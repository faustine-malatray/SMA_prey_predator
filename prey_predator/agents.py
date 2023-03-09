from mesa import Agent
from prey_predator.random_walk import RandomWalker

###############################
#### SHEEP CLASS ##############
###############################


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.
    The init is the same as the RandomWalker, with some additionnal attributes : the energy, the age, and the last_ate indicator.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0
        self.last_ate = 0

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        Each step, the sheep also ages, and we check for potential exhaustion death.
        We consider that if the sheep moved and is out of energy, but eats immediately after, it can stay alive.
        This explains the order the methods are called in.
        """

        self.random_move()
        self.eat_grass()
        self.reproduce()
        self.aging()
        self.exhaustion_death()

    def random_move(self):
        """
        This randomly moves the sheep agent in the grid using the RandomWalker random_move method.
        Additionally, the sheep loses sheep_move_energy."""
        super().random_move()
        self.energy -= self.model.sheep_move_energy

    def eat_grass(self):
        """
        This function checks for grass in the sheep's current cell.
        If the sheep hasn't eaten this step, and hasn't eaten too recently (we require for the sheep to wait
        sheep_min_digestion long before eating again), and if there's a fully grown grass patch in the cell,
        the sheep eats, gains new energy, and the grasspatch's gets_eaten method is called.
        Otherwise, the last_ate attribute is incremented."""
        cell = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=0, include_center=True
        )
        ate = False
        if cell and (self.last_ate >= self.model.sheep_min_digestion):
            for thing in cell:
                if (type(thing) == GrassPatch) and (thing.grown):
                    self.energy += self.model.sheep_gain_from_food
                    self.last_ate = 0
                    thing.gets_eaten()
                    ate = True
                    break
        if not ate:
            self.last_ate += 1

    def reproduce(self):
        """
        If the sheep has more energy than the sheep_reproduction_energy value, and using a probability based
        on the sheep_reproduce value, the sheep can reproduce on its own. If it does, a new sheep agent is
        initialized in the parent's cell, and is added to the scheduler and the grid. The parent also loses
        reproduction energy."""
        if (self.energy > self.model.sheep_reproduction_energy) and (
            self.model.random.random() <= self.model.sheep_reproduce
        ):
            kid = Sheep(
                self.model.next_id(),
                self.pos,
                self.model,
                self.moore,
                energy=self.model.sheep_energy,
            )
            self.model.schedule.add(kid)
            self.model.grid.place_agent(kid, self.pos)

            self.energy -= self.model.sheep_reproduction_energy

    def exhaustion_death(self):
        """
        At each iteration, if the sheep has negative energy or if the sheep is older than
        its species' life expectancy, it dies using the RandomWalker dies method."""
        if self.energy and (self.energy <= 0):
            self.dies()
        elif self.age >= self.model.sheep_life_expectancy:
            self.dies()

    def aging(self):
        """
        At each step, the sheep's age is incremented by one."""
        self.age += 1


###############################
#### WOLF CLASS ###############
###############################


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    The init is the same as the RandomWalker, with some additionnal attributes : the energy, the age, and the last_ate indicator.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.age = 0
        self.last_ate = 0

    def step(self):
        """
        A model step. Move, then potentially eat sheep and reproduce.
        Each step, the wold also ages, and we check for potential exhaustion death.
        This explains the order the methods are called in.
        We consider that if the wolf moved and is out of energy, but eats immediately after, it can stay alive.
        This explains the order the methods are called in."""
        self.random_move()
        self.eat_sheep()
        self.reproduce()
        self.aging()
        self.exhaustion_death()

    def random_move(self):
        """
        This randomly moves the wolf agent in the grid using the RandomWalker random_move method.
        Additionally, the wolf loses wolf_move_energy."""
        super().random_move()
        self.energy -= self.model.wolf_move_energy

    def eat_sheep(self):
        """
        This function checks for sheep in the wolf's current cell.
        If the wold hasn't eaten this step, and hasn't eaten too recently (we require for the wolf to wait
        wolf_min_digestion long before eating again), and if there's a sheep in the cell,
        the wolf eats, gains new energy, and the sheep's dies method is called.
        Otherwise, the last_ate attribute is incremented."""
        cell = self.model.grid.get_neighbors(
            self.pos, moore=True, radius=0, include_center=True
        )
        ate = False
        if cell and (self.last_ate >= self.model.wolf_min_digestion):
            for thing in cell:
                if type(thing) == Sheep:
                    self.energy += self.model.wolf_gain_from_food
                    self.last_ate = 0
                    ate = True
                    thing.dies()
                    break
        if not ate:
            self.last_ate += 1

    def reproduce(self):
        """
        If the wolf has more energy than the wolf_reproduction_energy value, and using a probability based
        on the wolf_reproduce value, the wolf can reproduce on its own. If it does, a new wolf agent is
        initialized in the parent's cell, and is added to the scheduler and the grid. The parent also loses
        reproduction energy."""
        if (self.energy > self.model.wolf_reproduction_energy) and (
            self.model.random.random() <= self.model.wolf_reproduce
        ):
            # Si le loup a assez d'énergie, on crée un agent enfant, qu'on ajoute à la grille et au schedule.
            kid = Wolf(
                self.model.next_id(),
                self.pos,
                self.model,
                self.moore,
                energy=self.model.wolf_energy,
            )
            self.model.schedule.add(kid)
            self.model.grid.place_agent(kid, self.pos)

            self.energy -= self.model.wolf_reproduction_energy

    def exhaustion_death(self):
        """
        At each iteration, if the wolf has negative energy or if the wolf is older than
        its species' life expectancy, it dies using the RandomWalker dies method."""
        if self.energy and (self.energy <= 0):
            self.dies()
        elif self.age >= self.model.wolf_life_expectancy:
            self.dies()

    def aging(self):
        """
        At each step, the wolf's age is incremented by one."""
        self.age += 1


###############################
#### GRASSPATCH CLASS #########
###############################


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep.
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass
        Args:
            pos: a position in the grid,
            model: the according model it belongs to,
            grown: (boolean) Whether the patch of grass is fully grown or not,
            countdown: Time for the patch of grass to be fully grown again.
            The countdown value should be initialized with a model variable.
        """
        super().__init__(unique_id, model)
        self.grown = fully_grown
        self.countdown = countdown

    def step(self):
        """
        Each step, the countdown to full growth is decreased by 1.
        We then apply the update_growth method."""
        self.countdown -= 1
        self.update_growth()

    def update_growth(self):
        """
        This method updates the grown attribute. If the grass isn't already grown and if the countdown
        has reached 0, then the boolean grown becomes True."""
        if (not self.grown) and (self.countdown <= 0):
            self.grown = True

    def gets_eaten(self):
        """
        This method will be used when a sheep eats the grass patch.
        The countdown turns back to its maximum value, and the grown boolean becomes False."""
        self.countdown = self.model.grass_regrowth_time
        self.grown = False
