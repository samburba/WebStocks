#Run this script to auto add all stocks to the database
#Needs to run in django shell
#(python manage.py shell) & copy and paste this in
from stocks.models import Stock
with open('NASDAQ.txt', 'r') as f:
    for line in f:
        c_line = line.strip()
        if c_line:
            entry = Stock(slug=c_line)
            entry.save()
