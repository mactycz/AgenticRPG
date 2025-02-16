import random
class Character():


    BASE_STATS = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    def __init__(self, name, max_hp, stats, current_hp=None):
        self.name = name 
        self.max_hp = max_hp
        self.stats = self.BASE_STATS.copy()
        if stats:
            self.stats.update(stats)
        self.current_hp = max_hp if current_hp is None  else current_hp

        if self.current_hp>self.max_hp: self.current_hp=self.max_hp
        if self.current_hp<=0: self.current_hp = 0
    
    def take_damage(self, damage):
        self.current_hp-=damage
        if self.current_hp<=0: self.current_hp = 0

    def is_alive(self):
        return self.current_hp>0
    
    def roll(self, dice=20):
        return random.randint(1,dice)
    
    def result(self, stat, required, dice):
        roll_value = self.roll(dice)
        modifier = (self.stats.get(stat,10)-10)//2
        total = roll_value + modifier
        if roll_value == 1:
            return False
        elif roll_value == 20:
            return True
        else:
            return total >= required

