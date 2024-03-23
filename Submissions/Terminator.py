# bot code goes here
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
import random

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = UppercutSkill
SECONDARY_SKILL = Hadoken

# constants, for easier move return
# movements
JUMP = ("move", (0, 1))
FORWARD = ("move", (1, 0))
BACK = ("move", (-1, 0))
JUMP_FORWARD = ("move", (1, 1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = (SECONDARY,)
moves_iter = iter(moves)


# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL

    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        # Storing character information
        hp_me = get_hp(player)
        hp_enemy = get_hp(enemy)

        my_skills = [get_primary_skill(player), get_secondary_skill(player)]
        enemy_skills = [get_primary_skill(enemy), get_secondary_skill(enemy)]

        proj_type = 0
        proj_distance = 1000000
        if enemy_projectiles:
            proj_type = get_projectile_type(enemy_projectiles[0])
            proj_distance = abs(
                get_pos(player)[0] - get_proj_pos(enemy_projectiles[0])[0]
            )

        is_enemy_blocked = get_block_status(enemy)

        last_move = get_last_move(player)
        enemy_last_move = get_last_move(enemy)

        my_cooldown = [
            primary_on_cooldown(player),
            secondary_on_cooldown(player),
            heavy_on_cooldown(player),
        ]

        enemy_cooldowns = [
            primary_on_cooldown(enemy),
            secondary_on_cooldown(enemy),
            heavy_on_cooldown(enemy),
        ]

        enemy_ranges = [prim_range(enemy), seco_range(enemy)]

        my_ranges = [prim_range(player), seco_range(player)]

        my_recovery = get_recovery(player)

        if proj_type == enemy_skills[0]:
            enemy_proj_range = enemy_ranges[0]
        elif proj_type == enemy_skills[1]:
            enemy_proj_range = enemy_ranges[1]

        # Calculate distance between the player and the enemy
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

        # If the enemy projectile is a Hadoken or Boomerang and it is close enough (<1), then jump
        if (proj_type == Hadoken) or (proj_type == Boomerang):
            if proj_distance < 2:
                return JUMP_FORWARD

        if proj_type == Grenade:
            if (proj_distance <= 3) and (proj_distance >= 2):
                return JUMP_BACKWARD
            elif proj_distance <= 1:
                if (not (my_cooldown[1])) and (distance < 7) and (distance > 2):
                    return SECONDARY
                elif (distance < 2) and (is_enemy_blocked == 0):
                    if not (my_cooldown[0]):
                        return random.choice([PRIMARY, BLOCK, LIGHT, JUMP_BACKWARD])
                    if not (my_cooldown[2]):
                        return random.choice([HEAVY, BLOCK, LIGHT, JUMP_BACKWARD])
                    else:
                        return random.choice([BLOCK, LIGHT, JUMP_BACKWARD])
                elif distance == 2:
                    return random.choice([BLOCK, FORWARD, JUMP_FORWARD, JUMP_BACKWARD])

        if proj_type == BearTrap:
            if proj_distance < 1:
                if not (my_cooldown[0]):
                    return random.choice([JUMP_FORWARD, BLOCK, PRIMARY])
                elif not my_cooldown[2]:
                    return random.choice([JUMP_FORWARD, BLOCK, HEAVY])
                elif not my_cooldown[1]:
                    return random.choice([JUMP_FORWARD, BLOCK, SECONDARY])
                else:
                    return random.choice([JUMP_FORWARD, BLOCK, LIGHT])

        if distance < 2 and (is_enemy_blocked != 0):
            if not (my_cooldown[0]):
                return random.choice(
                    [
                        JUMP_FORWARD,
                        JUMP_BACKWARD,
                        PRIMARY,
                        PRIMARY,
                        PRIMARY,
                        PRIMARY,
                        LIGHT,
                    ]
                )
            elif not (my_cooldown[2]):
                return random.choice(
                    [JUMP_FORWARD, JUMP_BACKWARD, HEAVY, HEAVY, HEAVY, HEAVY, LIGHT]
                )
            else:
                return random.choice([JUMP_FORWARD, JUMP_BACKWARD, LIGHT])
        elif distance < 2 and (is_enemy_blocked == 0):
            if not (my_cooldown[0]):
                return random.choice(
                    [
                        BLOCK,
                        BLOCK,
                        JUMP_FORWARD,
                        JUMP_FORWARD,
                        JUMP_BACKWARD,
                        JUMP_BACKWARD,
                        PRIMARY,
                        PRIMARY,
                        PRIMARY,
                        PRIMARY,
                        LIGHT,
                    ]
                )
            elif not (my_cooldown[2]):
                return random.choice(
                    [
                        BLOCK,
                        BLOCK,
                        JUMP_FORWARD,
                        JUMP_FORWARD,
                        JUMP_BACKWARD,
                        JUMP_BACKWARD,
                        HEAVY,
                        HEAVY,
                        HEAVY,
                        HEAVY,
                        LIGHT,
                    ]
                )
            else:
                return random.choice(
                    [
                        BLOCK,
                        BLOCK,
                        JUMP_FORWARD,
                        JUMP_FORWARD,
                        JUMP_BACKWARD,
                        JUMP_BACKWARD,
                        LIGHT,
                    ]
                )
        elif distance >= 2:
            if not (my_cooldown[1]):
                return random.choice([JUMP_FORWARD, JUMP_BACKWARD, SECONDARY, FORWARD])
            else:
                return random.choice([JUMP_FORWARD, JUMP_BACKWARD, FORWARD])
