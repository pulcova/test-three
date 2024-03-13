import random
import string
from .models import QueryTicket

def generate_ticket_number():
    length = 10  
    while True: 
        ticket_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not QueryTicket.objects.filter(ticket_number=ticket_number).exists():
            break
    return ticket_number
