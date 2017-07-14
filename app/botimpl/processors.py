from app.bot import BaseProcessor, BotProcessorFactory
from datetime import datetime, timedelta
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

class GreetingProcessor(BaseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass

class RoomProcessor(BaseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass        

class MeetingRoomProcessor(BaseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        bookingtime = getInputFromRequest(input, "booking_time", ErrorMessages.BOOKING_TIME, True)
        duration = getInputFromRequest(input, "num_time", ErrorMessages.DURATION, True)

    def getInputFromRequest(self, input, param, error=ErrorMessages.GENERAL, required=False):

        if BotConstants.RESULT in input:

            result = input[BotConstants.RESULT]

            if BotConstants.PARAMETERS in result:

                parameters = result[BotConstants.PARAMETERS]

                param_value = ''
                if param in parameters:
                    param_value = parameters[param]

                if param_value is not None and (param_value == "" or len(str(param_value)) == 0) and required:
                    raise BotException(error)

                return param_value

        if not required:
            raise BotException(error)