"""Generates the TradMusic mockup screens and FIXTURES.md from data.py.

Usage: python3 tools/generate.py
"""
from html import escape as e
from pathlib import Path
from data import *

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------- formatting
def t12(dt):
    h = dt.hour % 12 or 12
    return f"{h}:{dt.minute:02d} {'am' if dt.hour < 12 else 'pm'}"


def short_date(dt):
    return f"{dt:%a} {dt.day} {dt:%b}"


def long_date(dt):
    return f"{dt:%A} {dt.day} {dt:%B} {dt.year}"


def iso(dt):
    return f"{dt:%Y-%m-%dT%H:%M}"


def time_from(s):
    h, m = map(int, s.split(":"))
    return t12(TODAY.replace(hour=h, minute=m))


def icon(name):
    return f'<i class="fa-solid fa-{name}" aria-hidden="true"></i>'


def upcoming(g):
    return resolve(g[2]) > TODAY


# ---------------------------------------------------------------- layout
NAV = [("musicians", "Musicians"), ("gigs", "Gigs"), ("venues", "Venues"), ("about", "About")]


def user_menu(user_key):
    email, first, last, roles = USERS[user_key]
    items = []
    if "ROLE_MUSICIAN" in roles:
        slug = next(s for s, m in MUSICIANS.items() if m["user"] == user_key)
        avatar = f"uploads/musicians/{slug}.jpg"
        items += [
            '<li class="user-menu__heading">Musician</li>',
            '<li><a class="user-menu__link" href="my-profile.html">My profile</a></li>',
            '<li><a class="user-menu__link" href="my-join-requests.html">My join requests</a></li>',
        ]
    else:
        avatar = "assets/images/placeholder-musician.svg"
    if "ROLE_VENUE_MANAGER" in roles:
        venues = [s for s, v in VENUES.items() if v["manager"] == user_key]
        pending = sum(1 for jr in JOIN_REQUESTS if jr[2] == "pending" and gig(jr[1])[1] in venues)
        count = f' <span class="badge badge--count" aria-label="{pending} pending">{pending}</span>' if pending else ""
        items += [
            '<li class="user-menu__heading">Venue manager</li>',
            '<li><a class="user-menu__link" href="my-venues.html">My venues</a></li>',
            f'<li><a class="user-menu__link" href="join-requests.html">Join requests{count}</a></li>',
        ]
    items.append(f'<li class="user-menu__separator"><a class="user-menu__link" href="index.html"><span>Log out</span>{icon("right-from-bracket")}</a></li>')
    li = "\n                    ".join(items)
    return f"""<details class="user-menu">
                <summary class="user-menu__toggle">
                    <img src="{avatar}" alt="">
                    <span class="user-menu__name">{e(first)} {e(last)}</span>
                </summary>
                <ul class="user-menu__list">
                    {li}
                </ul>
            </details>"""


def page(filename, title, body, active=None, user=None):
    nav = "\n                ".join(
        f'<li><a class="site-nav__link" href="{k}.html"{" aria-current=\"page\"" if k == active else ""}>{label}</a></li>'
        for k, label in NAV
    )
    if user:
        account = user_menu(user)
    else:
        account = """<a class="btn btn--ghost btn--sm" href="login.html">Log in</a>
            <a class="btn btn--accent btn--sm" href="register.html">Sign up</a>"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(title)}</title>
    <link rel="icon" href="assets/images/logo.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
    <link rel="stylesheet" href="assets/styles/app.css">
</head>
<body>

<header class="site-header">
    <div class="container site-header__inner">
        <a class="site-header__brand" href="index.html">
            <img src="assets/images/logo.svg" alt="" width="40" height="40">
            TradMusic
        </a>
        <nav class="site-nav" aria-label="Main">
            <ul class="site-nav__list">
                {nav}
            </ul>
        </nav>
        <div class="site-header__account">
            {account}
        </div>
    </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
    <div class="container site-footer__inner">
        <p>TradMusic &copy; 2026 — Irish traditional music, live.</p>
        <ul class="site-footer__links">
            <li><a href="about.html">About</a></li>
            <li><a href="musicians.html">Musicians</a></li>
            <li><a href="gigs.html">Gigs</a></li>
            <li><a href="venues.html">Venues</a></li>
        </ul>
    </div>
</footer>

</body>
</html>
"""
    (ROOT / filename).write_text(html)


# ---------------------------------------------------------------- components
def instrument_badges(slugs):
    items = "\n".join(
        f'<li><a class="badge badge--instrument" href="musicians.html?instrument={s}"><img src="uploads/instruments/{s}.svg" alt=""> {e(INSTRUMENT_NAME[s])}</a></li>'
        for s in slugs
    )
    return f'<ul class="badge-list">\n{items}\n</ul>'


def musician_card(slug):
    m = MUSICIANS[slug]
    tag = '<span class="card__tag badge badge--available">Available</span>' if m["available"] else ""
    return f"""<article class="card">
    <img class="card__media card__media--square" src="uploads/musicians/{slug}.jpg" alt="">
    {tag}
    <div class="card__body">
        <h3 class="card__title"><a class="card__link" href="musician.html">{e(musician_name(slug))}</a></h3>
        <p class="card__meta"><span>{icon("location-dot")}{TOWN_NAME[m["town"]]}</span></p>
        {instrument_badges(m["instruments"])}
    </div>
</article>"""


def venue_card(slug):
    v = VENUES[slug]
    n_gigs = sum(1 for g in GIGS if g[1] == slug and upcoming(g))
    n_sessions = sum(1 for s in SESSIONS if s[0] == slug)
    sessions = f'<span>{icon("repeat")}{n_sessions} weekly session{"s" if n_sessions > 1 else ""}</span>' if n_sessions else ""
    return f"""<article class="card">
    <img class="card__media" src="uploads/venues/{slug}.jpg" alt="">
    <div class="card__body">
        <h3 class="card__title"><a class="card__link" href="venue.html">{e(v["name"])}</a></h3>
        <p class="card__meta">
            <span>{icon("location-dot")}{TOWN_NAME[v["town"]]}</span>
            <span>{icon("calendar")}{n_gigs} upcoming gig{"s" if n_gigs > 1 else ""}</span>
            {sessions}
        </p>
    </div>
</article>"""


def date_block(dt):
    return f"""<time class="event__date" datetime="{iso(dt)}">
        <span class="event__weekday">{dt:%a}</span>
        <span class="event__day">{dt.day}</span>
        <span class="event__month">{dt:%b}</span>
    </time>"""


def gig_row(g, title="venue", action=True):
    ref, venue, mod, lineup, desc = g
    dt = resolve(mod)
    v = VENUES[venue]
    past = not upcoming(g)
    heading = e(v["name"]) if title == "venue" else f"{dt:%A} {dt.day} {dt:%B}"
    meta = []
    if title == "venue":
        meta.append(f'<span>{icon("location-dot")}{TOWN_NAME[v["town"]]}</span>')
    meta.append(f'<span>{icon("clock")}{t12(dt)}</span>')
    meta.append(f'<span>{icon("users")}{e(", ".join(musician_name(s) for s in lineup))}</span>')
    act = f"""
    <div class="event__action">
        <a class="btn btn--secondary btn--sm" href="gig.html">See the gig</a>
    </div>""" if action and not past else ""
    metas = "\n            ".join(meta)
    return f"""<li class="event{" event--past" if past else ""}">
    {date_block(dt)}
    <div class="event__body">
        <h3 class="event__title"><a href="gig.html">{heading}</a></h3>
        <p class="event__meta">
            {metas}
        </p>
    </div>{act}
</li>"""


def session_row(s):
    venue, name, day, time = s
    return f"""<li class="event">
    <div class="event__date event__date--weekly">
        <span class="event__weekday">Every</span>
        <span class="event__day">{day[:3]}</span>
    </div>
    <div class="event__body">
        <h3 class="event__title">{e(name)}</h3>
        <p class="event__meta">
            <span>{icon("clock")}{time_from(time)}</span>
            <span>{icon("door-open")}All musicians welcome</span>
        </p>
    </div>
</li>"""


def select(form, field, label, options, selected=None, placeholder=None, required=True):
    req = ' class="required"' if required else ""
    reqattr = ' required="required"' if required else ""
    opts = []
    if placeholder is not None:
        opts.append(f'<option value="">{e(placeholder)}</option>')
    for i, (value, text) in enumerate(options, 1):
        sel = ' selected="selected"' if value == selected else ""
        opts.append(f'<option value="{i}"{sel}>{e(text)}</option>')
    o = "\n        ".join(opts)
    return f"""<div>
    <label for="{form}_{field}"{req}>{label}</label>
    <select id="{form}_{field}" name="{form}[{field}]"{reqattr}>
        {o}
    </select>
</div>"""


def text_field(form, field, label, value="", type_="text", required=True, help_=None, attrs=""):
    req = ' class="required"' if required else ""
    reqattr = ' required="required"' if required else ""
    val = f' value="{e(value)}"' if value else ""
    described = f' aria-describedby="{form}_{field}_help"' if help_ else ""
    help_html = f'\n    <p id="{form}_{field}_help" class="help-text">{help_}</p>' if help_ else ""
    return f"""<div>
    <label for="{form}_{field}"{req}>{label}</label>
    <input type="{type_}" id="{form}_{field}" name="{form}[{field}]"{reqattr}{described}{attrs}{val}>{help_html}
</div>"""


def textarea(form, field, label, value="", required=True, help_=None, attrs=""):
    req = ' class="required"' if required else ""
    reqattr = ' required="required"' if required else ""
    described = f' aria-describedby="{form}_{field}_help"' if help_ else ""
    help_html = f'\n    <p id="{form}_{field}_help" class="help-text">{help_}</p>' if help_ else ""
    return f"""<div>
    <label for="{form}_{field}"{req}>{label}</label>
    <textarea id="{form}_{field}" name="{form}[{field}]"{reqattr}{described}{attrs}>{e(value)}</textarea>{help_html}
</div>"""


def checkboxes(form, field, label, options, checked):
    pairs = "\n        ".join(
        f'<input type="checkbox" id="{form}_{field}_{i}" name="{form}[{field}][]" value="{i + 1}"{" checked=\"checked\"" if v in checked else ""}><label for="{form}_{field}_{i}">{e(text)}</label>'
        for i, (v, text) in enumerate(options)
    )
    return f"""<div>
    <label>{label}</label>
    <div id="{form}_{field}">
        {pairs}
    </div>
</div>"""


def symfony_form(name, rows, submit, method="post", multipart=False, token=True):
    enctype = ' enctype="multipart/form-data"' if multipart else ""
    tok = f'\n        <input type="hidden" id="{name}__token" name="{name}[_token]" value="csrf-token">' if token else ""
    inner = "\n".join(rows).replace("\n", "\n        ")
    return f"""<form name="{name}" method="{method}"{enctype}>
    <div id="{name}">
        {inner}
        <div><button type="submit" id="{name}_submit" name="{name}[submit]">{submit}</button></div>{tok}
    </div>
</form>"""


def indent(html, n):
    pad = " " * n
    return "\n".join(pad + line if line.strip() else line for line in html.split("\n"))


def post_button(label, cls, icon_name=None):
    ic = icon(icon_name) + " " if icon_name else ""
    return f"""<form class="inline-form" method="post" action="#">
    <input type="hidden" name="_token" value="csrf-token">
    <button class="btn {cls} btn--sm" type="submit">{ic}{label}</button>
</form>"""


STATUS_BADGE = {
    "pending": f'<span class="badge badge--pending">{icon("hourglass-half")} Pending</span>',
    "accepted": f'<span class="badge badge--accepted">{icon("check")} Accepted</span>',
    "declined": f'<span class="badge badge--declined">{icon("xmark")} Declined</span>',
}

TOWN_OPTIONS = [(s, n) for s, n in TOWNS]
UPCOMING_GIGS = sorted([g for g in GIGS if upcoming(g)], key=lambda g: resolve(g[2]))
PAST_GIGS = sorted([g for g in GIGS if not upcoming(g)], key=lambda g: resolve(g[2]), reverse=True)
BY_LAST_NAME = sorted(MUSICIANS, key=lambda s: USERS[MUSICIANS[s]["user"]][2])


# ================================================================ screens
def screen_index():
    gigs = "\n".join(gig_row(g) for g in UPCOMING_GIGS[:4])
    available = [s for s in BY_LAST_NAME if MUSICIANS[s]["available"]][:4]
    cards = "\n".join(musician_card(s) for s in available)
    body = f"""
<section class="hero hero--photo">
    <div class="container">
        <h1>Find your trad musicians in seconds</h1>
        <p>Fiddlers, pipers and bodhrán players across Ireland, the pubs where they play, and the sessions you can join.</p>
        <div class="button-group">
            <a class="btn btn--accent" href="musicians.html">Browse musicians {icon("arrow-right")}</a>
            <a class="btn btn--ghost" href="gigs.html">See upcoming gigs</a>
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <div class="section__header">
            <h2>Upcoming gigs</h2>
            <a class="section__link" href="gigs.html">All gigs {icon("arrow-right")}</a>
        </div>
        <ul class="event-list">
{indent(gigs, 12)}
        </ul>
    </div>
</section>

<section class="section section--alt">
    <div class="container">
        <div class="section__header">
            <h2>Available musicians</h2>
            <a class="section__link" href="musicians.html">All musicians {icon("arrow-right")}</a>
        </div>
        <div class="grid">
{indent(cards, 12)}
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <div class="cta-band">
            <div>
                <h2>You play trad music?</h2>
                <p>Create your musician profile, get contacted by organisers and ask to join gigs near you.</p>
            </div>
            <a class="btn btn--accent" href="register.html">Join TradMusic</a>
        </div>
    </div>
</section>"""
    page("index.html", "TradMusic — Find your trad musicians", body)


def screen_musicians():
    first_page = BY_LAST_NAME[:6]
    cards = "\n".join(musician_card(s) for s in first_page)
    filters = symfony_form("musician_search", [
        select("musician_search", "town", "Town", TOWN_OPTIONS, placeholder="All towns", required=False),
        select("musician_search", "instrument", "Instrument", INSTRUMENTS, placeholder="All instruments", required=False),
    ], f'{icon("magnifying-glass")} Search', method="get", token=False)
    body = f"""
<div class="container">
    <header class="page-header">
        <h1>Musicians</h1>
        <p>Find a fiddler for your wedding, a piper for your festival or a whole band for your pub.</p>
    </header>

    <div class="filters">
{indent(filters, 8)}
    </div>

    <section class="section">
        <h2 class="visually-hidden">Results</h2>
        <p class="text-muted" style="margin-bottom: var(--space-md)">{len(MUSICIANS)} musicians</p>
        <div class="grid">
{indent(cards, 12)}
        </div>

        <nav class="pagination" aria-label="Pagination">
            <ul class="pagination__list">
                <li><a class="pagination__link" aria-disabled="true">{icon("chevron-left")}<span class="visually-hidden">Previous page</span></a></li>
                <li><a class="pagination__link" href="musicians.html?page=1" aria-current="page">1</a></li>
                <li><a class="pagination__link" href="musicians.html?page=2">2</a></li>
                <li><a class="pagination__link" href="musicians.html?page=2">{icon("chevron-right")}<span class="visually-hidden">Next page</span></a></li>
            </ul>
        </nav>
    </section>
</div>"""
    page("musicians.html", "Musicians · TradMusic", body, active="musicians")


def screen_musician():
    slug = "aoife-brennan"
    m = MUSICIANS[slug]
    name = musician_name(slug)
    first = USERS[m["user"]][1]
    gigs = [g for g in UPCOMING_GIGS if slug in g[3]]
    gig_list = "\n".join(gig_row(g) for g in gigs)
    contact = symfony_form("contact", [
        text_field("contact", "name", "Your name"),
        text_field("contact", "email", "Your email", type_="email"),
        textarea("contact", "message", "Message", help_=f"Tell {first} about the date, the place and the kind of event."),
    ], "Send message")
    body = f"""
<div class="container">
    <header class="page-header">
        <div class="profile">
            <img class="profile__photo" src="uploads/musicians/{slug}.jpg" alt="">
            <div class="profile__body">
                <h1>{e(name)}</h1>
                <div class="profile__meta">
                    <span class="badge badge--town">{icon("location-dot")} {TOWN_NAME[m["town"]]}</span>
                    <span class="badge badge--available">Available</span>
                </div>
                {instrument_badges(m["instruments"]).replace(chr(10), chr(10) + " " * 16)}
            </div>
        </div>
    </header>

    <div class="split section">
        <div class="stack-lg">
            <section class="prose">
                <h2 style="margin-top: 0">About {e(first)}</h2>
                <p>{e(m["bio"])}</p>
            </section>

            <section>
                <div class="section__header section__header--sm">
                    <h2>Upcoming gigs</h2>
                </div>
                <ul class="event-list">
{indent(gig_list, 20)}
                </ul>
            </section>
        </div>

        <aside class="form-panel">
            <h2 class="form-panel__title">Contact {e(first)}</h2>
{indent(contact, 12)}
        </aside>
    </div>
</div>"""
    page("musician.html", f"{name} · TradMusic", body, active="musicians")


def screen_venues():
    cards = "\n".join(venue_card(s) for s in sorted(VENUES, key=lambda s: VENUES[s]["name"]))
    filters = symfony_form("venue_search", [
        select("venue_search", "town", "Town", TOWN_OPTIONS, placeholder="All towns", required=False),
    ], f'{icon("magnifying-glass")} Search', method="get", token=False)
    body = f"""
<div class="container">
    <header class="page-header">
        <h1>Venues</h1>
        <p>The pubs where trad music is played, from Dublin to Doolin.</p>
    </header>

    <div class="filters">
{indent(filters, 8)}
    </div>

    <section class="section">
        <h2 class="visually-hidden">Results</h2>
        <div class="grid grid--wide">
{indent(cards, 12)}
        </div>
    </section>
</div>"""
    page("venues.html", "Venues · TradMusic", body, active="venues")


def screen_venue():
    slug = "the-crooked-bow"
    v = VENUES[slug]
    gigs = "\n".join(gig_row(g, title="date") for g in UPCOMING_GIGS if g[1] == slug)
    sessions = "\n".join(session_row(s) for s in SESSIONS if s[0] == slug)
    body = f"""
<div class="container">
    <header class="page-header">
        <img class="venue-banner" src="uploads/venues/{slug}.jpg" alt="">
        <h1 style="margin-top: var(--space-lg)">{e(v["name"])}</h1>
        <p>{e(v["description"])}</p>
    </header>

    <div class="split section">
        <div class="stack-lg">
            <section>
                <div class="section__header section__header--sm">
                    <h2>Upcoming gigs</h2>
                </div>
                <ul class="event-list">
{indent(gigs, 20)}
                </ul>
            </section>

            <section>
                <div class="section__header section__header--sm">
                    <h2>Weekly sessions</h2>
                </div>
                <ul class="event-list">
{indent(sessions, 20)}
                </ul>
            </section>
        </div>

        <aside class="info-panel">
            <div class="info-panel__body">
                <h2 class="info-panel__title">Find us</h2>
                <ul class="info-panel__list">
                    <li>{icon("location-dot")}<span>{e(v["address"])}</span></li>
                    <li>{icon("city")}<a href="venues.html?town={v["town"]}">More venues in {TOWN_NAME[v["town"]]}</a></li>
                </ul>
            </div>
        </aside>
    </div>
</div>"""
    page("venue.html", f"{v['name']} · TradMusic", body, active="venues")


def screen_gigs():
    rows = "\n".join(gig_row(g) for g in UPCOMING_GIGS)
    filters = symfony_form("gig_search", [
        select("gig_search", "town", "Town", TOWN_OPTIONS, placeholder="All towns", required=False),
    ], f'{icon("magnifying-glass")} Search', method="get", token=False)
    body = f"""
<div class="container">
    <header class="page-header">
        <h1>Gigs</h1>
        <p>Live trad music in the pubs of Ireland. Sessions are listed on each venue's page.</p>
    </header>

    <nav class="tabs" aria-label="Gigs">
        <ul class="tabs__list">
            <li><a class="tabs__link" href="gigs.html" aria-current="page">Upcoming gigs</a></li>
            <li><a class="tabs__link" href="gigs.html?when=past">Past gigs</a></li>
        </ul>
    </nav>

    <div class="filters">
{indent(filters, 8)}
    </div>

    <section class="section">
        <h2 class="visually-hidden">Upcoming gigs</h2>
        <ul class="event-list">
{indent(rows, 12)}
        </ul>
    </section>
</div>"""
    page("gigs.html", "Gigs · TradMusic", body, active="gigs")


def screen_gig():
    g = gig("gig-01")
    ref, venue, mod, lineup, desc = g
    dt = resolve(mod)
    v = VENUES[venue]
    lineup_html = "\n".join(f"""<li class="lineup__item">
    <img class="lineup__avatar" src="uploads/musicians/{s}.jpg" alt="">
    <div>
        <p class="lineup__name"><a href="musician.html">{e(musician_name(s))}</a></p>
        <p class="lineup__instruments">{e(", ".join(INSTRUMENT_NAME[i] for i in MUSICIANS[s]["instruments"]))}</p>
    </div>
</li>""" for s in lineup)
    join_form = symfony_form("join_request", [
        textarea("join_request", "message", "Message to the venue manager", required=False,
                 help_="Optional — 500 characters max.", attrs=' maxlength="500"'),
    ], "Ask to join")
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">Gig</p>
        <h1>{e(v["name"])}</h1>
        <p><time datetime="{iso(dt)}">{long_date(dt)}, {t12(dt)}</time> · {TOWN_NAME[v["town"]]}</p>
    </header>

    <div class="split">
        <div class="stack-lg">
            <section class="prose">
                <p>{e(desc)}</p>
            </section>

            <section>
                <div class="section__header section__header--sm">
                    <h2>Lineup</h2>
                </div>
                <ul class="lineup">
{indent(lineup_html, 20)}
                </ul>
            </section>
        </div>

        <aside class="stack-lg">
            <div class="join-status">
                <h2 class="join-status__title">{icon("music")} Want to play at this gig?</h2>
{indent(join_form, 16)}
            </div>

            <article class="info-panel">
                <img class="info-panel__media" src="uploads/venues/{venue}.jpg" alt="">
                <div class="info-panel__body">
                    <h2 class="info-panel__title"><a href="venue.html">{e(v["name"])}</a></h2>
                    <ul class="info-panel__list">
                        <li>{icon("location-dot")}<span>{e(v["address"])}</span></li>
                    </ul>
                </div>
            </article>
        </aside>
    </div>
</div>"""
    page("gig.html", f"Gig at {v['name']}, {short_date(dt)} · TradMusic", body, active="gigs", user="declan")


def screen_about():
    body = f"""
<div class="container">
    <header class="page-header">
        <h1>About TradMusic</h1>
        <p>A meeting place for Irish traditional musicians, the pubs that host them and everyone who loves a good session.</p>
    </header>

    <section class="prose section">
        <h2 style="margin-top: 0">Why TradMusic?</h2>
        <p>Every night, somewhere in Ireland, a fiddle, a flute and a bodhrán start a set of reels in the corner of a pub. Finding out where and when has always relied on word of mouth. TradMusic puts it all in one place.</p>

        <h2>For music lovers</h2>
        <ul>
            <li>Browse upcoming gigs in your town.</li>
            <li>Discover the weekly sessions of each venue.</li>
            <li>Contact an available musician for your wedding, festival or party.</li>
        </ul>

        <h2>For musicians</h2>
        <ul>
            <li>Create a profile with your instruments and your town.</li>
            <li>Let organisers know when you are available.</li>
            <li>Ask venue managers to join the lineup of their gigs.</li>
        </ul>

        <h2>For venues</h2>
        <ul>
            <li>Publish your gigs and your weekly sessions.</li>
            <li>Build the lineup of each gig and answer musicians' join requests.</li>
        </ul>

        <p><a class="btn" href="register.html">Create your account</a></p>
    </section>
</div>"""
    page("about.html", "About · TradMusic", body, active="about")


def screen_login():
    body = f"""
<div class="container container--narrow section">
    <div class="form-panel">
        <h1 class="form-panel__title">Log in</h1>

        <form method="post">
            <div>
                <label for="username">Email</label>
                <input type="email" value="" name="_username" id="username" autocomplete="email" required autofocus>
            </div>
            <div>
                <label for="password">Password</label>
                <input type="password" name="_password" id="password" autocomplete="current-password" required>
            </div>
            <div>
                <input type="checkbox" name="_remember_me" id="remember_me">
                <label for="remember_me">Remember me</label>
            </div>
            <input type="hidden" name="_csrf_token" value="csrf-token">
            <button type="submit">Log in</button>
        </form>

        <p class="form-panel__footer">No account yet? <a href="register.html">Sign up</a></p>
    </div>
</div>"""
    page("login.html", "Log in · TradMusic", body)


def screen_register():
    form = "registration_form"
    rows = [
        f"""<div>
    <label class="required">I want to</label>
    <div id="{form}_accountType">
        <input type="radio" id="{form}_accountType_0" name="{form}[accountType]" required="required" value="musician" checked="checked"><label for="{form}_accountType_0" class="required">create a musician profile</label>
        <input type="radio" id="{form}_accountType_1" name="{form}[accountType]" required="required" value="venue_manager"><label for="{form}_accountType_1" class="required">manage a venue</label>
    </div>
</div>""",
        text_field(form, "firstName", "First name"),
        text_field(form, "lastName", "Last name"),
        text_field(form, "email", "Email", type_="email"),
        text_field(form, "plainPassword", "Password", type_="password", help_="At least 8 characters.", attrs=' autocomplete="new-password"'),
    ]
    body = f"""
<div class="container container--narrow section">
    <div class="form-panel">
        <h1 class="form-panel__title">Create your account</h1>
{indent(symfony_form(form, rows, "Sign up"), 8)}
        <p class="form-panel__footer">Already registered? <a href="login.html">Log in</a></p>
    </div>
</div>"""
    page("register.html", "Sign up · TradMusic", body)


def screen_my_profile():
    slug = "aoife-brennan"
    m = MUSICIANS[slug]
    _, first, last, _ = USERS[m["user"]]
    form = "musician_profile"
    rows = [
        text_field(form, "firstName", "First name", first),
        text_field(form, "lastName", "Last name", last),
        select(form, "town", "Town", TOWN_OPTIONS, selected=m["town"], placeholder="Choose a town"),
        checkboxes(form, "instruments", "Instruments", INSTRUMENTS, m["instruments"]),
        textarea(form, "bio", "About you", m["bio"], required=False),
        f"""<div>
    <label for="{form}_available">Available for hire</label>
    <input type="checkbox" id="{form}_available" name="{form}[available]" value="1"{" checked=\"checked\"" if m["available"] else ""} aria-describedby="{form}_available_help">
    <p id="{form}_available_help" class="help-text">Visitors can contact you through your profile.</p>
</div>""",
        text_field(form, "photo", "Photo", type_="file", required=False,
                   help_="JPEG or PNG. Leave empty to keep your current photo.", attrs=' accept="image/jpeg, image/png"'),
    ]
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">My account</p>
        <h1>My profile</h1>
        <div class="page-header__actions">
            <a class="btn btn--secondary btn--sm" href="musician.html">{icon("eye")} View my public profile</a>
        </div>
    </header>

    <div class="alert-list">
        <div class="alert alert--success" role="status"><p>Your profile has been updated.</p></div>
    </div>

    <div class="form-panel">
{indent(symfony_form(form, rows, "Save", multipart=True), 8)}
    </div>
</div>"""
    page("my-profile.html", "My profile · TradMusic", body, user="aoife")


def screen_my_join_requests():
    slug = "aoife-brennan"
    reqs = sorted([jr for jr in JOIN_REQUESTS if jr[0] == slug], key=lambda jr: resolve(gig(jr[1])[2]), reverse=True)
    rows = []
    for musician, ref, status, created, message in reqs:
        g = gig(ref)
        dt = resolve(g[2])
        msg = f"“{e(message)}”" if message else "—"
        rows.append(f"""<tr>
    <td><a href="gig.html"><strong>{e(VENUES[g[1]]["name"])}</strong></a><br><time class="text-muted" datetime="{iso(dt)}">{short_date(dt)}, {t12(dt)}</time></td>
    <td class="table__message">{msg}</td>
    <td><time datetime="{iso(resolve(created))}">{short_date(resolve(created))}</time></td>
    <td>{STATUS_BADGE[status]}</td>
</tr>""")
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">My account</p>
        <h1>My join requests</h1>
        <p>The gigs you asked to play at, and the venue managers' answers.</p>
    </header>

    <div class="table-wrapper">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Gig</th>
                    <th scope="col">Message</th>
                    <th scope="col">Sent on</th>
                    <th scope="col">Status</th>
                </tr>
            </thead>
            <tbody>
{indent(chr(10).join(rows), 16)}
            </tbody>
        </table>
    </div>
</div>"""
    page("my-join-requests.html", "My join requests · TradMusic", body, user="aoife")


def screen_my_venues():
    mine = [s for s in VENUES if VENUES[s]["manager"] == "grainne"]
    cards = []
    for s in mine:
        v = VENUES[s]
        n_gigs = sum(1 for g in GIGS if g[1] == s and upcoming(g))
        pending = sum(1 for jr in JOIN_REQUESTS if jr[2] == "pending" and gig(jr[1])[1] == s)
        pend = f'<span>{icon("hourglass-half")}{pending} pending request{"s" if pending > 1 else ""}</span>' if pending else ""
        cards.append(f"""<article class="card">
    <img class="card__media" src="uploads/venues/{s}.jpg" alt="">
    <div class="card__body">
        <h2 class="card__title">{e(v["name"])}</h2>
        <p class="card__meta">
            <span>{icon("location-dot")}{TOWN_NAME[v["town"]]}</span>
            <span>{icon("calendar")}{n_gigs} upcoming gig{"s" if n_gigs > 1 else ""}</span>
            {pend}
        </p>
        <div class="card__footer button-group">
            <a class="btn btn--sm" href="venue-manage.html">{icon("list-check")} Manage gigs &amp; sessions</a>
            <a class="btn btn--secondary btn--sm" href="venue-form.html">{icon("pen")} Edit</a>
        </div>
    </div>
</article>""")
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">Venue manager</p>
        <h1>My venues</h1>
        <div class="page-header__actions">
            <a class="btn btn--sm" href="venue-form.html">{icon("plus")} New venue</a>
        </div>
    </header>

    <div class="grid grid--wide">
{indent(chr(10).join(cards), 8)}
    </div>
</div>"""
    page("my-venues.html", "My venues · TradMusic", body, user="grainne")


def screen_venue_form():
    slug = "the-crooked-bow"
    v = VENUES[slug]
    form = "venue"
    rows = [
        text_field(form, "name", "Name", v["name"]),
        select(form, "town", "Town", TOWN_OPTIONS, selected=v["town"], placeholder="Choose a town"),
        text_field(form, "address", "Address", v["address"]),
        textarea(form, "description", "Description", v["description"], required=False),
        text_field(form, "photo", "Photo", type_="file", required=False,
                   help_="JPEG or PNG. Leave empty to keep the current photo.", attrs=' accept="image/jpeg, image/png"'),
    ]
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">Venue manager</p>
        <h1>Edit {e(v["name"])}</h1>
    </header>

    <div class="form-panel">
{indent(symfony_form(form, rows, "Save", multipart=True), 8)}
    </div>
</div>"""
    page("venue-form.html", f"Edit {v['name']} · TradMusic", body, user="grainne")


def screen_venue_manage():
    slug = "the-crooked-bow"
    v = VENUES[slug]
    gig_rows = []
    for g in sorted([g for g in GIGS if g[1] == slug], key=lambda g: resolve(g[2])):
        dt = resolve(g[2])
        pending = sum(1 for jr in JOIN_REQUESTS if jr[1] == g[0] and jr[2] == "pending")
        pend = f'<a href="join-requests.html"><span class="badge badge--pending">{pending} pending</span></a>' if pending else '<span class="text-muted">—</span>'
        gig_rows.append(f"""<tr>
    <td><a href="gig.html"><strong><time datetime="{iso(dt)}">{short_date(dt)}, {t12(dt)}</time></strong></a></td>
    <td>{e(", ".join(musician_name(s) for s in g[3]))}</td>
    <td>{pend}</td>
    <td>
        <div class="table__actions">
            <a class="btn btn--secondary btn--sm" href="gig-form.html">{icon("pen")} Edit</a>
{indent(post_button("Delete", "btn--danger", "trash"), 12)}
        </div>
    </td>
</tr>""")
    session_rows = []
    for s in [s for s in SESSIONS if s[0] == slug]:
        session_rows.append(f"""<tr>
    <td><strong>{e(s[1])}</strong></td>
    <td>Every {s[2]}</td>
    <td>{time_from(s[3])}</td>
    <td>
        <div class="table__actions">
            <a class="btn btn--secondary btn--sm" href="session-form.html">{icon("pen")} Edit</a>
{indent(post_button("Delete", "btn--danger", "trash"), 12)}
        </div>
    </td>
</tr>""")
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">Venue manager</p>
        <h1>{e(v["name"])}</h1>
        <div class="page-header__actions">
            <a class="btn btn--secondary btn--sm" href="venue.html">{icon("eye")} View public page</a>
            <a class="btn btn--secondary btn--sm" href="venue-form.html">{icon("pen")} Edit venue</a>
        </div>
    </header>

    <div class="alert-list">
        <div class="alert alert--success" role="status"><p>The gig has been saved.</p></div>
    </div>

    <section class="section" style="padding-top: 0">
        <div class="section__header">
            <h2>Gigs</h2>
            <a class="btn btn--sm" href="gig-form.html">{icon("plus")} New gig</a>
        </div>
        <div class="table-wrapper">
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">Date</th>
                        <th scope="col">Lineup</th>
                        <th scope="col">Join requests</th>
                        <th scope="col"><span class="visually-hidden">Actions</span></th>
                    </tr>
                </thead>
                <tbody>
{indent(chr(10).join(gig_rows), 20)}
                </tbody>
            </table>
        </div>
    </section>

    <section class="section" style="padding-top: 0">
        <div class="section__header">
            <h2>Weekly sessions</h2>
            <a class="btn btn--sm" href="session-form.html">{icon("plus")} New session</a>
        </div>
        <div class="table-wrapper">
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Day</th>
                        <th scope="col">Time</th>
                        <th scope="col"><span class="visually-hidden">Actions</span></th>
                    </tr>
                </thead>
                <tbody>
{indent(chr(10).join(session_rows), 20)}
                </tbody>
            </table>
        </div>
    </section>
</div>"""
    page("venue-manage.html", f"Manage {v['name']} · TradMusic", body, user="grainne")


def screen_gig_form():
    g = gig("gig-01")
    dt = resolve(g[2])
    v = VENUES[g[1]]
    form = "gig"
    musicians = [(s, musician_name(s)) for s in BY_LAST_NAME]
    rows = [
        text_field(form, "startsAt", "Date and time", iso(dt), type_="datetime-local"),
        checkboxes(form, "lineup", "Lineup", musicians, g[3]),
        textarea(form, "description", "Description", g[4] or "", required=False),
    ]
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">{e(v["name"])}</p>
        <h1>Edit gig of {short_date(dt)}</h1>
    </header>

    <div class="form-panel">
{indent(symfony_form(form, rows, "Save"), 8)}
    </div>
</div>"""
    page("gig-form.html", f"Edit gig · TradMusic", body, user="grainne")


def screen_session_form():
    s = SESSIONS[0]
    v = VENUES[s[0]]
    form = "session"
    days = [(d, d) for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
    rows = [
        text_field(form, "name", "Name", s[1]),
        select(form, "dayOfWeek", "Day of the week", days, selected=s[2], placeholder="Choose a day"),
        text_field(form, "startsAt", "Time", s[3], type_="time"),
    ]
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">{e(v["name"])}</p>
        <h1>Edit session</h1>
    </header>

    <div class="form-panel">
{indent(symfony_form(form, rows, "Save"), 8)}
    </div>
</div>"""
    page("session-form.html", "Edit session · TradMusic", body, user="grainne")


def screen_join_requests():
    venues = [s for s in VENUES if VENUES[s]["manager"] == "grainne"]
    reqs = [jr for jr in JOIN_REQUESTS if gig(jr[1])[1] in venues]
    order = {"pending": 0, "accepted": 1, "declined": 1}
    reqs.sort(key=lambda jr: (order[jr[2]], resolve(gig(jr[1])[2])))
    rows = []
    for musician, ref, status, created, message in reqs:
        g = gig(ref)
        dt = resolve(g[2])
        msg = f"“{e(message)}”" if message else "—"
        actions = f"""<div class="table__actions">
{indent(post_button("Accept", "", "check"), 4)}
{indent(post_button("Decline", "btn--danger", "xmark"), 4)}
</div>""" if status == "pending" else ""
        rows.append(f"""<tr>
    <td>
        <div class="lineup__item">
            <img class="lineup__avatar" src="uploads/musicians/{musician}.jpg" alt="">
            <a href="musician.html"><strong>{e(musician_name(musician))}</strong></a>
        </div>
    </td>
    <td>{e(VENUES[g[1]]["name"])}<br><time class="text-muted" datetime="{iso(dt)}">{short_date(dt)}, {t12(dt)}</time></td>
    <td class="table__message">{msg}</td>
    <td>{STATUS_BADGE[status]}</td>
    <td>
{indent(actions, 8)}
    </td>
</tr>""")
    body = f"""
<div class="container">
    <header class="page-header">
        <p class="page-header__eyebrow">Venue manager</p>
        <h1>Join requests</h1>
        <p>Musicians who asked to play at the gigs of your venues.</p>
    </header>

    <div class="table-wrapper">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Musician</th>
                    <th scope="col">Gig</th>
                    <th scope="col">Message</th>
                    <th scope="col">Status</th>
                    <th scope="col"><span class="visually-hidden">Actions</span></th>
                </tr>
            </thead>
            <tbody>
{indent(chr(10).join(rows), 16)}
            </tbody>
        </table>
    </div>
</div>"""
    page("join-requests.html", "Join requests · TradMusic", body, user="grainne")


def screen_404():
    body = f"""
<div class="container container--narrow section">
    <div class="empty-state">
        <i class="fa-solid fa-music" aria-hidden="true"></i>
        <h1>Page not found</h1>
        <p>This tune isn't in our repertoire. The page you are looking for doesn't exist or has been moved.</p>
        <a class="btn" href="index.html">Back to the home page</a>
    </div>
</div>"""
    page("404.html", "Page not found · TradMusic", body)


# ================================================================ FIXTURES.md
def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def fixtures():
    email = lambda key: f"`{USERS[key][0]}`"
    parts = [f"""# Données fictives (fixtures)

Ce fichier contient toutes les données à charger dans l'application Symfony. Recopiez-les dans vos classes de fixtures (DoctrineFixturesBundle) : une fois chargées, votre application doit afficher exactement les écrans de la maquette.

## Consignes

- **Ordre de chargement** : les tableaux sont présentés dans l'ordre de dépendance. Une entité ne référence que des entités des tableaux précédents.
- **Relations** : les relations sont indiquées par le **slug** de l'entité liée (ou l'**e-mail** pour un User). N'utilisez jamais d'identifiant numérique : il dépend de l'auto-incrément. Utilisez plutôt les références de fixtures (`addReference()` / `getReference()`).
- **Gigs** : un Gig n'a pas de slug. La colonne *Reference* sert uniquement à le désigner dans les fixtures ; ce n'est pas un champ de l'entité.
- **Dates relatives** : les dates des Gigs et des Join Requests sont des modificateurs à passer tels quels à PHP, par exemple `new \\DateTimeImmutable('+4 days 21:00')`. Ainsi, il y a toujours des Upcoming Gigs et des Past Gigs, quelle que soit la date du jour. La maquette affiche ces dates en prenant pour « aujourd'hui » le **lundi 12 octobre 2026** (en anglais dans les écrans).
- **Mots de passe** : tous les comptes utilisent le mot de passe `{PASSWORD}`. Il doit être haché avec `UserPasswordHasherInterface` avant d'être enregistré.
- **Images** : copiez le dossier `uploads/` du thème dans `public/uploads/` de votre projet. Les colonnes *Photo* et *Icon* donnent le nom du fichier.
- **Traduction** : les données restent en anglais, comme le contenu du site.
"""]

    parts.append("## 1. Instruments\n\n" + md_table(
        ["Slug", "Name", "Icon"],
        [(f"`{s}`", n, f"`{s}.svg`") for s, n in INSTRUMENTS]))

    parts.append("## 2. Towns\n\n" + md_table(["Slug", "Name"], [(f"`{s}`", n) for s, n in TOWNS]))

    parts.append("## 3. Users\n\nMot de passe de tous les comptes : `" + PASSWORD + "`.\n\n" + md_table(
        ["Email", "First name", "Last name", "Roles"],
        [(f"`{u[0]}`", u[1], u[2], ", ".join(f"`{r}`" for r in u[3])) for u in USERS.values()]))

    parts.append("## 4. Musicians\n\n" + md_table(
        ["Slug", "User", "Town", "Instruments", "Available", "Photo", "Bio"],
        [(f"`{s}`", email(m["user"]), f"`{m['town']}`", ", ".join(f"`{i}`" for i in m["instruments"]),
          "yes" if m["available"] else "no", f"`{s}.jpg`", m["bio"]) for s, m in MUSICIANS.items()]))

    parts.append("## 5. Venues\n\n" + md_table(
        ["Slug", "Name", "Town", "Address", "Manager", "Photo", "Description"],
        [(f"`{s}`", v["name"], f"`{v['town']}`", v["address"], email(v["manager"]), f"`{s}.jpg`", v["description"])
         for s, v in VENUES.items()]))

    parts.append("## 6. Gigs\n\nLa description est facultative (vide = `null`).\n\n" + md_table(
        ["Reference", "Venue", "Starts at", "Lineup", "Description"],
        [(f"`{g[0]}`", f"`{g[1]}`", f"`{g[2]}`", ", ".join(f"`{s}`" for s in g[3]), g[4] or "")
         for g in GIGS]))

    parts.append("## 7. Sessions\n\n" + md_table(
        ["Venue", "Name", "Day of week", "Time"],
        [(f"`{s[0]}`", s[1], s[2], f"`{s[3]}`") for s in SESSIONS]))

    parts.append("## 8. Join Requests\n\nLe message est facultatif (vide = `null`). Une Join Request *Accepted* correspond à un Musician déjà présent dans le Lineup du Gig.\n\n" + md_table(
        ["Musician", "Gig", "Status", "Created at", "Message"],
        [(f"`{jr[0]}`", f"`{jr[1]}`", f"`{jr[2]}`", f"`{jr[3]}`", jr[4] or "") for jr in JOIN_REQUESTS]))

    rows = [(f"`{p}`", user, f"[unsplash.com/photos/{pid}](https://unsplash.com/photos/{pid})")
            for p, (pid, user) in PHOTO_CREDITS.items()]
    parts.append("## Crédits photos\n\nToutes les photos proviennent d'[Unsplash](https://unsplash.com) et sont utilisées selon la [licence Unsplash](https://unsplash.com/license).\n\n" + md_table(["File", "Photographer", "Source"], rows))

    (ROOT / "FIXTURES.md").write_text("\n\n".join(parts) + "\n")


# ================================================================ checks
def checks():
    for musician, ref, status, _, _ in JOIN_REQUESTS:
        g = gig(ref)
        in_lineup = musician in g[3]
        assert (status == "accepted") == in_lineup, (musician, ref)
        assert VENUES[g[1]]["manager"] != MUSICIANS[musician]["user"], (musician, ref)
        if status == "pending":
            assert upcoming(g), (musician, ref)
    pairs = [(jr[0], jr[1]) for jr in JOIN_REQUESTS]
    assert len(pairs) == len(set(pairs))


if __name__ == "__main__":
    checks()
    for fn in [screen_index, screen_musicians, screen_musician, screen_venues, screen_venue, screen_gigs,
               screen_gig, screen_about, screen_login, screen_register, screen_my_profile,
               screen_my_join_requests, screen_my_venues, screen_venue_form, screen_venue_manage,
               screen_gig_form, screen_session_form, screen_join_requests, screen_404]:
        fn()
    fixtures()
    print("ok")
