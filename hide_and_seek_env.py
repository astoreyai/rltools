# hide_and_seek_env.py
import gym
from gym_minigrid.minigrid import MiniGridEnv
from strategy import BasicStrategy, IntermediateStrategy, AdvancedStrategy

class Unit:
    def __init__(self, unit_type, role):
        self.unit_type = unit_type  # drone, tank, buggy
        self.role = role  # OFF or DEF
        self.health = 100
        self.mobility = 5
        self.is_alive = True
        self.position = None
        self.strategy = None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
        else:
            self.mobility = max(1, 5 * (self.health / 100))

    def attack(self, target):
        if self.is_alive:
            target.take_damage(20)

class HideSeekEnv(MiniGridEnv):
    def __init__(self, size, units):
        super().__init__(grid_size=size, max_steps=100)
        self.units = units

    def _gen_grid(self, width, height):
        self.grid = self._create_empty_grid(width, height)
        self.place_agents()

    def place_agents(self):
        for unit in self.units.values():
            if unit.is_alive:
                unit.position = self.place_agent()

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)
        self.run_strategies()
        return obs, reward, done, info

    def run_strategies(self):
        for unit in self.units.values():
            if unit.is_alive:
                action, target_or_position = unit.strategy.decide_action(unit, self.units.values())
                self.execute_action(unit, action, target_or_position)

    def execute_action(self, unit, action, target_or_position):
        if action == "move":
            unit.position = target_or_position
        elif action == "attack":
            target = target_or_position
            unit.attack(target)

class HideSeek1v1Env(HideSeekEnv):
    def __init__(self):
        units = {
            "OFF.drone": Unit("drone", "OFF"),
            "DEF.drone": Unit("drone", "DEF")
        }
        # Assign strategies (you can change to Intermediate or Advanced later)
        units["OFF.drone"].strategy = BasicStrategy()
        units["DEF.drone"].strategy = BasicStrategy()
        super().__init__(size=10, units=units)

class HideSeek2v2Env(HideSeekEnv):
    def __init__(self):
        units = {
            "OFF.drone": Unit("drone", "OFF"),
            "OFF.tank": Unit("tank", "OFF"),
            "DEF.drone": Unit("drone", "DEF"),
            "DEF.tank": Unit("tank", "DEF")
        }
        units["OFF.drone"].strategy = IntermediateStrategy()
        units["DEF.drone"].strategy = IntermediateStrategy()
        super().__init__(size=15, units=units)

class HideSeek3v3Env(HideSeekEnv):
    def __init__(self):
        units = {
            "OFF.drone": Unit("drone", "OFF"),
            "OFF.tank": Unit("tank", "OFF"),
            "OFF.buggy": Unit("buggy", "OFF"),
            "DEF.drone": Unit("drone", "DEF"),
            "DEF.tank": Unit("tank", "DEF"),
            "DEF.buggy": Unit("buggy", "DEF")
        }
        units["OFF.drone"].strategy = AdvancedStrategy()
        units["DEF.drone"].strategy = AdvancedStrategy()
        super().__init__(size=20, units=units)
