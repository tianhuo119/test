from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import
url="http://132.33.13.171:2005/services/getPortStatus?wsdl"
imp=Import('http://schemas.xmlsoap.org/soap/encoding/')
d=ImportDoctor(imp)
client=Client(url,doctor=d)
result=client.service.getPortStatus("<input><Device>SX-YC-ZXJF-S-1.CN2</Device><PortName>GigabitEthernet5/0/0</PortName><WsId>2017071233</WsId></input>")