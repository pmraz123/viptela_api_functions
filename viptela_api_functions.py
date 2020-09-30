#! /usr/bin/env python

import requests
import json
import pprint
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import csv
import pandas
import sys
import click
import tabulate
from tabulate import _table_formats, tabulate
import ast
import re
import numpy as np
#import yaml
#--------------------------------------------------------------------------------------------------
#              LOGIN function to  VMANAGE_HOST
#              proxy state = TRUE - proxy is used
#              for proxy you have to define authnetication to this function. (I'm not going to use username/passwd as input)
#              If you want to share this file - ensure you remove your credentials.
#              proxy state = TRUE - its going directly and is not used
#--------------------------------------------------------------------------------------------------
'''
------------------------
Mandatory:
------------------------
export VMANAGE_HOST=vmanage-XYZ.viptela.net
export VMANAGE_USERNAME=admin
export VMANAGE_PASSWORD=admin
export PROXY_STATE=True
export PROXY_SERVER=http://username:passwd@proxy_ip_or_dns_record:8000
export API_CALL=dataservice/certificate/vedge/list?api_key=staging

------------------------

------------------------
export JSON_KEYS="'deviceId', 'site-id', 'host-name', 'local-system-ip','version','template','availableVersions'"
------------------------
'''

VMANAGE_HOST = os.environ.get("VMANAGE_HOST")
VMANAGE_USERNAME = os.environ.get("VMANAGE_USERNAME")
VMANAGE_PASSWORD = os.environ.get("VMANAGE_PASSWORD")
PROXY_STATE = os.environ.get("PROXY_STATE")
PROXY_SERVER = os.environ.get("PROXY_SERVER")
API_CALL = os.environ.get("API_CALL")
JSON_KEYS = os.environ.get("JSON_KEYS")


if VMANAGE_HOST is None or VMANAGE_USERNAME is None or VMANAGE_PASSWORD is None or PROXY_STATE is None or PROXY_SERVER is None or API_CALL is None:
    print("CISCO SDWAN details must be set via environment variables before running.")
    print("   export VMANAGE_HOST=10.10.30.190")
    print("   export VMANAGE_USERNAME=admin")
    print("   export VMANAGE_PASSWORD=admin")
    print("   export PROXY_STATE=True")
    print("   export PROXY_SERVER=http://username:passwd@proxy_ip_or_dns_record:8000")
    print("   export API_CALL=dataservice/certificate/vedge/list?api_key=staging")
    print("")
    exit("1")

def login():
  base_url = 'https://%s/'%(VMANAGE_HOST)
  login_action = '/j_security_check'
  login_data = {'j_username' : VMANAGE_USERNAME, 'j_password' : VMANAGE_PASSWORD}
  #Format data for loginForm
  #URL for posting login data
  login_url = base_url + login_action
  #URL for retrieving client token
  token_url = base_url + 'dataservice/client/token'
  #cookies + proxy If needed
  http_proxyf = PROXY_SERVER
  if PROXY_STATE == "True":
    os.environ["http_proxy"] = http_proxyf
    os.environ["https_proxy"] = http_proxyf
    print("-" * 40)
    print("Proxy Enabled, proxy State:", PROXY_STATE)
    print("-" * 40)
    sess = requests.session()
  elif PROXY_STATE == "False":
    print("-" * 40)
    print("Proxy Disabled, proxy State:",PROXY_STATE)
    print("-" * 40)
    sess = requests.session()
  #If the  VMANAGE_HOST has a certificate signed by a trusted authority change verify to True
  warnings.simplefilter('ignore',InsecureRequestWarning)
  login_response = sess.post(url=login_url, data=login_data, verify=False)

  if login_response.status_code != 200:
    error_msg("Login Token Failed, probably wrong authentication, url or proxy issue. Status code:",login_response.status_code)
    exit(0)
  elif login_response.status_code == 200:
    login_token = sess.get(url=token_url, verify=False)
    if b'<html>' in login_token.content:
      error_msg("Login Token Failed, probably wrong authentication, url or proxy issue. Status code:",login_response.status_code)
      exit(0)
    else:
      sess.headers['X-XSRF-TOKEN'] = login_token.content
      #print("LOGIN successfull....")
      return (sess,base_url)


#--------------------------------------------------------------------------------------------------
#              function to verify If it is JSON type ?
#--------------------------------------------------------------------------------------------------
def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return myjson, False
  return json_object, True
#--------------------------------------------------------------------------------------------------
#              other  functions
#--------------------------------------------------------------------------------------------------
# error message
def error_msg(error_msg,status_code):
    print('-' * 120)
    print(error_msg,status_code)
    print('-' * 120)
    return
#--------------------------------------------------------------------------------------------------
# get_api_with_outputs
#--------------------------------------------------------------------------------------------------
def get_api_function_outputs():
  (sess,base_url) = login()
  get_api_url = base_url + API_CALL
  #print(get_api_url)
  warnings.simplefilter('ignore',InsecureRequestWarning)
  staging_get_url_json = sess.get(url=get_api_url, verify=False)
  #print(staging_get_url_json.status_code)
  if staging_get_url_json.status_code != 200:
        print('-' * 120)
        print("API you provided is wrong, code is:",staging_get_url_json.status_code)
        print('-' * 120)
        exit(0)

  (get_api_json,is_jason_status) = is_json(staging_get_url_json.content)

  if is_jason_status == True:
    print("-" * 120)
    print("Output is JSON format.")
    print("If you want to use parsing-json function, identify keys and define as in bellow example:")
    print("export JSON_KEYS=\"'deviceId', 'site-id', 'host-name', 'local-system-ip'\"")
    print("-" * 120)
    yes_or_no_output = yes_or_no("Would you like to save output to file?")
    if yes_or_no_output == True:
      try:
        filename = input("Enter Filename.....(if not defined, JSON_OUTPUT.txt will be used): ") or "JSON_OUTPUT.txt"
        is_empty = isNotBlank(filename)
        if is_empty == False:
          print("Writing to NOT_JSON_OUTPUT.txt")
          f = open('JSON_OUTPUT.txt', 'w')
          json_dumps = json.dumps(get_api_json, sort_keys=False, indent=4)
          f.write(json_dumps)
          f.close()
        else:
          print("Output writing to",filename,"file.")
          encoding = 'utf-8'
          #get_api_string = str(get_api_json, encoding)
          f = open(filename, 'w')
          json_dumps = json.dumps(get_api_json, sort_keys=False, indent=4)
          f.write(json_dumps)
          f.close()
      except ValueError:
        print("Incorrect file name.(probably empty string)")
        exit(0)
      else:
        exit(0)
    encoding = 'utf-8'
    json_to_file = json.dumps(get_api_json, sort_keys=False, indent=4)
    f = open('JSON_OUTPUT.txt', 'w')
    f.write(json_to_file)
    f.close()
    return get_api_json
  if is_jason_status == False:
    print("-" * 120)
    print("Output is NOT JSON type  dont use parsing_json_arg function as this is not JSON/dict with keys, it will not work")
    #print("Writing output to ...... NOT_JSON_OUTPUT.txt")
    print("-" * 120)
    encoding = 'utf-8'
    get_api_string = str(get_api_json, encoding)
    yes_or_no_output = yes_or_no("Would you like to save output to file?")
    if yes_or_no_output == True:
      try:
        filename = input("Enter Filename.....(if not defined, NOT_JSON_OUTPUT.txt will be used): ") or "NOT_JSON_OUTPUT.txt"
        is_empty = isNotBlank(filename)
        if is_empty == False:
          print("Writing to NOT_JSON_OUTPUT.txt")
          f = open('NOT_JSON_OUTPUT.txt', 'w')
          f.write(get_api_string)
          f.close()
        else:
          print("Output writing to",filename,"file.")
          encoding = 'utf-8'
          f = open(filename, 'w')
          f.write(get_api_string)
          f.close()
      except ValueError:
        print("Incorrect file name.(probably empty string)")
        exit(0)
      else:
        exit(0)

#--------------------------------------------------------------------------------------------------
# get_api - with API defined in OS
#--------------------------------------------------------------------------------------------------
def get_api_only():
  (sess,base_url) = login()
  get_api_url = base_url + API_CALL
  warnings.simplefilter('ignore',InsecureRequestWarning)
  staging_get_url_json = sess.get(url=get_api_url, verify=False)
  if staging_get_url_json.status_code != 200:
        print('-' * 120)
        print("API you provided is wrong, code is:",staging_get_url_json.status_code)
        print('-' * 120)
        exit(0)

  (get_api_json,is_jason_status) = is_json(staging_get_url_json.content)
  if is_jason_status == True:
    return (get_api_json,is_jason_status)
  if is_jason_status == False:
    return (get_api_json,is_jason_status)

#--------------------------------------------------------------------------------------------------
# get_api - with API defined in OS
#--------------------------------------------------------------------------------------------------

def get_api_only_arg(API):
  (sess,base_url) = login()
  get_api_url = base_url + API
  warnings.simplefilter('ignore',InsecureRequestWarning)
  staging_get_url_json = sess.get(url=get_api_url, verify=False)
  if staging_get_url_json.status_code != 200:
        print('-' * 120)
        print("API you provided is wrong, code is:",staging_get_url_json.status_code)
        print('-' * 120)
        exit(0)

  (get_api_json,is_jason_status) = is_json(staging_get_url_json.content)
  if is_jason_status == True:
    return (get_api_json,is_jason_status)
  if is_jason_status == False:
    return (get_api_json,is_jason_status)

#--------------------------------------------------------------------------------------------------
# other small functions
#--------------------------------------------------------------------------------------------------
def Convert(string):
    li = list(string.split(","))
    return li

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()

#input is, header, list and will be saved to CSV.
def save_dict_to_csv(df, default_file_name):
  yes_or_no_output = yes_or_no("Would you like to save output?")
  if yes_or_no_output == True:
    try:
      filename = input("Enter filename.....(if not defined, this will be used:")
      is_empty = isNotBlank(filename)
      if is_empty == False:
        print("Writing to", default_file_name)
        df.to_csv(default_file_name, index=False)
      else:
        print("Output Writing to file ", filename)
        df.to_csv(filename, index=False)
    except ValueError:
      print("Incorrect file name.(probably empty string)")
      exit(0)
    else:
      exit(0)


def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    try:
      if reply[0] == 'y':
        return True
      if reply[0] == 'n':
        return False
      else:
        return yes_or_no("Please (y/n) only.")
    except:
        return yes_or_no("Please (y/n) only.")


def isNotBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return True
    #myString is None OR myString is empty or blank
    return False


#--------------------------------------------------------------------------------------------------
#              click, functions - part of interpreter
#--------------------------------------------------------------------------------------------------

@click.group()
def cli():
    """
    Command line tool for APIs -  CISCO SDWAN.\n
    - get-api: get API call and exportin to JSON/txt\n
    - parsing-json: exported JSON can be parsed based on keys

    """
    pass

@click.command()
def get_api():
  get_api_function_outputs()

@click.command()
def parsing_json():
  if JSON_KEYS is None:
    print("-" * 120)
    print("JSON_KEYS is missing. Ensure you use format defined bellow, you can add/remove keys, but keep exact the same format.")
    print("As I'm not exactly checking format of input, ensure you will follow example.\n\nExample to define JSON_KEYS:\n\n")
    print("export JSON_KEYS=\"'deviceId', 'site-id', 'host-name', 'local-system-ip'\"")
    print("If you need help to identify JSON_KEYS look to JSON_OUTPUT.txt file in your directory.")
    print("-" * 120)
    exit("1")

  (get_api_json,is_jason_status) = get_api_only()
  #print("-" * 120)

  if is_jason_status == False:
    print("Output from API is not JSON, parsing function is only for JSON outputs....")
    print("Exiting...")
    exit(0)
  else:
    json_parameters=ast.literal_eval(JSON_KEYS)
    print("-" * 120)
    print("Parsing api call defined by API_CALLs based on keys provided in JSON_KEYS:")
    print(json_parameters)
    print("-" * 120)
    data = get_api_json
    devices = []
    devices = [{key: device.get(key, "N/A") for key in json_parameters} for device in data["data"]]
    df = pandas.DataFrame(devices)
    headers = json_parameters
    print(tabulate(df , headers, tablefmt="fancy_grid"))
    yes_or_no_output = yes_or_no("Would you like to save output to csv? ")
    if yes_or_no_output == True:
      try:
        filename = input("Enter Filename.....(if not defined, output.csv will be used): ") or "output.csv"
        is_empty = isNotBlank(filename)
        if is_empty == False:
          print("Writing to output.csv")
          df.to_csv(filename, index=False)
        else:
          print("CSV writing to",filename,"file.")
          df.to_csv(filename, index=False)
      except ValueError:
        print("Incorrect file name.(probably empty string)")
        exit(0)
      else:
        exit(0)

@click.command()
def onboarded_devices():
    API = "dataservice/device"
    warnings.simplefilter('ignore',InsecureRequestWarning)
    (get_api_json,is_jason_status) = get_api_only_arg(API)
    data = get_api_json
    headers = ["host-name", "device-type", "local-system-ip", "site-id", "device-model", "reachability", "uptime-date"]

    devices = []
    devices = [{key: device.get(key, "N/A") for key in headers} for device in data["data"]]
    df = pandas.DataFrame(devices)
    print(tabulate(df , headers, tablefmt="fancy_grid"))
    save_dict_to_csv(df, "onboarded_devices.csv")

@click.command()
def all_devices():
    API = "dataservice/certificate/vedge/list?api_key=staging"
    warnings.simplefilter('ignore',InsecureRequestWarning)
    (get_api_json,is_jason_status) = get_api_only_arg(API)
    data = get_api_json
    headers = ["host-name","uuid", "local-system-ip", "site-id", "reachability", "uptime-date"]
    devices = []
    devices = [{key: device.get(key, "N/A") for key in headers} for device in data["data"]]
    df = pandas.DataFrame(devices)
    print(tabulate(df , headers, tablefmt="fancy_grid"))
    save_dict_to_csv(df, "all_devices.csv")


@click.command()
@click.option("--template", help="ID of the template you wish to retrieve information for")
def attached_devices(template):
  if template == None:
    print("template ID note defined....Exiting")
    exit(1)
  API = "dataservice/template/device/config/attached/{0}".format(template)
  warnings.simplefilter('ignore',InsecureRequestWarning)
  (get_api_json,is_jason_status) = get_api_only_arg(API)
  data = get_api_json
  headers = ["host-name", "deviceIP", "uuid", "personality"]
  devices = []
  devices = [{key: device.get(key, "N/A") for key in headers} for device in data["data"]]
  df = pandas.DataFrame(devices)
  print(tabulate(df , headers, tablefmt="fancy_grid"))
  save_dict_to_csv(df, "attached_devices.csv")

@click.command()
def list_templates():
#finished_here
    API = "dataservice/template/device"
    warnings.simplefilter('ignore',InsecureRequestWarning)
    (get_api_json,is_jason_status) = get_api_only_arg(API)
    data = get_api_json
    headers = ["templateName", "deviceType", "templateId", "devicesAttached", "templateAttached", "lastUpdatedBy", "lastUpdatedOn"]
    devices = []
    devices = [{key: device.get(key, "N/A") for key in headers} for device in data["data"]]
    df = pandas.DataFrame(devices)
    print(tabulate(df , headers, tablefmt="fancy_grid"))
    save_dict_to_csv(df, "list_templates.csv")


cli.add_command(get_api)
cli.add_command(parsing_json)
cli.add_command(onboarded_devices)
cli.add_command(all_devices)
cli.add_command(attached_devices)
cli.add_command(list_templates)

if __name__ == "__main__":
  cli()
