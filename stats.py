from plotnine import (
    ggplot,
    geom_point,
    aes,
    geom_line,
    ggtitle,
    labs,
    scale_color_identity,
    scale_color_manual,
    scale_x_continuous,
    theme,
    xlab,
    ylab,
    facet_wrap,
    facet_grid,
    geom_smooth,
)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import pandas as pd

human_dict = {
    "AIGame_0": ["FRANCE", "GERMANY"],
    "AIGame_1": ["FRANCE", "RUSSIA", "TURKEY"],
    "AIGame_2": ["FRANCE", "RUSSIA", "TURKEY"],
    "AIGame_3": ["FRANCE", "RUSSIA", "TURKEY"],
    "AIGame_4": ["FRANCE", "RUSSIA", "TURKEY"],
    "AIGame_5": ["ENGLAND", "FRANCE", "TURKEY"],
    "AIGame_6": ["RUSSIA", "TURKEY"],
    "AIGame_7": ["AUSTRIA", "FRANCE", "GERMANY"],
    "AIGame_8": ["FRANCE", "GERMANY"],
    "AIGame_9": ["FRANCE", "GERMANY", "ITALY", "TURKEY"],
    "AIGame_10": ["AUSTRIA", "GERMANY", "ITALY"],
    "AIGame_11": ["AUSTRIA", "FRANCE", "GERMANY", "ITALY"],
    "AIGame_12": ["AUSTRIA", "FRANCE", "GERMANY", "ITALY"],
    "AIGame_13": ["FRANCE", "GERMANY", "TURKEY"],
    "AIGame_14": ["RUSSIA", "TURKEY"],
    "AIGame_15": ["FRANCE", "GERMANY"],
    "AIGame_16": ["AUSTRIA", "TURKEY"],
    "AIGame_17": ["AUSTRIA", "FRANCE", "GERMANY", "ITALY"],
    "AIGame_18": ["AUSTRIA", "GERMANY"],
    "AIGame_19": ["AUSTRIA", "ITALY", "TURKEY"],
    "AIGame_20": ["ENGLAND", "RUSSIA", "TURKEY"],
    "AIGame_21": ["ENGLAND", "ITALY"],
    "AIGame_22": ["AUSTRIA", "ENGLAND", "RUSSIA"],
    "AIGame_23": ["AUSTRIA", "ENGLAND", "ITALY", "RUSSIA"],
}

first_time_dict = {
    "AIGame_0": ["GERMANY", "FRANCE"],
    "AIGame_1": ["RUSSIA", "FRANCE"],
    "AIGame_2": ["RUSSIA", "FRANCE"],
    "AIGame_3": ["RUSSIA", "TURKEY", "FRANCE"],
    "AIGame_4": ["RUSSIA", "TURKEY"],
    "AIGame_5": ["FRANCE", "TURKEY"],
    "AIGame_6": ["RUSSIA"],
    "AIGame_7": [],
    "AIGame_8": [],
    "AIGame_9": ["GERMANY"],
    "AIGame_10": [],
    "AIGame_11": ["GERMANY", "FRANCE"],
    "AIGame_12": ["FRANCE"],
    "AIGame_13": [],
    "AIGame_14": [],
    "AIGame_15": [],
    "AIGame_16": ["TURKEY", "AUSTRIA"],
    "AIGame_17": ["FRANCE", "GERMANY"],
    "AIGame_18": [],
    "AIGame_19": ["TURKEY"],
    "AIGame_20": ["ENGLAND", "RUSSIA", "TURKEY"],
    "AIGame_21": ["ENGLAND"],
    "AIGame_22": ["RUSSIA"],
    "AIGame_23": ["ITALY"],
}

experienced_dict = {
    "AIGame_0": [],
    "AIGame_1": ["TURKEY"],
    "AIGame_2": ["TURKEY"],
    "AIGame_3": [],
    "AIGame_4": ["FRANCE"],
    "AIGame_5": ["ENGLAND"],
    "AIGame_6": ["TURKEY"],
    "AIGame_7": ["AUSTRIA", "FRANCE", "GERMANY"],
    "AIGame_8": ["FRANCE", "GERMANY"],
    "AIGame_9": ["ITALY", "TURKEY", "FRANCE"],
    "AIGame_10": ["ITALY", "AUSTRIA", "GERMANY"],
    "AIGame_11": ["ITALY", "AUSTRIA"],
    "AIGame_12": ["ITALY", "AUSTRIA", "GERMANY"],
    "AIGame_13": ["TURKEY", "FRANCE", "GERMANY"],
    "AIGame_14": ["TURKEY", "RUSSIA"],
    "AIGame_15": ["FRANCE", "GERMANY"],
    "AIGame_16": [],
    "AIGame_17": ["ITALY", "AUSTRIA"],
    "AIGame_18": ["AUSTRIA", "GERMANY"],
    "AIGame_19": ["ITALY", "AUSTRIA"],
    "AIGame_20": [],
    "AIGame_21": ["ITALY"],
    "AIGame_22": ["AUSTRIA", "ENGLAND"],
    "AIGame_23": ["AUSTRIA", "RUSSIA", "ENGLAND"],
}

repeated_players = {
    "totonchym": {
        "AIGame_0": "FRANCE",
        "AIGame_2": "TURKEY",
        "AIGame_7": "FRANCE",
        "AIGame_11": "AUSTRIA",
        "AIGame_12": "ITALY",
        "AIGame_13": "GERMANY",
        "AIGame_14": "RUSSIA",
        "AIGame_15": "GERMANY",
        "AIGame_19": "ITALY",
    },
    "eddie": {
        "AIGame_0": "GERMANY",
        "AIGame_1": "TURKEY",
        "AIGame_5": "ENGLAND",
        "AIGame_9": "ITALY",
        "AIGame_12": "AUSTRIA",
    },
    "rawles": {
        "AIGame_1": "FRANCE",
        "AIGame_4": "FRANCE",
        "AIGame_6": "TURKEY",
        "AIGame_7": "AUSTRIA",
        "AIGame_8": "GERMANY",
        "AIGame_9": "TURKEY",
        "AIGame_10": "ITALY",
        "AIGame_12": "GERMANY",
    },
    "ben": {"AIGame_2": "RUSSIA", "AIGame_10": "AUSTRIA"},
    "aguoman": {"AIGame_3": "RUSSIA", "AIGame_13": "FRANCE", "AIGame_23": "ENGLAND"},
    "kirk": {
        "AIGame_4": "RUSSIA",
        "AIGame_14": "TURKEY",
        "AIGame_15": "FRANCE",
        "AIGame_19": "AUSTRIA",
    },
    "marko": {
        "AIGame_5": "FRANCE",
        "AIGame_9": "FRANCE",
        "AIGame_10": "GERMANY",
        "AIGame_11": "ITALY",
    },
    "sloth": {
        "AIGame_6": "RUSSIA",
        "AIGame_7": "GERMANY",
        "AIGame_8": "FRANCE",
        "AIGame_13": "TURKEY",
    },
    "aashutosh": {"AIGame_16": "TURKEY", "AIGame_17": "AUSTRIA"},
    "singhal": {"AIGame_16": "AUSTRIA", "AIGame_17": "ITALY", "AIGame_18": "GERMANY"},
    "parul": {"AIGame_17": "GERMANY", "AIGame_18": "AUSTRIA"},
    "antonio": {
        "AIGame_20": "TURKEY",
        "AIGame_21": "ITALY",
        "AIGame_22": "ENGLAND",
        "AIGame_23": "RUSSIA",
    },
    "kunal": {"AIGame_21": "ENGLAND", "AIGame_22": "AUSTRIA"},
    "zander": {"AIGame_22": "RUSSIA", "AIGame_23": "AUSTRIA"},
}

repeated_mapping = {
    "AIGame_0": ["FRANCE", "GERMANY"],
    "AIGame_1": ["TURKEY", "FRANCE"],
    "AIGame_2": ["TURKEY", "RUSSIA"],
    "AIGame_3": ["RUSSIA"],
    "AIGame_4": ["FRANCE", "RUSSIA"],
    "AIGame_5": ["ENGLAND", "FRANCE"],
    "AIGame_6": ["TURKEY", "RUSSIA"],
    "AIGame_7": ["FRANCE", "AUSTRIA", "GERMANY"],
    "AIGame_8": ["GERMANY", "FRANCE"],
    "AIGame_9": ["ITALY", "TURKEY", "FRANCE"],
    "AIGame_10": ["ITALY", "AUSTRIA", "GERMANY"],
    "AIGame_11": ["AUSTRIA", "ITALY"],
    "AIGame_12": ["ITALY", "AUSTRIA", "GERMANY"],
    "AIGame_13": ["GERMANY", "FRANCE", "TURKEY"],
    "AIGame_14": ["RUSSIA", "TURKEY"],
    "AIGame_15": ["GERMANY", "FRANCE"],
    "AIGame_16": ["TURKEY", "AUSTRIA"],
    "AIGame_17": ["AUSTRIA", "ITALY", "GERMANY"],
    "AIGame_18": ["GERMANY", "AUSTRIA"],
    "AIGame_19": ["ITALY", "AUSTRIA"],
    "AIGame_20": ["TURKEY"],
    "AIGame_21": ["ITALY", "ENGLAND"],
    "AIGame_22": ["ENGLAND", "AUSTRIA", "RUSSIA"],
    "AIGame_23": ["ENGLAND", "RUSSIA", "AUSTRIA"],
}


human_scs = {
    "AIGame_0": {
        "S1901M": {"FRANCE": 3, "GERMANY": 3},
        "S1902M": {"FRANCE": 5, "GERMANY": 5},
        "S1903M": {"FRANCE": 5, "GERMANY": 6},
        "S1904M": {"FRANCE": 7, "GERMANY": 5},
        "S1905M": {"FRANCE": 7, "GERMANY": 6},
        "S1906M": {"FRANCE": 7, "GERMANY": 7},
        "S1907M": {"FRANCE": 10, "GERMANY": 8},
        "S1908M": {"FRANCE": 11, "GERMANY": 9},
    },
    "AIGame_1": {
        "S1901M": {"FRANCE": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"FRANCE": 5, "RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"FRANCE": 5, "RUSSIA": 6, "TURKEY": 3},
        "S1904M": {"FRANCE": 8, "RUSSIA": 4, "TURKEY": 1},
        "S1905M": {"FRANCE": 8, "RUSSIA": 2, "TURKEY": 1},
        "S1906M": {"FRANCE": 9, "RUSSIA": 2, "TURKEY": 0},
        "S1907M": {"FRANCE": 9, "RUSSIA": 2, "TURKEY": 0},
        "S1908M": {"FRANCE": 10, "RUSSIA": 2, "TURKEY": 0},
    },
    "AIGame_10": {
        "S1901M": {"AUSTRIA": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 4, "GERMANY": 5, "ITALY": 3},
        "S1903M": {"AUSTRIA": 4, "GERMANY": 6, "ITALY": 4},
        "S1904M": {"AUSTRIA": 2, "GERMANY": 6, "ITALY": 5},
        "S1905M": {"AUSTRIA": 2, "GERMANY": 4, "ITALY": 5},
        "S1906M": {"AUSTRIA": 2, "GERMANY": 1, "ITALY": 3},
        "S1907M": {"AUSTRIA": 2, "GERMANY": 1, "ITALY": 1},
        "S1908M": {"AUSTRIA": 0, "GERMANY": 0, "ITALY": 0},
    },
    "AIGame_11": {
        "S1901M": {"AUSTRIA": 3, "FRANCE": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 5, "FRANCE": 5, "GERMANY": 5, "ITALY": 4},
        "S1903M": {"AUSTRIA": 5, "FRANCE": 5, "GERMANY": 5, "ITALY": 4},
        "S1904M": {"AUSTRIA": 7, "FRANCE": 5, "GERMANY": 5, "ITALY": 3},
        "S1905M": {"AUSTRIA": 7, "FRANCE": 6, "GERMANY": 4, "ITALY": 2},
        "S1906M": {"AUSTRIA": 7, "FRANCE": 7, "GERMANY": 4, "ITALY": 1},
        "S1907M": {"AUSTRIA": 5, "FRANCE": 9, "GERMANY": 4, "ITALY": 0},
    },
    "AIGame_12": {
        "S1901M": {"AUSTRIA": 3, "FRANCE": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 4, "FRANCE": 4, "GERMANY": 6, "ITALY": 4},
        "S1903M": {"AUSTRIA": 1, "FRANCE": 4, "GERMANY": 6, "ITALY": 6},
        "S1904M": {"AUSTRIA": 0, "FRANCE": 4, "GERMANY": 6, "ITALY": 6},
        "S1905M": {"AUSTRIA": 0, "FRANCE": 3, "GERMANY": 5, "ITALY": 7},
        "S1906M": {"AUSTRIA": 0, "FRANCE": 2, "GERMANY": 5, "ITALY": 9},
        "S1907M": {"AUSTRIA": 0, "FRANCE": 1, "GERMANY": 1, "ITALY": 9},
        "S1908M": {"AUSTRIA": 0, "FRANCE": 0, "GERMANY": 0, "ITALY": 10},
    },
    "AIGame_13": {
        "S1901M": {"FRANCE": 3, "GERMANY": 3, "TURKEY": 3},
        "S1902M": {"FRANCE": 5, "GERMANY": 5, "TURKEY": 4},
        "S1903M": {"FRANCE": 5, "GERMANY": 6, "TURKEY": 3},
        "S1904M": {"FRANCE": 6, "GERMANY": 6, "TURKEY": 3},
        "S1905M": {"FRANCE": 9, "GERMANY": 4, "TURKEY": 2},
        "S1906M": {"FRANCE": 9, "GERMANY": 4, "TURKEY": 1},
        "S1907M": {"FRANCE": 8, "GERMANY": 5, "TURKEY": 0},
        "S1908M": {"FRANCE": 8, "GERMANY": 6, "TURKEY": 0},
    },
    "AIGame_14": {
        "S1901M": {"RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"RUSSIA": 6, "TURKEY": 3},
        "S1904M": {"RUSSIA": 4, "TURKEY": 2},
        "S1905M": {"RUSSIA": 3, "TURKEY": 0},
        "S1906M": {"RUSSIA": 1, "TURKEY": 0},
        "S1907M": {"RUSSIA": 0, "TURKEY": 0},
        "S1908M": {"RUSSIA": 0, "TURKEY": 0},
        "S1909M": {"RUSSIA": 0, "TURKEY": 0},
    },
    "AIGame_15": {
        "S1901M": {"FRANCE": 3, "GERMANY": 3},
        "S1902M": {"FRANCE": 5, "GERMANY": 5},
        "S1903M": {"FRANCE": 5, "GERMANY": 6},
        "S1904M": {"FRANCE": 5, "GERMANY": 7},
        "S1905M": {"FRANCE": 7, "GERMANY": 7},
        "S1906M": {"FRANCE": 8, "GERMANY": 8},
        "S1907M": {"FRANCE": 8, "GERMANY": 9},
        "S1908M": {"FRANCE": 8, "GERMANY": 11},
    },
    "AIGame_16": {
        "S1901M": {"AUSTRIA": 3, "TURKEY": 3},
        "S1902M": {"AUSTRIA": 4, "TURKEY": 4},
        "S1903M": {"AUSTRIA": 3, "TURKEY": 5},
        "S1904M": {"AUSTRIA": 3, "TURKEY": 4},
        "S1905M": {"AUSTRIA": 5, "TURKEY": 3},
        "S1906M": {"AUSTRIA": 7, "TURKEY": 2},
        "S1907M": {"AUSTRIA": 7, "TURKEY": 2},
        "S1908M": {"AUSTRIA": 5, "TURKEY": 2},
    },
    "AIGame_17": {
        "S1901M": {"AUSTRIA": 3, "FRANCE": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 3, "FRANCE": 5, "GERMANY": 3, "ITALY": 4},
        "S1903M": {"AUSTRIA": 2, "FRANCE": 6, "GERMANY": 3, "ITALY": 3},
        "S1904M": {"AUSTRIA": 1, "FRANCE": 7, "GERMANY": 0, "ITALY": 2},
        "S1905M": {"AUSTRIA": 0, "FRANCE": 7, "GERMANY": 0, "ITALY": 1},
        "S1906M": {"AUSTRIA": 0, "FRANCE": 7, "GERMANY": 0, "ITALY": 0},
        "S1907M": {"AUSTRIA": 0, "FRANCE": 6, "GERMANY": 0, "ITALY": 0},
        "S1908M": {"AUSTRIA": 0, "FRANCE": 2, "GERMANY": 0, "ITALY": 0},
    },
    "AIGame_18": {
        "S1901M": {"AUSTRIA": 3, "GERMANY": 3},
        "S1902M": {"AUSTRIA": 2, "GERMANY": 6},
        "S1903M": {"AUSTRIA": 0, "GERMANY": 7},
        "S1904M": {"AUSTRIA": 0, "GERMANY": 5},
        "S1905M": {"AUSTRIA": 0, "GERMANY": 5},
        "S1906M": {"AUSTRIA": 0, "GERMANY": 4},
        "S1907M": {"AUSTRIA": 0, "GERMANY": 3},
    },
    "AIGame_19": {
        "S1901M": {"AUSTRIA": 3, "ITALY": 3, "TURKEY": 3},
        "S1902M": {"AUSTRIA": 4, "ITALY": 4, "TURKEY": 4},
        "S1903M": {"AUSTRIA": 4, "ITALY": 6, "TURKEY": 4},
        "S1904M": {"AUSTRIA": 5, "ITALY": 6, "TURKEY": 3},
        "S1905M": {"AUSTRIA": 4, "ITALY": 7, "TURKEY": 2},
        "S1906M": {"AUSTRIA": 3, "ITALY": 8, "TURKEY": 0},
        "S1907M": {"AUSTRIA": 1, "ITALY": 8, "TURKEY": 0},
        "S1908M": {"AUSTRIA": 0, "ITALY": 7, "TURKEY": 0},
    },
    "AIGame_2": {
        "S1901M": {"FRANCE": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"FRANCE": 6, "RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"FRANCE": 6, "RUSSIA": 5, "TURKEY": 3},
        "S1904M": {"FRANCE": 7, "RUSSIA": 5, "TURKEY": 4},
        "S1905M": {"FRANCE": 7, "RUSSIA": 4, "TURKEY": 3},
        "S1906M": {"FRANCE": 8, "RUSSIA": 2, "TURKEY": 3},
    },
    "AIGame_20": {
        "S1901M": {"ENGLAND": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"ENGLAND": 4, "RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"ENGLAND": 4, "RUSSIA": 6, "TURKEY": 3},
        "S1904M": {"ENGLAND": 3, "RUSSIA": 4, "TURKEY": 2},
        "S1905M": {"ENGLAND": 2, "RUSSIA": 3, "TURKEY": 1},
        "S1906M": {"ENGLAND": 2, "RUSSIA": 2, "TURKEY": 1},
        "S1907M": {"ENGLAND": 1, "RUSSIA": 2, "TURKEY": 2},
        "S1908M": {"ENGLAND": 1, "RUSSIA": 3, "TURKEY": 1},
    },
    "AIGame_21": {
        "S1901M": {"ENGLAND": 3, "ITALY": 3},
        "S1902M": {"ENGLAND": 4, "ITALY": 5},
        "S1903M": {"ENGLAND": 4, "ITALY": 5},
        "S1904M": {"ENGLAND": 2, "ITALY": 5},
        "S1905M": {"ENGLAND": 1, "ITALY": 5},
        "S1906M": {"ENGLAND": 1, "ITALY": 5},
        "S1907M": {"ENGLAND": 1, "ITALY": 5},
        "S1908M": {"ENGLAND": 1, "ITALY": 4},
        "S1909M": {"ENGLAND": 1, "ITALY": 4},
    },
    "AIGame_22": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "RUSSIA": 4},
        "S1902M": {"AUSTRIA": 3, "ENGLAND": 5, "RUSSIA": 5},
        "S1903M": {"AUSTRIA": 3, "ENGLAND": 8, "RUSSIA": 4},
        "S1904M": {"AUSTRIA": 3, "ENGLAND": 7, "RUSSIA": 4},
        "S1905M": {"AUSTRIA": 1, "ENGLAND": 5, "RUSSIA": 6},
        "S1906M": {"AUSTRIA": 0, "ENGLAND": 3, "RUSSIA": 7},
        "S1907M": {"AUSTRIA": 0, "ENGLAND": 3, "RUSSIA": 7},
        "S1908M": {"AUSTRIA": 0, "ENGLAND": 3, "RUSSIA": 6},
        "S1909M": {"AUSTRIA": 0, "ENGLAND": 4, "RUSSIA": 3},
    },
    "AIGame_23": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "ITALY": 3, "RUSSIA": 4},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 5, "ITALY": 4, "RUSSIA": 5},
        "S1903M": {"AUSTRIA": 5, "ENGLAND": 3, "ITALY": 4, "RUSSIA": 7},
        "S1904M": {"AUSTRIA": 4, "ENGLAND": 1, "ITALY": 5, "RUSSIA": 7},
        "S1905M": {"AUSTRIA": 2, "ENGLAND": 1, "ITALY": 6, "RUSSIA": 8},
        "S1906M": {"AUSTRIA": 0, "ENGLAND": 0, "ITALY": 6, "RUSSIA": 8},
        "S1907M": {"AUSTRIA": 0, "ENGLAND": 0, "ITALY": 5, "RUSSIA": 8},
        "S1908M": {"AUSTRIA": 0, "ENGLAND": 0, "ITALY": 4, "RUSSIA": 9},
    },
    "AIGame_3": {
        "S1901M": {"FRANCE": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"FRANCE": 6, "RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"FRANCE": 6, "RUSSIA": 6, "TURKEY": 4},
        "S1904M": {"FRANCE": 5, "RUSSIA": 6, "TURKEY": 4},
        "S1905M": {"FRANCE": 4, "RUSSIA": 7, "TURKEY": 4},
        "S1906M": {"FRANCE": 1, "RUSSIA": 5, "TURKEY": 3},
        "S1907M": {"FRANCE": 1, "RUSSIA": 4, "TURKEY": 3},
    },
    "AIGame_4": {
        "S1901M": {"FRANCE": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"FRANCE": 6, "RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"FRANCE": 6, "RUSSIA": 4, "TURKEY": 3},
        "S1904M": {"FRANCE": 6, "RUSSIA": 3, "TURKEY": 1},
        "S1905M": {"FRANCE": 5, "RUSSIA": 3, "TURKEY": 0},
        "S1906M": {"FRANCE": 4, "RUSSIA": 3, "TURKEY": 0},
    },
    "AIGame_5": {
        "S1901M": {"ENGLAND": 3, "FRANCE": 3, "TURKEY": 3},
        "S1902M": {"ENGLAND": 4, "FRANCE": 5, "TURKEY": 4},
        "S1903M": {"ENGLAND": 4, "FRANCE": 7, "TURKEY": 2},
        "S1904M": {"ENGLAND": 5, "FRANCE": 6, "TURKEY": 1},
        "S1905M": {"ENGLAND": 5, "FRANCE": 7, "TURKEY": 1},
        "S1906M": {"ENGLAND": 5, "FRANCE": 6, "TURKEY": 1},
        "S1907M": {"ENGLAND": 6, "FRANCE": 8, "TURKEY": 1},
    },
    "AIGame_6": {
        "S1901M": {"RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"RUSSIA": 5, "TURKEY": 2},
        "S1904M": {"RUSSIA": 3, "TURKEY": 0},
        "S1905M": {"RUSSIA": 3, "TURKEY": 0},
        "S1906M": {"RUSSIA": 4, "TURKEY": 0},
        "S1907M": {"RUSSIA": 4, "TURKEY": 0},
        "S1908M": {"RUSSIA": 4, "TURKEY": 0},
    },
    "AIGame_7": {
        "S1901M": {"AUSTRIA": 3, "FRANCE": 3, "GERMANY": 3},
        "S1902M": {"AUSTRIA": 3, "FRANCE": 5, "GERMANY": 5},
        "S1903M": {"AUSTRIA": 2, "FRANCE": 6, "GERMANY": 4},
        "S1904M": {"AUSTRIA": 1, "FRANCE": 6, "GERMANY": 5},
        "S1905M": {"AUSTRIA": 0, "FRANCE": 6, "GERMANY": 5},
        "S1906M": {"AUSTRIA": 0, "FRANCE": 7, "GERMANY": 6},
        "S1907M": {"AUSTRIA": 0, "FRANCE": 7, "GERMANY": 6},
        "S1908M": {"AUSTRIA": 0, "FRANCE": 8, "GERMANY": 6},
    },
    "AIGame_8": {
        "S1901M": {"FRANCE": 3, "GERMANY": 3},
        "S1902M": {"FRANCE": 5, "GERMANY": 6},
        "S1903M": {"FRANCE": 5, "GERMANY": 8},
        "S1904M": {"FRANCE": 5, "GERMANY": 7},
        "S1905M": {"FRANCE": 5, "GERMANY": 7},
        "S1906M": {"FRANCE": 5, "GERMANY": 7},
        "S1907M": {"FRANCE": 6, "GERMANY": 7},
        "S1908M": {"FRANCE": 8, "GERMANY": 8},
    },
    "AIGame_9": {
        "S1901M": {"FRANCE": 3, "GERMANY": 3, "ITALY": 3, "TURKEY": 3},
        "S1902M": {"FRANCE": 5, "GERMANY": 5, "ITALY": 5, "TURKEY": 4},
        "S1903M": {"FRANCE": 6, "GERMANY": 5, "ITALY": 5, "TURKEY": 4},
        "S1904M": {"FRANCE": 7, "GERMANY": 5, "ITALY": 6, "TURKEY": 5},
        "S1905M": {"FRANCE": 9, "GERMANY": 6, "ITALY": 6, "TURKEY": 5},
        "S1906M": {"FRANCE": 7, "GERMANY": 6, "ITALY": 8, "TURKEY": 4},
        "S1907M": {"FRANCE": 9, "GERMANY": 5, "ITALY": 6, "TURKEY": 3},
    },
}

cicero_scs = {
    "AIGame_0": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "ITALY": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 4, "ITALY": 4, "RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"AUSTRIA": 6, "ENGLAND": 3, "ITALY": 4, "RUSSIA": 7, "TURKEY": 3},
        "S1904M": {"AUSTRIA": 7, "ENGLAND": 2, "ITALY": 3, "RUSSIA": 8, "TURKEY": 2},
        "S1905M": {"AUSTRIA": 8, "ENGLAND": 0, "ITALY": 2, "RUSSIA": 10, "TURKEY": 1},
        "S1906M": {"AUSTRIA": 9, "ENGLAND": 0, "ITALY": 2, "RUSSIA": 9, "TURKEY": 0},
        "S1907M": {"AUSTRIA": 8, "ENGLAND": 0, "ITALY": 0, "RUSSIA": 8, "TURKEY": 0},
        "S1908M": {"AUSTRIA": 6, "ENGLAND": 0, "ITALY": 0, "RUSSIA": 8, "TURKEY": 0},
    },
    "AIGame_1": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 4, "GERMANY": 6, "ITALY": 4},
        "S1903M": {"AUSTRIA": 6, "ENGLAND": 3, "GERMANY": 7, "ITALY": 4},
        "S1904M": {"AUSTRIA": 9, "ENGLAND": 1, "GERMANY": 7, "ITALY": 4},
        "S1905M": {"AUSTRIA": 10, "ENGLAND": 1, "GERMANY": 8, "ITALY": 4},
        "S1906M": {"AUSTRIA": 10, "ENGLAND": 0, "GERMANY": 9, "ITALY": 4},
        "S1907M": {"AUSTRIA": 11, "ENGLAND": 0, "GERMANY": 9, "ITALY": 3},
        "S1908M": {"AUSTRIA": 10, "ENGLAND": 0, "GERMANY": 8, "ITALY": 4},
    },
    "AIGame_10": {
        "S1901M": {"ENGLAND": 3, "FRANCE": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"ENGLAND": 4, "FRANCE": 5, "RUSSIA": 5, "TURKEY": 4},
        "S1903M": {"ENGLAND": 5, "FRANCE": 5, "RUSSIA": 5, "TURKEY": 5},
        "S1904M": {"ENGLAND": 5, "FRANCE": 5, "RUSSIA": 4, "TURKEY": 7},
        "S1905M": {"ENGLAND": 6, "FRANCE": 6, "RUSSIA": 4, "TURKEY": 7},
        "S1906M": {"ENGLAND": 10, "FRANCE": 5, "RUSSIA": 6, "TURKEY": 7},
        "S1907M": {"ENGLAND": 8, "FRANCE": 5, "RUSSIA": 8, "TURKEY": 9},
        "S1908M": {"ENGLAND": 10, "FRANCE": 5, "RUSSIA": 5, "TURKEY": 14},
    },
    "AIGame_11": {
        "S1901M": {"ENGLAND": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"ENGLAND": 5, "RUSSIA": 5, "TURKEY": 4},
        "S1903M": {"ENGLAND": 6, "RUSSIA": 6, "TURKEY": 3},
        "S1904M": {"ENGLAND": 5, "RUSSIA": 7, "TURKEY": 2},
        "S1905M": {"ENGLAND": 5, "RUSSIA": 8, "TURKEY": 2},
        "S1906M": {"ENGLAND": 5, "RUSSIA": 8, "TURKEY": 2},
        "S1907M": {"ENGLAND": 5, "RUSSIA": 8, "TURKEY": 3},
    },
    "AIGame_12": {
        "S1901M": {"ENGLAND": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"ENGLAND": 4, "RUSSIA": 7, "TURKEY": 4},
        "S1903M": {"ENGLAND": 5, "RUSSIA": 8, "TURKEY": 4},
        "S1904M": {"ENGLAND": 5, "RUSSIA": 8, "TURKEY": 5},
        "S1905M": {"ENGLAND": 6, "RUSSIA": 9, "TURKEY": 4},
        "S1906M": {"ENGLAND": 7, "RUSSIA": 8, "TURKEY": 3},
        "S1907M": {"ENGLAND": 10, "RUSSIA": 10, "TURKEY": 3},
        "S1908M": {"ENGLAND": 12, "RUSSIA": 8, "TURKEY": 4},
    },
    "AIGame_13": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "ITALY": 3, "RUSSIA": 4},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 5, "ITALY": 4, "RUSSIA": 6},
        "S1903M": {"AUSTRIA": 7, "ENGLAND": 3, "ITALY": 3, "RUSSIA": 7},
        "S1904M": {"AUSTRIA": 8, "ENGLAND": 3, "ITALY": 1, "RUSSIA": 7},
        "S1905M": {"AUSTRIA": 10, "ENGLAND": 2, "ITALY": 0, "RUSSIA": 7},
        "S1906M": {"AUSTRIA": 11, "ENGLAND": 2, "ITALY": 0, "RUSSIA": 7},
        "S1907M": {"AUSTRIA": 14, "ENGLAND": 3, "ITALY": 0, "RUSSIA": 4},
        "S1908M": {"AUSTRIA": 12, "ENGLAND": 4, "ITALY": 0, "RUSSIA": 4},
    },
    "AIGame_14": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "FRANCE": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 4, "FRANCE": 6, "GERMANY": 5, "ITALY": 4},
        "S1903M": {"AUSTRIA": 6, "ENGLAND": 2, "FRANCE": 7, "GERMANY": 6, "ITALY": 4},
        "S1904M": {"AUSTRIA": 7, "ENGLAND": 2, "FRANCE": 8, "GERMANY": 6, "ITALY": 5},
        "S1905M": {"AUSTRIA": 9, "ENGLAND": 1, "FRANCE": 9, "GERMANY": 6, "ITALY": 6},
        "S1906M": {"AUSTRIA": 12, "ENGLAND": 0, "FRANCE": 9, "GERMANY": 8, "ITALY": 4},
        "S1907M": {"AUSTRIA": 15, "ENGLAND": 0, "FRANCE": 9, "GERMANY": 8, "ITALY": 2},
        "S1908M": {"AUSTRIA": 16, "ENGLAND": 0, "FRANCE": 9, "GERMANY": 8, "ITALY": 1},
        "S1909M": {"AUSTRIA": 17, "ENGLAND": 0, "FRANCE": 9, "GERMANY": 8, "ITALY": 0},
    },
    "AIGame_15": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "ITALY": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 5, "ITALY": 4, "RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"AUSTRIA": 5, "ENGLAND": 3, "ITALY": 4, "RUSSIA": 7, "TURKEY": 4},
        "S1904M": {"AUSTRIA": 4, "ENGLAND": 3, "ITALY": 5, "RUSSIA": 6, "TURKEY": 4},
        "S1905M": {"AUSTRIA": 3, "ENGLAND": 1, "ITALY": 6, "RUSSIA": 6, "TURKEY": 4},
        "S1906M": {"AUSTRIA": 1, "ENGLAND": 0, "ITALY": 6, "RUSSIA": 6, "TURKEY": 5},
        "S1907M": {"AUSTRIA": 0, "ENGLAND": 0, "ITALY": 8, "RUSSIA": 2, "TURKEY": 7},
        "S1908M": {"AUSTRIA": 0, "ENGLAND": 0, "ITALY": 7, "RUSSIA": 0, "TURKEY": 8},
    },
    "AIGame_16": {
        "S1901M": {"ENGLAND": 3, "FRANCE": 3, "GERMANY": 3, "ITALY": 3, "RUSSIA": 4},
        "S1902M": {"ENGLAND": 4, "FRANCE": 6, "GERMANY": 5, "ITALY": 4, "RUSSIA": 6},
        "S1903M": {"ENGLAND": 4, "FRANCE": 6, "GERMANY": 5, "ITALY": 6, "RUSSIA": 5},
        "S1904M": {"ENGLAND": 4, "FRANCE": 7, "GERMANY": 4, "ITALY": 5, "RUSSIA": 7},
        "S1905M": {"ENGLAND": 3, "FRANCE": 7, "GERMANY": 5, "ITALY": 4, "RUSSIA": 7},
        "S1906M": {"ENGLAND": 3, "FRANCE": 7, "GERMANY": 5, "ITALY": 3, "RUSSIA": 7},
        "S1907M": {"ENGLAND": 3, "FRANCE": 8, "GERMANY": 6, "ITALY": 3, "RUSSIA": 5},
        "S1908M": {"ENGLAND": 3, "FRANCE": 10, "GERMANY": 6, "ITALY": 2, "RUSSIA": 6},
    },
    "AIGame_17": {
        "S1901M": {"ENGLAND": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"ENGLAND": 5, "RUSSIA": 5, "TURKEY": 5},
        "S1903M": {"ENGLAND": 5, "RUSSIA": 8, "TURKEY": 6},
        "S1904M": {"ENGLAND": 7, "RUSSIA": 8, "TURKEY": 9},
        "S1905M": {"ENGLAND": 8, "RUSSIA": 7, "TURKEY": 11},
        "S1906M": {"ENGLAND": 10, "RUSSIA": 3, "TURKEY": 14},
        "S1907M": {"ENGLAND": 13, "RUSSIA": 0, "TURKEY": 15},
        "S1908M": {"ENGLAND": 15, "RUSSIA": 0, "TURKEY": 17},
    },
    "AIGame_18": {
        "S1901M": {"ENGLAND": 3, "FRANCE": 3, "ITALY": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"ENGLAND": 4, "FRANCE": 3, "ITALY": 5, "RUSSIA": 6, "TURKEY": 5},
        "S1903M": {"ENGLAND": 6, "FRANCE": 4, "ITALY": 7, "RUSSIA": 7, "TURKEY": 3},
        "S1904M": {"ENGLAND": 7, "FRANCE": 4, "ITALY": 8, "RUSSIA": 6, "TURKEY": 4},
        "S1905M": {"ENGLAND": 6, "FRANCE": 5, "ITALY": 8, "RUSSIA": 6, "TURKEY": 4},
        "S1906M": {"ENGLAND": 7, "FRANCE": 5, "ITALY": 7, "RUSSIA": 8, "TURKEY": 3},
        "S1907M": {"ENGLAND": 8, "FRANCE": 5, "ITALY": 7, "RUSSIA": 8, "TURKEY": 3},
    },
    "AIGame_19": {
        "S1901M": {"ENGLAND": 3, "FRANCE": 3, "GERMANY": 3, "RUSSIA": 4},
        "S1902M": {"ENGLAND": 3, "FRANCE": 5, "GERMANY": 5, "RUSSIA": 5},
        "S1903M": {"ENGLAND": 4, "FRANCE": 5, "GERMANY": 7, "RUSSIA": 4},
        "S1904M": {"ENGLAND": 4, "FRANCE": 6, "GERMANY": 6, "RUSSIA": 4},
        "S1905M": {"ENGLAND": 3, "FRANCE": 7, "GERMANY": 6, "RUSSIA": 5},
        "S1906M": {"ENGLAND": 4, "FRANCE": 7, "GERMANY": 4, "RUSSIA": 8},
        "S1907M": {"ENGLAND": 4, "FRANCE": 6, "GERMANY": 4, "RUSSIA": 11},
        "S1908M": {"ENGLAND": 5, "FRANCE": 5, "GERMANY": 3, "RUSSIA": 14},
    },
    "AIGame_2": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 4, "GERMANY": 5, "ITALY": 4},
        "S1903M": {"AUSTRIA": 6, "ENGLAND": 4, "GERMANY": 6, "ITALY": 4},
        "S1904M": {"AUSTRIA": 5, "ENGLAND": 3, "GERMANY": 6, "ITALY": 4},
        "S1905M": {"AUSTRIA": 6, "ENGLAND": 3, "GERMANY": 6, "ITALY": 5},
        "S1906M": {"AUSTRIA": 7, "ENGLAND": 2, "GERMANY": 7, "ITALY": 5},
    },
    "AIGame_20": {
        "S1901M": {"AUSTRIA": 3, "FRANCE": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 4, "FRANCE": 4, "GERMANY": 6, "ITALY": 4},
        "S1903M": {"AUSTRIA": 6, "FRANCE": 5, "GERMANY": 7, "ITALY": 3},
        "S1904M": {"AUSTRIA": 9, "FRANCE": 6, "GERMANY": 8, "ITALY": 2},
        "S1905M": {"AUSTRIA": 9, "FRANCE": 7, "GERMANY": 10, "ITALY": 2},
        "S1906M": {"AUSTRIA": 9, "FRANCE": 8, "GERMANY": 10, "ITALY": 2},
        "S1907M": {"AUSTRIA": 8, "FRANCE": 8, "GERMANY": 10, "ITALY": 3},
        "S1908M": {"AUSTRIA": 9, "FRANCE": 8, "GERMANY": 10, "ITALY": 2},
    },
    "AIGame_21": {
        "S1901M": {"AUSTRIA": 3, "FRANCE": 3, "GERMANY": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"AUSTRIA": 4, "FRANCE": 5, "GERMANY": 5, "RUSSIA": 5, "TURKEY": 4},
        "S1903M": {"AUSTRIA": 4, "FRANCE": 6, "GERMANY": 5, "RUSSIA": 5, "TURKEY": 5},
        "S1904M": {"AUSTRIA": 3, "FRANCE": 7, "GERMANY": 5, "RUSSIA": 6, "TURKEY": 6},
        "S1905M": {"AUSTRIA": 2, "FRANCE": 8, "GERMANY": 5, "RUSSIA": 6, "TURKEY": 7},
        "S1906M": {"AUSTRIA": 1, "FRANCE": 8, "GERMANY": 5, "RUSSIA": 7, "TURKEY": 7},
        "S1907M": {"AUSTRIA": 1, "FRANCE": 9, "GERMANY": 3, "RUSSIA": 7, "TURKEY": 8},
        "S1908M": {"AUSTRIA": 1, "FRANCE": 10, "GERMANY": 3, "RUSSIA": 5, "TURKEY": 10},
        "S1909M": {"AUSTRIA": 2, "FRANCE": 12, "GERMANY": 3, "RUSSIA": 1, "TURKEY": 11},
    },
    "AIGame_22": {
        "S1901M": {"FRANCE": 3, "GERMANY": 3, "ITALY": 3, "TURKEY": 3},
        "S1902M": {"FRANCE": 5, "GERMANY": 5, "ITALY": 4, "TURKEY": 4},
        "S1903M": {"FRANCE": 5, "GERMANY": 4, "ITALY": 5, "TURKEY": 4},
        "S1904M": {"FRANCE": 3, "GERMANY": 5, "ITALY": 6, "TURKEY": 6},
        "S1905M": {"FRANCE": 2, "GERMANY": 6, "ITALY": 8, "TURKEY": 6},
        "S1906M": {"FRANCE": 2, "GERMANY": 6, "ITALY": 9, "TURKEY": 7},
        "S1907M": {"FRANCE": 1, "GERMANY": 7, "ITALY": 9, "TURKEY": 7},
        "S1908M": {"FRANCE": 0, "GERMANY": 7, "ITALY": 12, "TURKEY": 6},
        "S1909M": {"FRANCE": 0, "GERMANY": 8, "ITALY": 12, "TURKEY": 7},
    },
    "AIGame_23": {
        "S1901M": {"FRANCE": 3, "GERMANY": 3, "TURKEY": 3},
        "S1902M": {"FRANCE": 5, "GERMANY": 5, "TURKEY": 4},
        "S1903M": {"FRANCE": 5, "GERMANY": 6, "TURKEY": 4},
        "S1904M": {"FRANCE": 7, "GERMANY": 6, "TURKEY": 4},
        "S1905M": {"FRANCE": 8, "GERMANY": 5, "TURKEY": 4},
        "S1906M": {"FRANCE": 10, "GERMANY": 5, "TURKEY": 5},
        "S1907M": {"FRANCE": 11, "GERMANY": 5, "TURKEY": 5},
        "S1908M": {"FRANCE": 11, "GERMANY": 5, "TURKEY": 5},
    },
    "AIGame_3": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 4, "GERMANY": 4, "ITALY": 4},
        "S1903M": {"AUSTRIA": 6, "ENGLAND": 4, "GERMANY": 5, "ITALY": 3},
        "S1904M": {"AUSTRIA": 6, "ENGLAND": 4, "GERMANY": 5, "ITALY": 4},
        "S1905M": {"AUSTRIA": 6, "ENGLAND": 3, "GERMANY": 7, "ITALY": 3},
        "S1906M": {"AUSTRIA": 7, "ENGLAND": 3, "GERMANY": 9, "ITALY": 6},
        "S1907M": {"AUSTRIA": 6, "ENGLAND": 2, "GERMANY": 11, "ITALY": 7},
    },
    "AIGame_4": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 4, "GERMANY": 5, "ITALY": 4},
        "S1903M": {"AUSTRIA": 8, "ENGLAND": 3, "GERMANY": 6, "ITALY": 4},
        "S1904M": {"AUSTRIA": 7, "ENGLAND": 3, "GERMANY": 8, "ITALY": 6},
        "S1905M": {"AUSTRIA": 8, "ENGLAND": 3, "GERMANY": 9, "ITALY": 6},
        "S1906M": {"AUSTRIA": 9, "ENGLAND": 4, "GERMANY": 8, "ITALY": 6},
    },
    "AIGame_5": {
        "S1901M": {"AUSTRIA": 3, "GERMANY": 3, "ITALY": 3, "RUSSIA": 4},
        "S1902M": {"AUSTRIA": 5, "GERMANY": 5, "ITALY": 4, "RUSSIA": 5},
        "S1903M": {"AUSTRIA": 7, "GERMANY": 6, "ITALY": 3, "RUSSIA": 5},
        "S1904M": {"AUSTRIA": 8, "GERMANY": 5, "ITALY": 3, "RUSSIA": 6},
        "S1905M": {"AUSTRIA": 9, "GERMANY": 4, "ITALY": 2, "RUSSIA": 6},
        "S1906M": {"AUSTRIA": 11, "GERMANY": 4, "ITALY": 3, "RUSSIA": 4},
        "S1907M": {"AUSTRIA": 13, "GERMANY": 3, "ITALY": 1, "RUSSIA": 2},
    },
    "AIGame_6": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "FRANCE": 3, "GERMANY": 3, "ITALY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 4, "FRANCE": 6, "GERMANY": 4, "ITALY": 4},
        "S1903M": {"AUSTRIA": 6, "ENGLAND": 5, "FRANCE": 7, "GERMANY": 4, "ITALY": 5},
        "S1904M": {"AUSTRIA": 6, "ENGLAND": 5, "FRANCE": 9, "GERMANY": 3, "ITALY": 8},
        "S1905M": {"AUSTRIA": 4, "ENGLAND": 4, "FRANCE": 11, "GERMANY": 2, "ITALY": 10},
        "S1906M": {"AUSTRIA": 4, "ENGLAND": 3, "FRANCE": 12, "GERMANY": 2, "ITALY": 9},
        "S1907M": {"AUSTRIA": 5, "ENGLAND": 2, "FRANCE": 12, "GERMANY": 2, "ITALY": 9},
        "S1908M": {"AUSTRIA": 6, "ENGLAND": 1, "FRANCE": 12, "GERMANY": 2, "ITALY": 9},
    },
    "AIGame_7": {
        "S1901M": {"ENGLAND": 3, "ITALY": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"ENGLAND": 5, "ITALY": 3, "RUSSIA": 7, "TURKEY": 5},
        "S1903M": {"ENGLAND": 4, "ITALY": 4, "RUSSIA": 8, "TURKEY": 6},
        "S1904M": {"ENGLAND": 3, "ITALY": 4, "RUSSIA": 8, "TURKEY": 7},
        "S1905M": {"ENGLAND": 3, "ITALY": 6, "RUSSIA": 7, "TURKEY": 7},
        "S1906M": {"ENGLAND": 1, "ITALY": 7, "RUSSIA": 5, "TURKEY": 8},
        "S1907M": {"ENGLAND": 1, "ITALY": 6, "RUSSIA": 5, "TURKEY": 9},
        "S1908M": {"ENGLAND": 0, "ITALY": 4, "RUSSIA": 5, "TURKEY": 11},
    },
    "AIGame_8": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "ITALY": 3, "RUSSIA": 4, "TURKEY": 3},
        "S1902M": {"AUSTRIA": 5, "ENGLAND": 4, "ITALY": 4, "RUSSIA": 6, "TURKEY": 4},
        "S1903M": {"AUSTRIA": 6, "ENGLAND": 4, "ITALY": 3, "RUSSIA": 5, "TURKEY": 3},
        "S1904M": {"AUSTRIA": 8, "ENGLAND": 3, "ITALY": 4, "RUSSIA": 7, "TURKEY": 0},
        "S1905M": {"AUSTRIA": 9, "ENGLAND": 3, "ITALY": 3, "RUSSIA": 7, "TURKEY": 0},
        "S1906M": {"AUSTRIA": 12, "ENGLAND": 3, "ITALY": 1, "RUSSIA": 6, "TURKEY": 0},
        "S1907M": {"AUSTRIA": 13, "ENGLAND": 3, "ITALY": 0, "RUSSIA": 5, "TURKEY": 0},
        "S1908M": {"AUSTRIA": 14, "ENGLAND": 1, "ITALY": 0, "RUSSIA": 3, "TURKEY": 0},
    },
    "AIGame_9": {
        "S1901M": {"AUSTRIA": 3, "ENGLAND": 3, "RUSSIA": 4},
        "S1902M": {"AUSTRIA": 4, "ENGLAND": 4, "RUSSIA": 5},
        "S1903M": {"AUSTRIA": 4, "ENGLAND": 5, "RUSSIA": 5},
        "S1904M": {"AUSTRIA": 1, "ENGLAND": 4, "RUSSIA": 6},
        "S1905M": {"AUSTRIA": 1, "ENGLAND": 0, "RUSSIA": 7},
        "S1906M": {"AUSTRIA": 0, "ENGLAND": 0, "RUSSIA": 9},
        "S1907M": {"AUSTRIA": 0, "ENGLAND": 0, "RUSSIA": 11},
    },
}

f1 = {
    "AIGame_0": {
        "S1901M": {"FRANCE": 0.75},
        "F1901M": {"FRANCE": 0.75, "GERMANY": 0.75},
        "S1902M": {"FRANCE": 0.8888888888888888, "GERMANY": 0.75},
        "F1902M": {"FRANCE": 0.8888888888888888, "GERMANY": 0.5714285714285714},
        "S1903M": {"FRANCE": 0.8888888888888888, "GERMANY": 0.5},
        "F1903M": {"FRANCE": 0.8888888888888888, "GERMANY": 0.5},
        "S1904M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1904M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1905M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1905M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1906M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1906M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1907M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1907M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1908M": {"FRANCE": 1.0, "GERMANY": 1.0},
    },
    "AIGame_1": {
        "S1901M": {},
        "F1901M": {"TURKEY": 0.4},
        "S1902M": {"FRANCE": 0.4, "RUSSIA": 0.8571428571428571, "TURKEY": 0.4},
        "F1902M": {"FRANCE": 0.4, "RUSSIA": 0.8571428571428571, "TURKEY": 0.4},
        "S1903M": {"FRANCE": 0.4, "RUSSIA": 1.0, "TURKEY": 0.6666666666666666},
        "F1903M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8888888888888888,
            "TURKEY": 0.8571428571428571,
        },
        "S1904M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
        "F1904M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
        "S1905M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
        "F1905M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
        "S1906M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
        "F1906M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
        "S1907M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
        "F1907M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
        "S1908M": {
            "FRANCE": 0.3333333333333333,
            "RUSSIA": 0.8,
            "TURKEY": 0.8571428571428571,
        },
    },
    "AIGame_10": {
        "S1901M": {"AUSTRIA": 0.4, "GERMANY": 0.5714285714285714},
        "F1901M": {"AUSTRIA": 0.4, "GERMANY": 0.5714285714285714},
        "S1902M": {
            "AUSTRIA": 0.4,
            "GERMANY": 0.5714285714285714,
            "ITALY": 0.8571428571428571,
        },
        "F1902M": {
            "AUSTRIA": 0.3333333333333333,
            "GERMANY": 0.5714285714285714,
            "ITALY": 0.5714285714285714,
        },
        "S1903M": {
            "AUSTRIA": 0.6666666666666666,
            "GERMANY": 0.5714285714285714,
            "ITALY": 0.4,
        },
        "F1903M": {"AUSTRIA": 1.0, "GERMANY": 0.5714285714285714, "ITALY": 0.4},
        "S1904M": {
            "AUSTRIA": 1.0,
            "GERMANY": 0.8571428571428571,
            "ITALY": 0.6666666666666666,
        },
        "F1904M": {
            "AUSTRIA": 1.0,
            "GERMANY": 0.8571428571428571,
            "ITALY": 0.6666666666666666,
        },
        "S1905M": {"AUSTRIA": 1.0, "GERMANY": 0.75, "ITALY": 0.6666666666666666},
        "F1905M": {"AUSTRIA": 1.0, "GERMANY": 0.75, "ITALY": 0.6666666666666666},
        "S1906M": {"AUSTRIA": 1.0, "GERMANY": 0.75, "ITALY": 0.6666666666666666},
        "F1906M": {"AUSTRIA": 1.0, "GERMANY": 0.75, "ITALY": 0.6666666666666666},
        "S1907M": {
            "AUSTRIA": 1.0,
            "GERMANY": 0.5714285714285714,
            "ITALY": 0.6666666666666666,
        },
        "F1907M": {
            "AUSTRIA": 1.0,
            "GERMANY": 0.5714285714285714,
            "ITALY": 0.6666666666666666,
        },
        "S1908M": {
            "GERMANY": 0.5714285714285714,
            "AUSTRIA": 1.0,
            "ITALY": 0.6666666666666666,
        },
    },
    "AIGame_11": {
        "S1901M": {
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.6666666666666666,
            "ITALY": 0.6666666666666666,
        },
        "F1901M": {
            "AUSTRIA": 0.6666666666666666,
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.6666666666666666,
            "ITALY": 0.6666666666666666,
        },
        "S1902M": {
            "AUSTRIA": 0.6666666666666666,
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.5714285714285714,
            "ITALY": 0.6666666666666666,
        },
        "F1902M": {
            "AUSTRIA": 0.6666666666666666,
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.5714285714285714,
            "ITALY": 0.6666666666666666,
        },
        "S1903M": {
            "AUSTRIA": 0.6666666666666666,
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.5,
            "ITALY": 0.6666666666666666,
        },
        "F1903M": {
            "AUSTRIA": 0.6666666666666666,
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.5,
            "ITALY": 0.6666666666666666,
        },
        "S1904M": {
            "AUSTRIA": 0.5714285714285714,
            "FRANCE": 0.3333333333333333,
            "GERMANY": 0.5,
            "ITALY": 0.3333333333333333,
        },
        "F1904M": {
            "AUSTRIA": 0.5714285714285714,
            "FRANCE": 0.5714285714285714,
            "GERMANY": 0.75,
            "ITALY": 0.3333333333333333,
        },
        "S1905M": {
            "AUSTRIA": 0.5714285714285714,
            "FRANCE": 0.5714285714285714,
            "GERMANY": 0.75,
            "ITALY": 0.3333333333333333,
        },
        "F1905M": {
            "AUSTRIA": 0.5714285714285714,
            "FRANCE": 0.8571428571428571,
            "GERMANY": 0.75,
            "ITALY": 0.3333333333333333,
        },
        "S1906M": {
            "AUSTRIA": 0.5714285714285714,
            "FRANCE": 0.8571428571428571,
            "GERMANY": 0.75,
            "ITALY": 0.3333333333333333,
        },
        "F1906M": {
            "AUSTRIA": 0.5714285714285714,
            "FRANCE": 0.8571428571428571,
            "GERMANY": 0.75,
            "ITALY": 0.3333333333333333,
        },
        "S1907M": {
            "AUSTRIA": 0.5714285714285714,
            "FRANCE": 0.8571428571428571,
            "GERMANY": 0.75,
            "ITALY": 0.3333333333333333,
        },
    },
    "AIGame_12": {
        "S1901M": {"ITALY": 0.0},
        "F1901M": {"ITALY": 0.0},
        "S1902M": {"ITALY": 0.4},
        "F1902M": {"GERMANY": 0.5, "ITALY": 0.4},
        "S1903M": {"GERMANY": 0.5, "ITALY": 0.4},
        "F1903M": {"GERMANY": 0.5, "ITALY": 0.4},
        "S1904M": {"GERMANY": 0.8, "ITALY": 0.4},
        "F1904M": {"GERMANY": 0.8, "ITALY": 0.5714285714285714},
        "S1905M": {"GERMANY": 0.8, "ITALY": 0.3333333333333333},
        "F1905M": {"GERMANY": 0.8, "ITALY": 0.3333333333333333},
        "S1906M": {"FRANCE": 0.5, "GERMANY": 0.8, "ITALY": 0.3333333333333333},
        "F1906M": {
            "FRANCE": 0.5,
            "GERMANY": 0.8571428571428571,
            "ITALY": 0.3333333333333333,
        },
        "S1907M": {
            "FRANCE": 0.5,
            "GERMANY": 0.8571428571428571,
            "ITALY": 0.3333333333333333,
        },
        "F1907M": {
            "FRANCE": 0.5,
            "GERMANY": 0.8571428571428571,
            "ITALY": 0.3333333333333333,
        },
        "S1908M": {
            "FRANCE": 0.5,
            "GERMANY": 0.8571428571428571,
            "ITALY": 0.5714285714285714,
        },
    },
    "AIGame_13": {
        "S1901M": {"TURKEY": 0.6666666666666666},
        "F1901M": {"GERMANY": 1.0, "TURKEY": 0.8571428571428571},
        "S1902M": {"GERMANY": 1.0, "TURKEY": 0.8888888888888888},
        "F1902M": {"GERMANY": 0.75, "TURKEY": 0.8888888888888888},
        "S1903M": {"GERMANY": 0.75, "TURKEY": 0.8888888888888888},
        "F1903M": {"GERMANY": 0.75, "TURKEY": 0.8888888888888888},
        "S1904M": {"GERMANY": 0.5714285714285714, "TURKEY": 0.8},
        "F1904M": {"GERMANY": 0.5714285714285714, "TURKEY": 0.8},
        "S1905M": {"GERMANY": 0.75, "TURKEY": 0.8},
        "F1905M": {"GERMANY": 0.75, "TURKEY": 0.8},
        "S1906M": {"GERMANY": 0.8571428571428571, "TURKEY": 0.8},
        "F1906M": {"GERMANY": 0.8571428571428571, "TURKEY": 0.8},
        "S1907M": {"GERMANY": 0.8571428571428571, "TURKEY": 0.8},
        "F1907M": {"GERMANY": 0.8571428571428571, "TURKEY": 0.8},
        "S1908M": {"TURKEY": 0.8, "GERMANY": 0.8571428571428571},
    },
    "AIGame_14": {
        "S1901M": {},
        "F1901M": {"TURKEY": 0.5714285714285714},
        "S1902M": {"TURKEY": 0.75},
        "F1902M": {"RUSSIA": 0.5714285714285714, "TURKEY": 0.75},
        "S1903M": {"RUSSIA": 0.6666666666666666, "TURKEY": 0.75},
        "F1903M": {"RUSSIA": 0.6666666666666666, "TURKEY": 0.8888888888888888},
        "S1904M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "F1904M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "S1905M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "F1905M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "S1906M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "F1906M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "S1907M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "F1907M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "S1908M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "F1908M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
        "S1909M": {"RUSSIA": 0.8, "TURKEY": 0.8888888888888888},
    },
    "AIGame_15": {
        "S1901M": {"FRANCE": 1.0, "GERMANY": 0.75},
        "F1901M": {"FRANCE": 1.0, "GERMANY": 0.75},
        "S1902M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1902M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1903M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1903M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1904M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1904M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1905M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1905M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1906M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1906M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1907M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1907M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1908M": {"GERMANY": 1.0, "FRANCE": 1.0},
    },
    "AIGame_16": {
        "S1901M": {"TURKEY": 0.75},
        "F1901M": {"TURKEY": 0.75},
        "S1902M": {"TURKEY": 0.5},
        "F1902M": {"AUSTRIA": 0.3333333333333333, "TURKEY": 0.5},
        "S1903M": {"AUSTRIA": 0.5714285714285714, "TURKEY": 0.6666666666666666},
        "F1903M": {"AUSTRIA": 0.5714285714285714, "TURKEY": 0.6666666666666666},
        "S1904M": {"AUSTRIA": 0.75, "TURKEY": 0.6666666666666666},
        "F1904M": {"AUSTRIA": 0.75, "TURKEY": 0.6666666666666666},
        "S1905M": {"AUSTRIA": 0.75, "TURKEY": 0.5},
        "F1905M": {"AUSTRIA": 0.75, "TURKEY": 0.5},
        "S1906M": {"AUSTRIA": 0.75, "TURKEY": 0.5},
        "F1906M": {"AUSTRIA": 0.75, "TURKEY": 0.5},
        "S1907M": {"AUSTRIA": 0.75, "TURKEY": 0.5},
        "F1907M": {"AUSTRIA": 0.75, "TURKEY": 0.5},
        "S1908M": {"TURKEY": 0.5, "AUSTRIA": 0.75},
    },
    "AIGame_17": {
        "S1901M": {"FRANCE": 1.0, "ITALY": 0.4},
        "F1901M": {"FRANCE": 1.0, "ITALY": 0.0},
        "S1902M": {"AUSTRIA": 0.5, "FRANCE": 1.0, "GERMANY": 0.5, "ITALY": 0.4},
        "F1902M": {
            "AUSTRIA": 0.3333333333333333,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "S1903M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.6666666666666666,
            "ITALY": 0.8571428571428571,
        },
        "F1903M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.6666666666666666,
            "ITALY": 0.75,
        },
        "S1904M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "F1904M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "S1905M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "F1905M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "S1906M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "F1906M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "S1907M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "F1907M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
        "S1908M": {
            "AUSTRIA": 0.5,
            "FRANCE": 1.0,
            "GERMANY": 0.8,
            "ITALY": 0.8571428571428571,
        },
    },
    "AIGame_18": {
        "S1901M": {"AUSTRIA": 0.3333333333333333, "GERMANY": 0.5714285714285714},
        "F1901M": {"AUSTRIA": 0.3333333333333333, "GERMANY": 0.5714285714285714},
        "S1902M": {"AUSTRIA": 0.3333333333333333, "GERMANY": 0.5714285714285714},
        "F1902M": {"AUSTRIA": 0.75, "GERMANY": 0.5714285714285714},
        "S1903M": {"AUSTRIA": 0.75, "GERMANY": 0.8888888888888888},
        "F1903M": {"AUSTRIA": 0.75, "GERMANY": 0.8888888888888888},
        "S1904M": {"AUSTRIA": 0.6666666666666666, "GERMANY": 0.8888888888888888},
        "F1904M": {"AUSTRIA": 0.6666666666666666, "GERMANY": 0.8888888888888888},
        "S1905M": {"AUSTRIA": 0.6666666666666666, "GERMANY": 0.8888888888888888},
        "F1905M": {"AUSTRIA": 0.6666666666666666, "GERMANY": 0.8888888888888888},
        "S1906M": {"AUSTRIA": 0.6666666666666666, "GERMANY": 0.8888888888888888},
        "F1906M": {"AUSTRIA": 0.6666666666666666, "GERMANY": 0.8888888888888888},
        "S1907M": {"GERMANY": 0.8888888888888888, "AUSTRIA": 0.6666666666666666},
    },
    "AIGame_19": {
        "S1901M": {"AUSTRIA": 0.75},
        "F1901M": {"AUSTRIA": 0.8888888888888888},
        "S1902M": {"AUSTRIA": 0.8888888888888888, "TURKEY": 0.4},
        "F1902M": {"AUSTRIA": 0.8888888888888888, "TURKEY": 0.4},
        "S1903M": {"AUSTRIA": 0.75, "ITALY": 0.5, "TURKEY": 0.4},
        "F1903M": {
            "AUSTRIA": 0.8888888888888888,
            "ITALY": 0.5,
            "TURKEY": 0.6666666666666666,
        },
        "S1904M": {
            "AUSTRIA": 0.8888888888888888,
            "ITALY": 0.5714285714285714,
            "TURKEY": 0.4,
        },
        "F1904M": {"AUSTRIA": 0.8888888888888888, "ITALY": 0.5, "TURKEY": 0.4},
        "S1905M": {"AUSTRIA": 0.8888888888888888, "ITALY": 0.5, "TURKEY": 0.4},
        "F1905M": {
            "AUSTRIA": 0.8888888888888888,
            "ITALY": 0.6666666666666666,
            "TURKEY": 0.4,
        },
        "S1906M": {
            "AUSTRIA": 0.8888888888888888,
            "ITALY": 0.6666666666666666,
            "TURKEY": 0.4,
        },
        "F1906M": {
            "AUSTRIA": 0.8888888888888888,
            "ITALY": 0.6666666666666666,
            "TURKEY": 0.4,
        },
        "S1907M": {
            "AUSTRIA": 0.8888888888888888,
            "ITALY": 0.6666666666666666,
            "TURKEY": 0.4,
        },
        "F1907M": {
            "AUSTRIA": 0.8888888888888888,
            "ITALY": 0.6666666666666666,
            "TURKEY": 0.4,
        },
        "S1908M": {
            "AUSTRIA": 0.8888888888888888,
            "TURKEY": 0.4,
            "ITALY": 0.6666666666666666,
        },
    },
    "AIGame_2": {
        "S1901M": {"FRANCE": 0.4, "RUSSIA": 0.6666666666666666, "TURKEY": 0.4},
        "F1901M": {
            "FRANCE": 0.4,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.6666666666666666,
        },
        "S1902M": {"FRANCE": 0.4, "RUSSIA": 0.8571428571428571, "TURKEY": 1.0},
        "F1902M": {
            "FRANCE": 0.4,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.5714285714285714,
        },
        "S1903M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.5714285714285714,
        },
        "F1903M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.8888888888888888,
        },
        "S1904M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.8888888888888888,
        },
        "F1904M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.8888888888888888,
        },
        "S1905M": {
            "FRANCE": 1.0,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.8888888888888888,
        },
        "F1905M": {"FRANCE": 1.0, "RUSSIA": 0.8571428571428571, "TURKEY": 1.0},
        "S1906M": {"FRANCE": 1.0, "RUSSIA": 1.0, "TURKEY": 1.0},
    },
    "AIGame_20": {
        "S1901M": {"ENGLAND": 0.4, "TURKEY": 0.0},
        "F1901M": {"ENGLAND": 0.0, "TURKEY": 0.8571428571428571},
        "S1902M": {"ENGLAND": 0.0, "RUSSIA": 0.4, "TURKEY": 0.4},
        "F1902M": {"ENGLAND": 0.0, "RUSSIA": 0.3333333333333333, "TURKEY": 0.4},
        "S1903M": {
            "ENGLAND": 0.4,
            "RUSSIA": 0.6666666666666666,
            "TURKEY": 0.6666666666666666,
        },
        "F1903M": {"ENGLAND": 0.4, "RUSSIA": 0.4, "TURKEY": 0.4},
        "S1904M": {"ENGLAND": 0.6666666666666666, "RUSSIA": 0.4, "TURKEY": 0.4},
        "F1904M": {"ENGLAND": 0.6666666666666666, "RUSSIA": 0.4, "TURKEY": 0.4},
        "S1905M": {
            "ENGLAND": 0.6666666666666666,
            "RUSSIA": 0.6666666666666666,
            "TURKEY": 0.8571428571428571,
        },
        "F1905M": {
            "ENGLAND": 0.6666666666666666,
            "RUSSIA": 0.6666666666666666,
            "TURKEY": 0.8571428571428571,
        },
        "S1906M": {
            "ENGLAND": 0.6666666666666666,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.8571428571428571,
        },
        "F1906M": {
            "ENGLAND": 0.6666666666666666,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 1.0,
        },
        "S1907M": {
            "ENGLAND": 0.6666666666666666,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 1.0,
        },
        "F1907M": {
            "ENGLAND": 0.6666666666666666,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 1.0,
        },
        "S1908M": {
            "ENGLAND": 0.6666666666666666,
            "TURKEY": 1.0,
            "RUSSIA": 0.8571428571428571,
        },
    },
    "AIGame_21": {
        "S1901M": {"ENGLAND": 0.0, "ITALY": 0.5714285714285714},
        "F1901M": {"ENGLAND": 0.0, "ITALY": 0.8888888888888888},
        "S1902M": {"ENGLAND": 0.3333333333333333, "ITALY": 0.8888888888888888},
        "F1902M": {"ENGLAND": 0.0, "ITALY": 0.75},
        "S1903M": {"ENGLAND": 0.0, "ITALY": 0.8888888888888888},
        "F1903M": {"ENGLAND": 0.3333333333333333, "ITALY": 0.8888888888888888},
        "S1904M": {"ENGLAND": 0.3333333333333333, "ITALY": 0.8888888888888888},
        "F1904M": {"ENGLAND": 0.3333333333333333, "ITALY": 0.8888888888888888},
        "S1905M": {"ENGLAND": 0.3333333333333333, "ITALY": 1.0},
        "F1905M": {"ENGLAND": 0.3333333333333333, "ITALY": 1.0},
        "S1906M": {"ENGLAND": 0.3333333333333333, "ITALY": 1.0},
        "F1906M": {"ENGLAND": 0.3333333333333333, "ITALY": 1.0},
        "S1907M": {"ENGLAND": 0.3333333333333333, "ITALY": 1.0},
        "F1907M": {"ENGLAND": 0.3333333333333333, "ITALY": 1.0},
        "S1908M": {"ENGLAND": 0.3333333333333333, "ITALY": 1.0},
        "F1908M": {"ENGLAND": 0.3333333333333333, "ITALY": 1.0},
        "S1909M": {"ITALY": 1.0, "ENGLAND": 0.3333333333333333},
    },
    "AIGame_22": {
        "S1901M": {"ENGLAND": 0.6666666666666666},
        "F1901M": {"ENGLAND": 1.0, "RUSSIA": 0.6666666666666666},
        "S1902M": {"ENGLAND": 1.0, "RUSSIA": 0.6666666666666666},
        "F1902M": {"AUSTRIA": 0.4, "ENGLAND": 1.0, "RUSSIA": 0.6666666666666666},
        "S1903M": {"AUSTRIA": 0.4, "ENGLAND": 1.0, "RUSSIA": 0.6666666666666666},
        "F1903M": {"AUSTRIA": 0.4, "ENGLAND": 1.0, "RUSSIA": 0.6666666666666666},
        "S1904M": {"AUSTRIA": 0.4, "ENGLAND": 1.0, "RUSSIA": 0.4},
        "F1904M": {"AUSTRIA": 0.4, "ENGLAND": 1.0, "RUSSIA": 0.4},
        "S1905M": {"AUSTRIA": 0.4, "ENGLAND": 1.0, "RUSSIA": 0.4},
        "F1905M": {"AUSTRIA": 0.6666666666666666, "ENGLAND": 1.0, "RUSSIA": 0.4},
        "S1906M": {"AUSTRIA": 0.6666666666666666, "ENGLAND": 1.0, "RUSSIA": 0.4},
        "F1906M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "RUSSIA": 0.6666666666666666,
        },
        "S1907M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "RUSSIA": 0.6666666666666666,
        },
        "F1907M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "RUSSIA": 0.8571428571428571,
        },
        "S1908M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "RUSSIA": 0.8571428571428571,
        },
        "F1908M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "RUSSIA": 0.8571428571428571,
        },
        "S1909M": {
            "ENGLAND": 1.0,
            "RUSSIA": 0.8571428571428571,
            "AUSTRIA": 0.6666666666666666,
        },
    },
    "AIGame_23": {
        "S1901M": {"AUSTRIA": 0.6666666666666666, "RUSSIA": 0.6666666666666666},
        "F1901M": {
            "AUSTRIA": 0.6666666666666666,
            "ITALY": 0.5,
            "RUSSIA": 0.8571428571428571,
        },
        "S1902M": {
            "AUSTRIA": 0.6666666666666666,
            "ITALY": 0.5,
            "RUSSIA": 0.8571428571428571,
        },
        "F1902M": {
            "AUSTRIA": 0.6666666666666666,
            "ITALY": 0.5,
            "RUSSIA": 0.8571428571428571,
        },
        "S1903M": {
            "AUSTRIA": 0.6666666666666666,
            "ITALY": 0.5,
            "RUSSIA": 0.8571428571428571,
        },
        "F1903M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.5,
            "RUSSIA": 0.8571428571428571,
        },
        "S1904M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.5,
            "RUSSIA": 0.8571428571428571,
        },
        "F1904M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.8,
            "RUSSIA": 0.8571428571428571,
        },
        "S1905M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.8,
            "RUSSIA": 1.0,
        },
        "F1905M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.8,
            "RUSSIA": 1.0,
        },
        "S1906M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.8,
            "RUSSIA": 1.0,
        },
        "F1906M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.8,
            "RUSSIA": 1.0,
        },
        "S1907M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.8,
            "RUSSIA": 1.0,
        },
        "F1907M": {
            "AUSTRIA": 0.6666666666666666,
            "ENGLAND": 1.0,
            "ITALY": 0.6666666666666666,
            "RUSSIA": 1.0,
        },
        "S1908M": {
            "AUSTRIA": 0.6666666666666666,
            "RUSSIA": 1.0,
            "ITALY": 0.6666666666666666,
            "ENGLAND": 1.0,
        },
    },
    "AIGame_3": {
        "S1901M": {"RUSSIA": 0.4, "TURKEY": 0.6666666666666666},
        "F1901M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 1.0,
            "TURKEY": 0.6666666666666666,
        },
        "S1902M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 1.0,
            "TURKEY": 0.8571428571428571,
        },
        "F1902M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 1.0,
            "TURKEY": 0.8571428571428571,
        },
        "S1903M": {
            "FRANCE": 0.8571428571428571,
            "RUSSIA": 1.0,
            "TURKEY": 0.8571428571428571,
        },
        "F1903M": {
            "FRANCE": 0.8571428571428571,
            "RUSSIA": 1.0,
            "TURKEY": 0.8571428571428571,
        },
        "S1904M": {
            "FRANCE": 0.8571428571428571,
            "RUSSIA": 1.0,
            "TURKEY": 0.8571428571428571,
        },
        "F1904M": {"FRANCE": 1.0, "RUSSIA": 1.0, "TURKEY": 0.8571428571428571},
        "S1905M": {"FRANCE": 1.0, "RUSSIA": 1.0, "TURKEY": 1.0},
        "F1905M": {"FRANCE": 1.0, "RUSSIA": 1.0, "TURKEY": 1.0},
        "S1906M": {"FRANCE": 1.0, "RUSSIA": 1.0, "TURKEY": 1.0},
        "F1906M": {"FRANCE": 1.0, "RUSSIA": 1.0, "TURKEY": 1.0},
        "S1907M": {"TURKEY": 1.0, "RUSSIA": 1.0, "FRANCE": 1.0},
    },
    "AIGame_4": {
        "S1901M": {"FRANCE": 0.6666666666666666},
        "F1901M": {"FRANCE": 0.6666666666666666, "TURKEY": 0.6666666666666666},
        "S1902M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 0.4,
            "TURKEY": 0.6666666666666666,
        },
        "F1902M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 0.0,
            "TURKEY": 0.6666666666666666,
        },
        "S1903M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 0.0,
            "TURKEY": 0.6666666666666666,
        },
        "F1903M": {
            "FRANCE": 0.6666666666666666,
            "RUSSIA": 0.4,
            "TURKEY": 0.6666666666666666,
        },
        "S1904M": {"FRANCE": 1.0, "RUSSIA": 0.4, "TURKEY": 0.6666666666666666},
        "F1904M": {"FRANCE": 1.0, "RUSSIA": 0.4, "TURKEY": 0.6666666666666666},
        "S1905M": {"FRANCE": 1.0, "RUSSIA": 0.4, "TURKEY": 0.8571428571428571},
        "F1905M": {"FRANCE": 1.0, "RUSSIA": 0.4, "TURKEY": 0.8571428571428571},
        "S1906M": {
            "FRANCE": 1.0,
            "RUSSIA": 0.8571428571428571,
            "TURKEY": 0.8571428571428571,
        },
    },
    "AIGame_5": {
        "S1901M": {"FRANCE": 0.75, "TURKEY": 0.4},
        "F1901M": {"ENGLAND": 0.4, "FRANCE": 0.75, "TURKEY": 0.6666666666666666},
        "S1902M": {
            "ENGLAND": 0.8571428571428571,
            "FRANCE": 0.75,
            "TURKEY": 0.6666666666666666,
        },
        "F1902M": {
            "ENGLAND": 0.8571428571428571,
            "FRANCE": 0.75,
            "TURKEY": 0.6666666666666666,
        },
        "S1903M": {
            "ENGLAND": 1.0,
            "FRANCE": 0.5714285714285714,
            "TURKEY": 0.6666666666666666,
        },
        "F1903M": {"ENGLAND": 1.0, "FRANCE": 0.5714285714285714, "TURKEY": 0.75},
        "S1904M": {"ENGLAND": 1.0, "FRANCE": 0.5, "TURKEY": 0.5714285714285714},
        "F1904M": {"ENGLAND": 1.0, "FRANCE": 0.5, "TURKEY": 0.5714285714285714},
        "S1905M": {
            "ENGLAND": 1.0,
            "FRANCE": 0.5714285714285714,
            "TURKEY": 0.5714285714285714,
        },
        "F1905M": {
            "ENGLAND": 1.0,
            "FRANCE": 0.5714285714285714,
            "TURKEY": 0.5714285714285714,
        },
        "S1906M": {
            "ENGLAND": 1.0,
            "FRANCE": 0.3333333333333333,
            "TURKEY": 0.5714285714285714,
        },
        "F1906M": {"ENGLAND": 1.0, "FRANCE": 0.3333333333333333, "TURKEY": 0.75},
        "S1907M": {"ENGLAND": 1.0, "FRANCE": 0.3333333333333333, "TURKEY": 0.75},
    },
    "AIGame_6": {
        "S1901M": {"TURKEY": 0.8888888888888888},
        "F1901M": {"TURKEY": 0.8888888888888888},
        "S1902M": {"TURKEY": 0.8888888888888888},
        "F1902M": {"RUSSIA": 0.5714285714285714, "TURKEY": 0.8888888888888888},
        "S1903M": {"RUSSIA": 0.75, "TURKEY": 0.8888888888888888},
        "F1903M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "S1904M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "F1904M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "S1905M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "F1905M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "S1906M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "F1906M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "S1907M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "F1907M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
        "S1908M": {"RUSSIA": 0.8888888888888888, "TURKEY": 0.8888888888888888},
    },
    "AIGame_7": {
        "S1901M": {"AUSTRIA": 0.8571428571428571, "FRANCE": 0.4, "GERMANY": 0.4},
        "F1901M": {"AUSTRIA": 1.0, "FRANCE": 0.75, "GERMANY": 0.6666666666666666},
        "S1902M": {"AUSTRIA": 1.0, "FRANCE": 0.8888888888888888, "GERMANY": 1.0},
        "F1902M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "S1903M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "F1903M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "S1904M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "F1904M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "S1905M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "F1905M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "S1906M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "F1906M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "S1907M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "F1907M": {"AUSTRIA": 1.0, "FRANCE": 1.0, "GERMANY": 1.0},
        "S1908M": {"FRANCE": 1.0, "AUSTRIA": 1.0, "GERMANY": 1.0},
    },
    "AIGame_8": {
        "S1901M": {"FRANCE": 0.8888888888888888, "GERMANY": 1.0},
        "F1901M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1902M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1902M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1903M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1903M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1904M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1904M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1905M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1905M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1906M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1906M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1907M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "F1907M": {"FRANCE": 1.0, "GERMANY": 1.0},
        "S1908M": {"FRANCE": 1.0, "GERMANY": 1.0},
    },
    "AIGame_9": {
        "S1901M": {"FRANCE": 0.3333333333333333, "TURKEY": 0.5},
        "F1901M": {
            "FRANCE": 0.3333333333333333,
            "GERMANY": 0.5,
            "ITALY": 0.5,
            "TURKEY": 0.5,
        },
        "S1902M": {
            "FRANCE": 0.3333333333333333,
            "GERMANY": 0.5,
            "ITALY": 0.8,
            "TURKEY": 0.5,
        },
        "F1902M": {
            "FRANCE": 0.3333333333333333,
            "GERMANY": 0.5,
            "ITALY": 0.8,
            "TURKEY": 0.5,
        },
        "S1903M": {
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.5,
            "ITALY": 1.0,
            "TURKEY": 0.5,
        },
        "F1903M": {
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.5,
            "ITALY": 1.0,
            "TURKEY": 0.5,
        },
        "S1904M": {
            "FRANCE": 0.6666666666666666,
            "GERMANY": 0.5,
            "ITALY": 1.0,
            "TURKEY": 0.5,
        },
        "F1904M": {"FRANCE": 1.0, "GERMANY": 0.5, "ITALY": 1.0, "TURKEY": 0.5},
        "S1905M": {
            "FRANCE": 1.0,
            "GERMANY": 0.5,
            "ITALY": 1.0,
            "TURKEY": 0.6666666666666666,
        },
        "F1905M": {
            "FRANCE": 1.0,
            "GERMANY": 0.5,
            "ITALY": 1.0,
            "TURKEY": 0.6666666666666666,
        },
        "S1906M": {
            "FRANCE": 1.0,
            "GERMANY": 0.5,
            "ITALY": 1.0,
            "TURKEY": 0.6666666666666666,
        },
        "F1906M": {
            "FRANCE": 1.0,
            "GERMANY": 0.5,
            "ITALY": 1.0,
            "TURKEY": 0.6666666666666666,
        },
        "S1907M": {
            "FRANCE": 1.0,
            "GERMANY": 0.5,
            "ITALY": 1.0,
            "TURKEY": 0.6666666666666666,
        },
    },
}


def get_human_endgame_sc(source):
    human_last_phase = {}

    for game, phases in human_scs.items():
        first_timers = source[game]
        for _, scs in phases.items():
            human_last_phase[game] = {power: scs[power] for power in first_timers}

    total_centers = {}

    for _, scs in human_last_phase.items():
        for power, centers in scs.items():
            if power not in total_centers:
                total_centers[power] = []
            total_centers[power].append(centers)

    for power, centers in sorted(total_centers.items()):
        print(power, sum(centers) / len(centers))


def get_cicero_endgame_sc():
    human_last_phase = {}

    for game, phases in cicero_scs.items():
        for _, scs in phases.items():
            human_last_phase[game] = scs

    total_centers = {}

    for _, scs in human_last_phase.items():
        for power, centers in scs.items():
            if power not in total_centers:
                total_centers[power] = []
            total_centers[power].append(centers)

    print(total_centers)

    for power, centers in sorted(total_centers.items()):
        print(power, sum(centers) / len(centers))


# get_human_endgame_sc(repeated_mapping)


def get_avg_f1(source):
    total_f1 = 0
    count = 0

    for game, info in f1.items():
        target_population = source[game]

        last_phase = list(info.keys())[0]
        for power, f1_scores in info[last_phase].items():
            if power in target_population:
                total_f1 += f1_scores
                count += 1

    print(total_f1 / count)


# get_avg_f1(experienced_dict)


def plot_f1_by_phase():
    human_avg = {}
    first_timer_avg = {}
    repeated_avg = {}

    for game, info in f1.items():
        human = human_dict[game]
        first_timer = first_time_dict[game]
        repeated = repeated_mapping[game]

        for phase, f1_scores in info.items():
            if phase not in human_avg:
                human_avg[phase] = []
            if phase not in first_timer_avg:
                first_timer_avg[phase] = []
            if phase not in repeated_avg:
                repeated_avg[phase] = []

            for power, f1_score in f1_scores.items():
                if power in human:
                    human_avg[phase].append(f1_score)
                if power in first_timer:
                    first_timer_avg[phase].append(f1_score)
                if power in repeated:
                    repeated_avg[phase].append(f1_score)

    print(first_timer_avg)
    human_data = []
    first_timer_data = []
    repeated_data = []
    xlabels = [i[0] + i[3:5] for i in list(human_avg.keys())]

    for phase, f1_scores in human_avg.items():
        human_data.append(sum(f1_scores) / len(f1_scores))
        first_timer_data.append(
            sum(first_timer_avg[phase]) / len(first_timer_avg[phase])
        )
        repeated_data.append(sum(repeated_avg[phase]) / len(repeated_avg[phase]))

    #     plot with points and lines connecting them
    # legends
    ff = (
        ggplot()
        + geom_point(aes(x=range(1, len(human_data) + 1), y=human_data), color="blue")
        + geom_line(
            aes(x=range(1, len(human_data) + 1), y=human_data),
            color="blue",
            linetype="dashed",
        )
        + geom_point(
            aes(x=range(1, len(first_timer_data) + 1), y=first_timer_data), color="red"
        )
        + geom_line(
            aes(x=range(1, len(first_timer_data) + 1), y=first_timer_data), color="red"
        )
        + geom_point(
            aes(x=range(1, len(repeated_data) + 1), y=repeated_data), color="green"
        )
        + geom_line(
            aes(x=range(1, len(repeated_data) + 1), y=repeated_data), color="green"
        )
        # + xlab('Phase')
        # + ylab('F1 Score')
        # + ggtitle('F1 Score by Phase')
        # + scale_x_continuous(breaks=range(1, len(human_data) + 1), labels=xlabels)
        # + scale_color_identity(guide='legend',name=' ',
        #                breaks=['green', 'red','blue'],
        #                labels=['veteran', 'average','first'])
        + theme(dpi=1000)
    )

    fig = ff.draw()
    # save the figure to the file
    fig.savefig("f1_by_phase.png")


# plot_f1_by_phase()

### cicero vs human by phase // 7 powers by phase


def sc_by_phase(powers=None):
    human_avg = {}
    # first_timer_avg = {}
    repeated_avg = {}
    cicero_avg = {}

    for game, info in cicero_scs.items():
        for phase, scs in info.items():
            if phase not in cicero_avg:
                cicero_avg[phase] = []
            for power, centers in scs.items():
                if not powers:
                    cicero_avg[phase].append(centers)
                else:
                    if power in powers:
                        cicero_avg[phase].append(centers)

    for game, info in human_scs.items():
        human = human_dict[game]
        # first_timer = first_time_dict[game]
        repeated = repeated_mapping[game]

        for phase, scs in info.items():
            if phase not in human_avg:
                human_avg[phase] = []
            # if phase not in first_timer_avg:
            # first_timer_avg[phase] = []
            if phase not in repeated_avg:
                repeated_avg[phase] = []

            for power, centers in scs.items():
                if power in human:
                    if not powers:
                        human_avg[phase].append(centers)
                    else:
                        if power in powers:
                            human_avg[phase].append(centers)
                # if power in first_timer:
                # if not powers:
                # first_timer_avg[phase].append(centers)
                # else:
                # if power in powers:
                # first_timer_avg[phase].append(centers)
                if power in repeated:
                    if not powers:
                        repeated_avg[phase].append(centers)
                    else:
                        if power in powers:
                            repeated_avg[phase].append(centers)

    human_data = []
    # first_timer_data = []
    repeated_data = []
    cicero_data = []

    # use matplotlib to plot the data
    for phase, scs in human_avg.items():
        if len(scs) == 0:
            continue
        human_data.append(sum(scs) / len(scs))
        # first_timer_data.append(sum(first_timer_avg[phase]) / len(first_timer_avg[phase]))

    for phase, scs in repeated_avg.items():
        if len(scs) == 0:
            continue
        repeated_data.append(sum(repeated_avg[phase]) / len(repeated_avg[phase]))

    for phase, scs in cicero_avg.items():
        if len(scs) == 0:
            continue
        cicero_data.append(sum(cicero_avg[phase]) / len(cicero_avg[phase]))

    if len(human_data) > 6:
        human_data = human_data[:6]
    human_data = human_data[:6]

    if len(repeated_data) > 6:
        repeated_data = repeated_data[:6]

    if len(cicero_data) > 6:
        cicero_data = cicero_data[:6]

    return human_data, cicero_data


y1s = []
y2s = []
x = []

first_x1, first_x2 = sc_by_phase(['FRANCE'])


y1s += first_x1
y2s += first_x2
x += [1, 2, 3, 4, 5, 6]


for power in ["AUSTRIA", "ENGLAND", "FRANCE", "GERMANY", "ITALY", "RUSSIA", "TURKEY"]:
    human_data, cicero_data = sc_by_phase([power])

    y1s += human_data
    y2s += cicero_data
    x += [1, 2, 3, 4, 5, 6]

categories = ["AVERAGE"] * 6 + ["AUSTRIA"] * 6 + ["ENGLAND"] * 6 + ["FRANCE"] * 6 + ["GERMANY"] * 6 + ["ITALY"] * 6 + ["RUSSIA"] * 6 + ["TURKEY"] * 6


df = pd.DataFrame({"x": x, "y1": y1s, "y2": y2s, "category": categories})


fig = (
    ggplot(df)
    + geom_point(aes(x="x", y="y1", color="'red'"))
    # + geom_line(aes(x="x", y='y1', color="'red'"))
    + geom_smooth(aes(x="x", y="y1", color="'red'"),  method="lm", se=False)
    + geom_point(aes(x="x", y="y2", color="'blue'"))
    # + geom_line(aes(x="x", y='y2', color="'blue'"))
    + geom_smooth(aes(x="x", y="y2", color="'blue'"), method="lm", se=False) #['lm', 'ols', 'wls', 'rlm', 'glm', 'gls', 'lowess', 'loess', 'mavg', 'gpr']
    + facet_wrap(["category"], ncol=2, dir="v")
    + theme(legend_position="none")
    + xlab('Year')
    + ylab('Number of Centers')
    # + ggtitle('F1 Score by Phase')
    + scale_color_identity(guide='legend',name=' ',
                   breaks=['red','blue'],
                   labels=['human', 'cicero'])
    + theme(dpi=1000)
).draw()

# save the figure to the file
fig.savefig("facet.png")

# sc_by_phase()
