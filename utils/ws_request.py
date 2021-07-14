import _thread as thread
import base64
import json
import time
import wave
import websocket

from utils.help import api_data,events_request


class WSRequest(object):
    def __init__(self, url, header=None):
        super(WSRequest, self).__init__()
        self.connect_start_time = 0 # 开始连接websocket
        self.receive_start_time = 0 # 发送完音频数据，开始接收数据

        self.speech_path = ''
        self.result_seg = {}
        self.exit_test = False

        # log txt Request.txt记录请求响应结果，asserterror.txt记录asr语音识别不一致结果
        self.file_name=time.strftime("%Y%m%d%H%M%S")+'_Request.txt'
        self.error_file_name=time.strftime("%Y%m%d%H%M%S")+'_asserterror.txt'

        
        self.ws = websocket.WebSocketApp(url,
                               header=header,
                               on_error=self.on_error,
                               on_close=self.on_close,
                               on_ping=self.on_ping,
                               on_pong=self.on_pong)

    def on_ping(self,ws):
        print('===on_ping===')

    def on_pong(self,ws):
        print('===on_pong===')
    

    def on_error(self,ws, error):
        total_time = int((time.time() - self.connect_start_time) * 1000)
        events_request("failed","websocket", "ERROR","ERROR", total_time,e=error)
        print("####### on_error #######")
        print(error)
        # 发生错误时关闭websocket连接
        self.ws.close()

    def on_close(self,ws,status_code,msg):
        total_time = int((time.time() - self.connect_start_time) * 1000)
        events_request("success","websocket", "CLOSE","CLOSE", total_time,e=msg)
        print('\n---------on_close---------\n', time.time(), '\nstatus code:{}\n msg:{}'.format(status_code,msg))


    def read_wav(self, speech_path, mode=1):
        self.speech_path = speech_path
        if mode == 2:
            # huiyan yunzhisheng
            with open(speech_path, mode="rb") as f:
                self.pcm_bytes = f.read(-1)
            return
        with wave.open(speech_path, mode="rb") as f:
            self.pcm_bytes = f.readframes(-1)


    def start(self, on_open=None, on_message=None):
        #websocket.enableTrace(True) 
        self.connect_start_time = time.time()

        http_proxy_host = None
        http_proxy_port = None
        if api_data()['is_use_fiddler']:
          http_proxy_host='localhost'
          http_proxy_port=8888

        print('\n---------start---------\n', self.connect_start_time, '\n')

        self.result_seg = {}
        self.ws.on_open=on_open
        self.ws.on_message=on_message
        self.ws.run_forever(http_proxy_host=http_proxy_host,http_proxy_port=http_proxy_port)
        total_time = int((time.time()-self.connect_start_time)*1000)

        print('\n---------finish---------\nwebsocket 总耗时：\n', (time.time()-self.connect_start_time)*1000, 'ms\n')

        text_seg = [self.result_seg[index]['str'] for index in self.result_seg]
        text = ''.join(text_seg)
        print('---------------\nresult:\n', text)

        return total_time
