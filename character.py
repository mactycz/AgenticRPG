import random
class Character():
    BASE_STATS = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    def __init__(self, name, max_hp, stats=None, current_hp=None,backstory=""):
        self.name = name 
        self.max_hp = max_hp
        self.stats = self.BASE_STATS.copy()
        if stats:
            self.stats.update(stats)
        self.current_hp = max_hp if current_hp is None  else current_hp

        if self.current_hp>self.max_hp: self.current_hp=self.max_hp
        if self.current_hp<=0: self.current_hp = 0
        self.backstory = backstory
    
    def take_damage(self, damage):
        self.current_hp-=damage
        if self.current_hp<=0: self.current_hp = 0

    def is_alive(self):
        return self.current_hp>0
    
    @staticmethod
    def roll(dice=20):
        return random.randint(1,dice)
    
    def result(self, stat, required, dice):
        roll_value = Character.roll(dice)
        modifier = (self.stats.get(stat,10)-10)//2
        total = roll_value + modifier
        if roll_value == 1:
            return False
        elif roll_value == 20:
            return True
        else:
            return total >= required

    def get_ui_stats(self):
        return (
            f"{self.current_hp}/{self.max_hp}",
            str(self.stats["STR"]),
            str(self.stats["DEX"]),
            str(self.stats["INT"]),
            str(self.stats["WIS"]),
            str(self.stats["CON"]),
            str(self.stats["CHA"])
        )

    def get_ui_info(self):
        return self.name, f"Main character backstory: {self.backstory}"
    

def create_character(name, backstory, str_val, dex_val, int_val, wis_val, con_val, cha_val, max_hp):
    stats = {
        "STR": int(str_val),
        "DEX": int(dex_val),
        "INT": int(int_val),
        "WIS": int(wis_val),
        "CON": int(con_val),
        "CHA": int(cha_val)
    }
    return Character(name=name, max_hp=int(max_hp), stats=stats,backstory=backstory)