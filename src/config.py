from typing import Final

FOLDER_PATH: Final = "data"
TERRORISM_FILE: Final = "globalterrorismdb_0718dist.csv"
POPULATION_FILE: Final = "countries_with_population.csv"
TERRORISM_FILE_PATH: Final = f"{FOLDER_PATH}/{TERRORISM_FILE}"
POPULATION_FILE_PATH: Final = f"{FOLDER_PATH}/{POPULATION_FILE}"

# Component id's
TARGET_TYPE_DROPDOWN_ID: Final = "target-type-dropdown"
ATTACK_TYPE_DROPDOWN_ID: Final = "attack-type-dropdown"

COUNTRY_RESET_BUTTON_ID: Final = "reset-button"

DONUT_CHART_ID: Final = 'donut-chart'
BAR_CHART_ID: Final = 'bar-chart'
MAP_ID: Final = 'world-map'

SELECTED_COUNTRY_STORE = 'selected-country-store'
