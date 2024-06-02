from obj_driver import OB3Driver
from texture_applier import LevEditorDriver   
from csv_read import CsvReader
import os
import shutil

def find_files_ending_with_ob3_in_dir(dir:str) -> list[str]:
    hits = []
    for file in os.listdir(str(dir)):
        if file.endswith(".ob3"):
            hits.append( os.path.join(dir, file))
    return hits

# TODO move to tkinter ---
PATH_TO_OB3Editor = r"C:\Users\verme\Desktop\temp\OB3Editor.exe"
OB3_WILL_BE_MADE_HERE = r"C:\Users\verme\GIT\hwar\hwar_level_builder"
SOURCE_OB3 = r"C:\HWAR\modtest2\Level51\Level51 original.ob3"
DEST_OB3 = r"C:\HWAR\modtest2\Level51\Level51.ob3"
PATH_TO_OBJECTS_CSV = r"C:\Users\verme\GIT\hwar\hwar_level_builder\objects.csv"
#--
MOD_FOLDER = r"C:\HWAR\modtest2\Level51"
LEV_TO_LOAD = r"C:\HWAR\modtest2\Level51\Level51.lev"
OBJ_TO_LOAD = r"C:\HWAR\modtest2\Level51\l6try.obj"
PATH_TO_HW_LEV_EDIT = r"C:\Users\verme\Desktop\temp\HW_LEV_Editor.exe"
PATH_TO_TEXTURES_CSV = r"C:\Users\verme\GIT\hwar\hwar_level_builder\textures.csv"
# end todo



def remake_ob3():
    # find and delete any .ob3 files in the directory
    for f in find_files_ending_with_ob3_in_dir(OB3_WILL_BE_MADE_HERE):
        os.remove(f)
    
    # launch
    ob3_driver = OB3Driver(PATH_TO_OB3Editor)
    ob3_driver.launch_ob3(SOURCE_OB3)
    
    # remove EVERYTHING
    ob3_driver.remove_all_objects()
    
    # read objects from csv
    all_objects = CsvReader(PATH_TO_OBJECTS_CSV).data
    for obj in all_objects:
        ob3_driver.add_object(obj["object_name"],
                              float(obj["x"]), 
                              float(obj["y"]), 
                              float(obj["z"]), 
                              str(obj["weapon"]),
                              int(obj["team"])
                              )
    
    
    # order from blender if X is forward, Y is up  is ... X, Z, Y
    
    # # create a carrier and a dedicated lifter
    # ob3_driver.add_object(GameObject.Carrier, 1950, 0, 476.2, team=Teams.FRIENDLY.value)
    # ob3_driver.add_object(GameObject.DedicatedLifter, 1972, 20, 441, team=Teams.FRIENDLY.value)
    # ob3_driver.add_object(-1, 2354, -2, 464, custom="l2fueltank", team=Teams.RECYCLE.value)
    # ob3_driver.add_object(-1, 2603, 9.5, 542, team=1, custom="l2fueltank")

    ob3_driver.close()
    # see if new ones created
    new_ob3 = [x for x in find_files_ending_with_ob3_in_dir(OB3_WILL_BE_MADE_HERE)]
    if not new_ob3:
        raise Exception("No new ob3 files created")
    else:
        print(f"New ob3 files created: {new_ob3}")
        # and copy the file from this directory to the PASTE HERE
        print("Copying new ob3 file to destination")
        shutil.copy(new_ob3[0], DEST_OB3) 
        print("Done")
    

def remake_lev_and_textures():
    # create a driver
    lev_editor = LevEditorDriver(PATH_TO_HW_LEV_EDIT)
    lev_editor.launch(LEV_TO_LOAD)
    # reload the obj
    lev_editor.apply_obj_file(OBJ_TO_LOAD)
    # read the textures
    all_textures = CsvReader(PATH_TO_TEXTURES_CSV).data
    for texture in all_textures:
        lev_editor.apply_texture(texture["texture_path"], texture["texture_id"])
    
    print("Deleting .aim file")
    # now we need to delete the aim file
    for file in os.listdir(str(MOD_FOLDER)):
        if file.endswith(".aim"):
            print(f"Deleting {file}")
            os.remove(os.path.join(MOD_FOLDER, file))
    # now we need to delete the lev file which is exactly Level51.lev if exists
    print("Deleting .lev file")
    for file in os.listdir(str(MOD_FOLDER)):
        if file.endswith(".lev"):
            if file == "Level51.lev":
                print(f"Deleting {file}")
                os.remove(os.path.join(MOD_FOLDER, file))
    # close
    lev_editor.close()
    print("Done - renaming file")
    # now 
    for file in os.listdir(str(MOD_FOLDER)):
        if file.endswith(".lev") and "NEW" in file:
            print(f"Renaming '{file}' to Level51.lev")
            os.rename(os.path.join(MOD_FOLDER, file), os.path.join(MOD_FOLDER, "Level51.lev"))
    


if __name__ == "__main__":
    # remake_lev_and_textures()
    remake_ob3()
