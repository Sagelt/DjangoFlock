DjangoFlock
===========

So, Games on Demand is pretty cool, but there's not really any _demand_ there.
It's more "Games we feel like running". I'm making this to support people
petitioning for games they want to play, but not run. Currently, it's just a
game scheduler, but more features coming!

Todo
----

Current:
 - Make Demand view actually do what it should (show demand per hour per game).
 - Notify people when games they've expressed interest in are being run.
 - Make Convention implicit; set your current convention in your user profile,
   have all data filtered to show just your convention, have top-banner status
   show your current convention.
 - Make user profiles, both in REST API and browser UI.
 - Decide on permissions model. Any user can make Events, but who can make
   Games and Publishers? Who can edit them?
 
Future:
 - Add Fullcalendar event-creation UI to browser UI.
 - Move to MongoDB backend. (Maybe.)
 - Get a real favicon.
 - Decide on a name. RPGflock? Constellator?
 - Publish events to per-Convention gCal/iCal/whatever it is format.
 - Make mobile UI.
 - Add oAuth/Facebook Connect account creation (Twitter, Facebook, what else?)
