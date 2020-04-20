# StaticPlacementGenerator

The StaticPlacementGenerator is a Python program used to generate the best default spare engine placement for a specific aircraft fleet, regardless of future flight data. 

## Background

Delta Air Lines is an industry-leading, globally operating United States airline servicing over 300 destinations with a fleet of approximately 900 aircraft. Delta’s Engine Demand Planning team (EDP), which falls under Delta TechOps, is responsible for planning engine removals, assigning spare engines to seven designated hubs, and setting up the logistics of the removals and repairs of these engines.

The objective of this project is to assist Delta’s EDP team with improving the allocation of spare engines across the contiguous United States. To assist Delta in decreasing both transportation and AOS costs incurred throughout the year, the solution determines the optimal configuration of all spare engines on a monthly basis through a Markov Decision Process. The solution outputs a configuration recommendation for the upcoming month associated with the minimal cost of all possible options. Delta’s EDP team can use the model to make data-informed, cost-driven decisions with the added benefit of reducing required labor hours.

This program currently generates optimal default spare placement for the following engine types:
- BR700-715C1-30
- CF6-80C2B6
- CF6-80C2B6F
- CF6-80C2B8F
- CF6-80E1A4
- CFM56-5A
- CFM56-5B3-3
- CFM56-7B26
- CFM56-7B27E-B1F
- JT8D-219
- PW2000-2037
- PW2000-2040
- PW4000-4060
- PW4000-4168
- TRENT8-892-17
- V2500-D5

Spare engine placement for additional engine types can be determined only if the necessary information is provided. 

## Installations and Setup

Instructions to install the required installations are outlined below with provided terminal commands. These instructions assume basic understanding of using Terminal on Mac. If your machine is not a Mac, these instructions may need to be altered slightly. 

### Before Cloning this Repository

Install `python3`. Check that your version matches the one below or is more recent.
```
python3 --version
Python 3.7.6
```

### Clone this Repository

To clone this repository, navigate to the folder in your terminal that you would like it to be in. Then run the following command:
```
git clone https://github.com/meredithmurfin/StaticPlacementGenerator.git
```

You should then be able to use this command to be in the local `StaticPlacementGenerator` directory on your machine:
```
cd StaticPlacementGenerator
```

## Usage

### Run the Program

Navigate to the `StaticPlacementGenerator` directory if you aren't there already.

In your terminal, run the following command:
```
python3 app.py
```

The program may take several hours to run. 

## Files Provided

## Authors

**Industrial and Systems Engineering, Georgia Institute of Technology**, Spring 2020

**Team 10**
- Samantha Davanzo
- Brian Davis
- Mary Elizabeth Davis
- Bella Jackson
- Meredith Murfin
- Miles Trumbauer