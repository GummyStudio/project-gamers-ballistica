
import babase, bascenev1 as bs
from typing import Callable
from ._fighter import Fighter

# Basically the controllers, and sessionplayer or CPU  can take one 
# like melee, brawl or rivals of aether.

# This is just a basic 
class Controller:
    def __init__(self, port: int):
        self.port = port
        self.sessionplayer: bs.SessionPlayer

        # An initialied character.
        self.character: Fighter = None
    
    def assigninput(
        self,
        inputtype: babase.InputType | tuple[babase.InputType, ...],
        call: Callable,
    ) -> None:
       
        return self.sessionplayer.assigninput(type=inputtype, call=call)

    def resetinput(self) -> None:
    
        return self.sessionplayer.resetinput()
    
class CPUSessionPlayer:
    def __init__(self, controller: Controller, level: int = 5):
        self.controller = controller
        self.level = level

    def think(self):
        # does thinking about currenct chracter and the opponent
        return
