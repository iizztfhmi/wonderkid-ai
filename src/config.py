"""
WonderKid AI
Position Scoring Configuration
"""

POSITION_CONFIG = {

    "ST": {
        "metrics": {
            "Gls": 0.25,
            "xG": 0.20,
            "Sh": 0.15,
            "SoT": 0.15,
            "SCA": 0.10,
            "GCA": 0.15
        }
    },

    "LW": {
        "metrics": {
            "Gls": 0.15,
            "Ast": 0.15,
            "xAG": 0.20,
            "PrgC": 0.20,
            "Succ": 0.15,
            "SCA": 0.15
        }
    },

    "RW": {
        "metrics": {
            "Gls": 0.15,
            "Ast": 0.15,
            "xAG": 0.20,
            "PrgC": 0.20,
            "PrgP": 0.15,
            "SCA": 0.15
        }
    },

    "CAM": {
        "metrics": {
            "Ast": 0.20,
            "xAG": 0.20,
            "KP": 0.20,
            "PrgP": 0.20,
            "GCA": 0.20
        }
    },

    "CM": {
        "metrics": {
            "PrgP": 0.25,
            "PrgC": 0.20,
            "Cmp%": 0.20,
            "KP": 0.15,
            "Carries": 0.20
        }
    },

    "CDM": {
        "metrics": {
            "Tkl": 0.25,
            "Int": 0.25,
            "Blocks": 0.20,
            "Recov": 0.15,
            "Cmp%": 0.15
        }
    },

    "LB": {
        "metrics": {
            "Tkl": 0.20,
            "PrgC": 0.20,
            "PrgP": 0.20,
            "Ast": 0.15,
            "xAG": 0.15,
            "Succ": 0.10
        }
    },

    "RB": {
        "metrics": {
            "Tkl": 0.20,
            "PrgC": 0.20,
            "PrgP": 0.20,
            "Ast": 0.15,
            "xAG": 0.15,
            "Succ": 0.10
        }
    },

    "CB": {
        "metrics": {
            "Tkl": 0.20,
            "Int": 0.20,
            "Clr": 0.20,
            "Blocks": 0.15,
            "Won": 0.15,
            "Tkl+Int": 0.10
        }
    }

}