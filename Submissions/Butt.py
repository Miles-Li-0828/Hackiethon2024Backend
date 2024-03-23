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

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
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
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        # Detect my hp
        hp = get_hp(player)
        hp_enermy = get_hp(enemy)
        is_e_startup = skill_cancellable(enemy)
        e_blocking_stat = get_block_status(enemy)

        # Avoid the projectile
        proj_d = 0
        if enemy_projectiles:
            proj_d = abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0])
        if proj_d and proj_d < 2:
            return JUMP

        # Check distacne and make movements
        if distance < 3:
            if is_e_startup:
                return HEAVY
            else:
                return LIGHT

        # Check if enemy is blocked
        # 看我们的技能
        if e_blocking_stat:
            if distance > 3 and distance < 7:
                return SECONDARY
            elif distance < 3:
                return BACK
            elif distance >= 7:
                return FORWARD

        return BACK
