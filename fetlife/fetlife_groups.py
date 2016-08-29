import mechanize, datetime, time, sqlite3, sqlalchemy, re
from bs4 import BeautifulSoup
from text_unidecode import unidecode

nickname = 'b3159584'
password = 'facebook'
url = 'https://fetlife.com/countries/84/kinksters'
br = mechanize.Browser()
br.set_handle_robots(False)
br.open('https://fetlife.com/login')
br.select_form(nr=0)
br.form.new_control('text', 'nickname_or_email', {'value': nickname})
br.form.new_control('password', 'password', {'value': password})
resp = br.submit()

time.sleep(2)

def getElement(table, name):    
    for el in table:
        try:
            if el.find('th').getText() == name:
                return el.find('td')
        except:
            return 'NA'

def getBottomElement(bottom, name):    
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
            return 'NA'

def getListElement(listElem, name):    
    for l in listElem:
        try:
            if l.findPreviousSibling().getText().strip() == name.strip():                
                return l.getText().strip()
        except:
            return 'NA' 

def getLookingForStatus(Looking_for_options, name):
    if name in Looking_for_options:
        return 1
    else:
        return 0

def getDSRelationshipStatus(D_s_Relationships, name):
    for relation in D_s_Relationships:
        if name in relation:
            return 1, relation.split()[-1]
        else:
            return 0

def getRelationshipStatus(Relationships, name):
    for relation in D_s_Relationships:
        if name in relation:
            return 1, relation.split()[-1]
        else:
            return 0
        
def getUserDetails(user_url, info, location, username):
    br.open('https://fetlife.com/' + user_url)
    html = br.response().read()
    soup = BeautifulSoup(html)
    bottom = soup.findAll(attrs = {'class':'bottom'})
    table = soup.findAll("tr")
    listElem = soup.findAll(attrs={'class':'list'})
    URL = user_url
    Nickname = username
    Age = info.split()[0].replace('M','').replace('F','')
    if 'M' in info:
        Gender = 'M'
    else:
        Gender = 'F'
    Role = info.split()[1]
    Location_Country = location.split(',')[-1].strip().replace('\n','')
    Location_Administrative_area = location.split(',')[-2].strip().replace('\n','')
    try:
        Location_City = location.split(',')[-3].strip().replace('\n','')
    except:
        Location_City = ''
    
    Sexual_Orientation = getElement(table, 'orientation:').getText()
    How_active  = getElement(table, 'active:')
    Looking_for = getElement(table, 'is looking for:')
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
    Looking_for_None = 0 if len(Looking_for_options)==0 else 1

    ## D/S relationship
    D_s_Relationships = getElement(table, 'D/s relationship status:').getText().strip().split('\n')

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
    Relationships = getElement(table, 'relationship status:')}

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
    
    
    About_me = getBottomElement(bottom, 'About me ')
    mini_feed = soup.find(attrs={'id':'mini_feed'})
    Latest_activity = mini_feed.find('li').getText()
    Fetishes = getBottomElement(bottom, 'Fetishes').split('\n')
    options = ['Into:', 'Curious about:', 'Soft limit:', 'Hard limit:']
    for option in options:
        try:
            option_idx = Fetishes.index(option)
            values = Fetishes[option_idx+1].split(',')
            values = [v.strip() for v in values]

            for value in values:
                the_fetish = re.findall(r'(.*?)\s\(', value)
                how_they_like_it = re.findall(r'\((.*?)\)', value)
            
            

    ## create a new table for fetishes
    
    Groups_member_of = getListElement(listElem, 'Groups member of').split('\n')
    Websites = getBottomElement(bottom, 'Websites').split('\n')[1:-1]
    Number_of_friends = soup.find('h4').getText()
    Contact_status_Our_Conversations = 'Our Conversations' in soup.getText()
    if soup.find(attrs = {'id':'friendship_confirm'}):
        Friends_status = True
    else:
        Friends_status = False

    Profile_picture = soup.find(attrs = {'class':'span-6'}).find('img')['src']
    Pictures = getBottomElement(bottom, 'Latest pictures')

    Date_first_crawled = str(datetime.datetime.now())
    Most_recent_date_updated  = str(datetime.datetime.now())
    
pg_idx = 0
while True:
    pg_idx+=1
    url_new = url + '?page=' + str(pg_idx)
    br.open(url_new)
    html = br.response().read()
    soup = BeautifulSoup(html)
    s = soup.findAll(attrs = {'class':'fl-margin--b-l fl-float--left fl-width--half'})
    print len(s)

    for i in s:
        username = i.find(attrs={'class':'fl-member-card__user'}).getText()
        user_url = i.find(attrs={'class':'fl-member-card__user'})['href']
        try:
            info = i.find(attrs={'class':'fl-member-fl-member-card__info'}).getText()
        except:
            info = i.find(attrs={'class':'fl-member-card__info'}).getText()
        location = i.find(attrs={'class':'fl-member-card__location'}).getText()

        #getUserDetails(user_url, info, location, username)




