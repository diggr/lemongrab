# LEMONGRAB

Gather company data from mobygames and wikidata and build cool (?) research datasets and visualizations.


## Requirements

* Python 3.7
* unified api
* diggrtoolbox

## Installation

* Download repo
* Install requirements

## Usage

Commands:

```zsh
$ python lemongrab.py <COMMAND>
```

| command | description |
| -- | -- |
| company-dataset | Builds base company dataset with game/release/production role information |
| wikidata-mapping | Fetches current wikidata mapping (Q-Number <-> Mobygames slug) and country information |
| company-network | Builds a network of companies based on their common work on games |
| browser | Opens the lemongrab browser frontend for data exploration |