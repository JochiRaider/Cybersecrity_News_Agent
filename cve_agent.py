#!/usr/bin/env python3
import requests

def cve_api_agent() -> list[list[str]]:
    response_object  = requests.get(f'https://services.nvd.nist.gov/rest/json/cves/1.0')
    response_object.raise_for_status()
    cve_json = response_object.json()
    output = []
    for i in range(20):
        id = cve_json['result']['CVE_Items'][i]['cve']['CVE_data_meta']['ID']
        url = cve_json['result']['CVE_Items'][i]['cve']['references']['reference_data'][0]['url']
        desc = cve_json['result']['CVE_Items'][i]['cve']['description']['description_data'][0]['value']
        output.append([id,url,desc])
    output.sort(key=lambda s: -len(s[2]))
    return output
    
def main():
    # test = cve_api_agent()
    # print(test)
    # with open('test_cve.txt','w') as f:
    #     f.write(str(test))
    pass

if __name__=='__main__':
    main()