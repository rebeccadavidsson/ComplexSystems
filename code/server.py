from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Environment
from ant import Ant
from colony import Colony

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true"}
    if isinstance(agent, Colony):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.6
    elif isinstance(agent, Ant):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3

    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)


server = ModularServer(Environment,
                       [grid],
                       "crazy ants",
                       {"n_colonies": 1, "n_ants": 3, "width": 10, "height": 10, "n_obstacles" :50})

# Their server
server.port = 8521 # The default
server.launch()
