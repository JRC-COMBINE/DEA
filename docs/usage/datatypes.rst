Datatypes
=========

>> this should probably be moved somewhere else

The datastructure for csv files is as follows:

│      +-- Data
│      |   +-- Cohort A
│      |   |   +-- Encounter 1
│      |   |       +-- File dynamic.csv
│      |   |       +-- File preprocessed.csv
│      |   |       +-- File processed.csv
│      |   |       +-- File raw.csv
│      |   |       +-- File intermediate_results.csv
│      |   |       +-- File results.csv
│      |   |   +-- Encounter 2
│      |   |       +-- File dynamic.csv
│      |   |       +-- File preprocessed.csv
│      |   |  +-- static.csv
│      |   |  +-- comorbidities.csv
│      |   |  +-- analysis.csv
│      |   +-- Cohort B
│      |       +-- Encounter 1
│      |       |   +-- ...

Basically we group by Cohort/Encounter and have inidividual files for each. 
Rule of thumb: if the data is static, we handle it on a cohort level, if it is dynamic we handle it on an encounter level.

While it would be possible to have static data stored at an encounter level, and we do so in the in-memory data structure - we do not want to create too many individual files, so for now we will accept the small increase in complexity.