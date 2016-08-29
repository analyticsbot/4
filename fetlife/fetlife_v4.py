## import necessary modules
import mechanize, datetime, time, sqlite3, sqlalchemy, re, argparse, logging, requests
from bs4 import BeautifulSoup
from text_unidecode import unidecode
import random,time,sys, shutil
from sqlalchemy import create_engine, MetaData
from dateutil import parser

## now stores the starting time, used to track running time
## start the logging at DEBUG level
now = time.time()
logging.basicConfig(filename='fetlife.log', filemode='a', \
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'\
                    , datefmt='%H:%M:%S', level=logging.DEBUG)

## accept arguments from the command line
##arparser = argparse.ArgumentParser()
##arparser.add_argument("-l", "--login", help="login username")
##arparser.add_argument("-p", "--password", help="login password")
##arparser.add_argument("-url", "--crawlurl", help="login username")
##arparser.add_argument("-mind", "--mindelay", help="login username")
##arparser.add_argument("-maxd", "--maxdelay", help="login username")
##arparser.add_argument("-maxp", "--maxprofiles", help="login username")
##arparser.add_argument("-no", "--newonly", help="login username")
##arparser.add_argument("-maxt", "--maxtime", help="login username")
##arparser.add_argument("-db", "--database", help="login username")
##arparser.add_argument("-deb", "--debug", help="login username")
##arparser.add_argument("-px", "--proxy", help="login username")

##args = arparser.parse_args()

## parse parameters from arguments
###nickname = 'b3159584'
##nickname = args.login
###password = 'facebook'
##password = args.password
###url = 'https://fetlife.com/countries/84/kinksters'
##url = args.crawlurl
##mindelay = int(args.mindelay)
##maxdelay = int(args.maxdelay)
##maxprofiles = int(args.maxprofiles)
##newonly = args.newonly
##maxtime = int(args.maxtime)
##database = str(args.database)
##debug = int(args.debug)
##proxy = args.proxy
IMAGES_FOLDER = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\fetlife\\images' ## where to save profile spocs

nickname = 'c1233645' ## login username to fetlife
password = 'facebook' ## password to fetlife for the above username
url = 'https://fetlife.com/countries/84/kinksters' ## url for which the profiles are to be scraped
mindelay = 1 ## minimum seconds to wait before scraping next profile
maxdelay = 3 ## maximum seconds to wait before scraping next profile
maxprofiles = 500 ## maximum profiles to be scraped before the script exits . 0 means go on indefenitly. 
newonly = 0 ## boolean field. 1 indicates scrape only new profiles. 0 means scrape and update exiting profiles too
maxtime = 100000 ## maxumum time in seconds for which the script should run before exiting. 0 means go forever
database = 'postgresql://postgres:postgres@localhost/Fetlife1' ## database connection url
debug = 1 ## whether to print output to screen
proxy = 0 ## whether to accept proxies

D_s_Relationships_values = ['Dominant','Sadist','Sadomasochist', 'Master','Mistress','Owner','Master and Owner','Mistress and Owner',\
                                'Top', 'Daddy', 'Mommy', 'Brother','Sister','Being Served','Considering','Protecting','Mentoring',\
                                'Teaching','Training','Switches','submissive', 'masochist', 'bottom', 'owned and collared', 'owned',\
                                'property', 'collared','slave', 'kajira','kajirus', 'in service','under protection', 'under consideration',\
                                'pet', 'toy', 'girl', 'boy', 'babygirl','babyboy', 'brat', 'Keyholder','in chastity', 'being mentored','student',\
                            'trainee', 'unowned', 'unpartnered', 'It\'s Complicated','Presently Inactive', 'Not Applicable']

Relationships_values = ['Single', 'Dating', 'Friend With Benefits', 'Play Partners','In A Relationship', 'Lover', 'In An Open Relationship',\
                            'Engaged', 'Married', 'Widow', 'Widower', 'Monogamous', 'Polyamorous', 'In A Poly Group', 'In A Leather Family', 'In a Pack',\
                            'In a Rope Family', 'Member Of A House', 'It\'s Complicated']

if debug:
    print 'Arguments read from command line'
    
## initiate the db connection to postgres
#engine = create_engine('postgresql://postgres:postgres@localhost/fetlife')
try:
    con = create_engine(database, client_encoding='utf8')
    meta = MetaData(bind=con, reflect=True)

    if debug:
        print 'Connection to db made successfully'
except:
    if debug:
        print 'Error connecting to db. Check connection string or if the db is up and running'
    sys.exit(1)
  
## intantiate the mechanize browser
br = mechanize.Browser()
br.set_handle_robots(False)
if proxy:
    br.set_proxies({"http": proxy})
br.open('https://fetlife.com/login')
br.select_form(nr=0)
br.form.new_control('text', 'nickname_or_email', {'value': nickname})
br.form.new_control('password', 'password', {'value': password})
resp = br.submit()

if debug:
        print 'Successfully logged in using the given credentials'

time.sleep(2)

def downloadImage(url, name):
    response = requests.get(url, stream=True)
    with open(IMAGES_FOLDER+'//'+str(name)+'.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def getElement(table, name):
    """ function to get the elements in tabular format
    table - all elements in table
    name - name of the element for which value is required
    """
    for el in table:
        try:
            if el.find('th').getText() == name:
                return el.find('td')
        except:
            return ''

def getBottomElement(bottom, name):
    """ function to get the bottom elements 
    bottom - all elements in bottom
    name - name of the element for which value is required
    """
    for b in bottom:
        try:
            if b.getText().strip() == name.strip():
                if name.strip() == 'Websites':
                    return b.findNextSibling().getText()
                elif name.strip() == 'Latest pictures':
                    pics = b.findNextSiblings('a')
                    value = ''
                    for p in pics:
                        value  = value + '; ' + p.find('img')['src']
                    return value
                value= ''
                ids = ''
                x = b.findNextSibling()
                while True:                    
                    if x.name == 'p':
                        value += ' ' + x.getText()
                        ids += ', ' + re.findall(r'\d+', x.find('a')['href'])[0]
                        x = x.findNextSibling()
                    else:
                        break
                return value.strip(), ids[1:].strip()
        except:
            return ''

def getListElement(listElem, name):
    """ function to get the elements in list format
    listElem - all elements in list
    name - name of the element for which value is required
    """
    ids = []
    try:
        for l in listElem:
            try:
                if l.findPreviousSibling().getText().strip() == name.strip():                
                    if name.strip() == 'Groups member of':
                        return l.getText().strip(), [re.findall(r'\d+',link['href'])[0] for link in l.findAll('a')]
                    else:
                        return l.getText().strip()
            except:
                return ''
    except:
        return ''

def getLookingForStatus(Looking_for_options, name):
    """ function to get the looking for values
    Looking_for_options - all looking for options
    name - name of the element for which value is required
    """
    try:
        if name in Looking_for_options:
            return True
        else:
            return False
    except:
        return False

def getDSRelationshipStatus(D_s_Relationships, name):
    """ function to get the D_s_Relationships values
    D_s_Relationships - all D_s_Relationships options
    name - name of the element for which value is required
    """
    returnValue = []
    try:
        for relation in D_s_Relationships:
            if relation.split()[-1].lower() != name.lower():
                returnValue.append(relation.split()[-1])
            else:
                returnValue.append('1')
##            else:
##                returnValue.append(['0', ''])
    except:
        returnValue.append(None)
    return returnValue

def checkDSRelationshipUnknown(D_s_Relationships, D_s_Relationships_values):
    if any(word in ' '.join(D_s_Relationships) for word in D_s_Relationships_values):
        return False
    else:
        return True

def checkRelationshipUnknown(Relationships, Relationships_values):
    if any(word in ' '.join(Relationships) for word in Relationships_values):
        return False
    else:
        return True

def getRelationshipStatus(Relationships, name):
    """ function to get the Relationships values
    Relationships - all Relationships options
    name - name of the element for which value is required
    """
    returnValue = []
    try:
        for relation in Relationships:
            if name in relation:
                if relation.split()[-1].lower() != name.lower():
                    returnValue.append(relation.split()[-1])
                else:
                    returnValue.append('1')
##            else:
##                returnValue.append(['0', ''])
    except:
        returnValue.append(None)
    return returnValue
        
def getUserDetails(user_url, info, location, username, con, meta, user_exists, websites, fetishes, groups, pictures, D_s_Relationships_values, Relationships_values):
    """ function to get the user data points from user page
    user_url - user url on fetlife
    info - info text from search page
    location - location text
    username - username of the user
    con - connection to the db
    meta - variable containing data on tables
    """
    br.open('https://fetlife.com/' + user_url)
    if debug:
        print 'Successfully opened the page of ', username
    html = br.response().read()
    soup = BeautifulSoup(html, 'lxml')
    bottom = soup.findAll(attrs = {'class':'bottom'})
    table = soup.findAll("tr")
    listElem = soup.findAll(attrs={'class':'list'})
    URL = 'https://fetlife.com/' + user_url
    id_user = re.findall(r'\d+', user_url)[0]
    Nickname = username
    try:
        Age = re.findall(r'\d+', info)[0]
    except:
        Age = ''
    if 'MtF' in info:
        Gender = 'MtF'
    elif 'FtM' in info:
        Gender = 'FtM'
    elif 'CD/TV' in info:
        Gender = 'CD/TV'
    elif 'TG' in info:
        Gender = 'TG'
    elif 'GF' in info:
        Gender = 'GF'
    elif 'GQ' in info:
        Gender = 'GQ'
    elif 'IS' in info:
        Gender = 'IS'
    elif 'B' in info:
        Gender = 'B'
    elif 'FEM' in info:
        Gender = 'FEM'
    elif 'M' in info:
        Gender = 'M'
    elif 'F' in info:
        Gender = 'F'
    else:
        Gender = 'Unknown'
    
    try:
        Role = info.split()[1]
    except:
        Role = ''
    try:
        Location_Country = location.split(',')[-1].strip().replace('\n','')
    except:
        Location_Country = ''
    try:
        Location_Administrative_area = location.split(',')[-2].strip().replace('\n','')
    except:
        Location_Administrative_area = ''
    try:
        Location_City = location.split(',')[-3].strip().replace('\n','')
    except:
        Location_City = ''
    print user_url, Location_Country, Location_Administrative_area, Location_City
    try:
        Sexual_Orientation = getElement(table, 'orientation:').getText().strip()
    except:
        Sexual_Orientation = ''
    try:
        How_active  = getElement(table, 'active:').getText().strip()
    except:
        How_active  = ''

    ## Looking for elements
    try:
        Looking_for = getElement(table, 'is looking for:')
    except:
        Looking_for_options = ''
    Looking_for_options = str(Looking_for).replace('<td>','').replace('</td>','').split('<br/>')
    Looking_for_A_Lifetime_Relationship_LTR = getLookingForStatus(Looking_for_options, 'A Lifetime Relationship (LTR)')
    Looking_for_A_Relationship = getLookingForStatus(Looking_for_options, 'A Relationship')
    Looking_for_A_Mentor_Teacher = getLookingForStatus(Looking_for_options, 'A Mentor/Teacher')
    Looking_for_Someone_To_Play_With = getLookingForStatus(Looking_for_options, 'Someone To Play With')
    Looking_for_A_Princess_By_Day_Slut_By_Night = getLookingForStatus(Looking_for_options, 'A Princess By Day, Slut By Night')
    Looking_for_Friendship = getLookingForStatus(Looking_for_options, 'Friendship')
    Looking_for_A_Master = getLookingForStatus(Looking_for_options, 'A Master')
    Looking_for_A_Mistress = getLookingForStatus(Looking_for_options, 'A Mistress')
    Looking_for_A_sub = getLookingForStatus(Looking_for_options, 'A sub')
    Looking_for_A_slave = getLookingForStatus(Looking_for_options, 'A slave')
    Looking_for_Events = getLookingForStatus(Looking_for_options, 'Events')
    Looking_for_None = False if len(Looking_for_options)==0 else True

    ## D/S relationship
    try:
        D_s_Relationships = getElement(table, 'D/s relationship status:').getText().strip().split('\n')
    except:
        D_s_Relationships = ''
    D_s_Relationships_Dominant = getDSRelationshipStatus(D_s_Relationships, 'Dominant')
    D_s_Relationships_Sadist = getDSRelationshipStatus(D_s_Relationships, 'Sadist')
    D_s_Relationships_Sadomasochist = getDSRelationshipStatus(D_s_Relationships, 'Sadomasochist')
    D_s_Relationships_Master = getDSRelationshipStatus(D_s_Relationships, 'Master')
    D_s_Relationships_Mistress = getDSRelationshipStatus(D_s_Relationships, 'Mistress')
    D_s_Relationships_Owner = getDSRelationshipStatus(D_s_Relationships, 'Owner')
    D_s_Relationships_Master_and_Owner = getDSRelationshipStatus(D_s_Relationships, 'Master and Owner')
    D_s_Relationships_Mistress_and_Owner = getDSRelationshipStatus(D_s_Relationships, 'Mistress and Owner')
    D_s_Relationships_Top = getDSRelationshipStatus(D_s_Relationships, 'Top')
    D_s_Relationships_Daddy = getDSRelationshipStatus(D_s_Relationships, 'Daddy')
    D_s_Relationships_Mommy = getDSRelationshipStatus(D_s_Relationships, 'Mommy')
    D_s_Relationships_Brother = getDSRelationshipStatus(D_s_Relationships, 'Brother')
    D_s_Relationships_Sister = getDSRelationshipStatus(D_s_Relationships, 'Sister')
    D_s_Relationships_Being_Served = getDSRelationshipStatus(D_s_Relationships, 'Being Served')
    D_s_Relationships_Considering = getDSRelationshipStatus(D_s_Relationships, 'Considering')
    D_s_Relationships_Protecting = getDSRelationshipStatus(D_s_Relationships, 'Protecting')
    D_s_Relationships_Mentoring = getDSRelationshipStatus(D_s_Relationships, 'Mentoring')
    D_s_Relationships_Teaching = getDSRelationshipStatus(D_s_Relationships, 'Teaching')
    D_s_Relationships_Training = getDSRelationshipStatus(D_s_Relationships, 'Training')
    D_s_Relationships_Switches = getDSRelationshipStatus(D_s_Relationships, 'Switches')
    D_s_Relationships_submissive = getDSRelationshipStatus(D_s_Relationships, 'submissive')
    D_s_Relationships_masochist = getDSRelationshipStatus(D_s_Relationships, 'masochist')
    D_s_Relationships_bottom = getDSRelationshipStatus(D_s_Relationships, 'bottom')
    D_s_Relationships_owned_and_collared = getDSRelationshipStatus(D_s_Relationships, 'owned and collared')
    D_s_Relationships_owned = getDSRelationshipStatus(D_s_Relationships, 'owned')
    D_s_Relationships_property = getDSRelationshipStatus(D_s_Relationships, 'property')
    D_s_Relationships_collared = getDSRelationshipStatus(D_s_Relationships, 'collared')
    D_s_Relationships_slave = getDSRelationshipStatus(D_s_Relationships, 'slave')
    D_s_Relationships_kajira = getDSRelationshipStatus(D_s_Relationships, 'kajira')
    D_s_Relationships_kajirus = getDSRelationshipStatus(D_s_Relationships, 'kajirus')
    D_s_Relationships_in_service = getDSRelationshipStatus(D_s_Relationships, 'in service')
    D_s_Relationships_under_protection = getDSRelationshipStatus(D_s_Relationships, 'under protection')
    D_s_Relationships_under_consideration = getDSRelationshipStatus(D_s_Relationships, 'under consideration')
    D_s_Relationships_pet = getDSRelationshipStatus(D_s_Relationships, 'pet')
    D_s_Relationships_toy = getDSRelationshipStatus(D_s_Relationships, 'toy')
    D_s_Relationships_girl = getDSRelationshipStatus(D_s_Relationships, 'girl')
    D_s_Relationships_boy = getDSRelationshipStatus(D_s_Relationships, 'boy')
    D_s_Relationships_babygirl = getDSRelationshipStatus(D_s_Relationships, 'babygirl')
    D_s_Relationships_babyboy = getDSRelationshipStatus(D_s_Relationships, 'babyboy')
    D_s_Relationships_brat = getDSRelationshipStatus(D_s_Relationships, 'brat')
    D_s_Relationships_Keyholder = getDSRelationshipStatus(D_s_Relationships, 'Keyholder') 
    D_s_Relationships_in_chastity = getDSRelationshipStatus(D_s_Relationships, 'in chastity')
    D_s_Relationships_being_mentored = getDSRelationshipStatus(D_s_Relationships, 'being mentored')
    D_s_Relationships_student = getDSRelationshipStatus(D_s_Relationships, 'student')
    D_s_Relationships_trainee = getDSRelationshipStatus(D_s_Relationships, 'trainee')
    D_s_Relationships_unowned = getDSRelationshipStatus(D_s_Relationships, 'unowned')
    D_s_Relationships_unpartnered = getDSRelationshipStatus(D_s_Relationships, 'unpartnered')
    D_s_Relationships_Its_Complicated = getDSRelationshipStatus(D_s_Relationships, 'It\'s Complicated')
    D_s_Relationships_Presently_Inactive = getDSRelationshipStatus(D_s_Relationships, 'Presently Inactive')
    D_s_Relationships_Not_Applicable = getDSRelationshipStatus(D_s_Relationships, 'Not Applicable')
    D_s_Relationships_unknown = checkDSRelationshipUnknown(D_s_Relationships, D_s_Relationships_values)
    ## Relationships
    try:
        Relationships = getElement(table, 'relationship status:').getText().strip().split('\n')
    except:
        Relationships = ''
    
    Relationships_Single = getRelationshipStatus(Relationships, 'Single')
    Relationships_Dating = getRelationshipStatus(Relationships, 'Dating')
    Relationships_Friend_With_Benefits = getRelationshipStatus(Relationships, 'Friend With Benefits')
    Relationships_Play_Partners = getRelationshipStatus(Relationships, 'Play Partners')
    Relationships_In_A_Relationship = getRelationshipStatus(Relationships, 'In A Relationship')
    Relationships_Lover = getRelationshipStatus(Relationships, 'Lover')
    Relationships_In_An_Open_Relationship = getRelationshipStatus(Relationships, 'In An Open Relationship')
    Relationships_Engaged = getRelationshipStatus(Relationships, 'Engaged')
    Relationships_Married = getRelationshipStatus(Relationships, 'Married')
    Relationships_Widow = getRelationshipStatus(Relationships, 'Widow')
    Relationships_Widower = getRelationshipStatus(Relationships, 'Widower')
    Relationships_Monogamous = getRelationshipStatus(Relationships, 'Monogamous')
    Relationships_Polyamorous = getRelationshipStatus(Relationships, 'Polyamorous')
    Relationships_In_A_Poly_Group = getRelationshipStatus(Relationships, 'In A Poly Group')
    Relationships_In_A_Leather_Family = getRelationshipStatus(Relationships, 'In A Leather Family')
    Relationships_In_a_Pack = getRelationshipStatus(Relationships, 'In a Pack')
    Relationships_In_a_Rope_Family = getRelationshipStatus(Relationships, 'In a Rope Family')
    Relationships_Member_Of_A_House = getRelationshipStatus(Relationships, 'Member Of A House')
    Relationships_Its_Complicated = getRelationshipStatus(Relationships, 'It\'s Complicated')
    Relationships_unknown = checkRelationshipUnknown(Relationships, Relationships_values)
    
    try:
        About_me = getBottomElement(bottom, 'About me ')[0]
    except:
        About_me = ''
    try:
        mini_feed = soup.find(attrs={'id':'mini_feed'})
        Latest_activity = mini_feed.find('li').getText().replace('\n','').strip()
        Latest_activity_time = mini_feed.find(attrs = {'class':'timestamp'}).getText().strip()
        Latest_activity_time = parser.parse(Latest_activity_time)
    except:
        Latest_activity = ''
        Latest_activity_time = ''
        
    try:
        Number_of_friends = soup.find('h4').getText()
    except:
        pass
    try:
        Contact_status_Our_Conversations = 'Our Conversations' in soup.getText()
    except:
        Contact_status_Our_Conversations = ''
    try:
        if soup.find(attrs = {'id':'friendship_confirm'}):
            Friends_status = True
        else:
            Friends_status = False
    except:
        Friends_status = False

    Profile_picture = soup.find(attrs = {'class':'span-6'}).find('img')['src']
    downloadImage(Profile_picture, id_user)

    Date_first_crawled = str(datetime.datetime.now())
    if not user_exists:
        Most_recent_date_updated  = str(datetime.datetime.now())
    else:
        Most_recent_date_updated  = (con.execute(users.select().where(users.c.id_user == int(id_user)))).fetchone()['Most_recent_date_updated']
    
    user_details = {'id_user':int(id_user), 'Most_recent_date_updated':Most_recent_date_updated, 'Date_first_crawled':Date_first_crawled,\
                    'Friends_status':Friends_status, 'Profile_picture':Profile_picture, 'Number_of_friends':Number_of_friends, \
                    'Latest_activity':Latest_activity, 'About_me':About_me, 'Relationships_Its_Complicated':Relationships_Its_Complicated,\
                    'Relationships_Member_Of_A_House':Relationships_Member_Of_A_House, \
                    'Relationships_In_a_Rope_Family':Relationships_In_a_Rope_Family,\
                    'Relationships_In_a_Pack':Relationships_In_a_Pack, 'Relationships_In_A_Leather_Family':Relationships_In_A_Leather_Family,\
                    'Relationships_In_A_Poly_Group':Relationships_In_A_Poly_Group, 'Relationships_Polyamorous':Relationships_Polyamorous,\
                    'Relationships_Monogamous':Relationships_Monogamous, 'Relationships_Married':Relationships_Married,\
                    'Relationships_Engaged':Relationships_Engaged, 'Relationships_Widower':Relationships_Widower,\
                    'Relationships_Widow':Relationships_Widow, 'Relationships_In_An_Open_Relationship':Relationships_In_An_Open_Relationship,\
                    'Relationships_Lover':Relationships_Lover, 'Relationships_In_A_Relationship':Relationships_In_A_Relationship,\
                    'Relationships_Play_Partners':Relationships_Play_Partners,'Relationships_Friend_With_Benefits':Relationships_Friend_With_Benefits,\
                    'Relationships_Dating':Relationships_Dating, 'Relationships_Single':Relationships_Single, \
                    'D_s_Relationships_Not_Applicable':D_s_Relationships_Not_Applicable, 'D_s_Relationships_Presently_Inactive': D_s_Relationships_Presently_Inactive,\
                    'D_s_Relationships_Its_Complicated':D_s_Relationships_Its_Complicated, 'D_s_Relationships_unpartnered':D_s_Relationships_unpartnered,\
                    'D_s_Relationships_unowned':D_s_Relationships_unowned, 'D_s_Relationships_trainee':D_s_Relationships_trainee,\
                    'D_s_Relationships_student':D_s_Relationships_student, 'D_s_Relationships_being_mentored':D_s_Relationships_being_mentored,\
                    'D_s_Relationships_in_chastity':D_s_Relationships_in_chastity, 'D_s_Relationships_Keyholder':D_s_Relationships_Keyholder,\
                    'D_s_Relationships_brat':D_s_Relationships_brat, 'D_s_Relationships_babyboy':D_s_Relationships_babyboy,\
                    'D_s_Relationships_babygirl':D_s_Relationships_babygirl, 'D_s_Relationships_boy':D_s_Relationships_boy,\
                    'D_s_Relationships_girl':D_s_Relationships_girl, 'D_s_Relationships_toy':D_s_Relationships_toy,\
                    'D_s_Relationships_pet':D_s_Relationships_pet, 'nickname':Nickname,'url':URL,'age':Age,\
                    'role':Role,'gender':Gender,'Location_Country':Location_Country,'Location_Administrative_area':Location_Administrative_area,\
                    'Location_City':Location_City,'Sexual_Orientation':Sexual_Orientation,'How_active':How_active,\
                    'Looking_for_A_Lifetime_Relationship_LTR':Looking_for_A_Lifetime_Relationship_LTR,\
                    'Looking_for_A_Relationship':Looking_for_A_Relationship,\
                    'Looking_for_A_Mentor_Teacher':Looking_for_A_Mentor_Teacher,\
                    'Looking_for_Someone_To_Play_With':Looking_for_Someone_To_Play_With,\
                    'Looking_for_A_Princess_By_Day_Slut_By_Night':Looking_for_A_Princess_By_Day_Slut_By_Night,\
                    'Looking_for_Friendship':Looking_for_Friendship,'Looking_for_A_Master':Looking_for_A_Master,\
                    'Looking_for_A_Mistress':Looking_for_A_Mistress,'Looking_for_A_sub':Looking_for_A_sub,\
                    'Looking_for_A_slave':Looking_for_A_slave,'Looking_for_Events':Looking_for_Events,\
                    'Looking_for_None':Looking_for_None,'D_s_Relationships_Dominant':D_s_Relationships_Dominant,\
                    'D_s_Relationships_Sadist':D_s_Relationships_Sadist,\
                    'D_s_Relationships_Sadomasochist':D_s_Relationships_Sadomasochist,\
                    'D_s_Relationships_Master':D_s_Relationships_Master,'D_s_Relationships_Mistress':D_s_Relationships_Mistress,\
                    'D_s_Relationships_Owner':D_s_Relationships_Owner,\
                    'D_s_Relationships_Master_and_Owner':D_s_Relationships_Master_and_Owner,\
                    'D_s_Relationships_Mistress_and_Owner':D_s_Relationships_Mistress_and_Owner,\
                    'D_s_Relationships_Top':D_s_Relationships_Top,'D_s_Relationships_Daddy':D_s_Relationships_Daddy,\
                    'D_s_Relationships_Mommy':D_s_Relationships_Mommy,'D_s_Relationships_Brother':D_s_Relationships_Brother,\
                    'D_s_Relationships_Sister':D_s_Relationships_Sister,'D_s_Relationships_Being_Served':D_s_Relationships_Being_Served,\
                    'D_s_Relationships_Considering':D_s_Relationships_Considering,'D_s_Relationships_Protecting':D_s_Relationships_Protecting,'D_s_Relationships_Mentoring':D_s_Relationships_Mentoring,'D_s_Relationships_Teaching':D_s_Relationships_Teaching,'D_s_Relationships_Training':D_s_Relationships_Training,'D_s_Relationships_Switches':D_s_Relationships_Switches,'D_s_Relationships_submissive':D_s_Relationships_submissive,'D_s_Relationships_masochist':D_s_Relationships_masochist,'D_s_Relationships_bottom':D_s_Relationships_bottom,'D_s_Relationships_owned_and_collared':D_s_Relationships_owned_and_collared,'D_s_Relationships_owned':D_s_Relationships_owned,'D_s_Relationships_property':D_s_Relationships_property,'D_s_Relationships_collared':D_s_Relationships_collared,'D_s_Relationships_slave':D_s_Relationships_slave,'D_s_Relationships_kajira':D_s_Relationships_kajira,'D_s_Relationships_kajirus':D_s_Relationships_kajirus,'D_s_Relationships_in_service':D_s_Relationships_in_service,'D_s_Relationships_under_protection':D_s_Relationships_under_protection,'D_s_Relationships_under_consideration':D_s_Relationships_under_consideration}

    #print user_details
    
    if not user_exists:
        con.execute(meta.tables['users'].insert(), user_details)
    elif user_exists:
        con.execute(meta.tables['users'].update().where(users.c.id == user_exists['id']), user_details)

    user_id = (con.execute(users.select().where(users.c.id_user == int(id_user)))).fetchone()['id']

    ## Pictures
    try:
        Pictures = getBottomElement(bottom, 'Latest pictures').split(';')
        i  = 2
        for picture in Pictures:
            if len(picture)>5:
                downloadImage(picture.strip(), str(id_user) + '_'+str(i) )
                i+=1
                picture_details  = {'picture_location':picture, 'user_id':user_id}
                
                if not user_exists:
                    con.execute(meta.tables['pictures'].insert(), picture_details)
                elif user_exists:
                    con.execute(meta.tables['pictures'].delete().where(pictures.c.user_id == int(user_id)))
                    con.execute(meta.tables['pictures'].insert(), picture_details)
    except:
        pass

    ## Website data
    try:
        Websites = getBottomElement(bottom, 'Websites').split('\n')[1:-1]
        for website in Websites:
            website_details  = {'website_name':website, 'user_id':user_id}
            if not user_exists:
                con.execute(meta.tables['websites'].insert(), website_details)
            elif user_exists:
                con.execute(meta.tables['websites'].delete().where(users.c.user_id == int(user_id)))
                con.execute(meta.tables['websites'].insert(), website_details)
    except Exception,e:
        print str(e)
        pass

    ## Groups data        
    try:
        Groups_member_of, Group_Ids = getListElement(listElem, 'Groups member of')
        Groups_member_of = Groups_member_of.split('\n')
        count = 0
        for group in Groups_member_of:
            group_details  = {'group_name':group.strip(), 'user_id':user_id, 'group_id': int(Group_Ids[count])}
            count+=1
            if not user_exists:
                con.execute(meta.tables['groups'].insert(), group_details)
            elif user_exists:
                con.execute(meta.tables['groups'].delete().where(groups.c.user_id == int(user_id)))
                con.execute(meta.tables['groups'].insert(), group_details)
    except:
        pass

    ## Fetishes    
    try:
        Fetishes, Fetish_ids = getBottomElement(bottom, 'Fetishes')
        Fetishes = Fetishes.split('\n')
        Fetish_ids = Fetish_ids.split(',')
    except:
        Fetishes = ''
    options = ['Into:', 'Curious about:', 'Soft limit:', 'Hard limit:']
    for option in options:
        try:
            option_idx = Fetishes.index(option)
            values = Fetishes[option_idx+1].split(',')
            values = [v.strip() for v in values]
            fetish_id = Fetish_ids[int(option_idx/2)]

            for value in values:
                the_fetish = re.findall(r'(.*?)\s\(', value)[0].replace('"','').strip()
                how_they_like_it = re.findall(r'\((.*?)\)', value)[0]

                fetish_details = {'option':option, 'the_fetish':the_fetish,\
                                  'how_they_like_it':how_they_like_it, 'user_id':user_id, 'fetish_id':int(fetish_id)}
            
                if not user_exists:
                    con.execute(meta.tables['fetishes'].insert(), fetish_details)
                elif user_exists:
                    con.execute(meta.tables['fetishes'].delete().where(fetishes.c.user_id == int(user_id)))
                    con.execute(meta.tables['fetishes'].insert(), fetish_details)
        except:
            pass


numProfilesScraped = 0
users = meta.tables['users']
websites = meta.tables['websites']
fetishes = meta.tables['fetishes']
groups = meta.tables['groups']
pictures = meta.tables['pictures']
pg_idx = 0
while True:
    try:
        pg_idx+=1
        url_new = url + '?page=' + str(pg_idx)
        print url_new
        br.open(url_new)
        print br.title()
        html = br.response().read()
        soup = BeautifulSoup(html, 'lxml')
        s = soup.findAll(attrs = {'class':'fl-margin--b-l fl-float--left fl-width--half'})
        print len(s)

        for i in s:
            later = time.time()
            difference = int(later - now)
            if maxtime !=0:
                if difference > maxtime:
                    print 'Maximum time of profiles scraped. Exiting!'
                    sys.exit(1)
            username = i.find(attrs={'class':'fl-member-card__user'}).getText()
            user_url = i.find(attrs={'class':'fl-member-card__user'})['href']
            try:
                info = i.find(attrs={'class':'fl-member-fl-member-card__info'}).getText()
            except:
                info = i.find(attrs={'class':'fl-member-card__info'}).getText()
            location = i.find(attrs={'class':'fl-member-card__location'}).getText()

            print username, user_url
            id_user = re.findall(r'\d+', user_url)[0]
            
            user_exists = (con.execute(users.select().where(users.c.id_user == int(id_user)))).fetchone()
            print 'user_exists', user_exists
            if newonly == 1 and user_exists:
                pass
            elif newonly == 1 and not user_exists:
                getUserDetails(user_url, info, location, username, con, meta, user_exists, websites, fetishes, groups, pictures, D_s_Relationships_values, Relationships_values)
                numProfilesScraped +=1
            elif newonly == 0 and user_exists:
                getUserDetails(user_url, info, location, username, con, meta, user_exists, websites, fetishes, groups, pictures, D_s_Relationships_values, Relationships_values)
                numProfilesScraped +=1
            elif newonly == 0 and not user_exists:
                getUserDetails(user_url, info, location, username, con, meta, user_exists, websites, fetishes, groups, pictures, D_s_Relationships_values, Relationships_values)
                numProfilesScraped +=1
                
            print 'numProfilesScraped', numProfilesScraped   
            if maxprofiles !=0:
                if numProfilesScraped > maxprofiles:
                    print 'Maximum number of profiles scraped. Exiting!'
                    sys.exit(1)
            wait_time = random.randint(mindelay, maxdelay)
            print 'waiting for', wait_time, 'seconds...'
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print '\nPausing...  (Hit ENTER to continue, type quit to exit.)'
        try:
            response = raw_input()
            if response == 'quit':
                break
            print 'Resuming...'
        except KeyboardInterrupt  :
            print 'Resuming...'
            continue


