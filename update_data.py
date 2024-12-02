import requests
import json
import time
import base64

def fetch_vpn_data():
    url = 'https://www.vpngate.net/api/iphone/'
    response = requests.get(url)
    # 跳过开头的注释行
    lines = response.text.split('\n')[2:]
    servers = []
    
    for line in lines:
        if not line.strip():
            continue
            
        parts = line.split(',')
        if len(parts) < 15:
            continue
            
        try:
            server = {
                'ip': parts[1],
                'score': parts[2],
                'ping': parts[3],
                'speed': parts[4],
                'countryLong': parts[5],
                'countryShort': parts[6],
                'numVpnSessions': parts[7],
                'uptime': parts[8],
                'totalUsers': parts[9],
                'configData': parts[14]  # OpenVPN 配置数据
            }
            servers.append(server)
        except IndexError:
            continue
            
    return servers

def main():
    try:
        servers = fetch_vpn_data()
        timestamp = int(time.time())
        
        data = {
            'timestamp': timestamp,
            'servers': servers
        }
        
        with open('vpn_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
