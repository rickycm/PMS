__author__ = 'ricky'
import datetime

P_TYPE = [(1, u'Apartment'), (2, u'House'), (3, u'Villa'), (4, u'Room'), (5, u'Studio'), (6, u'Master Bedroom'),
    (7, u'Junior Master Bedroom'), (8, u'Common Room with Private Access'), (9, u'Common Room')]
P_STATUS = [(1, u'Free to rent'), (2, u'Rented'), (3, u'On Maintenance'), (-1, u'Deleted')]
PERSON_TYPE = [(1, u'Person'), (2, u'Company'), (3, u'Family')]
RENTAL_TYPE = [(1, u'Monthly'), (2, u'Quarterly'), (3, u'Yearly'), (4, u'Daily')]
USER_TYPE = [(1, u'Manager'), (2, u'Owner'), (3, u'Tenant')]
ACTION = [(1, u'Check-in'), (2, u'Check-out'), (3, u'Pay Rental Bill'), (4, u'Rise Maintenance Bill'),
          (5, u'Pay Maintenance Bill')]
GENDER_CHOICE = [(u'M', u'Male'), (u'F', u'Female')]
PAID = [(0, u'Not Paid'), (1, u'Paid'), (-1, u'Deleted')]
STATUS = [(0, u'Invalid'), (1, u'Normal'), (-1, u'Deleted')]
TENANTSTATUS = [(0, u'Deactive'), (1, u'Active'), (-1, u'Deleted')]
CURRENCY = [('SGD', u'SGD'), ('USD', u'USD'), ('CNY', u'CNY')]


