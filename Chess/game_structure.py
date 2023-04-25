import chess
import paho.mqtt.client as mqtt
from chess_speech import speech_to_move
import chess.engine

def main():

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


    
    board = chess.Board()
    while (not board.is_checkmate()):
        while True:
            print(board)
            if board.is_check():
                print("You are in check!")
            print(board.legal_moves)
            start_square = input('Starting square:')
            if start_square == 'q':
                client.publish("ece180d/central/special", start_square, qos=1)
                exit()
            elif start_square == 'eng':
                engine = chess.engine.SimpleEngine.popen_uci("D:\Documents\ECE-180DA\\team3\Team-3\Stockfish\stockfish-windows-2022-x86-64-avx2")
                result = engine.play(board, chess.engine.Limit(time=0.1))
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
            if make_move == 'y':
                end_square = input('Ending square:')
                #print("Speak ending square")
                #end_square = speech_to_move()
                print("End square" + end_square)
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
    
if __name__ == '__main__':
    main()



###
#Use board.pieces with chess.piece_type, and board.turn to get a square set
#From the square set can convert to list and it gives squares where the pieces are at
#Use this to color highlight and potentially can try and find legal moves from that as the 
#starting square somehow and maybe highlight those and if it's a capture can do diff color
#Can also look at the board.peek to get move order and somehow display that.
###

def try_start_piece(board:chess.Board, piece_name:str):
    piece_pos = list(board.pieces(chess.PIECE_NAMES.index(piece_name), board.turn))
