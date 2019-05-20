# mv-model

This repository contains modeling work done by Eric, Rishi, and Eli for Dr. Eng's multivariable calculus final project.

## Dependencies

* Python 3

## Project Structure

The overall model is represented by a directed acyclic graph, which is an instance of `network.Graph`. All of the relevant graph classes are in `network.py`.

In order to account for different crops grown in different seasons, `crops.py` contains two objects, `KharifCrops` and `RabiCrops`, which describe the irrigation districts under their respective seasons. This makes it possible for the model construction procedure in `model.py` to be season-agnostic.

