from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


# def agent_portrayal(agent):
#     portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

#     if agent.wealth > 0:
#         portrayal["Color"] = "red"
#         portrayal["Layer"] = 0
#     else:
#         portrayal["Color"] = "grey"
#         portrayal["Layer"] = 1
#         portrayal["r"] = 0.2
#     return portrayal


def wolf_sheep_portrayal(agent):
    if agent is None:
        pass

    portrayal = {"Shape": "circle", "Filled": "true", "Layer": 0}

    if type(agent) is Sheep:
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2

    elif type(agent) is Wolf:
        portrayal["Color"] = "black"
        portrayal["r"] = 0.5

    elif type(agent) is GrassPatch:
        portrayal["Color"] = "green"
        portrayal["r"] = 1

    return portrayal


## CanvasGrid(portrayal, grid_width, grid_height, canvas_width, canvas_height)
canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#000000"}, {
        "Label": "Sheep", "Color": "#c7c5c5"}]
)

model_params = {"initial_sheep": 10, "initial_wolves": 10}  # à modifier

server = ModularServer(
    WolfSheep, [canvas_element,
                chart_element], "Prey Predator Model", model_params
)
server.port = 8521
