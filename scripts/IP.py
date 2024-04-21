import re
import requests
import json
import multiprocessing
import time

class Main:
    def __init__(self, text, regex=None) -> None:
        self.text: str = text
        self.regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        self.API = "6995a9418d5237bc245b093aafd9e516cf318cd70157fe0455274fd3692a412f979093a5b2c547cc"

    def abuseipdb(self, ip) -> dict:
        data = {}
        # Defining the api-endpoint
        url = 'https://api.abuseipdb.com/api/v2/check'

        querystring = {
            'ipAddress': ip,
            'maxAgeInDays': '90'
        }

        headers = {
            'Accept': 'application/json',
            'Key': self.API
        }

        response = requests.request(method='GET', url=url, headers=headers, params=querystring)

        # Formatted output
        decoded_response = json.loads(response.text)
        dr_data = decoded_response.get("data", {})
        data["isPublic"] = str(dr_data.get("isPublic"))
        data["isWhitelisted"] = str(dr_data.get("isWhitelisted"))
        data["Confidence"] = str(dr_data.get("abuseConfidenceScore"))
        data["countryCode"] = str(dr_data.get("countryCode"))
        data["usageType"] = str(dr_data.get("usageType"))
        data["isp"] = str(dr_data.get("isp"))
        data["domain"] = str(dr_data.get("domain"))
        data["hostnames"] = str(dr_data.get("hostnames"))
        data["isTor"] = str(dr_data.get("isTor"))
        data["totalReports"] = str(dr_data.get("totalReports"))
        data["lastReportedAt"] = str(dr_data.get("lastReportedAt"))
        return data        

    def fetch_data_for_ip(self, queue: multiprocessing.Queue, ip) -> dict:
        data = {"IP": ip, "IP2": ip,"I3P": ip,"I4P": ip,"I5P": ip,"IP6": ip,"IP7": ip,"IP8": ip,"I9P": ip,"I00P": ip,"00IP": ip,"I00P": ip,}
        # data = {"IP": ip}
        # ab_report = self.abuseipdb(ip)
        # data |= ab_report
        queue.put(data)

    def run(self):
        # Code here
        matched_ips = re.findall(self.regex, self.text, re.MULTILINE)
        result = []

        start_time = time.perf_counter ()
        queue = multiprocessing.Queue()
        processes: list[multiprocessing.Process] = []
        for ip in matched_ips:
            process = multiprocessing.Process(target=self.fetch_data_for_ip, args=(queue, ip))
            processes.append(process)
            # result.append(self.fetch_data_for_ip(ip))
        
        [x.start() for x in processes]
        [x.join() for x in processes]
        [result.append(queue.get()) for x in processes]
        end_time = time.perf_counter ()
        print(end_time - start_time, "seconds")
        return result