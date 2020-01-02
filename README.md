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

## `company-dataset`

Builds base company dataset with game/release/production role information

## `wikidata-mapping`

Fetches current wikidata mapping (Q-Number <-> Mobygames slug) and country information

## `company-network`

Builds a network of companies based on their common work on games

| Option | Description | Multiple | Default value | 
| -- | -- | -- | -- |
| --country/-c | Release country | X | -- |
| --platform/-p | Release platform | X | -- |
| --roles/--no-roles | Differentiate companies by their production roles | -- | --no-roles |
| --publisher/--no-publisher | Include/exclude publisher roles; only needed when --roles option is set | -- | --no-publisher |

## `browser`

Opens the lemongrab browser frontend for data exploration


# Datasets

## Company dataset

`datasets/mobygames_companies.json`

This dataset contains all companies and the games they were working on.

### Structure:

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

## Wikidata mapping and country information

`datasets/wikidata_mapping.json`

Contains a mapping of Mobygames company slugs to wikidata items as well as country information from 
wikidata (if available) 

### Structure:

```json
[
    {
        "mobygames_slug": "company-slug",
        "country": "Japan",
        "wkp": "Q111111"
    },
]
```

## Mobygames company id to slug mapping

`datasets/mobygames_companies_id_to_slug.json`

Mapping of the internal Mobygames company ids to their slug

### Structure:

```json
[
    {
        "company_id": "<company id>",
        "slug": "company slug"
    },
]
```


# License

GPLv3s

# Copyright

2019 Universitätsbibliothek Leipzig