from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import (
    HP,
    LEFTBORDER,
    RIGHTBORDER,
    LEFTSTART,
    RIGHTSTART,
    PARRYSTUN,
)

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = UppercutSkill
SECONDARY_SKILL = BearTrap

# Constants for easier move return
# Movements
JUMP = ("move", (0, 1))
FORWARD = ("move", (1, 0))
BACK = ("move", (-1, 0))
JUMP_FORWARD = ("move", (1, 1))
JUMP_BACKWARD = ("move", (-1, 1))

# Attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_primary_skill(PRIMARY_SKILL)
SECONDARY = get_secondary_skill(SECONDARY_SKILL)
CANCEL = ("skill_cancel",)

# No move, aka no input
NOMOVE = "NoMove"


# Function to calculate the best move against the opponent
def calculate_best_move(player, enemy, player_projectiles, enemy_projectiles):
    # Calculate distance between the player and the enemy
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

    # If the distance is close, perform an uppercut
    if distance < 2:
        return HEAVY
    # If the distance is moderate, set a bear trap
    elif distance >= 2 and distance < 5:
        return SECONDARY
    # If the distance is far, move towards the enemy
    else:
        return FORWARD


# Bot script class
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL

    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        return calculate_best_move(player, enemy, player_projectiles, enemy_projectiles)
