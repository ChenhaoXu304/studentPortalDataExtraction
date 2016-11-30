import requests
import html
import codecs
import getpass


def getAnnouncements(username,password):
    #start session
    with requests.Session() as s:
        s=requests.Session()
        init=s.get('https://students.nyuad.nyu.edu/announcements')

        login=s.post(
            init.url,
                         data={'j_username':username,'j_password':password,
                                     '_eventId_proceed':'Login'})

        print("Login:",login.status_code,login.reason)
        print("Login:",login.url)
        
        #As javascript is not supported, automatic redirects can only be done manually here
        inter=s.get('https://students.nyuad.nyu.edu/announcements')
        print("Inter:",inter.status_code,inter.reason)
        #print(inter.url)
        page=inter.text
        post_link_sp=page.find("action")+8
        post_link_ep=page.find("POST")+4
        post_link=page[post_link_sp:post_link_ep]
        post_link=html.unescape(post_link)
        #print(post_link)
        #print(page[post_link_sp:post_link_ep])
        RelayState_sp=page.find("RelayState")+19
        RelayState_ep=page.find('"/>',RelayState_sp)
        RelayState=page[RelayState_sp:RelayState_ep]
        RelayState=html.unescape(RelayState)
        
        SAMLResponse_sp=page.find("SAMLResponse")+21
        SAMLResponse_ep=page.find('"/>',SAMLResponse_sp)
        SAMLResponse=page[SAMLResponse_sp:SAMLResponse_ep]
        SAMLResponse=html.unescape(SAMLResponse)
        
        portal=s.post(post_link,data={"RelayState":RelayState,"SAMLResponse":SAMLResponse
                               })
        print("final:",portal.status_code,portal.reason)
        
       
        #get announcements
        announcements=s.get(
            "https://students.nyuad.nyu.edu/apps/announcements/index",
            data={"_":None,"amount":50,"category":None,"lastRaDate":None,
        "query":None,
        "start":0})
        
        print("Announcements:",announcements.status_code,announcements.reason)
        
        ann=announcements.json()
    return ann["announcements"]

def writeAnnouncements(ann,filename):
    fp=codecs.open(filename,'w',"utf-8")

    for a in ann:
        fp.write("Title: "+str(a['title'])+"<br />")
        if isinstance(a['category'],dict):
            fp.write("Category: "+str(a['category']['name'])+"<br />")
        fp.write("Content:  "+str(a['message'])+"<br />")
        fp.write("-"*50+"<br />")
    fp.close()

username=input("username: ")
password=getpass.getpass("password: ")
ann=getAnnouncements(username,password)
filename=input("filename: ")
writeAnnouncements(ann,filename)



