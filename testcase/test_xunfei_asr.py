import os
import logging
import base64
import json
from utils.help import *
import _thread as thread

class TestXunfeiASR:
    @classmethod
    def setup_class(cls):
        cls.wsreq = None
        cls.chunk_length = 3600
        cls.asr_result = ""
        cls.company_name = "讯飞asr"
        cls.lang_type = ""
        cls.asr_rusult_log_file = "./result/asr_result_log_{}.md".format(
            cls.company_name
        )
        cls.asred = ASREvaluationData()

        cls.lang = api_data()["asr_lang"]
        cls.audio_format = api_data()["asr_format"]
        cls.audio_path = api_data()["asr_audio_path"]
        with open(cls.asr_rusult_log_file, "w") as f:
            f.write("| asr识别结果 | 正确结果 |\n|--|--|\n")

    def set_lang_type(self, lang):
        if lang == "zh":
            self.lang_type = "zh"
        elif lang == "en":
            self.lang_type = "en"
        else:
            self.lang_type = "error"  # 无法识别其他语言，结束测试


    def on_message(self, ws, msg):
        print("\n---------on_message({})---------\n".format(self.company_name))
        total_time = int((time.time() - self.wsreq.receive_start_time) * 1000)
        self.wsreq.count_total_msg_receive_time += total_time
        print("\n[[[{}]]],[[[{}]]]\n".format(self.wsreq.receive_start_time, total_time))
        
        response = json.loads(msg)
        #temp_result_seg = response["result"]
        #print(temp_result_seg)

        # 解析结果
        if response["action"] == "started":
            print("handshake success, result: " + msg)

        if response["action"] == "result":
            result_1 = response
            # result_2 = json.loads(result_1["cn"])
            # result_3 = json.loads(result_2["st"])
            # result_4 = json.loads(result_3["rt"])
            print("rtasr result: " + result_1["data"])

        if response["action"] == "error":
            print("rtasr error: " + msg)
            ws.close()

        self.wsreq.receive_start_time = time.time()
        logging.info(self.asr_result)

    def on_open(self, ws):
        # 统计连接服务器时间
        total_time = int((time.time() - self.wsreq.connect_start_time) * 1000)
        print("\n---------on_open---------\n连接服务器时长：\n", total_time, "ms\n")

        def run(*args):
            while True:
                if self.wsreq.pcm_bytes is not None:
                    if len(self.wsreq.pcm_bytes) > self.chunk_length:
                        speech_chunk = self.wsreq.pcm_bytes[: self.chunk_length]
                        self.wsreq.pcm_bytes = self.wsreq.pcm_bytes[self.chunk_length :]
                        is_final = False
                    else:
                        print("正在发送最后一个片段...")
                        speech_chunk = self.wsreq.pcm_bytes
                        self.wsreq.pcm_bytes = None
                        is_final = True

                    speech_chunk = base64.b64encode(speech_chunk).decode()
                    message = {
                        "samp_rate": api_data()["asr_sample"],
                        "is_final": is_final,
                        "speech_chunk": speech_chunk,
                    }
                    ws.send(json.dumps(message))
                    if is_final:
                        ws.send(bytes("{\"end\": true}".encode('utf-8')))
                else:
                    break

        thread.start_new_thread(run, ())
        self.wsreq.receive_start_time = time.time()

    def starts(self, r, speech_path):
        txt = get_right_txt(speech_path)
        self.wsreq = r
        self.wsreq.count_total_msg_receive_time = 0
        self.set_lang_type(self.lang)
        self.asr_result = ""

        if self.lang_type == "error":
            print("无法识别的语言:{}，结束。".format(self.wsreq.lang))
            return

        self.wsreq.read_wav(speech_path=speech_path, mode=2)
        pt = self.wsreq.start(on_open=self.on_open, on_message=self.on_message)

        key = ""
        if self.asr_result == "":
            key = "【识别结果为空！！】"
        print(
            "【{} Result】\n预期结果：|{}|".format(speech_path, txt),
            "\n实际结果：{}|{}|".format(key, self.asr_result),
        )
        asr_result_log(self.asr_rusult_log_file, self.asr_result, txt)
        if self.asr_result == "":
            self.asred.result_count += 1
        self.asred.err_count(self.asr_result, txt)
        if self.wsreq.count_total_msg_receive_time == 0:
            self.wsreq.count_total_msg_receive_time = pt
        self.asred.response_time_list.append(self.wsreq.count_total_msg_receive_time)
        self.asred.total_time_list.append(pt)

        return self.wsreq.exit_test

    def test_random_audio(self, wsreq):
        count = 0
        total = int(api_data()["num"])
        wav_list = []
        filelist = os.listdir(self.audio_path)
        if len(filelist) < total:
            total = len(filelist)
        for i in range(len(filelist)):
            wav = self.audio_path + filelist[i]
            if total != 0 and count >= total:
                break
            if wav.endswith(self.audio_format) is False:
                continue
            else:
                wav_list.append(wav)
                count += 1
        for i in range(len(wav_list)):
            if wav_list[i].endswith(".pcm"):
                exit_test = self.starts(wsreq, wav_list[i])
                if exit_test:
                    self.wsreq.exit_test = False
                    continue

                print("还有...{}...个文件没发送".format(len(wav_list) - 1 - i))
                time.sleep(1)
            else:
                print("【ERROR】只支持PCM格式文件，请检查传输的音频格式")
                break
        output_file, content = self.asred.output(self.company_name, self.audio_path)
