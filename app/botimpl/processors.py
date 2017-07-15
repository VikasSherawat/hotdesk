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
        SEARCH_PROCESSOR = "search"

    def __init__(self):
        super(SplitwiseBotProcessorFactory, self).__init__()

    def getProcessor(self, action):

        if action == SplitwiseBotProcessorFactory.ProcessorType.SEAT_PROCESSOR:
            return SeatProcessor()
        elif action == SplitwiseBotProcessorFactory.ProcessorType.MEETING_PROCESSOR:
            return MeetingRoomProcessor()
        elif action == SplitwiseBotProcessorFactory.ProcessorType.SEARCH_PROCESSOR:
            return SearchProcessor()
        else:
            return MeetingRoomProcessor()

#Define processors below

class MyProcessor(BaseProcessor):

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

class GreetingProcessor(MyProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass

class SeatProcessor(MyProcessor):

    def __init__(self):
        pass

    def process(self, input):
        bookingtime = self.getInputFromRequest(input, "num_time", ErrorMessages.BOOKING_TIME, True)
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
              

class MeetingRoomProcessor(MyProcessor):

    def __init__(self):
        pass

    def process(self, input):
        bookingtime = self.getInputFromRequest(input, "num_time", ErrorMessages.BOOKING_TIME, True)
        duration = self.getInputFromRequest(input, "duration", ErrorMessages.DURATION, True)
        roomid = self.getInputFromRequest(input, "roomid")
        endtime = int(bookingtime)+int(duration)
        if roomid != "":
            return "Meeting room "+str(roomid)+" is booked from "+bookingtime+" to "+str(endtime)
        else:
            #check if the room is free
            booking_time = str(int(bookingtime)-12 if int(bookingtime)> 12 else int(bookingtime))
            if bookingtime > 12:
                booking_time += " pm"
            else:
                booking_time += " am"

            output = "Following rooms are available at time "+booking_time+"\n"
            rooms = Room.query.all()
            for room in rooms:
                output += str(room.roomnum)+"\n"
            
            return output

class UnknownProcessor(MyProcessor):

    def __init__(self):
        pass

    def process(self, input):
        pass

class SearchProcessor(MyProcessor):

    def __init__(self):
        pass

    def process(self, input):
        name = self.getInputFromRequest(input, "name", ErrorMessages.NAME, True)

        return name+" is seated at "+str(self.getseatbyuser(name))
    
    def getseatbyuser(self,name):
        seat = Seats.query.filter_by(user=name).first()
        if seat:
            return seat.seatnum
        else:
            return 0