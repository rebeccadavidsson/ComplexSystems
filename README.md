# ANT COLONY OPTIMIZATION

![](gif.gif)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. This project was written in Python3.


### Installing

Some requirements have to be installed in order to run the program. Install the requirements with the following command.

```
pip3 install -r requirements.txt
```

This will install the packages scipy, matplotlib, Mesa, tqdm, pandas, seaborn and numpy.

## Running the simulation

A full simulation is run by the command:

```
python3 run.py
```

This will automatically open up a new window where the simulation is run. Parameters are set in the file run.py. Parameters that can be easily changed are:
* Pheremone strength
* Decay (duration of pheromones)
* Sigma (spread/evaporation)
* Grid size (width and height)
* Number of ants


An environment is made that includes these variables with the following line of code:
```
env = Environment(width, height, n_colonies, n_ants, n_obstacles, decay, sigma,
                    moore=False, pheromone_strength)
```

### Tests and plotting

The model was run several times with varying parameters. For these tests, the file averageruns.py was used. This file can be run with the following command:

```
python3 averageruns.py
```

An example of how the plots were made is given in ```heatmap.ipynb```.

## Source

https://github.com/WouterVrielink/MC-ACO
