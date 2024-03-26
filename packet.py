# Do NOT modify this file.

from simulator import to_layer_three

class packet:
    ''' Represents the packets that are sent across the simulated network. '''
    def __init__(self, seqnum = 0, acknum = 0, payload = 0):
        ''' Initializes the relevent class variables for the packet class. '''
        self.seqnum = seqnum  # The packet's sequence number.
        self.acknum = acknum  # The packet's acknowledgment number.
        self.payload = payload  # The packet's payload.
        self.checksum = 0  # The packet's checksum.
        self.checksum = self.get_checksum()

    def get_checksum(self):
        ''' Computes the checksum of a packet's current contents and it can be 
            used to verify the checksum stored within the packet. '''
        checksum = 0
        if (self.payload != 0):
            for i in range(20):
                checksum = checksum + ord(self.payload.data[i])
        checksum = checksum + self.seqnum + self.acknum
        return checksum

def send_ack(calling_entity, acknowledgment_number):
    ''' 
    Sends an ACK to the calling entity.
    
    Parameters
    ----------
    - calling_entity : char
        - The character "S" to represent that the Sender or "R" to represent 
          that the Receiver is the entity that wants to send an ACK. With only
          unidirectional data transfer in this project, the Receiver should be 
          the only calling this function.
    - acknowledgment_number : int
        - The number of the acknowledgment being sent to the Sender.
    '''
    pkt = packet(acknum = acknowledgment_number)
    pkt.checksum = pkt.get_checksum()
    to_layer_three(calling_entity, pkt)