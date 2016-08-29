## import necessary modules
import mechanize, datetime, time, sqlite3, sqlalchemy, re, argparse, logging
from bs4 import BeautifulSoup
from text_unidecode import unidecode
import random,time,sys
from sqlalchemy import create_engine, MetaData

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

nickname = 'b3159584'
password = 'facebook'
url = 'https://fetlife.com/countries/84/kinksters'
mindelay = 1
maxdelay = 3
maxprofiles = 10
newonly = 0
maxtime = 1000
database = 'postgresql://postgres:postgres@localhost/fetlife'
debug = 1
proxy = 0

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
                x = b.findNextSibling()
                while True:                    
                    if x.name == 'p':
                        value += ' ' + x.getText()
                        x = x.findNextSibling()
                    else:
                        break
                return value.strip()
        except:
            return ''

def getListElement(listElem, name):
    """ function to get the elements in list format
    listElem - all elements in list
    name - name of the element for which value is required
    """
    try:
        for l in listElem:
            try:
                if l.findPreviousSibling().getText().strip() == name.strip():                
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
    try:
        for relation in D_s_Relationships:
            if name in relation:
                return ['1', relation.split()[-1]]
            else:
                return ['0', '']
    except:
        return ['0', '']

def getRelationshipStatus(Relationships, name):
    """ function to get the Relationships values
    Relationships - all Relationships options
    name - name of the element for which value is required
    """
    try:
        for relation in D_s_Relationships:
            if name in relation:
                return ['1', relation.split()[-1]]
            else:
                return ['0', '']
    except:
        return ['0', '']
        
def getUserDetails(user_url, info, location, username, con, meta):
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
    soup = BeautifulSoup(html)
    bottom = soup.findAll(attrs = {'class':'bottom'})
    table = soup.findAll("tr")
    listElem = soup.findAll(attrs={'class':'list'})
    URL = 'https://fetlife.com/' + user_url
    Nickname = username
    try:
        Age = info.split()[0].replace('M','').replace('F','')
    except:
        Age = ''
    if 'M' in info:
        Gender = 'M'
    else:
        Gender = 'F'
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
    Looking_for_options = ''
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

    ## Relationships
    try:
        Relationships = getElement(table, 'relationship status:')
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
    
    
    try:
        About_me = getBottomElement(bottom, 'About me ')
    except:
        About_me = ''
    try:
        mini_feed = soup.find(attrs={'id':'mini_feed'})
        Latest_activity = mini_feed.find('li').getText().replace('\n','').strip()
    except:
        Latest_activity = ''

    ## Fetishes
    
    try:
        Fetishes = getBottomElement(bottom, 'Fetishes').split('\n')
    except:
        Fetishes = ''
    options = ['Into:', 'Curious about:', 'Soft limit:', 'Hard limit:']
    for option in options:
        try:
            option_idx = Fetishes.index(option)
            values = Fetishes[option_idx+1].split(',')
            values = [v.strip() for v in values]

            for value in values:
                the_fetish = re.findall(r'(.*?)\s\(', value)[0]
                how_they_like_it = re.findall(r'\((.*?)\)', value)[0]

                fetish_details = {'option':option, 'the_fetish':the_fetish,\
                                  'how_they_like_it':how_they_like_it}
            
                con.execute(meta.tables['fetishes'].insert(), fetish_details)
        except:
            pass

    ## groups data
        
    try:
        Groups_member_of = getListElement(listElem, 'Groups member of').split('\n')
        for group in Groups_member_of:
            group_details  = {'group_name':group}
            con.execute(meta.tables['groups'].insert(), group_details)
    except:
        pass
    

    ## Website data
    try:
        Websites = getBottomElement(bottom, 'Websites').split('\n')[1:-1]
        for website in Websites:
            website_details  = {'website_name':group}
            con.execute(meta.tables['websites'].insert(), website_details)
    except:
        pass
        
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

    ## Pictures
    try:
        Pictures = getBottomElement(bottom, 'Latest pictures')
        for picture in Pictures:
            picture_details  = {'picture_location':picture}
            con.execute(meta.tables['pictures'].insert(), picture_details)
    except:
        pass

    Date_first_crawled = str(datetime.datetime.now())
    Most_recent_date_updated  = str(datetime.datetime.now())

    user_details = {'Most_recent_date_updated':Most_recent_date_updated, 'Date_first_crawled':Date_first_crawled,\
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

    con.execute(meta.tables['users'].insert(), user_details)

numProfilesScraped = 0
users = meta.tables['users']

pg_idx = 0
while True:
    try:
        pg_idx+=1
        url_new = url + '?page=' + str(pg_idx)
        print url_new
        br.open(url_new)
        print br.title()
        html = br.response().read()
        soup = BeautifulSoup(html)
        s = soup.findAll(attrs = {'class':'fl-margin--b-l fl-float--left fl-width--half'})
        print len(s)

        for i in s:
            later = time.time()
            difference = int(later - now)
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
            user_exists = False
            if newonly == True:
                
                user_exists = (con.execute(users.select().where(users.c.nickname == username))).fetchone()

            if not user_exists:
                getUserDetails(user_url, info, location, username, con, meta)
                numProfilesScraped +=1
                if numProfilesScraped > maxprofiles:
                    print 'Maximum number of profiles scraped. Exiting!'
                    sys.exit(1)
                time.sleep(random.randint(mindelay, maxdelay))

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


