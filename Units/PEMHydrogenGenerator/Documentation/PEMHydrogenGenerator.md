# PEM Hydrogen Generator - Unit Operations Data

## Introduction

The PEM Hydrogen Generator utilizes proton exchange membrane (PEM) technology to facilitate the electrolysis of water, producing hydrogen and oxygen gases. This document provides a concise overview of the unit operations data for the system.

## Water Feed

- **State**: Liquid
- **Temperature**: 298.15 K (Reference environment temperature)
- **Pressure**: 1 atm (Reference environment pressure)

## PEM Electrolyzer

- **Water Heating**: Before entering the PEM electrolyzer, water is heated using a counter-flow heat exchanger to reach the operating temperature of the electrolyzer.
- **Surface Area**: The electrolyzer surface area is assumed to be 1 m^2.

## Gas Outputs

### Hydrogen (H₂)

- **Heat Dissipation**: Exiting from the cathode, the produced hydrogen dissipates heat to the environment.
- **Cooling**: The hydrogen cools down to the reference environment temperature (298.15 K).

### Oxygen (O₂)

- **Separation**: Oxygen gas produced at the anode is separated from the water/oxygen mixture.
- **Cooling**: The oxygen cools down to the reference environment temperature (298.15 K).

## Water Recirculation

- The remaining hot water, post-electrolysis, is circulated back to the water supply stream for the next hydrogen production cycle.

## Electrolysis Reaction

The overall PEM electrolysis reaction can be described as:

H<sub>2</sub>O + Electricity + Heat → H<sub>2</sub> + O<sub>2</sub>



