# Team-3

## WELCOME TO WIZARDING CHESS 
 
### Environments

You need a few environments to run our game. Lucky for you they have been condensed to environment.yml
You can run it on anaconda by first downloading the file, open the location on anaconda, and call this function 

`conda env create -f environment.yml`

Now that the environment is created, activate it by 

`conda activate chessenv`

### Starting The Game
There are a few steps to play the online game. 
1) Download our git page
2) In chess_gui.py, update "self.piece_path" to where you have the Piece_images folder saved within the files downloaded (make sure to use / slashes)
3) In game_structure.py, update "engine = chess.engine.SimpleEngine.popen_uci" to where you have the stockfish folder saved
4) Open your anaconda window (make sure you are in the chessenv) and open the file that the 'chess' folder is saved under
5) Run chess_gui.py (command is: python chess_gui.py)
6) Now open a second anaconda window and repeat step 4
7) Now run game_structure.py  
8) The game will help you learn how to play via the tutorial 


Our current physical board is still under contstruction but we hope you enjoy the online version! 

Please fill out this survey afterwards! 
https://forms.gle/WcFgwhSJwRM4dtgr9
 
