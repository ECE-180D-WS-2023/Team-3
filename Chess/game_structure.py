import chess
import paho.mqtt.client as mqtt
from chess_speech import speech_to_move
from gesture_detector import gesture_cap
import chess.engine
import time

def quit_input(client: mqtt.Client, start_square):
    client.publish("ece180d/central/special", start_square, qos=1)
    time.sleep(1)

def eng_input(client: mqtt.Client):
    engine = chess.engine.SimpleEngine.popen_uci("D:\Documents\ECE-180DA\\team3\Team-3\Stockfish\stockfish-windows-2022-x86-64-avx2")
    #engine = chess.engine.SimpleEngine.popen_uci("C:/Users/neilk/Documents/ECE180/Team3/Team-3/Stockfish/stockfish-windows-2022-x86-64-avx2")
    result = engine.play(board, chess.engine.Limit(time=0.01))
    move = result.move
    client.publish("ece180d/central/move", move.uci(), qos=1)
    engine.quit()
    return move

def run_mate_tutorial(board: chess.Board, client: mqtt.Client):
    p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = False
    phase_list = [p1, p2, p3, p4, p5, p6, p7, p8]

    move_str = ['f2', 'f3', 'e7', 'e5', 'g2', 'g4', 'd8', 'h4']

    print('WELCOME TO WIZARDING CHESS')
    print('TOGETHER WE WILL WALK YOU THROUGH A 4 MOVE CHECKMATE')

    for i in range(8):
        while not phase_list[i]:
            print(f"Speak the starting square ({move_str[i]})")
            start_square = speech_to_move()
            print(f"Recognized word: {start_square}")
            print("Now we want to make sure it was correctly recognized. ")
            print("To confirm raise one finger to the camera otherwise raise 2 fingers.")
            gesture = gesture_cap()
            if gesture == 'y':
                if start_square == move_str[i]:
                    phase_list[i] = True
                    print("Nicely done!")

                    if i%2 == 1:
                        start = chess.parse_square(move_str[i-1])
                        end = chess.parse_square(move_str[i])
                        move = board.find_move(start, end)

                        board.push(move)
                        client.publish("ece180d/central/move", move_str[i-1]+move_str[i], qos=1)

                else:
                    print("Hmmm you confirmed the move but it didn't match what we wanted try again...")
            else:
                print("Let's try again...")
                continue
    board.reset()
    client.publish("ece180d/central/reset", "test", qos=1)
    

def run_game_instance(board: chess.Board, client: mqtt.Client):
    while (not board.is_game_over()):
        while True:
            print(board)
            if board.is_check():
                print("You are in check!")
            print(board.legal_moves)

            start_square = input('Starting square:')
            
            #print("Speak starting square:")
            #start_square = speech_to_move()

            if start_square == 'quit':
                quit_input(client, start_square)
                exit()
            elif start_square == 'engine':
                move = eng_input(client)
                break
            else:
                print("Start square:" + start_square)
                try:
                    start = chess.parse_square(start_square)
                except:
                    print('Not a valid square')
                    continue
            
            make_move = input("Confirm starting square (y/n)? ")
            #print("Gesture to view or proceed with move (1/2) fingers ")
            #make_move = gesture_cap()
            if make_move == 'y':
                client.publish("ece180d/central/start", start_square, qos=1)
                end_square = input('Ending square:')
                #print("Speak ending square")
                #end_square = speech_to_move()
                print("End square:" + end_square)
                client.publish("ece180d/central/stop", start_square, qos=1)
                try:
                    end = chess.parse_square(end_square)
                    confirm_move = input(f"Would you like to make the move {start_square}{end_square} (y/n)? ")
                    if confirm_move == 'n':
                        continue
                except:
                    print('Not a valid square')
                    continue
                try:
                    move = board.find_move(start, end)
                    if move in board.legal_moves:
                        client.publish("ece180d/central/move", start_square+end_square, qos=1)
                        break
                except:
                    if board.is_pinned(board.turn,start):
                        print('Square ' + start_square + ' is pinned to your king!')
                    elif board.king(board.turn) == start and board.is_attacked_by(not board.turn, end):
                        print('Cannot move your king into check!')
                    else:
                        print('Invalid move try again')
            elif make_move =='n':
                client.publish("ece180d/central/view", start_square, qos=1)
            else:
                continue
        board.push(move)
    print(board.outcome().result())


def main(board: chess.Board):
    while True:
        run_game_instance(board, client)
        board.reset()
        client.publish("ece180d/central/reset", "test", qos=1)

    
if __name__ == '__main__':

    def on_connect(client, userdata, flags, rc):
        print("Connection returned result: " + str(rc))

    # The callback of the client when it disconnects.
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print('Unexpected Disconnect')
        else:
            print('Expected Disconnect')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()

    reset = True
    board = chess.Board()

    play_tut = input("Would you like to play the tutorial? (y/n)")
    if play_tut == 'y':
        run_mate_tutorial(board, client)
    main(board)
    client.loop_stop()