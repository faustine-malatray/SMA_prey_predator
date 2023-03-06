"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height,
        width,
        initial_sheep,
        initial_wolves,
        sheep_reproduce,
        wolf_reproduce,
        wolf_gain_from_food,
        grass,
        grass_regrowth_time,
        sheep_gain_from_food,
        sheep_reproduction_energy,
        wolf_reproduction_energy,
        sheep_move_energy,
        wolf_move_energy,
        sheep_energy,
        wolf_energy,
        sheep_life_expectancy,
        wolf_life_expectancy
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.sheep_reproduction_energy = sheep_reproduction_energy
        self.wolf_reproduction_energy = wolf_reproduction_energy
        self.sheep_move_energy = sheep_move_energy
        self.wolf_move_energy = wolf_move_energy
        self.sheep_energy = sheep_energy
        self.wolf_energy = wolf_energy

        self.sheep_life_expectancy = sheep_life_expectancy
        self.wolf_life_expectancy = wolf_life_expectancy

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        # Create sheeps:
        for i in range(initial_sheep):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            sheep = Sheep(self.next_id(), pos=(x, y),
                          model=self, moore=True, energy=self.sheep_energy)
            self.schedule.add(sheep)
            self.grid.place_agent(sheep, (x, y))

        # Create wolves:
        for i in range(initial_wolves):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            wolf = Wolf(self.next_id(), pos=(x, y),
                        model=self, moore=True, energy=self.wolf_energy)
            self.schedule.add(wolf)
            self.grid.place_agent(wolf, (x, y))

        # Create grass patches
        for i in range(self.width):
            for j in range(self.height):
                if self.random.random() < 0.5:
                    grass = GrassPatch(self.next_id(), pos=(
                        i, j), model=self, fully_grown=True, countdown=self.grass_regrowth_time)
                    self.schedule.add(grass)
                    self.grid.place_agent(grass, (i, j))

    def step(self):
        self.schedule.step()
        # Collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=10):
        for i in range(step_count):
            self.step()
