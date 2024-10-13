# strategy.py
import random

class BasicStrategy:
    def decide_action(self, unit, other_units):
        if unit.is_alive:
            enemies = [u for u in other_units if u.role != unit.role and u.is_alive]
            if enemies and unit.position == enemies[0].position:
                return "attack", enemies[0]
            else:
                return "move", self.random_position()

    def random_position(self):
        return (random.randint(1, 10), random.randint(1, 10))

class IntermediateStrategy:
    def decide_action(self, unit, other_units):
        if unit.is_alive and unit.health < 50:
            return "move", self.random_safe_position()  # Retreat if health is low
        enemies = [u for u in other_units if u.role != unit.role and u.is_alive]
        return "move" if not enemies else "attack", enemies[0] if unit.position == enemies[0].position else self.random_position()

    def random_safe_position(self):
        return (random.randint(1, 10), random.randint(1, 10))

class AdvancedStrategy:
    def decide_action(self, unit, other_units):
        enemies = [u for u in other_units if u.role != unit.role and u.is_alive]
        if unit.health < 30:
            return "move", self.random_safe_position()
        if unit.unit_type == "drone":
            return "recon", self.find_enemy_position(enemies)
        elif unit.unit_type == "tank" and unit.is_under_attack():
            return "protect", self.find_weaker_ally(other_units)
        return "attack", enemies[0] if enemies and unit.position == enemies[0].position else self.random_position()

    def random_safe_position(self):
        return (random.randint(10, 15), random.randint(10, 15))

    def find_enemy_position(self, enemies):
        if enemies:
            return enemies[0].position
        return self.random_position()

    def find_weaker_ally(self, allies):
        return min(allies, key=lambda u: u.health) if allies else None
