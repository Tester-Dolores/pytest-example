import yaml
import logging
import time
import hmac
import base64
import hashlib
from locust import events
import Levenshtein as L
from utils.help import *

def get_xunfei_signa():
    api_key = api_data()['xunfei']['api_key']
    app_id = api_data()['xunfei']['app_id']
    ts = str(int(time.time()))
    tt = (app_id + ts).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(tt)
    baseString = md5.hexdigest()
    baseString = bytes(baseString, encoding='utf-8')

    apiKey = api_key.encode('utf-8')
    signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
    signa = base64.b64encode(signa)
    signa = str(signa, 'utf-8')

    return signa,ts,app_id

def api_data():
  with open("./data/apidata.yaml", encoding="UTF-8", errors="ignore") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
  return data


def write_str_file(str,file_name='1.txt'):
	with open("./report/"+file_name,"a+") as foo:
		foo.write(str)
	return file_name


def events_request(status,eventType="",name="", recvText="", total_time=0,e=''):
    if status == "success":
        events.request_success.fire(request_type=eventType,
                                    name=name,
                                    response_time=total_time,
                                    response_length=len(recvText))
    if status == "failed":
        events.request_failure.fire(request_type=eventType,
                                    name=name,
                                    response_time=total_time,
                                    response_length=len(recvText),
                                    exception=e)


class ASREvaluationData:
    def __init__(self) -> None:
        self.sum_distance, self.sum_length = 0, 0
        self.delete_num, self.insert_num, self.replace_num = 0, 0, 0

        self.err_sentence = 0
        self.total_sentence = 0
        self.response_time_list = []
        self.total_time_list = []  # 请求总用时（包含前后处理时间）
        self.result_count = 0  # 没有接收到asr识别结果的句子计数

    def get_rps(self):
        sum_rt, sum_pt = 0, 0
        avg_pt = 0
        length = len(self.response_time_list)  # 按理说两个time长度是一样的
        for i in self.response_time_list:
            sum_rt += i
        for i in self.total_time_list:
            sum_pt += i
        if sum_rt == 0 or length == 0:
            logging.error("接口没有响应？？？ time: {}".format(self.response_time_list))
            sum_rt = 100000
            length = 1000

            return 0, 100000, 100000, 100000, 100000

        avg_rt = sum_rt / length
        avg_pt = sum_pt / length
        self.response_time_list.sort()
        mid = length * (90 / 100)

        if isinstance(mid, int):
            mid_RT = self.response_time_list[mid]
        if isinstance(mid, float):
            index1 = int(str(mid).split(".")[0]) - 2
            index2 = int(str(mid).split(".")[0])
            if index1 < 0:
                index1 = 0
            if index2 > length:
                index2 = length - 1
            mid_RT = (
                self.response_time_list[index1] + self.response_time_list[index2]
            ) / 2

        return (
            min(self.response_time_list),
            max(self.response_time_list),
            avg_rt,
            mid_RT,
            avg_pt,
        )

    def err_count(self, asr_result, feature_text):
        self.total_sentence += 1
        distance = L.distance(asr_result, feature_text)
        self.sum_distance += distance
        if len(feature_text) == 0:
            self.sum_length += 1000000
        self.sum_length += len(feature_text)
        if distance != 0:
            self.err_sentence += 1

        edittops_result = L.editops(asr_result, feature_text)
        for r in edittops_result:
            if "delete" in r:
                self.delete_num += 1
            if "insert" in r:
                self.insert_num += 1
            if "replace" in r:
                self.replace_num += 1
        return self.sum_distance

    def get_cer(self):
        if self.sum_distance == 0:
            return 0
        cer = 100 * self.sum_distance / self.sum_length
        print(
            "cer="
            + str(self.sum_distance)
            + "/"
            + str(self.sum_length)
            + "="
            + str(cer)
        )

        return cer

    def get_wer(self):
        print("WER = ( D + I + S ) / N")
        if self.delete_num + self.insert_num + self.replace_num == 0:
            return 0, 100
        wer = (
            100
            * (self.delete_num + self.insert_num + self.replace_num)
            / self.sum_length
        )
        wrr = (
            100
            * (self.sum_length - self.delete_num - self.replace_num)
            / self.sum_length
        )
        print(
            "wer = ({}+{}+{})/{} = {}".format(
                self.delete_num, self.insert_num, self.replace_num, self.sum_length, wer
            )
        )
        print(
            "wrr = ({}-{}-{})/{} = {}".format(
                self.sum_length, self.delete_num, self.replace_num, self.sum_length, wrr
            )
        )

        return wer, wrr

    def get_ser(self):
        if self.err_sentence == 0:
            return 0
        ser = 100 * self.err_sentence / self.total_sentence
        print("ser = {} / {}".format(self.err_sentence, self.total_sentence))
        return ser

    def output(self, company_name, direction):

        cer = self.get_cer()
        wer, wrr = self.get_wer()
        ser = self.get_ser()
        min_RT, max_RT, avg_RT, mid_RT, avg_PT = self.get_rps()
        logging.info("RT TOTAL:\n{}\n".format(self.response_time_list))
        result = (
            "# 测试时间: {}\n\n|公司|测试集|CER| WER|WRR|SER|"
            "err_count|total_count|sentence_count|result_count|avg_RT(ms)|90%_RT(ms)|min_RT(ms)|max_RT(ms)|Average_PT(ms)|\n|--|--|--|--|--|\n"
            "|{}|{}|{}%|{}%|{}%|{}%|{}|{}|{}|{}|{}|{}|{}|{}|{}|  \n\n 增加显示响应时间列表：\n```\n{}\n```\n".format(
                time.strftime("%Y-%m-%d %H:%M:%S"),
                company_name,
                direction,
                str(round(cer, 2)),
                str(round(wer, 2)),
                str(round(wrr, 2)),
                str(round(ser, 2)),
                self.sum_distance,
                self.sum_length,
                self.total_sentence,
                self.total_sentence - self.result_count,
                avg_RT,
                mid_RT,
                min_RT,
                max_RT,
                avg_PT,
                self.response_time_list,
            )
        )
        file_name = "./result/asr_result_{}.md".format(company_name)
        with open(file_name, "w") as f:
            f.write(result)
        return file_name, result


def delete_punctuation(str):
    p = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" + "，。、？《》：；“”’{【}】|、·~！@#￥%……&*（）——+=-/"
    for i in str:
        if i in p:
            str = str.replace(i, "")
    return str


def asr_result_log(file_name, asr_result, feature_text):
    """
    记录asr识别结果
    """
    result = "| {} | {} | \n".format(asr_result, feature_text)
    with open(file_name, "a+") as f:
        f.write(result)


def get_right_txt(filename, file_format="txt"):
    """
    获取ASR正确识别结果
    """
    line1 = ""
    asr_audio_path = api_data()["asr_audio_path"]
    asr_format = api_data()["asr_format"]

    # 默认情况为 使用ref.txt作为预期文本存储文档，格式： 文件名 预期结果
    audio_name = filename.split("/")[-1].split(asr_format)[0]
    filename = asr_audio_path + "ref.txt"

    with open(filename, "r", encoding="UTF-8", errors="ignore") as f:
        lines = f.readlines()
        results = {}
        for line in lines:
            results[line.split(" ")[0]] = "".join(
                line.replace("\n", "").split(" ")[1:]
            )
        line1 = delete_punctuation(results[audio_name])
    return line1
