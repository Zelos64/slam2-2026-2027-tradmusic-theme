"""Single source of truth for the mockup screens and FIXTURES.md."""
from datetime import datetime, timedelta

TODAY = datetime(2026, 10, 12, 10, 0)  # Monday — the mockup's "today"

INSTRUMENTS = [
    ("banjo", "Banjo"),
    ("bodhran", "Bodhrán"),
    ("bouzouki", "Bouzouki"),
    ("button-accordion", "Button accordion"),
    ("concertina", "Concertina"),
    ("fiddle", "Fiddle"),
    ("flute", "Flute"),
    ("guitar", "Guitar"),
    ("harp", "Harp"),
    ("low-whistle", "Low whistle"),
    ("tin-whistle", "Tin whistle"),
    ("uilleann-pipes", "Uilleann pipes"),
]
INSTRUMENT_NAME = dict(INSTRUMENTS)

TOWNS = [("doolin", "Doolin"), ("dublin", "Dublin"), ("ennis", "Ennis"), ("galway", "Galway")]
TOWN_NAME = dict(TOWNS)

# key: (email, first name, last name, roles)
USERS = {
    "admin": ("admin@tradmusic.test", "Fiona", "Hayes", ["ROLE_ADMIN"]),
    "aoife": ("aoife.brennan@tradmusic.test", "Aoife", "Brennan", ["ROLE_MUSICIAN"]),
    "cillian": ("cillian.walsh@tradmusic.test", "Cillian", "Walsh", ["ROLE_MUSICIAN"]),
    "niamh": ("niamh.doherty@tradmusic.test", "Niamh", "Doherty", ["ROLE_MUSICIAN"]),
    "ronan": ("ronan.keane@tradmusic.test", "Ronan", "Keane", ["ROLE_MUSICIAN"]),
    "owen": ("owen.doyle@tradmusic.test", "Owen", "Doyle", ["ROLE_MUSICIAN", "ROLE_VENUE_MANAGER"]),
    "siobhan": ("siobhan.murphy@tradmusic.test", "Siobhán", "Murphy", ["ROLE_MUSICIAN"]),
    "declan": ("declan.farrell@tradmusic.test", "Declan", "Farrell", ["ROLE_MUSICIAN"]),
    "maire": ("maire.quinlan@tradmusic.test", "Máire", "Quinlan", ["ROLE_MUSICIAN"]),
    "padraig": ("padraig.lynch@tradmusic.test", "Pádraig", "Lynch", ["ROLE_MUSICIAN"]),
    "clodagh": ("clodagh.nolan@tradmusic.test", "Clodagh", "Nolan", ["ROLE_MUSICIAN"]),
    "grainne": ("grainne.kelly@tradmusic.test", "Gráinne", "Kelly", ["ROLE_VENUE_MANAGER"]),
    "liam": ("liam.byrne@tradmusic.test", "Liam", "Byrne", ["ROLE_VENUE_MANAGER"]),
}
PASSWORD = "password"

# slug: dict
MUSICIANS = {
    "aoife-brennan": dict(user="aoife", town="galway", instruments=["fiddle", "tin-whistle"], available=True,
        bio="Aoife grew up in Connemara, learning tunes by ear from her grandfather. She now plays fiddle in the pubs of Galway most weekends and teaches at the Crooked Bow's slow session."),
    "cillian-walsh": dict(user="cillian", town="ennis", instruments=["uilleann-pipes"], available=False,
        bio="Piper from County Clare, Cillian has been playing the uilleann pipes for twenty years. He is busy recording an album this autumn."),
    "niamh-doherty": dict(user="niamh", town="galway", instruments=["flute", "tin-whistle"], available=True,
        bio="Niamh plays a wooden flute in the Sligo style. You will often find her at the Friday gigs of Quay Street."),
    "ronan-keane": dict(user="ronan", town="doolin", instruments=["bodhran"], available=True,
        bio="Ronan keeps the rhythm for half the sessions of Doolin. He plays a goatskin bodhrán made by his uncle."),
    "owen-doyle": dict(user="owen", town="doolin", instruments=["fiddle"], available=False,
        bio="Owen runs Doyle's of Doolin and The Old Forge, and never misses a chance to take out his fiddle behind the bar."),
    "siobhan-murphy": dict(user="siobhan", town="dublin", instruments=["concertina"], available=True,
        bio="Siobhán plays an Anglo concertina and loves polkas and slides from Sliabh Luachra."),
    "declan-farrell": dict(user="declan", town="dublin", instruments=["banjo", "guitar"], available=True,
        bio="Tenor banjo player and guitar accompanist, Declan has toured with several Dublin bands."),
    "maire-quinlan": dict(user="maire", town="ennis", instruments=["harp"], available=False,
        bio="Máire plays the Irish harp, from O'Carolan airs to modern compositions."),
    "padraig-lynch": dict(user="padraig", town="dublin", instruments=["button-accordion"], available=True,
        bio="Pádraig plays a B/C button accordion and leads the Monday night session at the Tipper & Reel."),
    "clodagh-nolan": dict(user="clodagh", town="galway", instruments=["bouzouki", "guitar", "low-whistle"], available=True,
        bio="Clodagh backs tunes on the bouzouki and guitar, and brings out her low whistle for slow airs."),
}

VENUES = {
    "the-crooked-bow": dict(name="The Crooked Bow", town="galway", address="14 Quay Street, Galway", manager="grainne",
        description="A narrow, wood-panelled pub on Quay Street with live music seven nights a week. Musicians gather by the fireplace at the back."),
    "the-salmon-weir": dict(name="The Salmon Weir", town="galway", address="3 Newtownsmith, Galway", manager="grainne",
        description="A lively bar near the river, known for its big Friday gigs and its snug full of old photographs."),
    "doyles-of-doolin": dict(name="Doyle's of Doolin", town="doolin", address="Fisher Street, Doolin", manager="owen",
        description="A family pub on the road to the pier, where tunes start at lunchtime in summer."),
    "the-tipper-and-reel": dict(name="The Tipper & Reel", town="dublin", address="27 Capel Street, Dublin 1", manager="liam",
        description="A Dublin bar with a long counter and a small stage, home of the Monday night session."),
    "the-half-door": dict(name="The Half Door", town="dublin", address="8 Francis Street, Dublin 8", manager="liam",
        description="A tiny pub in the Liberties with red benches and late-night tunes on Fridays."),
    "the-old-forge": dict(name="The Old Forge", town="ennis", address="11 Abbey Street, Ennis", manager="owen",
        description="A former forge turned pub, with a courtyard where concerts are held on summer evenings."),
}

# ref, venue, modifier (relative to today), lineup, description
GIGS = [
    ("gig-01", "the-crooked-bow", "+4 days 21:00", ["aoife-brennan", "ronan-keane"],
     "Aoife and Ronan open the weekend with a set of Connemara reels and slides."),
    ("gig-02", "the-crooked-bow", "+5 days 21:30", ["clodagh-nolan", "cillian-walsh"], None),
    ("gig-03", "the-salmon-weir", "+11 days 20:30", ["niamh-doherty", "clodagh-nolan"],
     "Flute, whistles and bouzouki: an evening of slow airs and jigs."),
    ("gig-04", "doyles-of-doolin", "+2 days 21:00", ["owen-doyle", "ronan-keane"], None),
    ("gig-05", "doyles-of-doolin", "-4 days 20:30", ["cillian-walsh"],
     "A solo evening of piping, with stories from County Clare."),
    ("gig-06", "the-tipper-and-reel", "+3 days 21:00", ["siobhan-murphy", "declan-farrell", "padraig-lynch"],
     "Polkas, slides and a few songs with three Dublin regulars."),
    ("gig-07", "the-tipper-and-reel", "-9 days 21:00", ["declan-farrell"], None),
    ("gig-08", "the-half-door", "+6 days 17:00", ["padraig-lynch", "siobhan-murphy"],
     "A relaxed Sunday afternoon of box and concertina duets."),
    ("gig-09", "the-old-forge", "+9 days 20:00", ["maire-quinlan", "cillian-walsh"],
     "Harp and pipes in the old forge: O'Carolan tunes and airs."),
    ("gig-10", "the-salmon-weir", "-2 days 21:00", ["aoife-brennan", "clodagh-nolan"], None),
]

# venue, name, day of week, time
SESSIONS = [
    ("the-crooked-bow", "Slow Session for Learners", "Tuesday", "19:30"),
    ("the-crooked-bow", "Sunday Evening Session", "Sunday", "18:00"),
    ("doyles-of-doolin", "Big Thursday Session", "Thursday", "21:30"),
    ("the-tipper-and-reel", "Monday Night Session", "Monday", "21:00"),
    ("the-half-door", "Tunes at the Half Door", "Friday", "22:00"),
]

# musician, gig, status, created (relative), message
JOIN_REQUESTS = [
    ("niamh-doherty", "gig-01", "pending", "-1 day 09:40", "I play flute and whistle, I know most of the Friday regulars."),
    ("clodagh-nolan", "gig-01", "pending", "-2 days 18:15", None),
    ("cillian-walsh", "gig-02", "accepted", "-6 days 11:00", None),
    ("declan-farrell", "gig-08", "declined", "-3 days 14:20", "Happy to bring the banjo along."),
    ("siobhan-murphy", "gig-09", "pending", "-1 day 20:05", "I'll be in Clare that week, I'd love to join Máire and Cillian."),
    ("aoife-brennan", "gig-04", "pending", "-2 days 10:30", "Ronan told me you were looking for a fiddle on Wednesday."),
    ("aoife-brennan", "gig-10", "accepted", "-8 days 16:45", None),
    ("aoife-brennan", "gig-08", "declined", "-4 days 12:00", "I'm in Dublin that weekend, I can play some Galway tunes."),
]

# Unsplash photos: file -> (photo id, photographer)
PHOTO_CREDITS = {
    "uploads/musicians/aoife-brennan.jpg": ("ysyRG_lkmiM", "Nancy Hughes"),
    "uploads/musicians/cillian-walsh.jpg": ("iLCM22Qe_C0", "Mary Borysova"),
    "uploads/musicians/niamh-doherty.jpg": ("wfVREQs7KXQ", "Aswin Raj"),
    "uploads/musicians/ronan-keane.jpg": ("xD8DPNDYG6E", "Caleb Toranzo"),
    "uploads/musicians/owen-doyle.jpg": ("d9_2kPJBG0U", "Lucia Macedo"),
    "uploads/musicians/siobhan-murphy.jpg": ("BgTZHWcXvqY", "The Metropolitan Museum of Art"),
    "uploads/musicians/declan-farrell.jpg": ("inj45s7t9WY", "Duncan McNab"),
    "uploads/musicians/maire-quinlan.jpg": ("AGYEwWQ6Nww", "Patti Black"),
    "uploads/musicians/padraig-lynch.jpg": ("Yy5YeqtXjSc", "David Vilches"),
    "uploads/musicians/clodagh-nolan.jpg": ("WnIZ57zUK-E", "Joel Swick"),
    "uploads/venues/the-crooked-bow.jpg": ("3fDv4xwdFZs", "K. Mitch Hodge"),
    "uploads/venues/the-salmon-weir.jpg": ("4kLy0asVZhA", "Jonathan Borba"),
    "uploads/venues/doyles-of-doolin.jpg": ("xzLogOO5cmo", "Help Stay"),
    "uploads/venues/the-tipper-and-reel.jpg": ("nHBZT4Qi44Y", "Jon Tyson"),
    "uploads/venues/the-half-door.jpg": ("kPHYuzqoaz0", "Theme Photos"),
    "uploads/venues/the-old-forge.jpg": ("dE8kZkt25bs", "K. Mitch Hodge"),
    "assets/images/hero.jpg": ("8A4ZnQ9vxYg", "Jonathan Borba"),
}


def resolve(modifier):
    """Mimics PHP's new DateTimeImmutable('+4 days 21:00') from TODAY."""
    days, time = modifier.split(" days " if " days " in modifier else " day ")
    h, m = map(int, time.split(":"))
    return (TODAY + timedelta(days=int(days))).replace(hour=h, minute=m)


def full_name(user_key):
    _, first, last, _ = USERS[user_key]
    return f"{first} {last}"


def musician_name(slug):
    return full_name(MUSICIANS[slug]["user"])


def gig(ref):
    return next(g for g in GIGS if g[0] == ref)
