# LEMONGRAB

Gather company data from mobygames and wikidata and build awesome research 
datasets and visualizations.This tool provides various commands to fetch data 
(via cli) and visualize it (via browser).

![lemongrab logo](assets/lemongrab_header.png?raw=true "lemongrab")

## Requirements

* Python 3.7
* [unified api](https://git.sc.uni-leipzig.de/ubl/diggr/infrastructure/unifiedapi)
* [diggrtoolbox](https://github.com/diggr/diggrtoolbox)

## Prerequisites

It is recommended to install *lemongrab* in a virtual Python environment such as
Pipenv, virtualenv, or venv.

## Installation

Clone this repository and install the package.

```zsh
$ git clone https://git.sc.uni-leipzig.de/ubl/diggr/general/lemongrab
$ cd lemongrab
```

Open *lemongrab/settings.py* with an editor of your choice and edit the value
of *DIGGR_API* to the address of your instance of the *UnifiedAPI*. Save the file
and install lemongrab.

```
$ pip install .
```

## Initial setup / Create a project

Create a folder and initialize lemongrab.

```zsh
$ mkdir testproject && cd testproject
$ lemongrab init
```

This will create two directories, one for the company\_networks and on one for the
required datasets. Next: Create both the wikidata mapping and the mobygames companies
dataset by running:

```zsh
$ lemongrab build all
```

Note: If you already build the datasets somewhere else, you can copy those files into 
the *lemongrab_datasets* directory and save yourself some time.

## Features

The tool provides two main commands *company-network* and *browser*. The first
command builds a *GraphML* file to be inspected (e.g. with *Gephi*). The second 
command starts a web application which can be used to inspect the companies 
fetched earlier.

```zsh
$ lemongrab company-network -c "Japan" -p "Sony PlayStation" --roles
$ lemongrab browser
```

Every company network is supplied with a log file. To aggreate all logs of your project
simply invoke the *aggregate-logs* command.

```zsh
$ lemongrab aggregate-logs
```

This will build a CSV file in your project directory with the contents of all log files
in your current project.

## Usage

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
$ lemongrab company-network -c Japan -c Worldwide
```

### `game-company-sample-network`

Builds a network of companies based on a tulpa generated company sample.

```zsh
$ lemongrab game-company-sample-network ../tulpaproject/datasets/tulpa-companies.json
```

### `browser`

Opens the lemongrab browser frontend for data exploration

## Datasets

### Mobygames companies dataset

`lemongrab_datasets/mobygames_companies.json`

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

`lemongrab_datasets/wikidata_mapping.json`

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

## Authors

* Peter Mühleder <muehleder@saw-leipzig.de>
* Florian Rämisch <raemisch@ub.uni-leipzig.de>

## Copyright

2019-2020, Universitätsbibliothek Leipzig, <info@ub.uni-leipzig.de>
