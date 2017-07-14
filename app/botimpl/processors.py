from app.bot import BaseProcessor, BotProcessorFactory
from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
from splitwise.group import Group
from splitwise.debt import Debt
from datetime import datetime, timedelta
from botsplitwise import BotSplitwise
from botexception import BotException, LoginException
from constants import BotConstants, ErrorMessages
from flask import current_app as app
import random

class SplitwiseBotProcessorFactory(BotProcessorFactory):
    class ProcessorType(object):
        '''
        Processor Type
        '''
        ROOM_PROCESSOR = 'room'
        MEETING_PROCESSOR = 'meeting'
        HELP_PROCESSOR = "help"

    def __init__(self):
        super(SplitwiseBotProcessorFactory, self).__init__()

    def getProcessor(self, action):

        if action == SplitwiseBotProcessorFactory.ProcessorType.ROOM_PROCESSOR:
            return RoomProcessor()
        elif action == SplitwiseBotProcessorFactory.ProcessorType.MEETING_PROCESSOR:
            return MeetingRoomProcessor()
        else:
            return UnknownProcessor()

#Define processors below

class GreetingProcessor(SplitwiseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass

class RoomProcessor(SplitwiseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass        

class MeetingRoomProcessor(SplitwiseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass
