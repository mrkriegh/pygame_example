import pygame

# Special Singleton class to allow all scripts to access the same instance and allow volume to be updated universally.
class AudioController:
    __instance = None
    
    def __new__(cls):
        if(cls.__instance is None): cls.__instance = super(AudioController, cls).__new__(cls)
        return cls.__instance

    volume = {
        'master': 1,
        'music': 0.5,
        'player_attacks': 0.2,
        'player_spells': 1,
        'monster': 0.6
    }

    def adjust_volume(key, value):
        if(value > 1): value = 1
        elif(value < 0): value = 0

        volume[key] = value
