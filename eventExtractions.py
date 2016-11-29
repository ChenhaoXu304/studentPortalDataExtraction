import requests
import html
import codecs


def getEvents(username,password):
    with requests.Session() as s:
        init=s.get('https://students.nyuad.nyu.edu/')

        login=s.post(
            init.url,
                         data={'j_username':username,'j_password':password,
                                     '_eventId_proceed':'Login'})

        print("Login:",login.status_code,login.reason)
        print("Login:",login.url)
        #print(r1.url)
        #print(r1.text[:300])
        #print('Division')

        inter=s.get('https://students.nyuad.nyu.edu/')
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
        #s.get("https://students.nyuad.nyu.edu/calendars/")
        events=s.get(
        "https://events.nyuad.nyu.edu/live/json/events/exclude_group/NYUAD-Community-Life/exclude_group/NYUAD-Academic-Enrichment/exclude_group/NYUAD-NYC/exclude_group/NYUAD-TestGroup/exclude_group/CalAdmins/exclude_group/NYUAD-Learning-Development/exclude_group/LiveWhale%20Staff/exclude_tag/fitness-class/exclude_tag/faculty/"
        )#,data={S"_":"1480361799989",
        #"callback":"jQuery19106895467886702749_1480361799988",
        #"lw_auth":"22dd1311ea4844d6361cebd927f6137b"})
        #1480247989193
        print("Events:",events.status_code,events.reason)
        #print(announcements.text[:600])

        #ann=ann["data"]["html"]
        #print(ann["announcements"])
        '''
        fp=codecs.open("announcements.html",'w',"utf-8")
        fp.write(ann)
        fp.close()
        s.close()
        '''
        events=events.json()
        return events
def writeEvents(filename,events):
    fp=codecs.open(filename,'w',"utf-8")
    fp.write(str(events))
    fp.close()


