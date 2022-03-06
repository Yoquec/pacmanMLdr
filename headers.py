"""
Authors: Alvaro Viejo and Alejandro Mayo

File to get the header files
"""
header_vals = {
        "ticks": "NUMERIC",
        "screen_dim_x": "NUMERIC",
        "screen_dim_y": "NUMERIC",
        "pacman_pos_x": "NUMERIC",
        "pacman_pos_y": "NUMERIC",
        "legal_North": "{False, True}",
        "legal_South": "{False, True}",
        "legal_East": "{False, True}",
        "legal_West": "{False, True}",
        "legal_Stop": "{False, True}",
        "pacman_dir": "{East, North, South, Stop, West}",
        "ghost_num": "NUMERIC",
        "ghost1_alive": "{False, True}",
        "ghost2_alive": "{False, True}",
        "ghost3_alive": "{False, True}",
        "ghost4_alive": "{False, True}",
        "ghost1_x": "NUMERIC",
        "ghost1_y": "NUMERIC",
        "ghost2_x": "NUMERIC",
        "ghost2_y": "NUMERIC",
        "ghost3_x": "NUMERIC",
        "ghost3_y": "NUMERIC",
        "ghost4_x": "NUMERIC",
        "ghost4_y": "NUMERIC",
        "ghost1_dir": "{East, North, South, Stop, West, None}",
        "ghost2_dir": "{East, North, South, Stop, West, None}",
        "ghost3_dir": "{East, North, South, Stop, West, None}",
        "ghost4_dir": "{East, North, South, Stop, West, None}",
        "ghost1_dist": "NUMERIC",
        "ghost2_dist": "NUMERIC",
        "ghost3_dist": "NUMERIC",
        "ghost4_dist": "NUMERIC",
        "pacdots_remaining": "NUMERIC",
        "nearestpacdot_dist": "NUMERIC",
        "currentTickScore": "NUMERIC",
        "pacman_action": "{East, North, South, Stop, West, None}",
        "nextTickScore": "NUMERIC"
        }

# CSV_HEADERS = ','.join(header_vals.keys()) + "\n"

def generateArffHeaders(relationName: str) -> str:
    # Create the header with the relation name
    arffHeaders = f"@RELATION {relationName}\n\n"

    # Add the headers with the attributes and their types
    for key, val in zip(header_vals.keys(), header_vals.values()):
        arffHeaders += f"   @ATTRIBUTE {key} {val}\n"

    # Add the start data section header
    arffHeaders += "\n   @data\n"

    return arffHeaders
