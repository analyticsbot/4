import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Index
 
Base = declarative_base()
 
class Users(Base):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    nickname = Column(String(10485760), nullable=True)
    id_user = Column(Integer)
    url = Column(String(10485760), nullable=True)
    age = Column(Integer, nullable=True)
    
    role = Column(String(10485760), nullable=True)
    gender = Column(String(10485760), nullable=True)
    Location_Country = Column(String(10485760), nullable=True)
    Location_Administrative_area = Column(String(10485760), nullable=True)
    Location_City = Column(String(10485760), nullable=True)
    Sexual_Orientation = Column(String(10485760), nullable=True)
    How_active = Column(String(10485760), nullable=True)
    Looking_for_A_Lifetime_Relationship_LTR = Column(Boolean, nullable=True)
    Looking_for_A_Relationship = Column(Boolean, nullable=True)
    Looking_for_A_Mentor_Teacher = Column(Boolean, nullable=True)
    Looking_for_Someone_To_Play_With = Column(Boolean, nullable=True)
    Looking_for_A_Princess_By_Day_Slut_By_Night = Column(Boolean, nullable=True)
    Looking_for_Friendship = Column(Boolean, nullable=True)
    Looking_for_A_Master = Column(Boolean, nullable=True)
    Looking_for_A_Mistress = Column(Boolean, nullable=True)
    Looking_for_A_sub = Column(Boolean, nullable=True)
    Looking_for_A_slave = Column(Boolean, nullable=True)
    Looking_for_Events = Column(Boolean, nullable=True)
    Looking_for_None = Column(Boolean, nullable=True)

    D_s_Relationships_Dominant = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Sadist = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Sadomasochist = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Master = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Mistress = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Owner = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Master_and_Owner = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Mistress_and_Owner = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Top = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Daddy = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Mommy = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Brother = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Sister = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Being_Served = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Considering = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Protecting = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Mentoring = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Teaching = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Training = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Switches = Column(ARRAY(String), nullable=True)
    D_s_Relationships_submissive = Column(ARRAY(String), nullable=True)
    D_s_Relationships_masochist = Column(ARRAY(String), nullable=True)
    D_s_Relationships_bottom = Column(ARRAY(String), nullable=True)
    D_s_Relationships_owned_and_collared = Column(ARRAY(String), nullable=True)
    D_s_Relationships_owned = Column(ARRAY(String), nullable=True)
    D_s_Relationships_property = Column(ARRAY(String), nullable=True)
    D_s_Relationships_collared = Column(ARRAY(String), nullable=True)
    D_s_Relationships_slave = Column(ARRAY(String), nullable=True)
    D_s_Relationships_kajira = Column(ARRAY(String), nullable=True)
    D_s_Relationships_kajirus = Column(ARRAY(String), nullable=True)
    D_s_Relationships_in_service = Column(ARRAY(String), nullable=True)
    D_s_Relationships_under_protection = Column(ARRAY(String), nullable=True)
    D_s_Relationships_under_consideration = Column(ARRAY(String), nullable=True)
    D_s_Relationships_pet = Column(ARRAY(String), nullable=True)
    D_s_Relationships_toy = Column(ARRAY(String), nullable=True)
    D_s_Relationships_girl = Column(ARRAY(String), nullable=True)
    D_s_Relationships_boy = Column(ARRAY(String), nullable=True)
    D_s_Relationships_babygirl = Column(ARRAY(String), nullable=True)
    D_s_Relationships_babyboy = Column(ARRAY(String), nullable=True)
    D_s_Relationships_brat = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Keyholder = Column(ARRAY(String), nullable=True)
    D_s_Relationships_in_chastity = Column(ARRAY(String), nullable=True)
    D_s_Relationships_being_mentored = Column(ARRAY(String), nullable=True)
    D_s_Relationships_student = Column(ARRAY(String), nullable=True)
    D_s_Relationships_trainee = Column(ARRAY(String), nullable=True)
    D_s_Relationships_unowned = Column(ARRAY(String), nullable=True)
    D_s_Relationships_unpartnered = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Its_Complicated = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Presently_Inactive = Column(ARRAY(String), nullable=True)
    D_s_Relationships_Not_Applicable = Column(ARRAY(String), nullable=True)
    D_s_Relationships_unknown = Column(Boolean, nullable=True)
    
    Relationships_Single = Column(ARRAY(String), nullable=True)
    Relationships_Dating = Column(ARRAY(String), nullable=True)
    Relationships_Friend_With_Benefits = Column(ARRAY(String), nullable=True)
    Relationships_Play_Partners = Column(ARRAY(String), nullable=True)
    Relationships_In_A_Relationship = Column(ARRAY(String), nullable=True)
    Relationships_Lover = Column(ARRAY(String), nullable=True)
    Relationships_In_An_Open_Relationship = Column(ARRAY(String), nullable=True)
    Relationships_Widow = Column(ARRAY(String), nullable=True)
    Relationships_Widower = Column(ARRAY(String), nullable=True)
    Relationships_Engaged = Column(ARRAY(String), nullable=True)
    Relationships_Married = Column(ARRAY(String), nullable=True)
    Relationships_Monogamous = Column(ARRAY(String), nullable=True)
    Relationships_Polyamorous = Column(ARRAY(String), nullable=True)
    Relationships_In_A_Poly_Group = Column(ARRAY(String), nullable=True)
    Relationships_In_A_Leather_Family = Column(ARRAY(String), nullable=True)
    Relationships_In_a_Pack = Column(ARRAY(String), nullable=True)
    Relationships_In_a_Rope_Family = Column(ARRAY(String), nullable=True)
    Relationships_Member_Of_A_House = Column(ARRAY(String), nullable=True)    
    Relationships_Its_Complicated = Column(ARRAY(String), nullable=True)
    Relationships_unknown = Column(Boolean, nullable=True)

    About_me = Column(String(10485760), nullable=True)
    Latest_activity = Column(String(10485760), nullable=True)
    Latest_activity_time = Column(Date, nullable=True)
    Number_of_friends = Column(String(10485760), nullable=True)
    Contact_status_Our_Conversations = Column(String(10485760), nullable=True)
    Profile_picture = Column(String(10485760), nullable=True)
    Date_first_crawled = Column(String(10485760), nullable=True)
    Most_recent_date_updated = Column(String(10485760), nullable=True)

    Index('fet', 'age', 'role', 'gender', 'Location_Country','Location_Administrative_area'\
          , 'Location_City', 'Sexual_Orientation', 'How_active', 'Looking_for_A_Lifetime_Relationship_LTR',
            'Looking_for_A_Relationship', 'Looking_for_A_Mentor_Teacher', 'Looking_for_Someone_To_Play_With' , \
                                          'Looking_for_A_Princess_By_Day_Slut_By_Night' , 'Looking_for_Friendship' , \
                                          'Looking_for_A_Master' , 'Looking_for_A_Mistress' , 'Looking_for_A_sub' , \
                                          'Looking_for_A_slave' , 'Looking_for_Events' , 'Looking_for_None' , \
                                          'D_s_Relationships_Dominant' , 'D_s_Relationships_Sadist' , \
                                          'D_s_Relationships_Sadomasochist' , 'D_s_Relationships_Master' , \
                                          'D_s_Relationships_Mistress' , 'D_s_Relationships_Owner' , \
                                          'D_s_Relationships_Master_and_Owner' , 'D_s_Relationships_Mistress_and_Owner' , \
                                          'D_s_Relationships_Top' , 'D_s_Relationships_Daddy' , 'D_s_Relationships_Mommy' , \
                                          'D_s_Relationships_Brother' , 'D_s_Relationships_Sister' , \
                                          'D_s_Relationships_Being_Served' , 'D_s_Relationships_Considering' , \
                                          'D_s_Relationships_Protecting' , 'D_s_Relationships_Mentoring' , \
                                          'D_s_Relationships_Teaching' , 'D_s_Relationships_Training' , \
                                          'D_s_Relationships_Switches' , 'D_s_Relationships_submissive' , \
                                          'D_s_Relationships_masochist' , 'D_s_Relationships_bottom' , \
                                          'D_s_Relationships_owned_and_collared' , 'D_s_Relationships_owned' , \
                                          'D_s_Relationships_property' , 'D_s_Relationships_collared' , \
                                          'D_s_Relationships_slave' , 'D_s_Relationships_kajira' , \
                                          'D_s_Relationships_kajirus' , 'D_s_Relationships_in_service' , \
                                          'D_s_Relationships_under_protection' , 'D_s_Relationships_under_consideration' ,\
                                          'D_s_Relationships_pet' , 'D_s_Relationships_toy' , 'D_s_Relationships_girl' , \
                                          'D_s_Relationships_boy' , 'D_s_Relationships_babygirl' , \
                                          'D_s_Relationships_babyboy' , 'D_s_Relationships_brat' , \
                                          'D_s_Relationships_Keyholder' , 'D_s_Relationships_in_chastity' , \
                                          'D_s_Relationships_being_mentored' , 'D_s_Relationships_student' , \
                                          'D_s_Relationships_trainee' , 'D_s_Relationships_unowned' , \
                                          'D_s_Relationships_unpartnered' , 'D_s_Relationships_Its_Complicated' , \
                                          'D_s_Relationships_Presently_Inactive' , 'D_s_Relationships_Not_Applicable' , \
                                          'D_s_Relationships_unknown' , 'Relationships_Single' , 'Relationships_Dating' ,\
                                          'Relationships_Friend_With_Benefits' , 'Relationships_Play_Partners' ,\
                                          'Relationships_In_A_Relationship' , 'Relationships_Lover' , \
                                          'Relationships_In_An_Open_Relationship' , 'Relationships_Widow' , \
                                          'Relationships_Widower' , 'Relationships_Engaged' , 'Relationships_Married' ,\
                                          'Relationships_Monogamous' , 'Relationships_Polyamorous' , \
                                          'Relationships_In_A_Poly_Group' , 'Relationships_In_A_Leather_Family' , \
                                          'Relationships_In_a_Pack' , 'Relationships_In_a_Rope_Family' ,\
                                          'Relationships_Member_Of_A_House' , 'Relationships_Its_Complicated' , \
                                          'Relationships_unknown' , 'About_me' , 'Latest_activity' , \
                                          'Latest_activity_time' , 'Number_of_friends' , 'Contact_status_Our_Conversations' ,\
                                          'Profile_picture' , 'Date_first_crawled' , 'Most_recent_date_updated' )
 
class Websites(Base):
    __tablename__ = 'websites'
    # Here we define columns for the
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    website_name = Column(String(10485760))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

class Groups(Base):
    __tablename__ = 'groups'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    group_name = Column(String(10485760))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)
    group_id = Column(Integer)
    Index('idx_gp', 'group_name', 'group_id', 'user_id')

class Pictures(Base):
    __tablename__ = 'pictures'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    picture_location = Column(String(10485760))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)

class Fetishes(Base):
    __tablename__ = 'fetishes'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    option = Column(String(10485760))
    the_fetish = Column(String(10485760))
    how_they_like_it = Column(String(10485760))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)
    fetish_id = Column(Integer)
    Index('idx_2', 'the_fetish', 'how_they_like_it', 'user_id', 'fetish_id')
    
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('postgresql://postgres:postgres@localhost/Fetlife1')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)