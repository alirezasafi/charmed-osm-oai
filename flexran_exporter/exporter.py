import re
import json
import time
import requests
from pydantic import BaseSettings
from prometheus_client.core import Metric, REGISTRY
from prometheus_client import start_http_server


class Settings(BaseSettings):
    flexran_ip: str
    flexran_port: int


def flatten_transfer(input_dict):
    output = {}
    for key, value in input_dict.items():
        if type(value) == dict:
            for inner_key, inner_value in flatten_transfer(value).items():
                output[key+'_'+inner_key] = inner_value
        else:
            output[key] = value
    return output


class FlexRanCollector(object):
    def __init__(self, endpoint):
        self._endpoint = endpoint
        self._suburl = "stats_manager/"

    @staticmethod
    def load_to_json(dirty_str):
        regex_replace = [(r'\*\*(.+?)\*\*', ''), (r"(\w+): (\d+)", r'"\1":\2,'), (r"(\w+): -(\d+)", r'"\1":-\2,'),
                     (r"(\w+): (\w+)", r'"\1":"\2",'), (r"(\w+): \"(\d+)\.(\d+)\.(\d+)\.(\d+)\"", r'"\1":"\2.\3.\4.\5",'), (r"\s+", ""),
                     (r"(\w+){", r'"\1":{'), 
                     (r"(\w+):", r'"\1":'), (r'(\w+)""(\w+)', r'\1","\2'), ("\\x10", ""),
                     (r"(\d+),}", r'\1},'), (r"(\w+)\",}", r'\1"},'), ("},}", "}}"), ("}\"", '},"'),
                     (r'Harqstatus.*', ''), (r'\*\*BS.*splits":\[\]', ''), (r'UEstatistics.*BS', ',"UEstatistics":{')]
        for r, s in regex_replace:
            dirty_str = re.sub(r, s, dirty_str)
        try:
            clean_json = json.loads('{'+dirty_str+'}}')
            return clean_json
        except:
            print("response format error!")
            print(dirty_str)
            return {}

    def collect(self):
        url = f"http://{self._endpoint}/{self._suburl}"
        try:
            response = requests.get(url).content.decode('Utf-8')
            json_result = self.load_to_json(response)
            if len(json_result) != 0:
                UEstats = json_result.pop('UEstatistics')
                BSconf = json_result.copy()
                json_result = {
                    "UEstatistics": UEstats,
                    "BSconf": BSconf
                }
                flattern_result = flatten_transfer(json_result)
                for key, value in flattern_result.items():
                    if type(value) == str:
                        continue
                    metric = Metric(key, key, 'gauge')
                    metric.add_sample(key, value=value, labels={})
                    yield metric
        except requests.exceptions.ConnectionError:
            print("Failed to connect to server:", url)


if __name__ == '__main__':
    settings = Settings()
    start_http_server(int(8000))
    REGISTRY.register(FlexRanCollector(f"{settings.flexran_ip}:{settings.flexran_port}"))
    while True: time.sleep(1)
