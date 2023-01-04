import time
import requests
import math
import random

TOKEN = "BBFF-ff1kVAWEmxqKwWVRyayiCY72AdTPMM"  # Put your TOKEN here
DEVICE_LABEL = "sensormevg"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here
VARIABLE_LABEL_3 = "temperature-avg"  # Put your second variable label here


def get_request(variable):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}/{}/values".format(url, DEVICE_LABEL, variable)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.get(url=url, headers=headers)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    print("[INFO] Attemping to send data")
    get_request(VARIABLE_LABEL_1)
    print("[INFO] finished")


if __name__ == '__main__':
    #while (True):
    main()
    #time.sleep(1)