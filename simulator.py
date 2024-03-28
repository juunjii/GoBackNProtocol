# Only the nsimmax, lossprob, corruptprob, and Lambda class variables should
# be modified when testing. These variables MUST be returned to their
# original values before you submit each phase of the project. Do NOT modify 
# anything else in this file. 

from msg import *
from event_list import *
from event import *

import random
import copy

# 
class simulator:
    ''' Simulates a network's behavior. '''
    def __init__(self):
        ''' 
        Initializes the relevant class variables of the simulator.
        '''
        self.type = 'SNW'
        self.TRACE = 0  # For debugging.
        self.nsim = 0   # The number of messages passed down from layer 5 to 
                        # layer 4 so far.
        self.nsimmax = 5  # The number of messages to generate, then stop the
                           # simulation.
        self.time = 0.0
        self.lossprob = 0.2 # The probability that a packet is dropped. 
        self.corruptprob = 0.3  # The probability that one bit in a packet is 
                                # flipped / corrupted.
        self.Lambda = 1000  # The arrival rate of messages from layer 5.
        self.ntolayer3 = 0  # The number of packets sent to layer 3 so far.
        self.nlost = 0  # The number of packets lost in media / the network.
        self.ncorrupt = 0  # The number of packets corrupted by media / the
                           # network.        
        self.envlist = evl
        self.generate_next_arrival()  # Initialize the event list.

        #statistics counters
        self.totalMsgSent=0
        self.retransmittedData=0
        self.retransmittedAck=0
        self.retransmittedTotal=0
        self.droppedData=0
        self.droppedAck=0
        self.droppedTotal=0
        self.corruptedData=0
        self.corruptedAck=0
        self.corruptedTotal=0
        self.endTime=0

    def generate_next_arrival(self):
        ''' Initializes the simulator's event list. '''
        if (self.nsim >= (self.nsimmax - 1)):
            #print("simulation complete")
            return
        time = self.time + self.Lambda
        self.envlist.insert(event(time, "FROM_LAYER5", "S"))
        return

    def run(self):
        ''' Run the network  simulation by actualizing all of the events in 
            the event list. '''
        while (1):
            env = self.envlist.remove_head()
            if (env == None):
                print("simulation complete")
                
                self.endTime=self.time
                print("===========STATISTICS==========");
                print(" Total Number of Messages Sent                 -> ", self.totalMsgSent)
                print(" Total Number of Retransmissions               -> ", self.retransmittedTotal)
                print("   Total Number of Retransmitted Data Packets  -> ", self.retransmittedData)
                print("   Total Number of Retransmitted ACKs          -> ", self.retransmittedAck)
                print(" Total Number of Dropped Packets               -> ", self.droppedTotal)
                print("   Total Number of Dropped Data Packets        -> ", self.droppedData)
                print("   Total Number of Dropped ACKs                -> ", self.droppedAck)
                print(" Total Number of Corrupted Packets             -> ", self.corruptedTotal)
                print("   Total Number of Corrupted Data Packets      -> ", self.corruptedData)
                print("   Total Number of Corrupted ACKs              -> ", self.corruptedAck)
                print(" Final Simulation Time                         -> ", self.endTime)
                print("===========STATISTICS==========")
                print("")


                return
            else:
                self.time = env.evtime

            

            if (env.evtype == "FROM_LAYER5"):
                self.generate_next_arrival()
                ch = chr(97 + self.nsim % 26)
                m = msg(ch)
                self.nsim = self.nsim + 1
                if (env.eventity == "S"):
                    if (self.type == 'SNW'):
                        from SNW_Sender import a
                    else:
                        from GBN_Sender import a
                    a.S_output(m)
                else:
                    if (self.type == 'SNW'):
                        from SNW_Receiver import b
                    else:
                        from GBN_Receiver import b
                    b.R_output(m)

            elif (env.evtype == "FROM_LAYER3"):
                pkt2give = env.pkt
                if (env.eventity == "S"):
                    if (self.type == 'SNW'):
                        from SNW_Sender import a
                    else:
                        from GBN_Sender import a
                    a.S_input(pkt2give)
                else:
                    if (self.type == 'SNW'):
                        from SNW_Receiver import b
                    else:
                        from GBN_Receiver import b
                    b.R_input(pkt2give)

            elif (env.evtype == "TIMER_INTERRUPT"):
                if (env.eventity == "S"):
                    if (self.type == 'SNW'):
                        from SNW_Sender import a
                    else:
                        from GBN_Sender import a
                    a.S_handle_timer()

                else:
                    b.R_handle_timer()

            else:
                print("!!!!!!!????")

def to_layer_three(calling_entity, packet):
    ''' 
    Sends a packet to the calling entity's layer 3.

    Parameters
    ----------
    - calling_entity : char
        - The character "S" to represent that the Sender or "R" to represent 
        that the Receiver is the entity that is sending the packet to layer 3.
    - packet : packet
        - The packet that is being sent to layer 3.
    '''
    if (random.uniform(0, 1) < sim.lossprob):
        return

    pkt = copy.deepcopy(packet)

    if (random.uniform(0, 1) < sim.corruptprob):
        if (pkt.payload != 0):
            pkt.payload.data = pkt.payload.data[0:-1] + "1"
        else:
            pkt.seqnum = -1

    q = sim.envlist.head
    lasttime = sim.time
    while (q != None):
        if ((q.eventity != calling_entity) and (q.evtype == "FROM_LAYER3")):
            lasttime = q.evtime

        q = q.next

    eventime = lasttime + 1 + 9 * random.uniform(0, 1)
    if (calling_entity == "S"):
        sim.envlist.insert(event(eventime, "FROM_LAYER3", "R", pkt))
    else:
        sim.envlist.insert(event(eventime, "FROM_LAYER3", "S", pkt))

def to_layer_five(calling_entity, message):
    '''
    Passes the received message to layer 5.

    Parameters
    ----------
    - calling_entity : char
        - The character "S" to represent that the Sender or "R" to represent 
          that the Receiver is the entity that received this message.
    - message : msg
        - The message that the calling entity received.
    '''
    print(f"data received： {message}")

sim = simulator()