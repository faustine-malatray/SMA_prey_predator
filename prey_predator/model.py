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

    sheep_energy = 10
    wolf_energy = 10

    initial_sheep = 150
    initial_wolves = 100

    sheep_reproduce = 0.15
    wolf_reproduce = 0.11

    sheep_gain_from_food = 5
    wolf_gain_from_food = 20

    sheep_move_energy = 1
    wolf_move_energy = 1

    sheep_reproduction_energy = 2
    wolf_reproduction_energy = 3

    sheep_min_digestion = 3
    wolf_min_digestion = 10

    grass = True
    grass_regrowth_time = 20

    sheep_life_expectancy = 45
    wolf_life_expectancy = 100

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height,
        width,
        sheep_energy,
        wolf_energy,
        initial_sheep,
        initial_wolves,
        sheep_reproduce,
        wolf_reproduce,
        sheep_gain_from_food,
        wolf_gain_from_food,
        sheep_move_energy,
        wolf_move_energy,
        sheep_reproduction_energy,
        wolf_reproduction_energy,
        sheep_min_digestion,
        wolf_min_digestion,
        grass,
        grass_regrowth_time,
        sheep_life_expectancy,
        wolf_life_expectancy
    ):
        """
        Create a new Wolf-Sheep model with the given self-explanatory parameters.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width

        self.sheep_energy = sheep_energy
        self.wolf_energy = wolf_energy

        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves

        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce

        self.sheep_gain_from_food = sheep_gain_from_food
        self.wolf_gain_from_food = wolf_gain_from_food

        self.sheep_move_energy = sheep_move_energy
        self.wolf_move_energy = wolf_move_energy

        self.sheep_reproduction_energy = sheep_reproduction_energy
        self.wolf_reproduction_energy = wolf_reproduction_energy

        self.sheep_min_digestion = sheep_min_digestion
        self.wolf_min_digestion = wolf_min_digestion

        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time

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

        # Create sheep :
        # We choose to put initial sheep in random positions within the grid.
        # They are initialized with sheep_energy energy.
        for i in range(initial_sheep):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            sheep = Sheep(
                self.next_id(),
                pos=(x, y),
                model=self,
                moore=True,
                energy=self.sheep_energy,
            )
            self.schedule.add(sheep)
            self.grid.place_agent(sheep, (x, y))

        # Create wolves :
        # We choose to put initial wolves in random positions within the grid.
        # They are initialized with wolf_energy energy.
        for i in range(initial_wolves):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            wolf = Wolf(
                self.next_id(),
                pos=(x, y),
                model=self,
                moore=True,
                energy=self.wolf_energy,
            )
            self.schedule.add(wolf)
            self.grid.place_agent(wolf, (x, y))

        # Create grass patches :
        # Grass patches are created with a probability of 0.5 in each grid cell.
        # They all are created with the same grass_regrowth_time.
        if self.grass:
            for i in range(self.width):
                for j in range(self.height):
                    if self.random.random() < 0.5:
                        grass = GrassPatch(
                            self.next_id(),
                            pos=(i, j),
                            model=self,
                            fully_grown=True,
                            countdown=self.grass_regrowth_time,
                        )
                        self.schedule.add(grass)
                        self.grid.place_agent(grass, (i, j))

    def step(self):
        self.schedule.step()
        # Collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=10):
        for i in range(step_count):
            self.step()
