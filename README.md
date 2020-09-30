# Cisco Viptela vManage Python script

This repo contains a Python script for Cisco Viptela vManage.
Tested on macOS Catalyna.
Python module requirements will be built and defined later. So far - you can use manual module installation.
All outputs (pre-deffined) or you will build - can be saved to csv/txt/json (depends on format).



## Requirements
* Python 3.6+

## Installation

### Creating Python virtual environment

```bash
python3 -m venv env
env/bin/activate
```


### Installation from within repo

```bash
git clone https://github.com/pm7625/viptela_api_functions.git
cd viptela_api_functions

```

## Environment Variables
IP/DNS, port and credentials for the vManage server must be set for the script via environment variable

- export VMANAGE_HOST=vmanage-XYZ.viptela.net
- export VMANAGE_USERNAME=admin
- export VMANAGE_PASSWORD=admin
- export PROXY_STATE=True
- export PROXY_SERVER=http://username:passwd@proxy_ip_or_dns_record:8000
- export API_CALL=dataservice/certificate/vedge/list?api_key=staging

PROXY_STATE=True means proxy is used, the one defined via PROXY_SERVER


### Using the application

Once installed and setup, you can now get started.

Investigate the built-in help with the tool.

`python3 viptela_api_functions.py --help`

OUTPUT

```
python3 viptela_api_functions.py --help      
Usage: viptela_api_functions.py [OPTIONS] COMMAND [ARGS]...

  Command line tool for APIs -  CISCO SDWAN.

  - get-api: get API call and exportin to JSON/txt

  - parsing-json: exported JSON can be parsed based on keys

Options:
  --help  Show this message and exit.

Commands:
  all-devices
  attached-devices
  get-api
  list-templates
  onboarded-devices
  parsing-json
```

Look at the available templates. Each template will provide the number of devices already attached and the template ID.

`python3 viptela_api_functions.py list-tempaltes`

OUTPUT

```
python3 viptela_api_functions.py list-templates
----------------------------------------
Proxy Enabled, proxy State: True
----------------------------------------
╒═════════════════════════════════════════════════════════╤══════════════════╤══════════════════════════════════════╤════════════════════╤════════════════════╕
│ Template Name                                           │ Device Type      │ Template ID                          │   Attached devices │   Template version │
╞═════════════════════════════════════════════════════════╪══════════════════╪══════════════════════════════════════╪════════════════════╪════════════════════╡
│ vSmart                                                  │ vsmart           │ 69ce6af8-e372-41c1-834f-9a2c48c68c1a │                  2 │                  0 │
├─────────────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ LAB_ISR1100_6G_CLI_TEST_MASS_UPDATE                     │ vedge-ISR1100-6G │ 14ed1c42-fa46-4f54-9a20-b98a0dcb38de │                  0 │                  0 │
├─────────────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤
│ LAB_ISR1100_6G                                          │ vedge-ISR1100-6G │ f4afd73a-203b-4d52-8050-10208d88e918 │                  0 │                  0 │
├─────────────────────────────────────────────────────────┼──────────────────┼──────────────────────────────────────┼────────────────────┼────────────────────┤

```
Look what device is attached to template you define by template ID.
Template ID you can fine above ....

`python3 viptela_api_functions.py attached-devices --template 69ce6af8-e372-41c1-834f-9a2c48c68c1a`

OUTPUT

```
python3 viptela_api_functions.py attached-devices --template 69ce6af8-e372-41c1-834f-9a2c48c68c1a
----------------------------------------
Proxy Enabled, proxy State: True
----------------------------------------
╒════════════════════╤═════════════╤════════════╤══════════════════════════════════════╤═════════════╕
│ Host Name          │ Device IP   │    Site ID │ Host ID                              │ Host Type   │
╞════════════════════╪═════════════╪════════════╪══════════════════════════════════════╪═════════════╡
│ vSmart_EU_London   │ 1.1.1.4     │ 4294943322 │ 0ed41cb4-9859-482a-97e8-157d559f3c32 │ vsmart      │
├────────────────────┼─────────────┼────────────┼──────────────────────────────────────┼─────────────┤
│ vSmart_US_Virginia │ 1.1.1.5     │ 4294943321 │ fcde3948-f252-472d-83da-dca9d2cceccd │ vsmart      │
╘════════════════════╧═════════════╧════════════╧══════════════════════════════════════╧═════════════╛

```

Retrieve the list of devices that make up the SD-WAN fabric with python3 viptela_api_functions.py device-list.

`$ python3 viptela_api_functions.py onboarded-devices`

OUTPUT

```
╒════════════════════╤═══════════════╤══════════════════════════════════════╤══════════════╤════════════╤══════════════════╕
│ Host-Name          │ Device Type   │ Device ID                            │ System IP    │    Site ID │ Device Model     │
╞════════════════════╪═══════════════╪══════════════════════════════════════╪══════════════╪════════════╪══════════════════╡
│ vManage_London     │ vmanage       │ c319dcc2-9320-4d8d-b038-773a4bb15b5c │ 1.1.1.6      │ 4294943323 │ vmanage          │
├────────────────────┼───────────────┼──────────────────────────────────────┼──────────────┼────────────┼──────────────────┤
│ vSmart_EU_London   │ vsmart        │ 0ed41cb4-9859-482a-97e8-157d559f3c32 │ 1.1.1.4      │ 4294943322 │ vsmart           │
├────────────────────┼───────────────┼──────────────────────────────────────┼──────────────┼────────────┼──────────────────┤
│ vSmart_US_Virginia │ vsmart        │ fcde3948-f252-472d-83da-dca9d2cceccd │ 1.1.1.5      │ 4294943321 │ vsmart           │
├────────────────────┼───────────────┼──────────────────────────────────────┼──────────────┼────────────┼──────────────────┤
│ VBond_London       │ vbond         │ bbb62bdd-e87c-4f16-9dd2-12501bbfd56d │ 1.1.1.2      │ 4294943327 │ vedge-cloud      │
├────────────────────┼───────────────┼──────────────────────────────────────┼──────────────┼────────────┼──────────────────┤
│ vBond_Virginia     │ vbond         │ 47304062-5f0c-4aa0-9951-ef98d28c1b1e │ 1.1.1.3      │ 4294943326 │ vedge-cloud      │
├────────────────────┼───────────────┼──────────────────────────────────────┼──────────────┼────────────┼──────────────────┤

```
Retrieve any defined API call. If its JSON parsing-json script can be called.
You can save output to file (in case JSON - pretty JSON is saved for future work to get KEYS. If output is not JSON - that one can be saved too.
API which is called is one defined via
- export API_CALL=dataservice/certificate/vedge/list?api_key=staging

`$ python3 viptela_api_functions.py get-api`

OUTPUT

```
python3 viptela_api_functions.py get-api
----------------------------------------
Proxy Enabled, proxy State: True
----------------------------------------
------------------------------------------------------------------------------------------------------------------------
Output is JSON format.
If you want to use parsing-json function, identify keys and define as in bellow example:
export JSON_KEYS="'deviceId', 'site-id', 'host-name', 'local-system-ip'"
------------------------------------------------------------------------------------------------------------------------
Would you like to save output to file? (y/n): y
Enter Filename.....(if not defined, JSON_OUTPUT.txt will be used): JSON_mine.txt
Output writing to JSON_mine.txt file.

```

Parsing output of API specified by API_CALL. Parsin is done based on key defined by
- export JSON_KEYS="'deviceId', 'site-id', 'host-name', 'local-system-ip','version', 'template', 'availableVersions'"
- export API_CALL=dataservice/certificate/vedge/list?api_key=staging

`$ python3 viptela_api_functions.py parsing-json`

OUTPUT

```
 python3 viptela_api_functions.py parsing-json
----------------------------------------
Proxy Enabled, proxy State: True
----------------------------------------
Parsing api call defined by API_CALLs based on keys provided in JSON_KEYS: ('deviceId', 'site-id', 'host-name', 'local-system-ip', 'version', 'template', 'availableVersions')
------------------------------------------------------------------------------------------------------------------------
╒════╤════════════╤════════════╤════════════════════╤═══════════════════╤═══════════╤═════════════════════════════════════════════════╤══════════════════════╕
│    │ deviceId   │ site-id    │ host-name          │ local-system-ip   │ version   │ template                                        │ availableVersions    │
╞════╪════════════╪════════════╪════════════════════╪═══════════════════╪═══════════╪═════════════════════════════════════════════════╪══════════════════════╡
│  0 │ N/A        │ 1          │ HOSTNAME1          │ 10.255.255.1      │ 19.2.3    │ ST5_WAN1                                        │ ['19.2.2']           │
├────┼────────────┼────────────┼────────────────────┼───────────────────┼───────────┼─────────────────────────────────────────────────┼──────────────────────┤
│  1 │ N/A        │ 2          │ HOSTNAME2          │ 10.255.255.2      │ 19.2.3    │ ST5_WAN2                                        │ ['19.2.2']           │
├────┼────────────┼────────────┼────────────────────┼───────────────────┼───────────┼─────────────────────────────────────────────────┼──────────────────────┤
│  2 │ N/A        │ 3          │ HOSTNAME3          │ 10.255.255.3      │ N/A       │ N/A                                             │ []                   │
├────┼────────────┼────────────┼────────────────────┼───────────────────┼───────────┼─────────────────────────────────────────────────┼──────────────────────┤
│  3 │ N/A        │ 4          │ HOSTNAME4          │ 10.255.255.4      │ N/A       │ N/A                                             │ []                   │
├────┼────────────┼────────────┼────────────────────┼───────────────────┼───────────┼─────────────────────────────────────────────────┼──────────────────────┤


You may say you want to get just these ...
export JSON_KEYS="'site-id', 'host-name', 'local-system-ip','version'"

Outpul will be different:
------
Proxy Enabled, proxy State: True
----------------------------------------
Parsing api call defined by API_CALLs based on keys provided in JSON_KEYS: ('site-id', 'host-name', 'local-system-ip', 'version')
------------------------------------------------------------------------------------------------------------------------
╒════╤════════════╤════════════════════╤═══════════════════╤═══════════╕
│    │ site-id    │ host-name          │ local-system-ip   │ version   │
╞════╪════════════╪════════════════════╪═══════════════════╪═══════════╡
│  0 │ 1          │ HOSTNAME1          │ 10.255.255.1      │ 19.2.3    │
├────┼────────────┼────────────────────┼───────────────────┼───────────┤
│  1 │ 2          │ HOSTNAME2          │ 10.255.255.2      │ 19.2.3    │
├────┼────────────┼────────────────────┼───────────────────┼───────────┤
│  2 │ 3          │ HOSTNAME3          │ 10.255.255.3      │ N/A       │
├────┼────────────┼────────────────────┼───────────────────┼───────────┤
│  3 │ 4          │ HOSTNAME4          │ 10.255.255.4      │ N/A       │


Sure all outputs can be saved. As JSON(api-get) or as CSV(parsing-json). You can name them as you need.


```
