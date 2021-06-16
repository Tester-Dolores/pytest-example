import _thread as thread
import base64
import json
import time
import wave
import websocket

from utils.help import write_str_file,api_data,events_request


class WSRequest(object):
    def __init__(self, url, params):
        super(WSRequest, self).__init__()
        self.connect_start_time = 0 # 开始连接websocket
        self.receive_start_time = 0 # 发送完音频数据，开始接收数据

        self.speech_path = ''
        self.result_seg = {}

        # log txt Request.txt记录请求响应结果，asserterror.txt记录asr语音识别不一致结果
        self.file_name=time.strftime("%Y%m%d%H%M%S")+'_Request.txt'
        self.error_file_name=time.strftime("%Y%m%d%H%M%S")+'_asserterror.txt'
        write_str_file("URL:{}\nParams:{}\n".format(url,str(params)),file_name=self.file_name)

        params = json.dumps(params)
        self.ws = websocket.WebSocketApp(url,
                               header={'accept-header': params},
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close,
                               on_open=self.on_open)


    def on_message(self,ws, message):
        response = json.loads(message)
        temp_result_seg = response['data']
        self.receive_start_time = time.time()
        
        if 'msg' in response:
            if 'id' in temp_result_seg:
                self.result_seg[temp_result_seg['id']]=temp_result_seg
                total_time = int((time.time() - self.receive_start_time) * 1000)
                events_request("success","websocket","on message", result, total_time)
                write_str_file("\nResponse: \n"+str(response)+"\n",file_name=self.speech_path+self.file_name)
            if response['is_exit']:
                write_str_file("=====end====\n",file_name=self.file_name)
                print("尝试关闭")
                ws.close()

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

    def on_open(self,ws):
        # 统计连接服务器时间
        total_time = int((time.time() - self.connect_start_time) * 1000)
        print('\n---------on_open---------\n连接服务器时长：\n', total_time, 'ms\n')
        events_request("success","websocket","CONNECT", result, total_time)
        write_str_file("【"+time.strftime("%Y-%m-%d %H：%M：%S")+"】",file_name=self.speech_path+self.file_name)

        def run(*args):
            # 此次可能需要将wav文件转成binary格式,可参考 https://www.cnblogs.com/Tester_Dolores/p/14786502.html#wav
            message = {'speech_path': speech_path}
            ws.send(json.dumps(message))

        thread.start_new_thread(run, ())

    def start(self, speech_path):
        websocket.enableTrace(True) 
        self.connect_start_time = time.time()
        self.speech_path = speech_path.split("/")[-1]+"_"

        http_proxy_host = None
        http_proxy_port = None
        if api_data()['is_use_fiddler']:
          http_proxy_host='localhost'
          http_proxy_port=8888

        print('\n---------start---------\n', self.connect_start_time, '\n')
        write_str_file("======current request start========\n"+speech_path+"\n",file_name=self.speech_path+self.file_name)

        self.result_seg = {}
        self.ws.run_forever(http_proxy_host=http_proxy_host,http_proxy_port=http_proxy_port)

        print('\n---------finish---------\nwebsocket 总耗时：\n', (time.time()-self.connect_start_time)*1000, 'ms\n')

        text_seg = [self.result_seg[index]['str'] for index in self.result_seg]
        text = ''.join(text_seg)
        print('---------------\nresult:\n', text)
        write_str_file(" \n【send after】下面是self.result_seg数据\n"+text+"\n======current request end========\n\n",file_name=self.speech_path+self.file_name)
        return text
