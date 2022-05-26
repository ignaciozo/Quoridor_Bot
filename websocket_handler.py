import json
from random import randint
from tkinter.messagebox import NO
import websockets
import time
import game_player


gameplayers_array = []


async def send(websocket, action, data):
    message = json.dumps(
        {
            'action': action,
            'data': data,
        }
    )
    print(message)
    await websocket.send(message)


async def start(auth_token):
    uri = "wss://4yyity02md.execute-api.us-east-1.amazonaws.com/ws?token={}".format(auth_token)
    while True:
        try:
            print('connection to {}'.format(uri))
            async with websockets.connect(uri) as websocket:
                await play(websocket)
        except KeyboardInterrupt:
            print('Exiting...')
            break
        except Exception:
            print('connection error!')
            time.sleep(3)


async def play(websocket):
    global gameplayers_array
    while True:
        
        try:
            request = await websocket.recv()
            print(f"< {request}")
            request_data = json.loads(request)
            if request_data['event'] == 'update_user_list':
                pass
            if request_data['event'] == 'gameover':
                if gameplayers_array:
                    for i in range(len(gameplayers_array)):
                        if request_data['data']['game_id'] == gameplayers_array[i].game_id:
                            gameplayers_array.pop(i)
                pass
            if request_data['event'] == 'challenge':
                if request_data['data']['opponent'] == 'Ignacio':
                    await send(
                        websocket,
                        'accept_challenge',
                        {
                            'challenge_id': request_data['data']['challenge_id'],
                        },
                    )
            if request_data['event'] == 'your_turn':
                game_id = request_data['data']['game_id']
                if  len(gameplayers_array) == 0:    
                    game_id = request_data['data']['game_id']
                    turn_token = request_data['data']['turn_token']
                    side = request_data['data']['side']
                    walls = request_data['data']['walls']
                    player_1 = request_data['data']['player_1']
                    board = request_data['data']['board']
                    remaining_moves = request_data['data']['remaining_moves']
                    gameplayers_array.append(game_player.GamePlayer(game_id, turn_token,side, walls, player_1, board, remaining_moves))
                    await process_your_turn(websocket, request_data, 0)
                else:
                    for i in range (len(gameplayers_array)):
                        if gameplayers_array[i].game_id == game_id:
                            await process_your_turn(websocket, request_data,i)
                        
                    for i in range (len(gameplayers_array)):    
                        if gameplayers_array[i].game_id != game_id and i == len(gameplayers_array):
                            game_id = request_data['data']['game_id']
                            turn_token = request_data['data']['turn_token']
                            side = request_data['data']['side']
                            walls = request_data['data']['walls']
                            player_1 = request_data['data']['player_1']
                            board = request_data['data']['board']
                            remaining_moves = request_data['data']['remaining_moves']
                            gameplayers_array.append(game_player.GamePlayer(game_id, turn_token,side, walls, player_1, board, remaining_moves))
                            await process_your_turn(websocket, request_data,(i+1))

        except KeyboardInterrupt:
            print('Exiting...')
            break
        except Exception as e:
            print('error {}'.format(str(e)))
            break  # force login again


async def process_your_turn(websocket, request_data, i):
    #if randint(0, 4) >= 1:
        await process_move_v2(websocket, request_data, i)
    # else:
    #     await process_wall(websocket, request_data)




async def process_move_v2(websocket, request_data, i):
        #side = request_data['data']['side']
        pawn_board = request_data['data']['board']
        coordinates = gameplayers_array[i].move_piece(pawn_board)
        from_row = int(coordinates[0]) // 2
        from_col = int(coordinates[1]) // 2
        to_row = int(coordinates[2]) // 2
        to_col = int(coordinates[3]) // 2
        #print(request_data['data']['game_id'],request_data['data']['turn_token'])
        await send(
            websocket,
            'move',
            {
                'game_id': request_data['data']['game_id'],
                'turn_token': request_data['data']['turn_token'],
                'from_row': from_row,
                'from_col': from_col,
                'to_row': to_row,
                'to_col': to_col,
            },
        )

async def process_wall(websocket, request_data):
    await send(
        websocket,
        'wall',
        {
            'game_id': request_data['data']['game_id'],
            'turn_token': request_data['data']['turn_token'],
            'row': randint(0, 8),
            'col': randint(0, 8),
            'orientation': 'h' if randint(0, 1) == 0 else 'v'
        },
    )