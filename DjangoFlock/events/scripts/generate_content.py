from events.models import *
from django.contrib.auth.models import User
from datetime import datetime, timedelta

def run():
    for name in range(1, 11):
        User.objects.create_user("Test%s" % name, "test@example.com", "foobar")
    if not User.objects.get(username='kit'):
        kit = User.objects.create_superuser("kit", "kit.la.t@gmail.com", "foobar")
    
    p = Publisher(name='Test Publisher', publisher_url='http://example.com/')
    p.save()
    
    g = Game(name='Test Game', publisher=p, edition='1st')
    g.save()
    
    c = Convention(name='Test Convention')
    c.save()
    
    start = datetime.now() - timedelta(hours=4)
    end = datetime.now()
    e = Event(host=kit, game=g, convention=c, start=start, end=end, min=3, max=5)
    e.save()
    
    d = Demand(user=kit, game=g, start=start, end=end)
    d.save()