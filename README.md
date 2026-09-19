# $\color{green}\Huge{Frogger}$
This game is a simple Frogger, with a simple game mechanic. To beat each level, the frog needs to jump from petal to petal. Without falling into the water or leaving the screen.\
The game was modeled after the original frogger arcarde game and the mobil game Crossy Road. 
The frog and the petals are painted with water colour, then scanned and finally with python animated. 

AI was used for debugging purposes.\
#### $\color{green}\Huge{Photos:}$
<img width="225" height="250" alt="Photo Mainmenu" src="https://github.com/user-attachments/assets/41825e71-3630-4097-b750-615c4d9c2f6e"/>
<img width="225" height="250" alt="Photo Gameplay" src="https://github.com/user-attachments/assets/c60fcc7d-3622-4710-b459-c12c709c41cb"/>
<img width="225" height="250" alt="Photo  You died  screen" src="https://github.com/user-attachments/assets/b5a6e13e-cc71-4329-81e3-3cb9df7bd325"/>

#### $\color{green}\Huge{Sound\ Credits:}$

Music by muri_kuri: [ukulele loop.wav](https://freesound.org/people/muri_kuri/sounds/682461/)\
Sounds from freesound.org: [water_flows_through_crack_in_rocks.wav](https://freesound.org/people/volivieri/sounds/38392/) and [Splash (low fall).mp3](https://freesound.org/people/davidsonfreemedia/sounds/504588/)

---
### $\color{green}\Huge{Installation:}$
For Installation clone the repository and install this:
```
pip install -r requirements.txt
import pygame
from enum import Enum
import math
import random
import time
import pygame.draw
```

#### $\color{green}\Huge{Usage:}$
Start the game with following in your terminal:
```
python frog_game.py
```
Make sure you have access to all files, including the media folder! 

---
### $\color{green}\Huge{Structur:}$
'python frog_game.py' <- This holds the main game function and the gameloop. \
'python frog.py' <- This holds the frog class and all needed constants for it.\
'README.md' <- You are here 
