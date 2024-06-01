import pathlib
from dataclasses import dataclass
import os
import shutil
import wexpect

from game_objects import GameObject

OB3_EDIT_PATH = pathlib.Path(r"C:\Users\verme\Desktop\temp\OB3Editor.exe")
SOURCE_OB3 = r"C:\HWAR\modtest2\Level22\level22 original.ob3"
OB3_WILL_BE_MADE_HERE = r"C:\Users\verme\GIT\hwar\hwar_level_builder"
DEST_OB3 = r"C:\HWAR\modtest2\Level22\level22.ob3"

@dataclass  
class OB3Driver:
      
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
        self.child = wexpect.spawn(str(OB3_EDIT_PATH), timeout=4, maxread=5000)
        # read the welcome message
        self._wait('(Enter absolute or relative path. You can also drag and drop the file)')
        self.child.sendline(ob3_path)
        self._wait('What would you like to do?')
        self.child.sendline("8")
        
    def remove_object(self, id:int):  
        print(f"** REMOVING OBJECT '{id}' **")  
        self.child.sendline("6")
        self._wait("Which object do you want to remove?")
        self.child.sendline(str(id))
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        
    def add_object(self, new_obj_id_in_list:int, x:float, y:float, z:float, team:int=1) -> None:
        print(f"** ADDING NEW OBJECT WITH TYPE '{new_obj_id_in_list}' **")  
        self.child.sendline("4")
        self._wait("Choose an object type, type -1 for custom type")
        if isinstance(new_obj_id_in_list, GameObject):
            new_obj_id_in_list = new_obj_id_in_list.value
        self.child.sendline(str(new_obj_id_in_list))
        # skip weapons 
        self.child.sendline("-1")
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
        self._wait("11. Quit")

         
    def close(self):
        self.child.sendline("7") # save ob3
        self._wait("Press any key to continue . . .")
        self.child.sendline("")
        self._wait("11. Quit")
        self.child.sendline("11") # close  
        

def find_files_ending_with_ob3_in_dir(dir:pathlib.Path) -> list[str]:
    hits = []
    for file in os.listdir(str(dir)):
        if file.endswith(".ob3"):
            hits.append( os.path.join(dir, file))
    return hits

if __name__ == "__main__":
    # find and delete any .ob3 files in the directory
    for f in find_files_ending_with_ob3_in_dir(OB3_WILL_BE_MADE_HERE):
        os.remove(f)
    init_ob3 = []
    try:
        ob3_driver = OB3Driver()
        ob3_driver.launch_ob3(SOURCE_OB3)
        
        # do things 
        while True:
            ob3_driver.remove_object(1) # remove things
            
            
        ob3_driver.remove_object(374) # remove the magpie
        ob3_driver.remove_object(11) # remove the carrier
        ob3_driver.add_object(GameObject.Carrier, 2343.28, 9, 250, team=0)
        ob3_driver.add_object(GameObject.DedicatedLifter, 2343.28, 20, 250, team=0)
        
        
        
        ob3_driver.close()
    except OSError as ex:
        print(f"Ignoring OSError: {ex}")
    # see if new ones created
    new_ob3 = [x for x in find_files_ending_with_ob3_in_dir(OB3_WILL_BE_MADE_HERE) if x not in init_ob3]
    if not new_ob3:
        raise Exception("No new ob3 files created")
    else:
        print(f"New ob3 files created: {new_ob3}")
        # and copy the file from this directory to the PASTE HERE
        print("Copying new ob3 file to destination")
        shutil.copy(new_ob3[0], DEST_OB3) 
        print("Done")
    
    