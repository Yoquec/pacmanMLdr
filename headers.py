"""
File to get the header files
"""
header_vals =[
        "ticks",
        "screen_dim_x",
        "screen_dim_y",
        "pacman_pos_x",
        "pacman_pos_y",
        "legal_North",
        "legal_South",
        "legal_East",
        "legal_West",
        "legal_Stop",
        "pacman_dir",
        "ghost_num",
        "ghost1_alive",
        "ghost2_alive",
        "ghost3_alive",
        "ghost4_alive",
        "ghost_pos",
        "ghost_dirs",
        "ghost_dist",
        "pacdots_remaining",
        "nearestpacdot_dist",
        "score"
        ]

HEADERS = ','.join(header_vals) + "\n"
