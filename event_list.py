# Do NOT modify this file.

from event import event

class event_list:
    ''' Represents a list of events that that the simulation will 
        actualize. '''
    def __init__(self):
        ''' Initializes the head class variable of the event list. '''
        self.head = None

    def insert(self, p):
        ''' 
        Inserts a new event into the event list.

        Parameters
        ----------
        - p : event
            - The new event that will be inserted into the event list.   
        '''
        q = self.head
        # If the head is None
        if (q == None):
            self.head = p
            self.head.next = None
            self.head.prev = None
        else:
            qold = q
            while ((q != None) and (p.evtime > q.evtime)):
                qold = q
                q = q.next

            # Now qold.next == q, p.evtime <= q.evtime
            if (q == None):
                qold.next = p
                p.prev = qold
                p.next = None
            else:
                if (q == self.head):
                    p.next = q
                    p.prev = None
                    q.prev = p
                    self.head = p
                else:
                    p.next = q
                    p.prev = q.prev
                    p.prev.next = p
                    q.prev = p

    def print_self(self):
        ''' Prints out all events that are currently in the event list. '''
        q = self.head
        print("--------------\nEvent List Follows:\n")
        while (q != None):
            print(f"Event time: {q.evtime}, type: {q.evtype}, entity: {q.eventity}\n")
            q = q.next

        print("--------------\n")

    def remove_head(self):
        ''' Removes the event that's currently at the beginning of the event
            list. '''
        temp = self.head
        if temp == None:
            return None
        if (self.head.next == None):
            self.head = None
            return temp
        else:
            self.head.next.prev = None
            self.head = self.head.next
            return temp

    def start_timer(self, calling_entity, increment):
        ''' 
        Starts a timer for a specified length of time on behalf of the
        calling entity and inserts the timer event it into the event list.

        Parameters
        ----------
        - calling_entity : char
            - The character "S" to represent that the Sender or "R" to 
              represent that the Receiver is the entity the timer is for.
        - increment : float
            - The amount of time that will pass before the timer interrupts 
              the calling entity.
        '''
        from simulator import sim
        self.insert(event(sim.time + increment, "TIMER_INTERRUPT", calling_entity))

    def remove_timer(self):
        ''' Removes an expired timer from the event list. '''
        q = self.head
        while (q.evtype != "TIMER_INTERRUPT"):
            q = q.next

        if q.prev == None:
            self.head = q.next
        elif q.next == None:
            q.prev.next = None
        else:
            q.next.prev = q.prev
            q.prev.next = q.next

evl = event_list()