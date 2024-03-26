# Do NOT modify this file.

class circular_buffer:
    ''' Represents the circular buffer that should only be used when 
        implementing the Go-Back-N protocol. '''
    def __init__(self, n):
        ''' 
        Initializes the relevant class variables of the circular buffer.
        
        Parameters
        ----------
        - n : int
            - The maximum number of packets that can be stored in the 
              circular buffer. 
        '''
        # The next slot in the circular buffer to remove a packet.
        self.read = 0
        # The next slot in the circular buffer to add a packet.
        self.write = 0
        # The maximum number of packets that can be stored in the circular 
        # buffer.
        self.max = n
        # The current number of packets stored in the circular buffer.
        self.count = 0
        # The data structure that actually stores the buffered packets.
        self.buffer = []
        # Initialize all entries in the buffer to NULL values.
        for i in range(n):
            self.buffer.append(None)

    def push(self, packet):
        ''' 
        Attempts to store a packet in the next available slot in the circular 
        buffer and updates the relevant class variables afterward. 
        
        Parameters
        ----------
        - packet : packet
            - The packet that will be attempted to be stored in circular 
              buffer.
        '''
        if (self.count == self.max):
            return -1
        else:
            self.buffer[self.write] = packet

        self.write = (self.write + 1) % self.max
        self.count = self.count + 1

    def pop(self):
        ''' Attempts to remove a packet from the beginning of the circular 
            buffer and updates the relevant class variables. '''
        if (self.count == 0):
            return -1

        temp = self.buffer[self.read]
        self.read = (self.read + 1) % self.max
        self.count = self.count - 1

    def read_all(self):
        ''' Returns a list containing all of the currently buffered 
            packets. '''
        temp = []
        read = self.read
        for i in range(self.count):
            temp.append(self.buffer[read])
            read = (read + 1) % self.max
        return temp

    def isfull(self):
        ''' Determines if all slots in the circular buffer are currently 
            occupied. '''
        if (self.count == self.max):
            return True
        else:
            return False