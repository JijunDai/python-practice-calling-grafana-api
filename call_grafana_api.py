import requests
from dotenv import dotenv_values
import argparse
from multiprocessing import Process
 
def get_all_notification(config, headers):
    '''returns all alert ids list'''
    url = config["BASE_URL"] + "/api/alert-notifications/lookup"
    try:
        data = requests.get(url, headers=headers).json()
        notify_map = {entry['uid']:entry for entry in data}
    except Exception as e:
        print(type(e), e)
        return None
    return notify_map


def get_all_alerts_id(config, headers):
    '''returns all alert ids list'''
    url = config["BASE_URL"] + "/api/alerts"
    try:
        data = requests.get(url, headers=headers).json()
        id_map = {entry['id']:entry['url'] for entry in data}
    except Exception as e:
        print(type(e), e)
        return None
    return id_map

def mget_alert_notification_by_id(alert_id, config, headers, set_notify_uid, alert_path):
    '''get alert notification by alert id'''
    alert_notify_map = {}
    url = config["BASE_URL"] + "/api/alerts/" + str(alert_id)
    data = requests.get(url, headers=headers).json()
    notify_uid = [item['uid'] for item in data['Settings']['notifications']]
    alert_notify_map = {'id': data['Id'], 'uid': notify_uid, 'name': data['Name'], 'orgid': data['OrgId'], 'panelid': data['PanelId']}
    s = set(alert_notify_map['uid'])
    if set_notify_uid in s:
        print(f"\n- Name: {alert_notify_map['name']}\n{config['BASE_URL']}{alert_path}?viewPanel={alert_notify_map['panelid']}&orgId={alert_notify_map['orgid']}")


def main():

    parser = argparse.ArgumentParser(description="call Grafana APIs",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--notify", action="store_true", help="get all notifications")
    parser.add_argument("-u", "--notify_uid", help="set notification uid")
    args = parser.parse_args()
    args_config = vars(args)

    config = dotenv_values(".env")
    headers = { "Authorization" : "Bearer {}".format(config['GRAFANAID_TOKEN']),
        "Accept" : "application/json",
        "Content-Type" : "application/json"
    }
    
    if args_config['notify']:
        if (all_notify_map := get_all_notification(config, headers)) is None:
            print("Error: invalid API key probably")
            exit(1)
        for value in all_notify_map:
            print(all_notify_map[value])
        exit(0)
            
    if args_config['notify_uid']:
        set_notify_uid = args_config['notify_uid']
    else:
        set_notify_uid = config['OPSGENIE_NOTIFY_UID']

    procs = []

    if (alert_id_map := get_all_alerts_id(config, headers)) is None:
        print("Error: invalid API key probably")
        exit(1)
    
    for alert_id in alert_id_map.keys():
        proc = Process(target=mget_alert_notification_by_id, args=(alert_id,config,headers,set_notify_uid,alert_id_map[alert_id],))
        procs.append(proc)
        proc.start()

    # complete the multi-processes
    for proc in procs:
        proc.join()


if __name__ == "__main__":
    main()
