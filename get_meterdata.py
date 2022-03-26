import json
import requests
import datetime
import var.variable as variable

# 実行時刻を取得
now = datetime.datetime.now()

# アクセストークンをリクエストヘッダーに設定
header = {"Authorization": variable.token}

# 登録されている全デバイスを取得
response = requests.get("https://api.switch-bot.com/v1.0/devices", headers=header)
devices = json.loads(response.text)

# クラウドサービスが有効な温湿度計のデバイスIDを抽出
meterdevices = []
for device in devices["body"]["deviceList"]:
    if device["deviceType"] == "Meter" and device["enableCloudService"]:
        meterdevices.append(device["deviceId"])

# 全温湿度計に対してデータを取得
for deviceid in meterdevices:
    # デバイスの最新のステータスを取得
    url = "https://api.switch-bot.com/v1.0/devices/"+ deviceid +"/status"
    response = requests.get(url, headers=header)

    # 取得したjsonデータに実行時刻のデータを付与
    response_dict = json.loads(response.text)
    response_dict["date"] = str(now)
    
    # デバイスIDでファイル名を生成
    filename = variable.dir_path + deviceid + ".json"
    # JSON形式でファイル出力
    with open(filename, 'a') as f :
        json.dump(response_dict, f, ensure_ascii = False)
        f.write('\n')
