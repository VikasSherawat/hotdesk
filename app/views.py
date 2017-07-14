from flask import Blueprint, render_template, abort, request, redirect, url_for, session, current_app as app
from model import Seats
from botimpl import ChatBotController, FacebookMessenger
import json
from splitwise import Splitwise
import urllib
from app.botimpl.botexception import BotException, LoginException
from  app.botimpl.constants import BotConstants, ErrorMessages
import app.botimpl.allocation 


pages = Blueprint('pages', __name__,template_folder='templates')

FACEBOOK_ACCOUNT_LINKING_TOKEN = "account_linking_token"
FACEBOOK_REDIRECT_URI = "redirect_uri"
SPLITWISE_SECRET = "splitwise_secret"
SPLITWISE_OAUTH_TOKEN = "oauth_token"
SPLITWISE_OAUTH_VERIFIER = "oauth_verifier"
SPLITWISE_OAUTH_TOKEN_SECRET = "oauth_token_secret"


def askUserToLogin(senderId):
    messenger = FacebookMessenger(app.config['FACEBOOK_PAGE_ACCESS_TOKEN'],app.config['FACEBOOK_VERIFY_TOKEN'])
    messenger.sendLoginLink(senderId)

@pages.route("/")
def home():
    return render_template("home.html")


@pages.route("/messenger",methods=['GET'])
def facebookVerify():

    #Create a messenger object
    messenger = FacebookMessenger(app.config['FACEBOOK_PAGE_ACCESS_TOKEN'],app.config['FACEBOOK_VERIFY_TOKEN'])

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
        app.logger.debug("Asking user to login")
    except BotException as e:
        bot.messenger.send(senderId, str(e))
        app.logger.debug("BotException Occured " + str(e))
    except Exception as e:
        bot.messenger.send(senderId, ErrorMessages.GENERAL)
        app.logger.debug("Exception Occured "+str(e))
    return ('',204)


@pages.route("/notification", methods=['POST'])
def sendSeatsNotification():
    bot = ''
    senderId = ''
    try:
        data = json.loads(request.data)
        senderId = FacebookMessenger.getSenderId(data)
        seats = getSeats("personId")
        bot.messenger.send(sendId, seats)
    except Exception as e:
        bot.messenger.send(senderId, ErrorMessages.GENERAL)
        app.logger.debug("Exception Occured "+str(e))
    return ('',204)

@pages.route("/temp")
def temp():

    seat = Seats()
    seat.building = 1
    seat.floor = 2
    seat.seatnum = 3
    seat.save()
    return "done"
    

