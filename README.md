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

# company-dataset

Builds base company dataset with game/release/production role information

# wikidata-mapping 

Fetches current wikidata mapping (Q-Number <-> Mobygames slug) and country information

# company-network 

Builds a network of companies based on their common work on games

| Option | Description | Multiple | Default value | 
| -- | -- | -- | -- |
| --country/-c | Release country | X | -- |
| --platform/-p | Release platform | X | -- |
| --roles/--no-roles | Differentiate companies by their production roles | -- | --no-roles |
| --publisher/--no-publisher | Include/exclude publisher roles; only needed when --roles option is set | -- | --no-publisher |

# browser 

Opens the lemongrab browser frontend for data exploration