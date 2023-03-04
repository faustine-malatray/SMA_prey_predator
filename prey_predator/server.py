from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
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

    elif type(agent) is GrassPatch:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        if agent.grown:
            portrayal["Color"] = "darkseagreen"
        else:
            portrayal["Color"] = "honeydew"

    return portrayal


## CanvasGrid(portrayal, grid_width, grid_height, canvas_width, canvas_height)
canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#000000"},
     {"Label": "Sheep", "Color": "#c7c5c5"}]
)

model_params = {"height": 20,
                "width": 20,
                "initial_sheep": UserSettableParameter("number", "Initial Number of Sheeps", value=10),
                "initial_wolves": UserSettableParameter("number", "Initial Number of Wolves", value=3),
                "sheep_reproduce": UserSettableParameter("slider", "Sheep Reproducing Probability", value=0.5, min_value=0, max_value=1, step=0.01),
                "wolf_reproduce": UserSettableParameter("slider", "Wolves Reproducing Probability", value=0.1, min_value=0, max_value=1, step=0.01),
                "wolf_gain_from_food": UserSettableParameter("number", "Wolves Energy points with Food", value=5),
                "grass": UserSettableParameter("checkbox", "Are Sheeps eating Grass", value=True),
                "grass_regrowth_time": UserSettableParameter("number", "Grass Regrowth Time", value=5),
                "sheep_gain_from_food": UserSettableParameter("number", "Sheep Energy points with Food", value=3)}

server = ModularServer(WolfSheep,
                       [canvas_element,
                        chart_element],
                       "Prey Predator Model",
                       model_params)
server.port = 8521
