# Global Terrorism Dashboard

This project is an interactive dashboard built with Dash to help a fictitious security firm determine where to send its employees.

## Requirements
- Python 3.11.11
- pip (Python package manager)
- Git

## Features

- World map with color coding by number of attacks
- Clickable countries with:
  - Donut chart: Types of attacks
  - Bar chart: Attacks per year

## Setup & Installation
1. Clone repository
```bash
git clone https://github.com/iaryser/final_dviz_project.git
cd final_dviz_project
```

2. Create a virual environment (we recomment python 3.11.11)
```bash
python3.11 -m venv venv

# Activate the environment (macOS/Linux)
source venv/bin/activate

# OR on Windows (CMD)
venv\Scripts\activate
```

### If you **don't** have "Make installed
1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Run the application
```bash
python app.py
```

### If you have "Make" installed
1. Install the requirements:
```bash
make install
```

2. Run the application:
```bash
make run
```

### Open the dashboard
Open you favorite browser and navigate to `http://127.0.0.1:8050/`

## Attributions

We used the following datasets in this project:

### Global Terrorism Database (GTD)
We obtained the terrorism data from Kaggle:
[https://www.kaggle.com/datasets/START-UMD/gtd](https://www.kaggle.com/datasets/START-UMD/gtd)

> The Global Terrorism Database (GTD) is an open-source database that provides detailed information on terrorist attacks worldwide from 1970 through 2017. It includes over 180,000 domestic and international incidents. The GTD is maintained by the National Consortium for the Study of Terrorism and Responses to Terrorism (START) at the University of Maryland.

### Country Population Data
To normalize the number of attacks per country, we created a custom population dataset derived from World Bank data:
[https://data.worldbank.org/indicator/SP.POP.TOTL](https://data.worldbank.org/indicator/SP.POP.TOTL)

> Please note: our population dataset is static and intended only for this project. It will not be updated or maintained.

## Contact

If you have any questions, please contact us here:
- Timo Ryser: timo.ryser@stud.hslu.ch
- Laurin Lötscher: laurin.loetscher@stud.hslu.ch
