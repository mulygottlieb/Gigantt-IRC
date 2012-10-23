import json
import urllib2
import base64


def main():
    # Auth info
    username = raw_input('Username: ')
    password = raw_input('Password: ')
    if not username and password:
        print 'Username and password required for export.'
        return
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    
    # Helper to fetch from API
    def get_resp(url):
        req = urllib2.Request(url)
        req.add_header("Authorization", "Basic %s" % base64string)
        r = urllib2.urlopen(req)
        raw = r.read()
        resp = json.loads(raw)
        r.close()
        return resp, raw
    
    # Helper to get all messages for a channel
    def get_messages(channel, count=0, until_id=None):
        print '.'
        url = 'https://grove.io/api/channels/%s/messages' % channel.get('id')
        if until_id:
            url = '%s?until_id=%s' % (url, until_id)

        resp, raw = get_resp(url)
        if not resp:
            return
        
        # Save messages to file
        f = open('%s.%04d.json' % (channel.get('name'), count), 'w')
        f.write(raw)
        f.close()
        
        # Moare messages!
        until = resp[0].get('id')
        print 'until_id:', until
        get_messages(channel, count+1, until_id=until)

    resp, raw = get_resp('https://grove.io/api/auth')
    orgs = resp.get('organizations')
    print 'Found %s organization(s) to export.' % len(orgs)
    
    for org in orgs:
        print '\nExporting organization:', org.get('name')
        
        try:
            resp, raw = get_resp('https://grove.io/api/organizations/%s' % org.get('id'))
        except urllib2.HTTPError, ex:
            print 'Error: most likely this org has been suspended.'
            continue
        
        channels = resp.get('channels')
        print 'Found %s channel(s) to export.' % len(channels)
        for channel in channels:
            print 'Exporting channel:', channel.get('irc_name')
            get_messages(channel)
            

if __name__ == '__main__':
    print 'Exporting Grove data.\n'
    main()
    print '\nExport completed.'