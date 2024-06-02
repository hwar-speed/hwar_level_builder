import pathlib
from dataclasses import dataclass
import os
import shutil
import wexpect

from game_objects import game_objects
from teams import Teams
from typing import Union

@dataclass  
class OB3Driver:
    
    PATH_TO_OB3Editor:str
      
    def _wait(self, text:str):
        self.child.expect(text, timeout=4)
        print(self.child.before[:500])
        print(self.child.after[:500])
    
    def _wait_exact(self, text:str):
        self.child.expect_exact(text, timeout=4)
        print(self.child.before[:500])
        print(self.child.after[:500])

    def launch_ob3(self, ob3_path: str):
        # Launch the executable as a separate process
        self.child = wexpect.spawn(str(self.PATH_TO_OB3Editor), timeout=4, maxread=5000)
        # read the welcome message
        self._wait('(Enter absolute or relative path. You can also drag and drop the file)')
        self.child.sendline(ob3_path)
        self._wait('What would you like to do?')
        self.child.sendline("8")
        
    def remove_all_objects(self):
        print("** REMOVING ALL OBJECTS **")  
        self.child.sendline("10")
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        
    def remove_object(self, id:int):  
        print(f"** REMOVING OBJECT '{id}' **")  
        self.child.sendline("6")
        self._wait("Which object do you want to remove?")
        self.child.sendline(str(id))
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        
    def add_object(self, object_name:str, x:float, y:float, z:float, weapon:str, team:int=Teams.ENEMY1.value) -> None:
        # GTODO       
        
        # trying a small global y offset
        y += 2

        print(f"** ADDING NEW OBJECT WITH TYPE/ID='{object_name}' **")  
        self.child.sendline("4")
        self._wait("Choose an object type, type -1 for custom type")
        try:
            # this will only work if its a valid int that is in the game_objects dict
            obj_id = int(game_objects.get(object_name, "invalid"))
            self.child.sendline(str(obj_id))
        except ValueError:
            # this is for custom objects
            self.child.sendline("-1")
            self._wait_exact("ok smartypants, what is the object type name?")
            self.child.sendline(object_name)     
        
        # skip weapons 
        self._wait_exact(r"Choose an weapon attachment type, type -1 to skip, -2 for custom type,")
        if not weapon:
            weapon = "-1"
        self.child.sendline(weapon)
        self._wait("x:")
        self.child.sendline(str(x))
        self._wait("y:")
        self.child.sendline(str(y))
        self._wait("z:")
        self.child.sendline(str(z))
        # team number
        self._wait_exact(r"Enter the team number (0 - player, 1 - probably enemy...)")
        self.child.sendline(str(team))
        self._wait_exact(r"Do you want any addons(components/modules)? Y/N")
        self.child.sendline("N")
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        
    def edit_object_location(self, id:int, x:float, y:float, z:float):
        self.child.sendline("5")
        self._wait("Which object do you want to edit?")
        self.child.sendline(str(id))
        self._wait("13. Stop")
        self.child.sendline("3") #change location
        self._wait("x:")
        self.child.sendline(str(x))
        self._wait("y:")
        self.child.sendline(str(y))
        self._wait("z:")
        self.child.sendline(str(z))
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        self._wait("13. Stop")
        self.child.sendline("13") # stop editing this one
        self._wait("12. Quit")

         
    def close(self):
        self.child.sendline("7") # save ob3
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        self._wait("12. Quit")
        self.child.sendline("12") # close  
        