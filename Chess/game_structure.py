import chess
import paho.mqtt.client as mqtt
from chess_speech import speech_to_move
import chess.engine
import time


def run_game_instance(board: chess.Board, client: mqtt.Client):
    while (not board.is_game_over()):
        while True:
            print(board)
            if board.is_check():
                print("You are in check!")
            print(board.legal_moves)
            start_square = input('Starting square:')
            if start_square == 'q':
                client.publish("ece180d/central/special", start_square, qos=1)
                time.sleep(1)
                exit()
            elif start_square == 'eng':
                #engine = chess.engine.SimpleEngine.popen_uci("D:\Documents\ECE-180DA\\team3\Team-3\Stockfish\stockfish-windows-2022-x86-64-avx2")
                engine = chess.engine.SimpleEngine.popen_uci("C:/Users/neilk/Documents/ECE180/Team3/Team-3/Stockfish/stockfish-windows-2022-x86-64-avx2")
                result = engine.play(board, chess.engine.Limit(time=0.01))
                move = result.move
                client.publish("ece180d/central/move", move.uci(), qos=1)
                engine.quit()
                break

            #print("Speak starting square:")
            #start_square = speech_to_move()
            print("Start square:" + start_square)
            try:
                start = chess.parse_square(start_square)
            except:
                print('Not a valid square')
                continue
            
            make_move = input("Confirm starting square (y/n)?")
            #print("Speak confirmation or view choices (y/n)")
            #make_move = speech_to_move()
            if make_move == 'y':
                end_square = input('Ending square:')
                #print("Speak ending square")
                #end_square = speech_to_move()
                print("End square:" + end_square)
                try:
                    end = chess.parse_square(end_square)
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
    client.loop_stop()


def main(board: chess.Board):

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

    while True:
        run_game_instance(board, client)
        board.reset()
        client.publish("ece180d/central/reset", "test", qos=1)

    
if __name__ == '__main__':
    reset = True
    board = chess.Board()
    main(board)
