import os
import re
from BeautifulSoup import BeautifulSoup as BS



def esc(txt):
    txt = txt.replace('&nbsp;', ' ').strip()
    txt = re.sub(r'[^a-zA-Z0-9_]', '_', txt)
    txt = re.sub(r'_+', '_', txt)
    txt = txt.strip('_')
    return txt


def parse():
    soup = BS(open('index').read())
    for item in soup.findAll('div', 'course-item-list-header'):
        section = esc(item.find('h3').next.next)
        ul = item.nextSibling

        print 'echo "downloading %s"' % section
        print 'mkdir -p %s' % section
        for lecture_link in ul.findAll('a', 'lecture-link'):
            links = lecture_link.parent.find('div', 'course-lecture-item-resource').findAll('a')
            title = esc(lecture_link.next)

            download_link = links[-1]
            href = download_link['href'] 
            subfix = os.path.basename(href).split('?', 1)[0].split('.')[-1]
            fname = os.path.join(section, '%s.%s' % (title, subfix))
            print '''if [ ! -e "%s" ]; then
    wget --no-cookies --header "Cookie: $(cat cookies.txt)" '%s' -O '%s'
fi''' % (fname, href, fname)


            if len(links) >= 2:
                script_link = links[-2]
                shref = script_link['href']
                if shref.find('srt') > 0:
                    sfname = os.path.join(section, '%s.srt' % (title))
                    print '''if [ ! -e "%s" ]; then
    wget --no-cookies --header "Cookie: $(cat cookies.txt)" '%s' -O '%s'
fi''' % (sfname, shref, sfname)

            print

parse()
