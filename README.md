1. pick a source level, your new level will use that level's dimensions. In this example i am using L19 (the behemoth rescue, its called level22 in the game code) which is 256x256. *todo a list of all dimensions*
2. extract the game.mng file using watto game extractor
3. create a copy of the entire folder of the level you want to modify - we will modify the non-copy (the other is a backup)
4. (optional but recommended):
  - modify the `Config\Levels.lst` file and replace the reference to `Level1` near the top of your file with the new level (`Level22` in my example) - this means when we press "New game" we load our new map immediately for testing
  - create a shortcut with the game with the launch args `-setusupthebomb` so we can use cheats (e.g. `invulnerable 1` so we can explore the map without dying
6. inside your chosen level (22 in this example) you'll find a .lev file. open the .lev file using GameDream's HW_LEV_Editor https://github.com/GameDreamSt/HW_LEV_Editor and export the lev file to a .obj
  - select no for textures as there isnt an easy way we have found to re-import them yet.
7. open the .obj with blender and use the sculpt tool to scuplt the map as you want.
  - drag-drop the obj mesh in, you may need to change draw distance by pressing n then "View" (RHS) and increase "End"
  - i use the `scrape` tool with a very large radius and high strength to flatten the entire mesh
  - NOTE - do not add or delete and verticies, or scale the mesh as this can cause import issues
  - NOTE - you might want to resize the mesh to match the map (for example, the mesh in this level was about 2800x2800 but the map expected size seemed to be 10x the value in the .cfg file (2560x2560) -> this makes object location easier later.
8. when happy, use file->export and export as an .obj file without materials (Materials Export tickbox = empty)
9. rename the original .lev file to something like `levelXX original.lev` (where `XX` is `22` in this example) so we can reference the original file as we build from it
10. Open the HW_LEV_Editor again and drag-drop the `levelXX original.lev` file, then select modify terain with obj, then export to .lev
11. Now we're ready to modify .ob3 files. This is done using the python script in this repo (which deletes all objects, then adds them from a csv)
