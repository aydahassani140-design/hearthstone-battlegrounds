# src/combat_engine.py

import random
import uuid
from copy import deepcopy
from src.models import Minion, Player

class CombatEvent:
    """یک رویداد combat برای لاگ"""
    def __init__(self, kind, source=None, target=None, log=""):
        self.event_uuid = str(uuid.uuid4())
        self.kind = kind
        self.source = source  # {"player_id":..., "slot":..., "instance_id":...}
        self.target = target
        self.log = log

    def to_dict(self):
        return {
            "type": "combat_event",
            "event_uuid": self.event_uuid,
            "payload": {
                "kind": self.kind,
                "source": self.source,
                "target": self.target,
                "log": self.log
            }
        }

class CombatEngine:
    def __init__(self, player1: Player, player2: Player, seed=None):
        self.p1 = deepcopy(player1)
        self.p2 = deepcopy(player2)
        self.events = []
        self.combat_seed = seed or random.randint(0, 999999)
        self.rng = random.Random(self.combat_seed)

        self.p1_board = self.p1.board[:7]
        self.p2_board = self.p2.board[:7]

    def log_event(self, kind, source=None, target=None, log=""):
        evt = CombatEvent(kind, source, target, log)
        self.events.append(evt)
        print(evt.to_dict())  

    def get_first_attacker(self):
        if len(self.p1_board) > len(self.p2_board):
            return self.p1, self.p2
        elif len(self.p2_board) > len(self.p1_board):
            return self.p2, self.p1
        else:
            return (self.p1, self.p2) if self.rng.randint(0,1)==0 else (self.p2, self.p1)

    def perform_combat(self):
        attacker, defender = self.get_first_attacker()

        while self.p1_board and self.p2_board:
            atk_minion = attacker.board[0]

            taunts = [m for m in defender.board if "Taunt" in m.keywords]
            if taunts:
                target = self.rng.choice(taunts)
            else:
                target = self.rng.choice(defender.board)

            self.attack(atk_minion, target, attacker, defender)

            attacker, defender = defender, attacker

        self.calculate_hero_damage()

    def attack(self, attacker: Minion, target: Minion, atk_player: Player, def_player: Player):
        """حمله ساده: همزمان"""
        log_msg = f"{attacker.name} attacks {target.name}"

        if "Divine Shield" in target.keywords:
            target.keywords.remove("Divine Shield")
            log_msg += " (Divine Shield absorbed)"
        else:
            target.health -= attacker.attack

        if "Divine Shield" in attacker.keywords:
            attacker.keywords.remove("Divine Shield")
        else:
            attacker.health -= target.attack

        self.log_event("attack", 
                       source={"player_id": atk_player.name, "slot": 0, "instance_id": id(attacker)},
                       target={"player_id": def_player.name, "slot": 0, "instance_id": id(target)},
                       log=log_msg)

        self.resolve_deaths(atk_player, def_player)

    def resolve_deaths(self, atk_player, def_player):
        for player in [atk_player, def_player]:
            for minion in player.board[:]:
                if minion.health <= 0:
                    self.log_event("death", 
                                   source={"player_id": player.name, "slot": 0, "instance_id": id(minion)},
                                   log=f"{minion.name} dies")
                    player.board.remove(minion)
                    if "Reborn" in minion.keywords:
                        reborn = deepcopy(minion)
                        reborn.health = 1
                        reborn.keywords = [k for k in reborn.keywords if k!="Reborn"]
                        player.board.append(reborn)
                        self.log_event("reborn", 
                                       source={"player_id": player.name, "slot": 0, "instance_id": id(minion)},
                                       log=f"{minion.name} returns with Reborn")

                    if "Deathrattle" in minion.keywords:
                        token = Minion({"name": "Token 1/1", "attack": 1, "health": 1, "keywords":[]})
                        player.board.append(token)
                        self.log_event("deathrattle", 
                                       source={"player_id": player.name, "slot": 0, "instance_id": id(minion)},
                                       log=f"{minion.name} summons {token.name}")

    def calculate_hero_damage(self):
        for player in [self.p1, self.p2]:
            if not player.board: 
                opponent = self.p2 if player==self.p1 else self.p1
                damage = sum([m.attack for m in opponent.board]) + opponent.tavern_tier
                player.hp -= damage
                self.log_event("hero_damage",
                               source={"player_id": opponent.name},
                               target={"player_id": player.name},
                               log=f"{player.name} takes {damage} damage")
