import sys
import websocket_handler
import asyncio

if __name__ == '__main__':
    #if len(sys.argv) >= 2:
        auth_token = input()
        #auth_token = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(websocket_handler.start(auth_token))
    # else:
    #     print('please provide your auth_token')