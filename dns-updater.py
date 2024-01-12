import subprocess, re, requests, json

cloudflare_email = '' # Cloudflare Email goes here
cloudflare_token = '' # Get this from the API section of the Cloudflare dash
record_name = '' # The record name e.g. web.example.com
zone_id = '' # Get this in the Cloudflare DNS dash

def get_my_ip():
    shell_out = str(subprocess.check_output('ip -6 a', shell=True))
    regex = re.compile('[a-z\d]{0,4}:[a-z\d]{0,4}:[a-z\d]{0,4}:[a-z\d]{0,4}:[a-z\d]{0,4}:[a-z\d]{0,4}:[a-z\d]{0,4}:[a-z\d]{0,4}')
    return re.search(regex, shell_out).group(0)


def get_record_data(zone_id, record_name, headers):
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records?type=AAAA&name={}'.format(zone_id, record_name)
    result = requests.get(url, headers=headers)
    return json.loads(result.content)['result'][0]

def update_ip():
    payload = '''{{
        "content": "{}",
        "name": "{}",
        "type": "AAAA",
        "ttl": 3600
    }}'''.format(my_ip, record_name)

    change_url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(zone_id, record_id)
    result = requests.put(change_url, headers=headers, data=payload)
    print(vars(json.loads(result.content)['result'][0]))
    return json.loads(result.content)['result'][0]

def main():
    headers = {
            'Content-Type': 'application/json',
            'Authorization': cloudflare_token,
            'X-Auth-Email': cloudflare_email
            #'X-Auth-Key': ''
    }
    my_ip = get_my_ip()
    data = get_record_data(zone_id, record_name, headers)
    print(data)

    record_id = data['id']
    dns_ip = data['content']

    print('Record ID: ' + record_id + '\n'
          'Record value: ' + dns_ip + '\n'
          'Local IP: ' + my_ip)

    if dns_ip != my_ip:
        result = update_ip()

main()
