# LEMONGRAB

Gather company data from mobygames and wikidata and build awesome research 
datasets and visualizations.This tool provides various commands to fetch data 
(via cli) and visualize it (via browser).

## Requirements

* Python 3.7
* [unified api](https://git.sc.uni-leipzig.de/ubl/diggr/infrastructure/unifiedapi)
* [diggrtoolbox](https://github.com/diggr/diggrtoolbox)

## Installation

Clone this repository and install the requirements

```zsh
$ git clone https://git.sc.uni-leipzig.de/ubl/diggr/general/lemonggrab
$ cd lemongrab && pip install -r requirements.txt
```

## Features

The tool provides the following commands, which are intended to be used in the 
following order. The first two commands (*company-dataset* and *wikidata-mapping*)
generate/fetch the dataset and the mapping. The third command (*company-network*)
builds a *GraphML* file to be inspected (e.g. with *Gephi*). The fourth command
(*browser*) starts a web application which can be used to inspect the companies 
fetched earlier.

## Usage

Commands:

```zsh
$ python lemongrab.py <COMMAND>
```

### `company-dataset`

Builds base company dataset with game/release/production role information

### `wikidata-mapping`

Fetches current wikidata mapping (Q-Number <-> Mobygames slug) and country information

### `company-network`

Builds a network of companies based on their common work on games

| Option | Description | Multiple | Default value | 
| -- | -- | -- | -- |
| --country/-c | Release country | X | -- |
| --platform/-p | Release platform | X | -- |
| --gamelist/-g | Use tulpa gamelist as filter | -- | -- |
| --roles/--no-roles | Differentiate companies by their production roles | -- | --no-roles |
| --publisher/--no-publisher | Include/exclude publisher roles; only needed when --roles option is set | -- | --no-publisher |

You can either filter by Country/Platform OR tulpa gamelist.

Options which allow multiple invokation (currently country and platform) can be used multiple times in the same call, e.g.:

```zsh
$ python lemongrab.py company-network -c Japan -c Worldwide
```

### `browser`

Opens the lemongrab browser frontend for data exploration

## Datasets

### Company dataset

`datasets/mobygames_companies.json`

This dataset contains all companies and the games they were working on.

#### Structure:

```json

{
    "<comapny_id>": [
        {
            "company_name": "Fox Interactive, Inc.",
            "game_id": "672",
            "game_slug": "die-hard-trilogy",
            "game_title": "Die Hard Trilogy",
            "game_years": [
                1996,
                1997,
                1998
            ],
            "production_role": "Published by",
            "release_countries": [
                "Sweden",
                "United Kingdom",
                "Italy"
            ],
            "platform": "Sony PlayStation"            
        },
    ]
}

```

### Wikidata mapping and country information

`datasets/wikidata_mapping.json`

Contains a mapping of Mobygames company slugs to wikidata items as well as country information from 
wikidata (if available) 

#### Structure:

```json
[
    {
        "mobygames_slug": "company-slug",
        "country": "Japan",
        "wkp": "Q111111"
    },
]
```

### Mobygames company id to slug mapping

`datasets/mobygames_companies_id_to_slug.json`

Mapping of the internal Mobygames company ids to their slug

#### Structure:

```json
[
    {
        "company_id": "<company id>",
        "slug": "company slug"
    },
]
```


## License

GPLv3

## Copyright

2019 Universitätsbibliothek Leipzig