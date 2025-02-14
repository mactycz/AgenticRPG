class Character():

    def __init__(self, name, max_hp, stats, current_hp=None):
        self.name = name 
        self.max_hp = max_hp
        self.stats = stats
        self.current_hp = max_hp if current_hp is None  else current_hp

        if self.current_hp>self.max_hp: self.current_hp=self.max_hp
        if self.current_hp<=0: self.current_hp = 0
    
    def take_damage(self,damage):
        self.current_hp-=damage
        if self.current_hp<=0: self.current_hp = 0
    def is_alive(self):
        return self.current_hp>0
    