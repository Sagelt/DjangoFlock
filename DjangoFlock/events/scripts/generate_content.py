from datetime import datetime, timedelta
from django.contrib.auth.models import User
from events.models import *
import random

def run():
#    for name in range(1, 11):
#        User.objects.create_user("Test%s" % name, "test@example.com", "foobar")
#    if not User.objects.get(username='kit'):
#        kit = User.objects.create_superuser("kit", "kit.la.t@gmail.com", "foobar")
#    else:
#        kit = User.objects.get(username='kit')
#    
#    p = Publisher(name='Test Publisher', publisher_url='http://example.com/')
#    p.save()
#    
#    g = Game(name='Test Game', publisher=p, edition='1st')
#    g.save()
#    
#    c = Convention(name='Test Convention')
#    c.save()
#    
#    start = datetime.now() - timedelta(hours=4)
#    end = datetime.now()
#    e = Event(host=kit, game=g, convention=c, start=start, end=end, min=3, max=5)
#    e.save()
#    
#    d = Demand(user=kit, game=g, start=start, end=end)
#    d.save()

    c = Convention.objects.get(name='Test Convention')
    p = Publisher.objects.get(name='Test Publisher')
    
    for game in ('Apocalypse World', 'Fiasco', 'In a Wicked Age', 'Grey Ranks', 'Misspent Youth'):
        g = Game(name=game, publisher=p)
        g.save()
    
    for user in User.objects.all():
        now = datetime.now()
        hour = random.randint(9, 17)
        minute = random.choice([0, 30])
        start = datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute)
        end = start + timedelta(hours=random.randint(1, 6))
        g = random.choice(Game.objects.all())
        d = Demand(user=user, game=g, start=start, end=end, convention=c)
        d.save()