# world-news-23-november-2026-image — draw.py
# One-page broadsheet: 60 verified world-news stories from Monday 23 Nov 2026.
# Layout (new for this edition): nameplate band, hero 2/3 width + 3 secondary
# cards stacked on the right, then a 4-column sectioned grid below.
# Deterministic: no randomness, no clock, no network, fixed fonts, fixed order.
# Renders a 1024x1024 PNG. Run directly or via main.py.

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# Palette: warm paper, deep teal ink, amber + rust accents.
PAPER = (247, 243, 234)
INK = (18, 32, 31)
TEAL = (14, 90, 82)
TEAL_DARK = (9, 58, 53)
TEAL_SOFT = (226, 238, 235)
AMBER = (196, 122, 18)
RUST = (179, 64, 42)
GREY = (84, 96, 94)
RULE = (190, 196, 190)
CARD = (255, 255, 255)

WARNINGS = []


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap. Returns list of lines; warns if a single word is too wide."""
    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            if text_w(draw, word, f) > max_w:
                WARNINGS.append("word too wide: %r" % word)
                cur = word
            else:
                cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, s, f, max_w, max_lines, label):
    lines = wrap(draw, s, f, max_w)
    if len(lines) > max_lines:
        WARNINGS.append("%s needs %d lines (max %d): %r"
                        % (label, len(lines), max_lines, s))
    return lines[:max_lines]


# ---------------------------------------------------------------- data
HERO = {
    "kicker": "CLIMATE  •  ANTALYA, TURKEY  •  COP31",
    "headline": ["COP31 COLLAPSES", "WITHOUT DEAL"],
    "lines": [
        "After a record 44-hour overrun, nearly 200 nations fail to adopt the "
        "\u201cAntalya Pact\u201d. COP president Murat Kurum: \u201cThere is no "
        "consensus on this document.\u201d",
        "The breaking point: the final draft never mentions \u201cfossil fuels\u201d. "
        "The EU, UK, Norway, Panama, the Marshall Islands and least-developed "
        "nations reject it as too weak.",
        "UN chief Ant\u00f3nio Guterres is \u201cdeeply disappointed\u201d. The longest "
        "COP in history \u2014 and the first outright failure since Copenhagen "
        "2009. The $120bn adaptation-finance target was also dropped.",
    ],
}

SECONDARY = [
    ("US POLITICS",
     "Democrats win at least 258 House seats",
     "Largest majority since 1992; Hubbard beat Foxx by ~330 votes."),
    ("GULF WAR",
     "Iran strikes Bahrain; tankers hit in Hormuz",
     "Bahrain blames Iran for Sitra blast; 25 tankers hit in a week."),
    ("UKRAINE WAR",
     "Russian corvette reported destroyed off Libya",
     "Suspected Ukrainian sea drones; Ascalon also struck."),
]

# Grid: (headline, deck). 56 items in 8 sections.
SECTIONS = [
    ("WAR & DIPLOMACY", [
        ("Zelenskyy urges US to release Patriots",
         "Russia fired ~2,700 drones in a week"),
        ("Russian strikes near Kyiv kill 7",
         "Flats hit in Dymer; 10 missing, incl. 2 children"),
        ("Russia \u2018triple-taps\u2019 Zelenskyy\u2019s hometown",
         "Boy, 7, and medic, 20, killed in Kryvyi Rih"),
        ("Swedish Gripen pilot fails to down missile",
         "Bad weather blocked NATO intercept over Poland"),
        ("Zelenskyy: no written security guarantees yet",
         "Kyiv has seen no NATO-style pledges in writing"),
        ("\u2018El Chapo Isidro\u2019 captured, 11 killed",
         "FBI top-10 fugitive seized in Sinaloa raid"),
        ("Kim Jong Un snubs Trump, returns letter",
         "Unopened letter left at North Korea\u2019s UN mission"),
        ("Pentagon curbs military ties with Canada",
         "Secret memo limits engagement; NORAD unaffected"),
        ("US intel chief: Putin \u2018not America\u2019s friend\u2019",
         "Clayton rebukes Trump after Shenzhen summit"),
        ("Nepal PM in Delhi to meet Modi today",
         "Talks on energy, rail and a $2bn aid package"),
        ("Myanmar calls ASEAN ruling \u2018unfair\u2019",
         "Junta rejects partial representation at summit"),
        ("Political violence in Bangladesh: ~30 homes torched",
         "Awami League homes burned in Narail village"),
        ("Thousands march in Lisbon over living costs",
         "Wages 37% below EU average, unions say"),
        ("France: sixth weekend of protests",
         "Demonstrators return to streets nationwide"),
        ("Shenzhen Declaration: three nuclear powers to talk",
         "Trump, Xi, Putin agree nuclear-risk dialogue"),
    ]),
    ("CLIMATE & ENVIRONMENT", [
        ("Guterres \u2018deeply disappointed\u2019 by COP31 collapse",
         "UN chief blames fossil-fuel interests"),
        ("EU rejects text with no \u2018fossil fuels\u2019",
         "\u201cWe will not back a deal that ignores them\u201d"),
        ("India protests COP31 weakening rich nations\u2019 duty",
         "New Delhi cites equity concerns at summit"),
        ("COP31 draft first named transition, then deleted it",
         "$120bn adaptation target also dropped"),
    ]),
    ("US & WORLD POLITICS", [
        ("Trump orders contractors to consult White House",
         "Before responding to Congress, NDTV reports"),
        ("Democrats to hold 56 Senate seats",
         "Largest Senate majority in over a decade"),
        ("Minnesota fraud hearing heats up",
         "Senators grill Soros-funded witness"),
        ("Amit Shah pushes self-reliance in Arunachal",
         "Rs 4,000-crore infrastructure projects launched"),
        ("IFFI 2026 holds BRICS film roundtable",
         "India festival boosts film-industry ties"),
        ("India\u2019s top judge urges mandatory legal aid",
         "Law students must do aid work to graduate"),
        ("India higher-education bill may lapse",
         "Single-regulator plan may miss winter session"),
    ]),
    ("ECONOMY & MARKETS", [
        ("Oil down 3rd week; OPEC+ meets 29 Nov",
         "Brent $92.57; market eyes 2027 output decision"),
        ("Nasdaq enters correction; Nvidia dives 14% in a day",
         "Nvidia -47.5% from Oct peak; CEO Huang resigned Nov 12"),
        ("Anthropic IPO raises $81.3bn in record listing",
         "Shares opened $111.50, then fell ~10% on Friday"),
        ("EU proposes 3% Big Tech tax",
         "Levy on ads, data and digital intermediation"),
        ("Indian stocks rise 4th straight week",
         "Nifty +2.61%; record FII inflows in November"),
        ("India\u2019s oil and gas import bill up 60%",
         "October bill surges on higher crude prices"),
        ("Tata Steel signs Rs 28,000-crore deal",
         "Agreement with APL Apollo announced"),
        ("Pernod Ricard weighs India IPO",
         "India market nears US in global sales"),
        ("Bitcoin nears $62,100, 3-month low",
         "ETF holdings and stablecoin supply shrink"),
        ("Isomorphic Labs raises $5bn Series C",
         "Oracle closes $20bn data-centre financing"),
        ("Amazon reported near deal to buy Decart",
         "AI video startup acquisition not yet confirmed"),
    ]),
    ("TECHNOLOGY & AI", [
        ("SEC reviews Nvidia accounting; California subpoena",
         "Chip-diversion probe; Huang faces spy inquiry"),
        ("Fed flags $680bn AI infrastructure debt",
         "Circular financing tops $100bn, governor warns"),
        ("South Korea education minister quits over AI cheating",
         "111 suspected cases before university entrance exam"),
        ("China accused of hunting advanced AI chips",
         "Man charged in advanced-computing network case"),
    ]),
    ("DISASTER, TRANSPORT & AID", [
        ("Indonesia candy factory fire: 3 dead, 36-37 missing",
         "Blaze at Milkita plant in Banten; DNA samples sought"),
        ("Peru quake 6.7: 1 dead, 853 homeless",
         "Power cut for ~93,000; cinema-goers fled mid-film"),
        ("Delta glitch delays 1,000+ flights",
         "Weight-balance system fault; Atlanta ground stop"),
    ]),
    ("SPORT", [
        ("Liverpool rout Man Utd 4-0 in Pochettino debut",
         "Worst first defeat for a United boss in 100 years"),
        ("India post record Test 720/9 in Wellington",
         "Highest Test total on New Zealand soil"),
        ("Wembanyama drops 50 points, 19 rebounds",
         "Spurs win 114-91; rare 50-15-4-5 game"),
        ("NFL: Lions and Bears 8-2 before Thanksgiving",
         "Gibbs stars; Prescott throws five touchdowns"),
        ("Bridges buzzer-beater saves Knicks",
         "New York edges Blazers 97-96 after leading by 26"),
        ("Hong Kong Open: Antonsen wins by walkover",
         "Vitidsarn withdraws injured; Wang Zhiyi retains title"),
        ("Real Madrid beat Celta Vigo 2-1",
         "Mbapp\u00e9 misses penalty; Espi scores late winner"),
        ("Utah seal Big 12 final spot",
         "No. 2 Utah beat TCU 38-17"),
        ("Tom Jackson, Broncos star and ESPN analyst, dies at 75",
         "\u201cSunday NFL Countdown\u201d stalwart"),
    ]),
    ("CULTURE & MORE", [
        ("Paolo Bulgari dies aged 89",
         "Jewellery heir who built global luxury brand; funeral Monday"),
        ("Mohun Bagan top Indian Super League",
         "2-1 win over Churchill Brothers"),
        ("India U19 B win women\u2019s T20 tri-series",
         "Beat India U19 A by five wickets in final"),
    ]),
]

# Column assignment: 4 columns, sections kept whole.
COLUMNS = [
    [0],        # WAR & DIPLOMACY (15)
    [1, 2],     # CLIMATE (4) + US & WORLD POLITICS (7)
    [3, 4],     # ECONOMY (11) + TECH & AI (4)
    [5, 6, 7],  # DISASTER (3) + SPORT (9) + CULTURE (3)
]

FOOTER = ("Sources: AP  •  Reuters  •  AFP  •  CNN  •  Al Jazeera  •  Yonhap  •  "
          "NDTV  •  The Hindu  •  Times of India  •  CNA  •  Nikkei Asia  •  "
          "Le Monde   —   All 60 stories verified 23 Nov 2026")


# ---------------------------------------------------------------- drawing
def draw_nameplate(d):
    d.rectangle([0, 0, W, 52], fill=TEAL_DARK)
    d.rectangle([0, 52, W, 55], fill=AMBER)
    f_title = font(SERIF, 30)
    d.text((12, 11), "THE WORLD IN ONE PAGE", font=f_title, fill=PAPER)
    f_date = font(SANS_B, 15)
    date = "MONDAY 23 NOVEMBER 2026"
    d.text((W - 12 - text_w(d, date, f_date), 17), date, font=f_date, fill=AMBER)
    f_sub = font(SANS, 10)
    sub = "60 VERIFIED STORIES  •  NEWS-IMAGE-20261123"
    d.text((W - 12 - text_w(d, sub, f_sub), 36), sub, font=f_sub, fill=(200, 214, 210))


def draw_hero(d):
    x0, y0, x1, y1 = 10, 63, 648, 270
    d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
    d.rectangle([x0, y0, x1, y0 + 4], fill=RUST)
    f_kick = font(SANS_B, 11)
    d.text((x0 + 14, y0 + 12), HERO["kicker"], font=f_kick, fill=RUST)
    f_head = font(SERIF, 32)
    hy = y0 + 28
    for line in HERO["headline"]:
        d.text((x0 + 14, hy), line, font=f_head, fill=INK)
        hy += 37
    f_body = font(SANS, 11)
    by = hy + 3
    for i, para in enumerate(HERO["lines"]):
        lines = wrap(d, para, f_body, x1 - x0 - 28)
        for ln in lines:
            d.text((x0 + 14, by), ln, font=f_body, fill=(38, 52, 50))
            by += 15
        if i < len(HERO["lines"]) - 1:
            by += 4
    if by > y1 - 4:
        WARNINGS.append("hero text overflows by %d px" % (by - (y1 - 4)))


def draw_secondary(d):
    x0, x1 = 656, 1014
    y = 63
    card_h, gap = 66, 4
    f_tag = font(SANS_B, 10)
    f_head = font(SANS_B, 13)
    f_deck = font(SANS, 10)
    for tag, head, deck in SECONDARY:
        y1 = y + card_h
        d.rectangle([x0, y, x1, y1], fill=TEAL_SOFT, outline=RULE, width=1)
        d.rectangle([x0, y, x0 + 4, y1], fill=TEAL)
        tx = x0 + 12
        d.text((tx, y + 5), tag, font=f_tag, fill=TEAL)
        hl = fit_lines(d, head, f_head, x1 - tx - 8, 2, "secondary headline")
        hy = y + 19
        for ln in hl:
            d.text((tx, hy), ln, font=f_head, fill=INK)
            hy += 15
        dl = fit_lines(d, deck, f_deck, x1 - tx - 8, 1, "secondary deck")
        for ln in dl:
            d.text((tx, hy + 1), ln, font=f_deck, fill=GREY)
            hy += 13
        if hy > y1 - 2:
            WARNINGS.append("secondary card overflows: %r" % head)
        y = y1 + gap


def section_header(d, x, y, w, title):
    f = font(SANS_B, 11)
    d.text((x, y), title, font=f, fill=TEAL)
    d.line([(x, y + 17), (x + w, y + 17)], fill=AMBER, width=2)
    return y + 24


def grid_item(d, x, y, w, head, deck):
    """Returns height used. Headline max 2 lines, deck max 1 line."""
    f_h = font(SANS_B, 11)
    f_d = font(SANS, 9)
    hl = fit_lines(d, head, f_h, w, 2, "grid headline")
    dl = fit_lines(d, deck, f_d, w, 1, "grid deck")
    cy = y
    for ln in hl:
        d.text((x, cy), ln, font=f_h, fill=INK)
        cy += 13
    for ln in dl:
        d.text((x, cy), ln, font=f_d, fill=GREY)
        cy += 11
    return cy - y


def draw_grid(d):
    y_top, y_bot = 280, 988
    d.line([(10, 276), (1014, 276)], fill=RULE, width=1)
    col_w = 244
    xs = [10, 262, 514, 766]
    f_h = font(SANS_B, 11)
    f_d = font(SANS, 9)
    for ci, sec_idxs in enumerate(COLUMNS):
        x = xs[ci]
        # Measure total content height for this column.
        total = 0
        blocks = []
        for si in sec_idxs:
            title, items = SECTIONS[si]
            total += 24  # header
            for head, deck in items:
                hl = wrap(d, head, f_h, col_w)
                dl = wrap(d, deck, f_d, col_w)
                h = len(hl) * 13 + len(dl) * 11
                blocks.append(h)
                total += h
        n_items = sum(len(SECTIONS[si][1]) for si in sec_idxs)
        n_heads = len(sec_idxs)
        avail = y_bot - y_top
        slack = avail - total
        if slack < 0:
            WARNINGS.append("column %d overflows by %d px" % (ci + 1, -slack))
            slack = 0
        # Distribute slack as even gaps between blocks (items + headers).
        n_gaps = n_items + n_heads
        gap = slack / n_gaps if n_gaps else 0
        y = y_top
        bi = 0
        for si in sec_idxs:
            title, items = SECTIONS[si]
            y = section_header(d, x, y, col_w, title)
            y += gap
            for head, deck in items:
                h = grid_item(d, x, y, col_w, head, deck)
                y += h + gap
                bi += 1
        if y > y_bot + 1:
            WARNINGS.append("column %d bottom %.1f exceeds %d" % (ci + 1, y, y_bot))
        # Vertical divider between columns.
        if ci < 3:
            d.line([(xs[ci] + col_w + 4, y_top), (xs[ci] + col_w + 4, y_bot)],
                   fill=RULE, width=1)


def draw_footer(d):
    d.line([(10, 994), (1014, 994)], fill=RULE, width=1)
    f = font(SANS, 9)
    d.text((10, 1001), FOOTER, font=f, fill=GREY)


def render(path=OUT):
    WARNINGS.clear()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_nameplate(d)
    draw_hero(d)
    draw_secondary(d)
    draw_grid(d)
    draw_footer(d)
    if len(SECTIONS) != 8:
        WARNINGS.append("section count != 8")
    n_grid = sum(len(items) for _, items in SECTIONS)
    if n_grid != 56:
        WARNINGS.append("grid stories = %d, expected 56" % n_grid)
    if 1 + len(SECONDARY) + n_grid != 60:
        WARNINGS.append("total stories != 60")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, format="PNG", optimize=True)
    return WARNINGS


if __name__ == "__main__":
    warns = render()
    print("warnings: %d" % len(warns))
    for w in warns:
        print("  -", w)
