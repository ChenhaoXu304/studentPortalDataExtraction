import requests
import html
import codecs


def getAnnouncements(username,password):
    with requests.Session() as s:
        s=requests.Session()
        init=s.get('https://students.nyuad.nyu.edu/announcements')

        login=s.post(
            init.url,
                         data={'j_username':username,'j_password':password,
                                     '_eventId_proceed':'Login'})

        print("Login:",login.status_code,login.reason)
        print("Login:",login.url)
        #print(r1.url)
        #print(r1.text[:300])
        #print('Division')

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
        #print(RelayState)
        #print(page[RelayState_sp:RelayState_ep])
        SAMLResponse_sp=page.find("SAMLResponse")+21
        SAMLResponse_ep=page.find('"/>',SAMLResponse_sp)
        SAMLResponse=page[SAMLResponse_sp:SAMLResponse_ep]
        SAMLResponse=html.unescape(SAMLResponse)
        #print(SAMLResponse)
        #print(page[SAMLResponse_sp:SAMLResponse_ep])
        portal=s.post(post_link,data={"RelayState":RelayState,"SAMLResponse":SAMLResponse
                               })
        print("final:",portal.status_code,portal.reason)
        #print(portal.text[:600])
        '''
        content=portal.text.replace('\u2028','\n')
        s1=s.get("https://www.google-analytics.com/analytics.js")
        #print("google-analytics:",s1.status_code,s1.reason)
        #print(s1.text[:250])

        s2=s.get("https://api.usersnap.com/load/bf1e2b42-1121-428e-b112-c242f39abf42.js")
        #print("js2:",s2.status_code,s2.reason)
        #print(s2.text[:250])

        s3=s.get("https://d3mvnvhjmkxpjz.cloudfront.net/js/11748/usersnap2-11748-en.js")
        #print("js3:",s3.status_code,s3.reason)
        #print(s3.text[:250])
        scripts="<script>"+s1.text+s2.text+s3.text+"</script>"
        scripts=scripts.replace('\xeb',u'\xeb')'''

        announcements=s.get(
            "https://students.nyuad.nyu.edu/apps/announcements/index",
            data={"_":None,"amount":50,"category":None,"lastRaDate":None,
        "query":None,
        "start":0})
        #1480247989193
        print("Announcements:",announcements.status_code,announcements.reason)
        #print(announcements.text[:600])
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
'''
def printAnnouncements(ann):
    for a in ann:
        print("Title: ",str(a['title']))
        if isinstance(a['category'],dict):
            print("Category: "+str(a['category']['name']))
        print("Content:  "+str(a['message']))
        print("-"*60)
'''



