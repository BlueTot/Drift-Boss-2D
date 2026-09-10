# Drift Boss 2D

**Drift Boss 2D: A modded remake of Drift Boss** is a modded remake of the mathplayground.com game drift boss, but in 2 dimensions only. Check out doc/`docs/DOC.md` to find out how to play. Installation instructions are below.

## Installation

* Install Python3, pygame, tkinter.
* Debian-based Linux instructions: `sudo apt install python3-tk python3-pygame`
* Windows: Download and install python from [here](https://www.python.org/downloads/windows/)
   * Download and install pip
   * Intall pygame using `pip install pygame`
   * _Note: tkinter is included in the python installation_
  
## Running the Game

* Go to **releases** and download the zip file of the latest version
* Unzip it. Windows: click _Extract All_ Linux: `unzip <zipfilename>`
* Run the game: `python3 src/driftboss2d.py`.

## Playing the Game
* To steer, the space bar moves the car right. Release the space bar to straighten out.
* Progress is automatically stored in the gamedata.json file. When you quit the game, your progress will be updated to the file.
* Check the file `doc/DOC.md` to find out more information about how to play.
