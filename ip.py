import socket
import re
import subprocess
import csv

file = open("top-1m.csv", 'rb')
reader = csv.reader(file, delimiter = ',')

hostname = []
for i in reader:
	hostname.append(i[1])

final = []

for i in range(0, len(hostname) - 1):
	web = hostname[i]
	ip = ""
	try:
		ip = socket.getaddrinfo(hostname[i], 'https')
		socket.freeaddrinfo()
	except:
		pass

	ip_list = []

	for i in ip:
		ip_list.append(i[4])

	for i in range(0, len(ip_list)):
		ip_list[i] = ip_list[i][0]

	for i in range(0, len(ip_list) - 1):
		j = i + 1
		while j < len(ip_list):
			if ip_list[i] == ip_list[j]:
				ip_list.remove(ip_list[j])
			j += 1	

	for i in ip_list:
		if bool(re.search('[a-zA-Z]', i)):
			ip_list.remove(i)

	final.append((web, ip_list))

print final

f = open("ip.csv", 'w')

for i in final:
	f.write("%s\n" % i[0])
	num = 1
	for j in i[1]:
		f.write("%d,%s\n" % (num, j))
		num += 1