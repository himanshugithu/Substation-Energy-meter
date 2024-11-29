import requests
import json
from blink import blink
DEV_CREDENTIALS = {
    'username':"devtest",
    'password':"devtest"
    }
label = ["AE-EM","EM-CR-SB00-02","V2.0.0","EM-V2.0.0"]
def create_cin(uri_cnt, value, cin_labels=label, data_format="json", credentials = DEV_CREDENTIALS):
    """
        Method description:
        Deletes/Unregisters an application entity(AE) from the OneM2M framework/tree
        under the specified CSE
        Parameters:
        uri_cse : [str] URI of parent CSE
        ae_name : [str] name of the AE
        fmt_ex : [str] payload format
    """
    headers = {
        'X-M2M-Origin': f'{credentials["username"]}:{credentials["password"]}',
        'Content-type': f'application/{data_format};ty=4'
        }
    body = {
        "m2m:cin": {
            "con": "{}".format(value),
            "lbl": cin_labels,
            "cnf": "text"
        }
    }
    try:
        response = requests.post(uri_cnt, json=body, headers=headers)
        if response.status_code == 201:
            print("data sent successfully!")
            blink()
    except TypeError:
        response = requests.post(uri_cnt, data=json.dumps(body), headers=headers)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))



_url = f"http://dev-onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-EM/EM-CR-SB00-02/Data"
if __name__ == "__main__":
    data= "something"
    create_cin(_url ,data)
# data = f"[{int(time.time())}" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "," + "0" + "]"