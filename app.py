#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for ,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    # address = db.Column(db.String(120))
    venue_location_id = db.Column(db.Integer, db.ForeignKey('venuelocation.id'),nullable=False )
    venue_location = db.relationship('VenueLocation',backref ='venuel', uselist= False)
    phone = db.Column(db.String(120))                       
    image_link = db.Column(db.String(500),nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    genres_list = db.relationship('VenueGenres', backref='venue')
    Show_list =  db.relationship('Show', backref='venue')
    seeking_talent_id =  db.Column(db.Integer, db.ForeignKey('seekingtalent.id'),nullable=False)
    seeking_talent =  db.relationship('SeekingTalent', backref='venuet', uselist=False)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<Venue ID: {self.id}, Venue Name:{self.name},Venuelocatid:{self.venue_location_id}, phone:{self.phone},Imagelink:{self.image_link},Facebooklink:{self.facebook_link},Seekingtalenid{self.seeking_talent_id}>'
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String)
    first_name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120)) 
    phone = db.Column(db.String(120))
    genres_list = db.relationship('ArtistGenres', backref='artist')
    image_link = db.Column(db.String(500),nullable=False)
    facebook_link = db.Column(db.String(120))
    website_link  = db.Column(db.String(120))
    loction_id = db.Column(db.Integer, db.ForeignKey('artistlocation.id'),nullable=False)
    loction = db.relationship("ArtistLocation",backref='artist',uselist=False)
    Show_list =  db.relationship('Show', backref='artist')
    Seeking_venu_id = db.Column(db.Integer, db.ForeignKey('seekingvenu.id'),nullable=False)
    Seeking_venu = db.relationship('SeekingVenu', backref='artist', uselist=False)
    Artist_Midlle_name = db.relationship('ArtisiMiddlename', backref='artist', uselist=False) 
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<Artist ID: {self.id}, Firstname: {self.first_name} , Lastname: {self.last_name}, phone:{self.phone}, Imagelink:{self.image_link},facebookLink:{self.facebook_link}, Loctionid:{self.loction_id},Seekingvenuid:{self.Seeking_venu_id}>'  
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
# Model Artist_genres 
class ArtistGenres(db.Model):  
    __tablename__ = "artistgenres"
    artist_id =  db.Column(db.Integer,db.ForeignKey('artist.id'),primary_key=True)
    genres = db.Column(db.String(120),primary_key=True,nullable=False)
    def __repr__(self):
        return f'<Artist ID: {self.artist_id}, Genres: {self.genres}>'
# Model Venue_genres
class VenueGenres(db.Model):
    __tablename__ = "venuegenres"
    venue_id =  db.Column(db.Integer,db.ForeignKey('venue.id'),primary_key=True)
    genres = db.Column(db.String(120),primary_key=True,nullable=False)
    def __repr__(self):
        return f'<Venue ID: {self.venue_id}, Genres: {self.genres}>'
# Model Artist_Location
class ArtistLocation(db.Model): 
   __tablename__ = "artistlocation"
   id = db.Column(db.Integer, primary_key=True)
   city = db.Column(db.String(120), nullable=False)
   state = db.Column(db.String(120))
def __repr__(self):
        return f'<City: {self.city}, Genres: {self.state}>'
# Model  SeekingVenu one to one relation with Aritst
class SeekingVenu(db.Model):
    __tablename__ = 'seekingvenu'
    id = db.Column(db.Integer, primary_key=True)
    seeking_venue = db.Column(db.Boolean,default = False)
    seeking_description = db.Column(db.String(500),default = 'Not currently seeking performance venues')
def __repr__(self):
    return f'<Seeking Venue Id: {self.seeking_venue_id}, SeekingVenue: {self.seeking_venue}, SeekingDescription: {self.seeking_description}>' 
# Model Artisi (Middle name) one to one relation with Aritst
class ArtisiMiddlename(db.Model):
    __tablename__ = 'artisimiddlename'
    middlename_id = db.Column(db.Integer, primary_key=True)
    middlename = db.Column(db.String(),default="Amy")
    # Artist_middlename = db.relationship("Artist", back_populates="ArtisiMiddlename", uselist=False)
    artist_id = db.Column(db.Integer,db.ForeignKey('artist.id'),unique=True,nullable=False)
def __repr__(self):
    return f'<Seeking Venue Id: {self.middlename_id}, {self.artist_id},{self.middlename}>'
#Model VenueLocation  Many to one  relation with Venue Model
class VenueLocation(db.Model): 
   __tablename__ = "venuelocation"
   id = db.Column(db.Integer, primary_key=True)
   city_venue = db.Column(db.String(120), nullable=False)
   state_venue = db.Column(db.String(120),nullable=False)
   street_number = db.Column(db.Integer,nullable=False)
   street_name  = db.Column(db.String(120),nullable=False)
    
def __repr__(self):
    return f'<city venue: {self.city_venue},state venue:{self.state_venue}, street number: {self.street_number}, streetname {self.street_name}>'

#Venue Seeking to Talent one to one relation by Many to one relationship
class SeekingTalent(db.Model):
   __tablename__ = 'seekingtalent'
   id = db.Column(db.Integer,primary_key=True)
   seeking_talent = db.Column(db.Boolean,default = False)
   seeking_description = db.Column(db.String(500),default = 'Not currently seeking talent')
  #  parent = db.relationship("Venue", back_populates="seekingtalent", uselist=False)
def __repr__(self):
    return f'<Seeking Talent Id: {self.seeking_talent_id }, SeekingTalent: {self.seeking_talent}, SeekingDescription: {self.seeking_description}>' 

#Show Model for Venue and Artist 
class Show(db.Model):
   __tablename__ = 'show'
   id = db.Column(db.Integer,primary_key=True)
   artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
   venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
   star_date = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)  
def __repr__(self):
    return f'<Seeking Talent Id: {self.artist_id }, SeekingTalent: {self.venue_id},Start Date:{self.star_date}>' 


 




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)
  # return babel.dates.format_datetime(date, format,locale='en')
app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
 
@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data. 
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venushow =  Venue.query.all()
  location = db.session.query( VenueLocation.state_venue,VenueLocation.city_venue, Venue.venue_location_id,Venue.name ,Venue.id).join(VenueLocation).all()
  print(location)
  check1=False
  temp=[]
  tem=''
  d = (len(temp))
  location = db.session.query( VenueLocation.state_venue,VenueLocation.city_venue, Venue.venue_location_id,Venue.name ,Venue.id).join(VenueLocation).all()
  city_venue=''
  state_venue=''
  recorder ={'city_venue':'', 'state_venue':'','venus':[{'name':''}]    }
  # ciyt= VenueLocation.query.distintc(VenueLocation.state_venue,VenueLocation.city_venue).all()
  j=0
  venus=[]
  city = db.session.query(VenueLocation.city_venue, VenueLocation.state_venue).distinct(VenueLocation.city_venue,VenueLocation.state_venue).all()
  # print(city)
  # print(tem)
  for i in city : 
     print(i.city_venue)
  for i in location :
      for j in temp :
        if j!=[]:
           if temp[d] == i.city_venue : 
              temp[j]['venus'].append({'name':i.name})
         
        #  for i in temp:
        #    i.venus.append({'name':i.name})
        #    print(up)
         
        #  temp.append(i.name)
        #  check1= False
          
        #  print(tem)
        else: 
         recorder ={'city_venue':i.city_venue, 'state_venue':i.state_venue,'venus':[{'name':i.name}]    }
      #  temp.append(i.city_venue)
         temp.append(recorder)
      #  temp.append(i.name)
         tem=i.city_venue
         j+=1
  # if check1:
             
  print(temp)
  print(tem)
  print(tem)
  # for i in location :   temprory good
    
  #   if  i.city_venue==tem:    
  #        temp.append(i.name)
         
          
  #        print(tem)
  #   elif i.city_venue!=tem:
  #      temp.append(i.city_venue)
  #      temp.append(i.name)
  #      tem=i.city_venue
  # Vlocation = Venue.query.join('venuelocation').filter_by(Venue.id==VenueLocation.id).all()
  # Vlocation = db.session.query(Venue).join(VenueLocation).all()
  # x = temp.index("cherry") 
  # print(x)
  # for i in location:
  #                         #  x = fruits.index("cherry")
  #     if i.city_venue==temp:
          
  #     elif i.city_venue!=temp:
  #         print(i)
  #     if i.id == i.venue_location_id and i.city_venue != temp:
  #          print(i.name )
  #     temp=i.city_venue 
   # elif (i.city_venue!=temp): 
  #   if i.id == i.venue_location_id and i.city_venue == temp:        
  #      for i in location:
  #        if(i.city_venue!=temp):
  #            print(i.name)
  #       #  elif i.city_venue==temp: 
  #       #     print(i.name)
  #   temp=i.city_venue
  # # datavnue=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop"}]
  #        datavnue[0].

       

  # print(Vlocation) 
 
 # venushow
#  data= [{
#     "city": "San Francisco",
#     "state": "CA",
#     "venues": [{
#       "id": 1,
#       "name": "The Musical Hop",
#       "num_upcoming_shows": 0,
#     }, {
#       "id": 3,
#       "name": "Park Square Live Music & Coffee",
#       "num_upcoming_shows": 1,
#     }]
#   }, {
#     "city": "New York",
#     "state": "NY",
#     "venues": [{
#       "id": 2,
#       "name": "The Dueling Pianos Bar",
#       "num_upcoming_shows": 0,
#     }]
#   }]
  return render_template('pages/venues.html', areas=venushow,temp=temp, cityv=city);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  # LIKE: query.filter(User.name.like('%ed%')) 
  # venuIlike =   ILIKE (case-insensitive LIKE): query.filter(Venue.name.ilike('%emmd%')) 
  searchname = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  print(searchname.count()) 
  count=searchname.count()
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  } 
  return render_template('pages/search_venues.html', results=searchname,count=count ,search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  datavenue= Venue.query.filter(Venue.id==venue_id).first() 

  upshowcount = Show.query.join(Artist.Show_list).filter(Show.venue_id == venue_id).filter(Show.star_date > datetime.utcnow()).count()
  pastshowcount = Show.query.join(Artist.Show_list).filter(Show.venue_id == venue_id).filter(Show.star_date < datetime.utcnow()).count()
  past_shows=  db.session.query(Artist,Show).join(Artist.Show_list).filter(Show.venue_id == venue_id).filter(Show.star_date < datetime.utcnow()).all()
  upcoming_shows = db.session.query(Artist,Show).join(Artist.Show_list).filter(Show.venue_id == venue_id).filter(Show.star_date > datetime.utcnow()).all()
 



  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]                                                                                     
  return render_template('pages/show_venue.html', venue=datavenue, upcoming_shows_count=upshowcount,upcoming_shows=upcoming_shows,past_shows_count=pastshowcount,past_shows=past_shows )

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  
    eror = False
    try:
     city_venue = request.form.get('city_venue')
     state_venue = request.form.get('state_venue')
     street_number = request.form.get('street_number')
     street_name = request.form.get('street_name')
     venueLocation = VenueLocation(city_venue=city_venue,state_venue=state_venue,
                                  street_number=street_number,street_name=street_name)
     db.session.add(venueLocation)   
     db.session.commit()
    except:
     eror = True
     db.session.rollback()
     print(sys.exc_info())
     flash('Eroere in Enter street_number')
    #add value venue genner                              
    # genres = request.form.getlist('genres')
    # venueGenres = VenueGenres( genres=genres )
    #add seekingTalent in venu
    try:
      poptextarea = request.form.get('seekingtalent',None)
      checkbox = request.form.get('checkbox')
      # print(checkbox)
    # print(poptextarea,checkbox ,sep='\n')
      if checkbox :
         checkbox =True 
         seekingTalent = SeekingTalent(seeking_talent=checkbox, seeking_description=poptextarea)
      else:
         checkbox =False  
         seekingTalent = SeekingTalent(seeking_talent=checkbox)
    # to commit venueLocation and talent seekimg tables
    # db.session.add(venueLocation)
      db.session.add(seekingTalent)
      db.session.commit() 
    except: 
       eror = True
       db.session.rollback()
       print(sys.exc_info())
       flash('Eroere in Enter seekingtalent')
    #vaues table esstainal to make value ready of other table   
    name = request.form.get('name')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')  
     
    try:
      venu= Venue(name=name ,phone=phone,image_link= image_link,
                facebook_link =facebook_link ,website_link=website_link,venue_location_id=venueLocation.id,seeking_talent_id=seekingTalent.id)   
      db.session.add(venu)
      db.session.commit() 
    except: 
      eror = True
      db.session.rollback()
      print(sys.exc_info())
      flash('venue was not Seccussfully you should enter different name for venue')
    # db.session.add(venueLocation)
    # db.session.add(seekingTalent)
       
    try:  
    # db.session.add(venu)
       genres = request.form.getlist('genres')
       for i in genres : 
          venueGenres = VenueGenres( genres=i,venue_id=venu.id)
          db.session.add(venueGenres)
       db.session.commit()
       db.session.close() 
    except:
      eror=True
      db.session.rollback
      flash('venue was not Seccussfully you should enter different name for venue')
    
    finally:
       db.session.close()
       if not eror:  
          flash('venue was Seccussfully ')
     
    print(poptextarea,checkbox ,sep='\n')
    print(name, phone , image_link , facebook_link,website_link, city_venue,state_venue, street_number,street_name,sep="\n")
  # return jsonify({"nane": name })
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  search_term=request.form.get('search_term', '')
  artist_check_id=  Artist.query.order_by(Artist.id).all()
  # print(artist_check_id)

  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  return render_template('pages/artists.html', artists=artist_check_id)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  join = Artist.first_name+Artist.last_name
  query = Artist.query.filter(Artist.last_name == search_term)
  searchfirstname = Artist.query.filter(join.ilike(f'%{search_term}%'))
  if(searchfirstname.count()==0):
     searchfirstname = Artist.query.filter(Artist.first_name.ilike(f'%{search_term}%'))
  print(query.count())
  print(searchfirstname.count())
  count = searchfirstname.count()
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=searchfirstname,count=count ,search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  dataar =  Artist.query.filter(Artist.id == artist_id).first()
  upshowcount = db.session.query(Venue.name,Venue.image_link,Show).join(Venue.Show_list).filter(Show.artist_id == artist_id).filter(Show.star_date > datetime.utcnow()).count() 
  pastshowcount = db.session.query(Venue.name,Venue.image_link,Show).join(Venue.Show_list).filter(Show.artist_id == artist_id).filter(Show.star_date < datetime.utcnow()).count() 
  # upcoming_shows= Show.query.filter(Show.artist_id == artist_id).filter(Show.star_date > datetime.utcnow()).all()
  # test = db.session.query(Artist).join(Show, Show.artist_id == artist_id  ).filter(Show.artist_id == artist_id).filter(Show.star_date > datetime.utcnow()).all() 
  # print(test)
  past_shows=  db.session.query(Venue.name,Venue.image_link,Show).join(Venue.Show_list).filter(Show.artist_id == artist_id).filter(Show.star_date < datetime.utcnow()).all()
  # past_showsmh=  db.session.query(Venue.name,Venue.image_link,Show).join(Venue.Show_list).filter(Show.artist_id == artist_id).filter(Show.star_date < datetime.utcnow()).count() 
  # print(past_showsmh) 
  upcoming_shows = db.session.query(Venue.name,Venue.image_link,Show).join(Venue.Show_list).filter(Show.artist_id == artist_id).filter(Show.star_date > datetime.utcnow()).all()
  # joinvenuandatrist = db.session.query(Venue,Artist).join(Artist).filter(Show.artist_id == artist_id).filter(Show.star_date > datetime.utcnow()).all()
  # print(joinvenuandatrist)
  # c = dataar.count() upcoming_shows
  d = 0
  # print(past_shows[0].Show.venue_id)
  # print(upcoming_shows) 
  # if upshow[0].star_date > datetime.utcnow():
  #      d+=1
  # print(d)
  # print(pastshowcount)
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  # data = list(filter(Artist.id== artist_id,artist_check_id))[0]                                     upcoming_shows
  return render_template('pages/show_artist.html', artist=dataar,past_shows_count=pastshowcount,upcoming_shows_count=upshowcount,upcoming_showsm=upcoming_shows,past_showsm=past_shows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # first_name = request.form.get('first_name')
  # last_name = request.form.get('last_name')
  # phone = request.form.get('phone')
  # image_link = request.form.get('image_link')
  # facebook_link = request.form.get('facebook_link')
  # website_link = request.form.get('website_link')

  cityequal= ArtistLocation.query.filter(ArtistLocation.city==request.form.get('city')).first()
  print(cityequal)
  if cityequal == None:
    city = request.form.get('city')
    state = request.form.get('state')
    artistLocation = ArtistLocation( city= city,state=state) 
    db.session.add(artistLocation) 
    db.session.commit()  
  # get data for atists genres 
  genres = request.form.getlist('genres')
  # get data for seeking venu +  add to table seeking venue 
  poptextarea = request.form.get('textarea')
  print(poptextarea)
  checkbox = request.form.get('checkbox')
  print(checkbox)
  if checkbox !=None :
     checkbox =True 
     seekingVenu = SeekingVenu(seeking_venue=checkbox, seeking_description=poptextarea)
  else:  
    checkbox =False  
    seekingVenu = SeekingVenu(seeking_venue=checkbox) 
  db.session.add(seekingVenu)   
  db.session.commit()
    
  # get artisi data and add data to table Aritst 
  first_name = request.form.get('first_name')
  last_name = request.form.get('last_name')
  phone = request.form.get('phone')
  image_link = request.form.get('image_link')
  facebook_link = request.form.get('facebook_link')
  website_link = request.form.get('website_link')
  if cityequal != None:
     artist = Artist(first_name=first_name, last_name=last_name,phone=phone,
      image_link= image_link,facebook_link=facebook_link,website_link=website_link,
           loction_id=cityequal.id,Seeking_venu_id=seekingVenu.id)
  else :
    artist = Artist(first_name=first_name, last_name=last_name,phone=phone,
      image_link= image_link,facebook_link=facebook_link,website_link=website_link,
           loction_id=artistLocation.id,Seeking_venu_id=seekingVenu.id)
  db.session.add(artist)
  db.session.commit()
  # get data middle name Add Middle name to table middl name
  middlename = request.form.get('middlename') 
  artisiMiddlename = ArtisiMiddlename(middlename= middlename,artist_id= artist.id)  
  db.session.add(artisiMiddlename)
  db.session.commit()
  # if request.method == 'POST' :
  #    print(request.form.get('checkbox'))
  # else: 
  #     checkbox = False
  #  add genres laist to aritstiTable 
  for i in genres : 
       artistGenres = ArtistGenres( genres=i,artist_id=artist.id)
       db.session.add(artistGenres)
       print(poptextarea,checkbox ,sep='\n')
  db.session.commit()
  #poptextarea = request.get_json()['']
  # checkbox = request.get_json()['checkbox']
  # checkbox1 = request.get_json()['Mohedmmed']

  # print(first_name,last_name,phone , image_link , facebook_link,website_link, city,state,middlename,genres,sep="\n")
  
  
  # on successful db insert, flash success  i have made a change to solve problem of Error name to firstname
  flash('Artist ' + request.form['first_name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')
  # return render_template('/artists/create') 

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  # show = db.session.query(Artist.first_name,Artist.last_name,,Venue.name).join(Show).filter(Show.artist_id==Artist.id).all()
  
  show = db.session.query(Artist,Show ,Venue.name).join(Venue).filter(Show.artist_id==Artist.id).all()
  print(show[0])
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=show)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # artist_check_id=  Artist.query.order_by(Artist.id).all()
  # venue_check_id =  Venue.query.order_by(Venue.id).all()
  start_date =  request.form.get('start_time')
  artist_id = request.form.get('artist_id')
  venue_id  = request.form.get('venue_id')
  error = False
  try:
     aritsshow =  Artist.query.filter_by(id=artist_id).first()
     venushow = Venue.query.filter_by(id=venue_id).first()
     print(aritsshow,venushow,sep='\n')
     d =1
  except  Exception:
          
          flash('Show was not successfully listed! you should enter Integer \n value in Venue ID and Artist ID Fildeis')

  
  try:    
     if aritsshow != None :
             artist_id = artist_id
              
     else :
       flash('Show  artis undfided was not successfully listed!') 
        
     if venushow != None :
        venue_id  =venue_id
     else :
        flash('Show  venue undfided was not successfully listed!')   
            

     show = Show(artist_id=artist_id,venue_id=venue_id, star_date=start_date)
     db.session.add(show)
     db.session.commit()
       
  except:
    error=True  
    db.session.rollback()     
    print(sys.exc_info())     
  finally:
    db.session.close() 
    if not error:
         flash('Show was successfully listed!')
  # else :
    
  #    flash('Show was successfully listed!')
  #    d = 1
  # show = Show(artist_id=artist_id,venue_id=venue_id, star_date=start_date)
  # db.session.add(show)
  # db.session.commit()
      
  # print(artist_id,venue_id,start_date,artist_check_id ,sep="\n")
  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')
  return render_template('pages/home.html')
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
 
# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
