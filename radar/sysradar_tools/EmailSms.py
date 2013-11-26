'''
Created on Jul 27, 2011

@author: oquidave
'''
from datetime import *
class EmailSms():
    '''
    These are helper tools for the systradar 
    Tools such as sms blaster, email blaster
    '''

    """def __init__(self, message):
        self.message = message
    """

    def contacts(self):
            "contacts of the concerned"
            techie_contacts = {}
            week_day = int(datetime.now().strftime('%w'))
            if week_day == 7:
                "send to only charles who works on sunday"
                techie_contacts['charles'] = {'email':'colupot@smsmedia.info', 'phone':'256754819814'}
            elif  week_day == 6:
                "send to david, bendon and peter, skip the sabath dude"
                techie_contacts['david'] = {'email':'dokwii@smsmedia.info', 'phone':'256754819815'}
                techie_contacts['peter'] = {'email':'sotandeka@smsmedia.info', 'phone':'256754819811'}
                techie_contacts['bendon'] = {'email':'bmurgor@smsmedia.info', 'phone':'256712087736'}
            else:
                "we are all at work during week days"
                techie_contacts['david'] = {'email':'dokwii@smsmedia.info', 'phone':'256754819815'}
                techie_contacts['charles'] = {'email':'colupot@smsmedia.info', 'phone':'256754819814'}
                techie_contacts['peter'] = {'email':'sotandeka@smsmedia.info', 'phone':'256754819811'}
                techie_contacts['bendon'] = {'email':'bmurgor@smsmedia.info', 'phone':'256712087736'}
            # return contacts dict
            return techie_contacts
        
    def create_sms_xml(self, sms_msg):
        "create the xml that will be posted to the api"
        from xml.etree import ElementTree as ET
        # create the root tag("XML")
        XML = ET.Element("XML")
        # create the first child (SENDBATCH)
        SENDBATCH = ET.SubElement(XML, "SENDBATCH")
        # add text
        SENDBATCH.text = sms_msg
        # add attributes
        username = 'admin';password = 'password'; reply_email = 'dokwii@smsmedia.info';senderid = 'SYSRADAR';status_report = '0'
        SENDBATCH.attrib['user'] = username
        SENDBATCH.attrib['password'] = password
        SENDBATCH.attrib['reply'] = reply_email
        SENDBATCH.attrib['status_report'] = status_report
        SENDBATCH.attrib['senderid'] = senderid
        # #create the  child(SMSLIST) to SENDBATCH node
        SMSLIST = ET.SubElement(SENDBATCH, "SMSLIST")
        # get contact and send add attributes to smslist tag
        techie_contacts = self.contacts()
        for techie, contact_dict in techie_contacts.iteritems():
            # create the  child(SMS_SEND) to SMSLIST for each number
            SMS_SEND = ET.SubElement(SMSLIST, "SMS_SEND")
            to = contact_dict['phone']
            SMS_SEND.attrib['to'] = to
            SMS_SEND.attrib['to_name'] = techie
        # Let's see the results
        # print ET.tostring(XML)
        msg_xml = ET.tostring(XML)
        return msg_xml

    def sms_blaster(self, sms_msg):
        "send an sms notification through the gw api"
        import httplib
        msg_xml = self.create_sms_xml(sms_msg)
        # host= "localhost"; port=10088
        host = "192.168.2.178"; port = 80
        conn = httplib.HTTPConnection(host, port)
        conn.request("POST", "/travelport/index.php", msg_xml)
        response = conn.getresponse()
        print response.status, response.reason
        if response.status == 200:
            # post was successfull, so get the xml response
            responsexml = response.read()
            post_status = "success"
        else:
            print "failed to send post request"
            post_status = "failed"
            responsexml = ''
        # close the connection
        conn.close()
        return post_status, responsexml
            
    def email_blaster(self, email_msg):
            "send and email notificatin to concerned"
            import smtplib
            SERVER = '192.168.2.1'
            FROM = 'sysradar@smsmedia.info'
            # TO = ['dokwii@smsmedia.info', 'tumwesigyeroger@yahoo.com', 'anakiyingi@smsmedia.info'] # must be a list
            TO = []
            SUBJECT = "SYSTEM DOWN ALERT"
            # TEXT = "This message was sent with Python's smtplib."
            techie_contacts = self.contacts()
            for techie, contact_dict in techie_contacts.iteritems():
                to = contact_dict['email']
                TO.append(to)
            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, email_msg)
            try:
                server = smtplib.SMTP(SERVER)
                server.sendmail(FROM, TO, message)
                server.quit()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"


def send_email(self, email_msg):
            "send and email "
            import smtplib
            SERVER = 'mail.smsmedia.info'
            FROM = 'sysradar@smsmedia.info'
            TO = ['dokwii@smsmedia.info']  # must be a list
            SUBJECT = "Test from zambia"
            TEXT = "This message was sent by christ from zambia"
            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                server = smtplib.SMTP(SERVER)
                server.sendmail(FROM, TO, message)
                server.quit()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"
