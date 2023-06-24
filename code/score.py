import pygame

#out of a lack of time and lazyness, I am just going to copy the audio controller to generate a quick score controller.
class ScoreController:
    __instance = None
    
    def __new__(cls):
        if(cls.__instance is None):
            cls.__instance = super(ScoreController, cls).__new__(cls)
            cls.__instance.top_kill_count = 0
            cls.__instance.kill_count = 0
        return cls.__instance
    
    def increase_kill_count(self):
        self.kill_count += 1
    
    def update_top_kill_count(self):
        if self.kill_count > self.top_kill_count:
            self.top_kill_count = self.kill_count
        self.reset_kill_count()
    
    def reset_kill_count(self):
        self.kill_count = 0
    
    def get_kill_count(self):
        return self.kill_count
    
    def get_top_kill_count(self):
        return self.top_kill_count