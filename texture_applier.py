import pathlib
from dataclasses import dataclass
import os
import shutil
import wexpect

from game_objects import game_objects
from teams import Teams
from typing import Union

@dataclass  
class LevEditorDriver:
    
    PATH_TO_HW_LEV_EDITOR:str
      
    def _wait(self, text:str):
        self.child.expect(text, timeout=4)
        print(self.child.before[:500])
        print(self.child.after[:500])
    
    def _wait_exact(self, text:str):
        self.child.expect_exact(text, timeout=4)
        print(self.child.before[:500])
        print(self.child.after[:500])

    def launch(self, lev_path: str):
        # Launch the executable as a separate process
        self.child = wexpect.spawn(str(self.PATH_TO_HW_LEV_EDITOR), timeout=4, maxread=5000)
        # read the welcome message
        self._wait_exact(r"(Enter absolute or relative path. You can also drag and drop the file)")
        self.child.sendline(lev_path)
        self._wait('12. Quit')
        
    def apply_obj_file(self, obj_path:str):
        self.child.sendline("6")
        self._wait_exact("Drop a file to import the .obj")
        self.child.sendline(obj_path)
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        
    def apply_texture(self, texture_path:str, texture_id:int):
        self.child.sendline("10")
        self._wait_exact("Drop a .tga file (all pixels which are not black #00000 will have their material index updated)")
        self.child.sendline(texture_path)
        self._wait_exact("Specify the material index to apply to non-black parts of the TGA? [0/1/2../254]:")
        self.child.sendline(texture_id)
        self._wait("Press any key to continue . . .")
        self.child.sendline("")       

    def close(self):
        self.child.sendline("1") # export to lev
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        self.child.close()
        