import requests
import smtplib


from bs4 import BeautifulSoup
from time import sleep

emailadrr = test@gmail.com #it has to be a gmail.
passemail = pass1234 #password of the gmail account
previousint = 0
ccaddrr = secondemail@gmail.com # a secondary email address in case the first one is not reacheable.
time_between_query = 60 #time between crawling, default 60 might involve blacklisting. Set to 3600 or use proxies.
#Send through Gmail Stuff
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


while True:
	try:
		page = requests.get("http://www.woko.ch/en/nachmieter-gesucht")
		soup = BeautifulSoup(page.content, 'html.parser')
		sleep(time_between_query)
		print("Crawling web")
		html = soup.find_all(id="GruppeID_98")[0]
		html.find(class_="anzahl")
		quantity_of_places = html.find(class_="anzahl").get_text()
		filtered = [int(s) for s in quantity_of_places.split() if s.isdigit()]
		filteredint = int(filtered[0])
		if (filteredint != previousint):
			sendemail(from_addr    = emailadrr, 
          to_addr_list = [emailadrr],
          cc_addr_list = [ccaddrr], 
          subject      = 'Ad from Woko', 
          message      = 'New ad from woko', 
          login        = emailadrr, 
          password     = passemail)
		previousint = filteredint
	except Exception as e:
		sendemail(from_addr    = emailadrr, 
          to_addr_list = [emailadrr],
          cc_addr_list = [ccaddrr], 
          subject      = 'Error in Ad Service', 
          message      = e, 
          login        = emailadrr, 
          password     = passemail)

