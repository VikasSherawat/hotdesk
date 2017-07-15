from app.bot import BaseProcessor, BotProcessorFactory
from datetime import datetime, timedelta
from botexception import BotException, LoginException
from constants import BotConstants, ErrorMessages
from flask import current_app as app
import random
from app.model import Booking,Room,Seats

class SplitwiseBotProcessorFactory(BotProcessorFactory):
    class ProcessorType(object):
        '''
        Processor Type
        '''
        SEAT_PROCESSOR = 'seat'
        MEETING_PROCESSOR = 'meeting'
        HELP_PROCESSOR = "help"

    def __init__(self):
        super(SplitwiseBotProcessorFactory, self).__init__()

    def getProcessor(self, action):

        if action == SplitwiseBotProcessorFactory.ProcessorType.SEAT_PROCESSOR:
            return SeatProcessor()
        elif action == SplitwiseBotProcessorFactory.ProcessorType.MEETING_PROCESSOR:
            return MeetingRoomProcessor()
        else:
            return MeetingRoomProcessor()

#Define processors below

class GreetingProcessor(BaseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass

class SeatProcessor(BaseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        bookingtime = getInputFromRequest(input, "num_time", ErrorMessages.BOOKING_TIME, True)
        if bookingtime == "":
            bookingtime = 1
        seatnum = input["seatnum"]
        if seatnum == 0:
             return ErrorMessages.GENERAL

        seat = Seats.query.filter_by(id = seatnum).first()
        if seat:
            seat.status = "Reserved"
            seat.save()
            return "Seat "+str(seatnum)+" is successfully reserved for next "+str(bookingtime)+" hours"
        else:
            return ErrorMessages.GENERAL
              

class MeetingRoomProcessor(BaseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        bookingtime = getInputFromRequest(input, "num_time", ErrorMessages.BOOKING_TIME, True)
        duration = getInputFromRequest(input, "duration", ErrorMessages.DURATION, True)
        roomid = getInputFromRequest(input, "roomid")
        endtime = int(bookingtime)+int(duration)
        if roomid != "":
            return "Meeting room "+str(roomid)+" is booked from "+bookingtime+" to "+str(endtime)
        else:
            #check if the room is free
            output = "Following rooms are available at time "+bookingtime+"\n"
            rooms = Room.query.all()
            for room in rooms:
                output += str(room.building)+ "."+str(room.floor)+"."+str(room.roomid)+"\n"
            
            return output
        

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

class UnknownProcessor(BaseProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass