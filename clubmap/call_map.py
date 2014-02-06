##a = {'neki':'sem', 'se':'dfasd'}
##f = open('test.txt', 'wb')
##f.write(str(a))
##
##f.close()
#db = {'So36': {'Title': 'Montech at So36', 'url': 'http://www.residentadvisor.net/event.aspx?512155', 'Venue': 'So36/ Oranienstrasse 190; Kreuzberg; 10999 Berlin; Germany', 'Cost': '5,- \x80', 'Time': '23:00 - 08:00', 'Date': 'Monday, 9 September 2013', 'Cost-list': [5]}, 'Intersoup': {'Title': 'Rocky Monday with Jaguwar at Intersoup', 'url': 'http://www.residentadvisor.net/event.aspx?511869', 'Venue': 'Intersoup/ Schliemannstrasse 31; 10437; Berlin; Germany', 'Cost': '0\x80', 'Time': '18:00 - 04:00', 'Date': 'Monday, 9 September 2013', 'Cost-list': [0]}, 'Chalet': {'Title': 'Limited Monday - Secret Lineup  at Chalet', 'url': 'http://www.residentadvisor.net/event.aspx?507570', 'Venue': 'Chalet/ Vor dem Schlesischen Tor 3; Kreuzberg; 10997 Berlin; Germany', 'Cost': 'tba', 'Time': '23:59 - 12:00', 'Date': 'Monday, 9 September 2013', 'Cost-list': [10]}, 'Mini.Mal Elektrokneipe': {'Title': 'Manic.Monday mit Juerga at Mini.Mal Elektrokneipe', 'url': 'http://www.residentadvisor.net/event.aspx?511408', 'Venue': 'Mini.Mal Elektrokneipe/ Rigaer Strasse 31; Friedrichshain; 10247 Berlin; Germany', 'Cost': '0', 'Time': '19:00 - 05:00', 'Date': 'Monday, 9 September 2013', 'Cost-list': [0]}, 'Globus ': {'Title': 'Electric Monday@Globus & +4 Bar, Tresor Berlin at Globus / +4bar', 'url': 'http://www.residentadvisor.net/event.aspx?512585', 'Venue': 'Globus / +4bar &nbsp;/ K\xf6penickerstrasse 70, Mitte, 10179 Berlin', 'Cost': 'tba', 'Time': '23:00 - 08:00', 'Date': 'Monday, 9 September 2013', 'Cost-list': [10]}, 'Crack Bellmer': {'Title': 'Montag auf Cr\xe4ck at Crack Bellmer', 'url': 'http://www.residentadvisor.net/event.aspx?517458', 'Venue': 'Crack Bellmer/ Revaler Strasse 99; 10245 Berlin-Friedrichshain; Berlin; Germany', 'Cost': 'Free entry!', 'Time': '22:00 - 06:00', 'Date': 'Monday, 9 September 2013', 'Cost-list': [0]}, 'Michelberger Hotel': {'Title': 'The Revival Hour at Michelberger Hotel', 'url': 'http://www.residentadvisor.net/event.aspx?517162', 'Venue': 'Michelberger Hotel/ Warschauer Strasse; Friedrichshain; 10234 Berlin; Germany', 'Cost': 'Free Entrance', 'Time': '19:00 - 23:59', 'Date': 'Monday, 9 September 2013', 'Cost-list': [0]}, 'Cake Club Berlin &nbsp;': {'Title': 'Electro Funk Roots at Cake Club Berlin', 'url': 'http://www.residentadvisor.net/event.aspx?514174', 'Venue': 'Cake Club Berlin &nbsp;/ Oranienstra\xdfe 32 10999 Berlin', 'Cost': 'Free', 'Time': '22:00 - 16:00', 'Date': 'Monday, 9 September - &nbsp; Tuesday, 10 September 2013', 'Cost-list': [0]}, 'Magdalena': {'Title': 'Rotation at Magdalena', 'url': 'http://www.residentadvisor.net/event.aspx?512471', 'Venue': 'Magdalena/ Stralauer Platz 33 -34; 10243 Berlin; Germany', 'Cost': '5\x80', 'Time': '23:00 - 09:00', 'Date': 'Monday, 9 September 2013', 'Cost-list': [5]}}

class call_map:
    def __init__(self, db):
        javascript = open('variables.js', 'wb')
        for venue, info in db.items():
            javascript.write('var %s = %s;\r\n' % (venue.split(' ')[0].split('.')[0], info))

        names = [x.split(' ')[0].split('.')[0] for x in db.keys()]    
        javascript.write('var events = [%s];\r\n' % (', '.join(names)))

        javascript.close()
            
