import pygame

# Special Singleton class to allow all scripts to access the same instance and allow volume to be updated universally.
class AudioController:
    __instance = None
    
    
    def __new__(cls):
        if(cls.__instance is None):
            cls.__instance = super(AudioController, cls).__new__(cls)
            cls.__instance.volume = {
                'master': 1,
                'music': 0.5,
                'player_attacks': 0.2,
                'player_spells': 1,
                'monster': 0.6
            }
        return cls.__instance

    def adjust_volume(self, key, value):
        self.volume[key] += value
        if(self.volume[key] > 1.0): self.volume[key] = 1
        elif(self.volume[key] < 0.0): self.volume[key] = 0

    def get_volume(self, key):
        return self.volume[key]
    
    def get_total_volume(self, key):
        return min(self.volume['master'],self.volume[key])
    
    def get_volume_dict(self):
        return self.volume