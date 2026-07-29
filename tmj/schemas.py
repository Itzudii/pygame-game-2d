
from player.model import Player
from items.checkpoints import Start,End,Flag
from items.fruits import Apple
from items.boxs import Box
gid_to_obj = {
        243:Apple,
        244:Box,
        245:Flag,
        246:End,
        247:Player,
        248:Start,
    }

name_to_path = {
            'Terrain (16x16).png':'assets\Terrain\Terrain (16x16).png',
        }