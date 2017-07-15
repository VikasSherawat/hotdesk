from model import Seats,Room
from flask import Blueprint, render_template, abort, request, redirect, url_for, session, current_app as myapp
from botimpl import ChatBotController, FacebookMessenger
import json
from splitwise import Splitwise
import urllib
from app.botimpl.botexception import BotException, LoginException
from  app.botimpl.constants import BotConstants, ErrorMessages
import app.botimpl.allocation 
import math
from flask import jsonify
import random
import os


pages = Blueprint('pages', __name__,template_folder='templates')

FACEBOOK_ACCOUNT_LINKING_TOKEN = "account_linking_token"
FACEBOOK_REDIRECT_URI = "redirect_uri"
SPLITWISE_SECRET = "splitwise_secret"
SPLITWISE_OAUTH_TOKEN = "oauth_token"
SPLITWISE_OAUTH_VERIFIER = "oauth_verifier"
SPLITWISE_OAUTH_TOKEN_SECRET = "oauth_token_secret"


users = {
  "naman":   {
        "fb_id": "1401079726611959",
        "name": "Naman",
        "team": "API"
    },
   "rukmani":  {
        "fb_id": "1082466331854538",
        "name": "Rukmani",
        "team": "Finance"
    }
}

num = 1


def askUserToLogin(senderId):
    messenger = FacebookMessenger(myapp.config['FACEBOOK_PAGE_ACCESS_TOKEN'],myapp.config['FACEBOOK_VERIFY_TOKEN'])
    messenger.sendLoginLink(senderId)

@pages.route("/")
def home():
    if not os.path.exists('test.db'):
        print "inserting rows"
        insert()
    return render_template("home.html")


@pages.route("/messenger",methods=['GET'])
def facebookVerify():

    #Create a messenger object
    messenger = FacebookMessenger(myapp.config['FACEBOOK_PAGE_ACCESS_TOKEN'],myapp.config['FACEBOOK_VERIFY_TOKEN'])

    #Get the request parameters from facebook
    verify_token = request.args['hub.verify_token']
    challenge = request.args['hub.challenge']

    #Verify that the request came from facebook
    if verify_token == messenger.getVerifyToken():
        #Return the challenge
        return challenge

    else:
        #Return Not found
        abort(404)


def checkFirstTimeLogin(data):
    entryList = data['entry']
    messagingList = entryList[0]['messaging']
    messagingDictionary = messagingList[0]
    if 'account_linking' in messagingDictionary:
        return True
    return  False


@pages.route("/messenger", methods=['POST'])
def facebookMessage():
    bot = ''
    senderId = ''
    try:
        data = json.loads(request.data)
        senderId = FacebookMessenger.getSenderId(data)
        bot = ChatBotController(senderId)
        if checkFirstTimeLogin(data):
            bot.messenger.send(senderId, BotConstants.LOGIN_SUCCESS)
            return ('', 204)
        bot.parse(data)
    except LoginException as e:
        askUserToLogin(senderId)
        myapp.logger.debug("Asking user to login")
    except BotException as e:
        bot.messenger.send(senderId, str(e))
        myapp.logger.debug("BotException Occured " + str(e))
    except Exception as e:
        bot.messenger.send(senderId, ErrorMessages.GENERAL)
        myapp.logger.debug("Exception Occured "+str(e))
    return ('',204)


@pages.route("/api/book", methods=['POST'])
def sendSeatsNotification():
    messenger = FacebookMessenger(myapp.config['FACEBOOK_PAGE_ACCESS_TOKEN'],myapp.config['FACEBOOK_VERIFY_TOKEN'])

    data = json.loads(request.data)
    print data
    user = users[data["id"]]
    try:
        seat = getSeats(user["team"])
        seatmsg = "You can goto desk"
        if not seat:
            seatmsg += "1.2.18"
        else:
            seat.status = 'Reserved'
            seat.user = user["name"]
            seat.teamname = user["team"]
            seat.save()
            seatmsg += str(seat.seatnum)
        messenger.send(user["fb_id"], seatmsg)
    except Exception as e:
        messenger.send(user["fb_id"], ErrorMessages.GENERAL)
        myapp.logger.debug("Exception Occured "+str(e))
    return ('',204)

@pages.route("/insert")
def insert():
    name = ["John","Haifen","Dan","Morres","Issac","Vikas","Bill","Ross","Chandler"]
    team = ["API","Finance"]
    for i in xrange(1,37):
        seat = Seats()
        if i in [1,5]:
            seat.user = random.choice(name)
            seat.status = "Allocated"
            seat.teamname = team[0]
        if i in [10]:
            seat.user = random.choice(name)
            seat.status = "Allocated"
            seat.teamname = team[1]

        seat.building = 1
        seat.floor = 1
        seat.seatnum = i
        seat.row = i/9 if i%9==0 else i/9+1 
        seat.save()

    for i in xrange(1,7):
        room = Room()
        room.building = 1
        room.floor = 1
        room.roomnum = i
        room.save()
    return "done"


@pages.route("/api/changeseatstatus",methods = ['POST'])
def changeSetStatus():
    data = json.loads(request.data)
    seatnum = data['seatnum']
    status = data['status']
    seat = Seats.query.filter_by(seatnum=seatnum).first()
    if seat:
        seat.status = status
        seat.save()
        return "status change"
    else:
        return "invalid seat number"

def getSeats(team):
    print "Team Name is "+team
    seats = Seats.query.filter_by(teamname = team).order_by(Seats.row).all()
    if not seats:
        seats = Seats.query.all()
        print "Number of record in seats "+str(len(seats))
        for row in xrange(1,4):
            #gives the first desk of an empty row
            seat = Seats.query.filter_by(row = row).first()
            if seat.status == "Free" or seat.user == None:
                print "Inside First For Loop"
                return seat
        
        #if all rows have some team-mates, it will give the first free desk in a row
        for seat in seats:
            if seat.row ==1:
                continue

            if seat.status == 'Free':
                print "Inside 2nd For Loop"
                return seat
    else:
        print "Inside getSeats"
        print seats
        for seat in seats: 
            seat = Seats.query.filter_by(user=None, row = seat.row).first()
            if seat:
                return seat
        seat = Seats.query.filter_by(user=None).first()
        if seat:
            return seat

    return Seats.query.filter_by(seatnum=11).first()

@pages.route("/findseat")
def findseat():
    num = "rukmani"
    user = users[num]
    try:
        seat = getSeats(user["team"])
        print "reached here"
        seatmsg = "You can goto desk "
        if not seat:
            seatmsg += "1.2.18"
        else:
            seat.status = 'Reserved'
            seat.user = user["name"]
            seat.teamname = user["team"]
            seat.save()
            seatmsg += str(seat.seatnum)
    except Exception as e:
        return "Exception Occured "+str(e)
    return seatmsg

@pages.route("/api/seats",methods=['GET'])
def getAllSeats():
    seats = Seats.query.all()
    seatsRes= []
    for seat in seats:
        obj= {}
        obj["id"] = seat.id
        obj["user"] = seat.user
        obj["status"] = seat.status
        obj["teamname"] = seat.teamname
        seatsRes.append(obj)

    return json.dumps(seatsRes), {'Content-type':'application/json'}


@pages.route("/api/reserveseats",methods = ['POST'])
def reserveseats():
    data = json.loads(request.data)
    seats = data['seatList']
    for seatnum in seats:
        seat = Seats.query.filter_by(seatnum=seatnum).first()
    if seat:
        seat.status = "Reserved"
        seat.save()
    else:
        return "invalid seat number"

    return "Status successfully changed"