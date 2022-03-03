# capstone_simulation

## Prereqs:

 - Install freecad https://www.freecadweb.org/
 - Make sure you have python 3.8 installed https://www.python.org/downloads/

## Part 1 (Setting up the workspace): 
 ref: https://wiki.freecadweb.org/Create_a_FeaturePython_object_part_I?fbclid=IwAR2IuU-8pjwPKtxybKVzVR6dMkJQGhRaON8HFrxmRCwhsQAi4Ba7HX2oa0E

 1. find your FreeCad Macro folder
 - On Linux it is usually /home/<username>/.FreeCAD/Macro/.
 - On Windows it is %APPDATA%\FreeCAD\Macro\, which is usually C:\Users\<username>\Appdata\Roaming\FreeCAD\Macro\.      (Appdata is a hidden folder you need to manually enter the path into your file explorer bar)
 - On Mac OSX it is usually /Users/<username>/Library/Preferences/FreeCAD/Macro/.

 2. Navigate to this Macro folder and run
  ```git init```
 then
 ``` git clone https://github.com/ethanbonn/capstone_simulation```
 3. Now you will have the capstone_simulation folder (with all our code) as a sub directory to Macro

## Part 2 (Running Code on FreeCAD):
 1. Configure the views
  - Start FreeCAD (if you haven't done so already).
  - Enable the Report view (View → Panels → Report view).
  - Enable the Python console (View → Panels → Python console) see FreeCAD Scripting Basics.
 2. import modules from our workspace in the python console at the bottom of freecad page
  (ex. ``` from capstone_simulation import surface```)
 
 
 ## Updating code:
 Anytime you've finished some code and you want to publish it here, run these commands:
 
 1. ``` git add .``` then ``` git commit -m "premerge"```
 1. ``` git pull origin main ``` grabs the latest version from this repository
 2. ``` git add .``` again, then ``` git commit -m "<write a message with whatever you changed>" then ``` git push origin main ``` 
 


