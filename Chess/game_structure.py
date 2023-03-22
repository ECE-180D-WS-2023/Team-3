import chess
import paho.mqtt.client as mqtt
from chess_speech import speech_to_move

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
            #print("Speak starting square:")
            #start_square = speech_to_move()
            print(start_square)
            try:
                start = chess.parse_square(start_square)
            except:
                print('Not a valid square')
                continue
            end_square = input('Ending square:')
            #print("Speak ending square")
            #end_square = speech_to_move()
            print(end_square)
            try:
                end = chess.parse_square(end_square)
            except:
                print('Not a valid square')
                continue
            try:
                move = board.find_move(start, end)
                if move in board.legal_moves:
                    # if board.king(board.turn) == start and abs(end-start) == 2:
                    #     if end_square[0] == "g":
                    #         rook_start = chess.square_name(end+1)
                    #         rook_end = chess.square_name(end-1)
                    #     else:
                    #         rook_start = chess.square_name(end-2)
                    #         rook_end = chess.square_name(end+1)
                    #     client.publish("ece180d/central", rook_start+rook_end, qos=1)
                    client.publish("ece180d/central", start_square+end_square, qos=1)
                    break
            except:
                if board.is_pinned(board.turn,start):
                    print('Square ' + start_square + ' is pinned to your king!')
                elif board.king(board.turn) == start and board.is_attacked_by(not board.turn, end):
                    print('Cannot move your king into check!')
                else:
                    print('Invalid move try again')

        board.push(move)
    print(board.outcome().result())
    client.loop_stop()
    
if __name__ == '__main__':
    main()
