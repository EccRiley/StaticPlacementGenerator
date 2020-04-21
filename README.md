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

### First Run

Some files will need to be created to use for all subsequent runs. These tasks will only need to be completed once per machine this program is used on.

Navigate to the `StaticPlacementGenerator` directory. Run the following command to set the `FIRST_RUN` environment variable to indicate this is the first time running this program on your machine:
```
export FIRST_RUN=true
```

Doing this will create the following for future use:
- All possible states exported to a file
- All possible removal situations for each engine type exported to a file

### Subsequent Runs

The `FIRST_RUN` environment variable can be set to FALSE for all future runs.
```
export FIRST_RUN=false
```

Prior to running this program, a few files may need to be updated.

#### Update Information to Reflect Current State/System

**`data_to_read/removal_info.csv`**

This file contains information on expected number of removals for each engine subtype. For each engine subtype, the following is specified:
- Expected maximum number of removals in a month for all airports
- Expected maximum number of removals in a month for each specific hub
- Expected maximum number of removals in a month for all airports excluding hubs
- Expected AOS cost
- Whether or not these files were updated from the previous run (if any of the data for a subtype has been updated, make sure to set the UPDATED column value for that row to be TRUE)

Our team based these values on past removal data for each type. We set the maximum number of removals that could happen based on data from 2015-2019 by taking the maximum that had ever occurred for each and adding 1 to it. For example, if no more than 3 removals ever occurred in ATL, we assumed the maximum number of removals that could ever happen at ATL would be 4.

*Limitations*:
- The maximum number of removals for all airports cannot be less than 1 or greater than 10
- The maximum number of removals for each specific hub cannot be greater than 10
- The maximum number of removals for all airports excluding hubs cannot be greater than 2

The purpose of this file is to minimize the iterations the program runs so that runtime is reduced and extremely unlikely situations are not considered.

**`data_to_read/engine_info.csv`**

This file contains information on total number of engines for each engine subtype. For each engine subtype, the following is specified:
- Total number of current spare engines 

*Limitations*:
- The total number of current spare engines cannot be less than 1 and cannot be greater than 5

### Run the Program

Navigate to the `StaticPlacementGenerator` directory if you aren't there already.

In your terminal, run the following command:
```
python3 app.py
```

The program may take several hours to run. 

## Files Provided

For each engine subtype (located in `StaticPlacementGenerator/data_to_read/engine_subtype/`):

| File 														| Description 												|
| ----------------------------------------------------------| --------------------------------------------------------- |
| `probabilities_of_num_removals_in_each_state_region`		| Probabilities of removals based on 2015-2019 data 		|
| `expected_transport_cost` 								| Expected transportation costs from hubs to state regions 	|
| `number_of_broken_engines_and_number_repaired` 			| Probabilities of engines repaired given on engines broken |

Turnover documents will be provided that will outline how to re-calculate probability values based on new past data.

**The format of these documents (the naming of the file, the header structure and naming, etc.) must remain the same in order for the program to work.**

## Authors

**Industrial and Systems Engineering, Georgia Institute of Technology**, Spring 2020

**Team 10**
- Samantha Davanzo
- Brian Davis
- Mary Elizabeth Davis
- Bella Jackson
- Meredith Murfin
- Miles Trumbauer