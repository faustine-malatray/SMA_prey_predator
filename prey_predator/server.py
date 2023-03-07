from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        pass

    portrayal = {"Filled": "true", "Layer": 0}

    if type(agent) is Sheep:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2

    elif type(agent) is Wolf:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "black"
        portrayal["r"] = 0.5

    return portrayal


## CanvasGrid(portrayal, grid_width, grid_height, canvas_width, canvas_height)
canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#000000"}, {
        "Label": "Sheep", "Color": "#c7c5c5"}]
)

model_params = {
    "height": 20,
    "width": 20,
    "sheep_energy": UserSettableParameter("number", "Energy of a Sheep", value=10),
    "wolf_energy": UserSettableParameter("number", "Energy of a Wolf", value=10),
    "initial_sheep": UserSettableParameter(
        "number", "Initial Number of Sheeps", value=10
    ),
    "initial_wolves": UserSettableParameter(
        "number", "Initial Number of Wolves", value=10
    ),
    "sheep_reproduce": UserSettableParameter(
        "slider",
        "Sheep Reproducing Probability",
        value=0.2,
        min_value=0,
        max_value=1,
        step=0.01,
    ),
    "wolf_reproduce": UserSettableParameter(
        "slider",
        "Wolves Reproducing Probability",
        value=0.05,
        min_value=0,
        max_value=1,
        step=0.01,
    ),
    "wolf_gain_from_food": UserSettableParameter(
        "number", "Wolves Energy points with Food", value=5
    ),
    "sheep_move_energy": UserSettableParameter(
        "number", "Sheep energy loss with movement", value=1
    ),
    "wolf_move_energy": UserSettableParameter(
        "number", "Wolves energy loss with movement", value=1
    ),
    "sheep_reproduction_energy": UserSettableParameter(
        "number", "Sheep energy loss with reproduction", value=2
    ),
    "wolf_reproduction_energy": UserSettableParameter(
        "number", "Wolves energy loss with reproduction", value=3
    ),
    "sheep_life_expectancy": UserSettableParameter(
        "number", "Sheep life expectancy", value=20
    ),
    "wolf_life_expectancy": UserSettableParameter(
        "number", "Wolf life expectancy", value=30
    ),
    "wolf_min_digestion": UserSettableParameter(
        "number", "Wolf digestion time", value=5
    ),
}


server = ModularServer(
    WolfSheep, [canvas_element,
                chart_element], "Prey Predator Model", model_params
)
server.port = 8521
