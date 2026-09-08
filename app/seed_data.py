"""Initial seed data for a fresh database — 12 chronological galleries spanning
from the age of the dinosaurs to the great Indian empires, plus default
site-wide settings and sample notices."""

GALLERIES = [
    dict(
        era_order=1, name="Jurassic Era", period="201 – 145 Million Years Ago",
        icon="🦖", wiki_topic="Jurassic",
        short_description="Fossils and skeletal reconstructions from the age of the dinosaurs.",
        description=(
            "The Jurassic Gallery houses fossilised remains, cast skeletons and interactive exhibits "
            "tracing the rise of the dinosaurs — including India's own Barapasaurus, unearthed in the "
            "Pranhita-Godavari Valley, one of the earliest sauropods known to science."
        ),
        history=(
            "The Jurassic Period followed the Triassic mass extinction and saw dinosaurs become the "
            "dominant land animals on Earth, alongside the first true birds and a warm, humid global "
            "climate that supported vast forests of ferns and conifers."
        ),
        highlights="Fossil Excavation Wall|Sauropod Skeleton Cast|Interactive Dino-Dig Zone|Amber Insect Collection",
        monuments=(
            "Tyrannosaurus :: Tyrannosaurus :: An apex predator whose fossil cast dominates the gallery entrance.\n"
            "Stegosaurus :: Stegosaurus :: Famed for its bony back plates and spiked tail.\n"
            "Archaeopteryx :: Archaeopteryx :: The iconic transitional fossil linking dinosaurs and birds.\n"
            "Barapasaurus :: Barapasaurus :: India's earliest known sauropod, discovered in Telangana."
        ),
        max_occupancy=120, current_occupancy=18,
    ),
    dict(
        era_order=2, name="The Ice Age", period="2.6 Million – 11,700 Years Ago",
        icon="🦣", wiki_topic="Ice_age",
        short_description="Megafauna of the Pleistocene — mammoths, cave lions and woolly rhinos.",
        description=(
            "Step into the last great Ice Age with life-sized mammoth reconstructions, preserved tusks "
            "and dioramas depicting how early humans hunted, sheltered and survived amid advancing "
            "glaciers and shifting tundra landscapes."
        ),
        history=(
            "Repeated glacial cycles during the Pleistocene epoch reshaped continents and drove the "
            "evolution of thick-furred megafauna. Early hominins adapted alongside these giants, leaving "
            "behind tools, hearths and cave art that mark humanity's first great survival story."
        ),
        highlights="Life-size Mammoth Cast|Ice Core Samples|Megafauna Diorama|Glacial Landscape Model",
        monuments=(
            "Woolly Mammoth :: Woolly_mammoth :: The enduring symbol of the Ice Age, adapted for extreme cold.\n"
            "Woolly Rhinoceros :: Woolly_rhinoceros :: A heavily built herbivore with a distinctive nasal horn.\n"
            "Smilodon :: Smilodon :: The sabre-toothed cat, one of the era's most formidable predators.\n"
            "Cave Lion :: Panthera_leo_spelaea :: A powerful predator of Ice Age Europe and Asia."
        ),
        max_occupancy=120, current_occupancy=22,
    ),
    dict(
        era_order=3, name="Stone Age Gallery", period="3.3 Million – 3300 BCE",
        icon="🪨", wiki_topic="Stone_Age",
        short_description="Tools, cave art and the dawn of human craftsmanship.",
        description=(
            "From crude Oldowan choppers to finely knapped Neolithic axes, this gallery traces humanity's "
            "first technological revolution, alongside replicas of India's own Bhimbetka rock shelters — "
            "a UNESCO World Heritage Site with paintings dating back tens of thousands of years."
        ),
        history=(
            "The Stone Age is conventionally divided into the Palaeolithic, Mesolithic and Neolithic "
            "periods, marking humanity's gradual shift from nomadic hunting and gathering to settled "
            "farming communities and the earliest forms of art and symbolic expression."
        ),
        highlights="Hand-axe Collection|Replica Cave Paintings|Neolithic Pottery Shards|Fire-making Demonstration",
        monuments=(
            "Bhimbetka Rock Shelters :: Bhimbetka_rock_shelters :: India's UNESCO-listed prehistoric rock art site.\n"
            "Hand Axe :: Hand_axe :: One of the earliest and most enduring stone tool designs.\n"
            "Venus of Willendorf :: Venus_of_Willendorf :: A celebrated Palaeolithic figurine of early symbolic art.\n"
            "Cave Painting :: Cave_painting :: Pigment-based artwork found on rock shelter walls worldwide."
        ),
        max_occupancy=140, current_occupancy=30,
    ),
    dict(
        era_order=4, name="Prehistoric Humanity", period="3.3 Million – 3000 BCE",
        icon="🔥", wiki_topic="Prehistory",
        short_description="Early human evolution, migration and the first settlements.",
        description=(
            "This wing charts the story of our own species — from early hominins in Africa to global "
            "migration, the domestication of fire, and the first permanent settlements that laid the "
            "foundation for civilisation itself."
        ),
        history=(
            "Prehistory spans the vast period before written records, pieced together through fossils, "
            "tools and genetic evidence. It closes with the Neolithic Revolution, when farming and "
            "settled life began to replace nomadic hunting and gathering across the globe."
        ),
        highlights="Hominin Skull Casts|Migration Route Map|Early Settlement Model|Domestication Timeline",
        monuments=(
            "Homo Erectus :: Homo_erectus :: An early human ancestor and among the first to migrate out of Africa.\n"
            "Neanderthal :: Neanderthal :: A close human relative known for early tool use and burial rites.\n"
            "Stonehenge :: Stonehenge :: A monumental prehistoric stone circle marking the Neolithic era's ambition.\n"
            "Göbekli Tepe :: Göbekli_Tepe :: Regarded as among the world's oldest known monumental structures."
        ),
        max_occupancy=130, current_occupancy=15,
    ),
    dict(
        era_order=5, name="Ancient River Civilizations", period="3300 – 1300 BCE",
        icon="🏺", wiki_topic="Indus_Valley_Civilisation",
        short_description="The Indus Valley, Mesopotamia and the birth of urban life.",
        description=(
            "Explore terracotta seals, granary models and jewellery from the Indus Valley Civilisation, "
            "one of the world's earliest urban cultures, alongside comparative exhibits on Mesopotamia "
            "and ancient Egypt that flourished along the same great rivers."
        ),
        history=(
            "The Indus Valley Civilisation, centred on cities like Mohenjo-daro and Harappa, featured "
            "remarkably advanced urban planning, drainage systems and a still-undeciphered script — "
            "standing among the great cradles of civilisation alongside Mesopotamia and Egypt."
        ),
        highlights="Indus Seals & Script|Granary Model|Bronze 'Dancing Girl' Replica|Standardised Weights Display",
        monuments=(
            "Mohenjo-daro :: Mohenjo-daro :: A meticulously planned Bronze Age city of the Indus Valley.\n"
            "Harappa :: Harappa :: One of the earliest and largest cities of the Indus Valley Civilisation.\n"
            "Great Bath, Mohenjo-daro :: Great_Bath,_Mohenjo-daro :: An early public water tank of remarkable engineering.\n"
            "Dholavira :: Dholavira :: A well-preserved Harappan city noted for its water conservation systems."
        ),
        max_occupancy=150, current_occupancy=45,
    ),
    dict(
        era_order=6, name="Ancient Indian Heritage", period="600 BCE – 200 CE",
        icon="☸️", wiki_topic="Maurya_Empire",
        short_description="The Mauryan Empire, Emperor Ashoka and the spread of Buddhism.",
        description=(
            "This gallery showcases Mauryan-era coinage, polished sandstone pillar fragments and Buddhist "
            "reliefs from Sanchi, tracing the reign of Emperor Ashoka and the golden age of ancient "
            "Indian statecraft, philosophy and art."
        ),
        history=(
            "The Maurya Empire, founded by Chandragupta Maurya, became one of the largest empires of its "
            "time. His grandson Ashoka, after the bloody Kalinga War, embraced Buddhism and inscribed "
            "edicts of non-violence and moral governance across the subcontinent."
        ),
        highlights="Ashokan Pillar Fragment|Mauryan Punch-marked Coins|Sanchi Stupa Relief Cast|Edict Inscriptions",
        monuments=(
            "Ashoka :: Ashoka :: The Mauryan emperor whose edicts remain landmarks of ancient governance.\n"
            "Pillars of Ashoka :: Pillars_of_Ashoka :: Polished sandstone pillars inscribed with Buddhist edicts.\n"
            "Sanchi :: Sanchi :: Home to India's oldest surviving stone stupa and gateways.\n"
            "Great Stupa :: Great_Stupa,_Sanchi :: A UNESCO World Heritage Buddhist monument."
        ),
        max_occupancy=140, current_occupancy=38,
    ),
    dict(
        era_order=7, name="The Roman Age", period="27 BCE – 476 CE",
        icon="🏛️", wiki_topic="Roman_Empire",
        short_description="Classical antiquity — engineering, law and empire.",
        description=(
            "Marble busts, mosaic reproductions and scale models of the Colosseum and Roman Forum "
            "illustrate the engineering and administrative genius of an empire that shaped Western "
            "civilisation for centuries."
        ),
        history=(
            "At its height, the Roman Empire spanned three continents, pioneering advances in law, "
            "engineering, architecture and governance whose influence is still felt in institutions "
            "around the world today."
        ),
        highlights="Colosseum Scale Model|Roman Mosaic Reproductions|Legionary Armour Replica|Aqueduct Cross-section",
        monuments=(
            "Colosseum :: Colosseum :: The largest amphitheatre ever built, a symbol of Roman engineering.\n"
            "Pantheon :: Pantheon,_Rome :: A remarkably preserved Roman temple with a record-setting dome.\n"
            "Roman Forum :: Roman_Forum :: The political and civic heart of ancient Rome.\n"
            "Pompeii :: Pompeii :: A Roman city frozen in time by the eruption of Mount Vesuvius."
        ),
        max_occupancy=130, current_occupancy=27,
    ),
    dict(
        era_order=8, name="Hindu Civilization & Temple Architecture", period="5th Century CE – Present",
        icon="🕉️", wiki_topic="Hindu_temple",
        short_description="Sacred architecture, sculpture and philosophy across two millennia.",
        description=(
            "From the rock-cut splendour of Khajuraho to the towering gopurams of the south, this gallery "
            "celebrates the continuous, living tradition of Hindu temple architecture, iconography and "
            "philosophy that has flourished across the subcontinent for over a thousand years."
        ),
        history=(
            "Hindu temple architecture evolved through distinct regional styles — Nagara in the north, "
            "Dravida in the south and Vesara in the Deccan — each reflecting sophisticated cosmology, "
            "mathematics and artistry refined over successive dynasties."
        ),
        highlights="Temple Architecture Models|Bronze Deity Sculptures|Cosmology & Mandala Exhibit|Devotional Music Corner",
        monuments=(
            "Khajuraho Group of Monuments :: Khajuraho_Group_of_Monuments :: UNESCO-listed temples famed for intricate carving.\n"
            "Konark Sun Temple :: Konark_Sun_Temple :: A 13th-century temple built in the form of a colossal chariot.\n"
            "Meenakshi Temple :: Meenakshi_Amman_Temple :: A towering Dravidian-style temple complex in Madurai.\n"
            "Brihadeeswarar Temple :: Brihadeeswarar_Temple :: A Chola-era masterpiece and UNESCO World Heritage Site."
        ),
        max_occupancy=150, current_occupancy=52,
    ),
    dict(
        era_order=9, name="Medieval India — The Sultanate Period", period="1206 – 1526 CE",
        icon="🕌", wiki_topic="Delhi_Sultanate",
        short_description="The Delhi Sultanate and the fusion of Indo-Islamic architecture.",
        description=(
            "Intricate calligraphy, coinage and architectural fragments from the Delhi Sultanate era trace "
            "the emergence of a distinctive Indo-Islamic architectural style that would culminate, "
            "centuries later, in the monuments of the Mughal age."
        ),
        history=(
            "Spanning five dynasties over three centuries, the Delhi Sultanate introduced new architectural "
            "techniques — arches, domes and minarets — that fused with existing Indian traditions to "
            "produce an entirely new visual language."
        ),
        highlights="Indo-Islamic Calligraphy|Sultanate-era Coinage|Qutb Complex Model|Arch & Dome Cutaway Display",
        monuments=(
            "Qutb Minar :: Qutb_Minar :: The world's tallest brick minaret, begun in 1192 CE.\n"
            "Alai Darwaza :: Alai_Darwaza :: An early masterpiece of Indo-Islamic architecture within the Qutb Complex.\n"
            "Tughlaqabad Fort :: Tughlaqabad_Fort :: A massive fortified city built by the Tughlaq dynasty.\n"
            "Hauz Khas Complex :: Hauz_Khas_Complex :: A former royal reservoir and madrasa complex in Delhi."
        ),
        max_occupancy=120, current_occupancy=20,
    ),
    dict(
        era_order=10, name="The Rajput Era", period="7th – 18th Century CE",
        icon="🛡️", wiki_topic="Rajput",
        short_description="Chivalry, valour and the hill forts of Rajputana.",
        description=(
            "Suits of armour, miniature paintings and scale models of the great hill forts of Rajasthan "
            "bring to life the martial traditions, courtly culture and architectural splendour of the "
            "Rajput kingdoms."
        ),
        history=(
            "The Rajput clans of Rajputana built some of the subcontinent's most formidable hill forts and "
            "are remembered for their codes of chivalry and honour, and for their long resistance against "
            "successive invasions."
        ),
        highlights="Rajput Armour & Weaponry|Miniature Painting Collection|Hill Fort Scale Models|Courtly Textiles Display",
        monuments=(
            "Chittorgarh Fort :: Chittorgarh_Fort :: One of India's largest forts, a symbol of Rajput resistance.\n"
            "Amber Fort :: Amer_Fort :: A UNESCO-listed hill fort known for its artistic Hindu style elements.\n"
            "Mehrangarh Fort :: Mehrangarh_Fort :: A towering fort overlooking the blue city of Jodhpur.\n"
            "Kumbhalgarh :: Kumbhalgarh :: Home to the second-longest continuous wall in the world."
        ),
        max_occupancy=130, current_occupancy=33,
    ),
    dict(
        era_order=11, name="The Mughal Era", period="1526 – 1857 CE",
        icon="🏯", wiki_topic="Mughal_Empire",
        short_description="Emperors, gardens and the golden age of Indo-Islamic art.",
        description=(
            "Marvel at replicas of Mughal miniature paintings, jewelled artefacts and architectural models "
            "of the Taj Mahal and Agra Fort — monuments to an empire renowned for its patronage of art, "
            "architecture and administration."
        ),
        history=(
            "Founded by Babur in 1526, the Mughal Empire reached its zenith under Akbar, Jahangir, Shah "
            "Jahan and Aurangzeb, leaving behind an enduring legacy of monumental architecture, miniature "
            "painting and administrative reform."
        ),
        highlights="Taj Mahal Scale Model|Mughal Miniature Paintings|Imperial Jewellery Replicas|Mughal Garden Diorama",
        monuments=(
            "Taj Mahal :: Taj_Mahal :: An ivory-white marble mausoleum and UNESCO World Heritage Site.\n"
            "Agra Fort :: Agra_Fort :: A red sandstone fortress that served as the main Mughal residence.\n"
            "Fatehpur Sikri :: Fatehpur_Sikri :: Akbar's short-lived but architecturally magnificent capital.\n"
            "Red Fort :: Red_Fort :: The principal residence of Mughal emperors in Delhi for nearly 200 years."
        ),
        max_occupancy=160, current_occupancy=70,
    ),
    dict(
        era_order=12, name="Sikh Heritage Gallery", period="1469 CE – Present",
        icon="🪯", wiki_topic="Sikh_Empire",
        short_description="The Sikh Gurus, the Khalsa and the Sikh Empire of Ranjit Singh.",
        description=(
            "This gallery honours the teachings of the Sikh Gurus, the founding of the Khalsa, and the "
            "rise of the Sikh Empire under Maharaja Ranjit Singh, alongside artefacts relating to the "
            "Golden Temple and Sikh martial and devotional traditions."
        ),
        history=(
            "Founded on the teachings of Guru Nanak and shaped by nine succeeding Gurus, Sikhism gave rise "
            "to a distinct faith and identity that, under Maharaja Ranjit Singh in the 19th century, "
            "flourished into a powerful and progressive empire in north-west India."
        ),
        highlights="Golden Temple Model|Sikh Manuscripts & Scripture|Khalsa Regalia Display|Ranjit Singh Court Artefacts",
        monuments=(
            "Golden Temple :: Golden_Temple :: The holiest Gurdwara of Sikhism, in Amritsar.\n"
            "Guru Nanak :: Guru_Nanak :: The founder of Sikhism and first of the ten Sikh Gurus.\n"
            "Akal Takht :: Akal_Takht :: The primary seat of temporal authority within Sikhism.\n"
            "Anandpur Sahib :: Anandpur_Sahib :: The birthplace of the Khalsa, founded in 1699."
        ),
        max_occupancy=130, current_occupancy=25,
    ),
]

NOTICES = [
    "Museum will remain closed on all national holidays as per the official calendar.",
    "New exhibit now open: 'Barapasaurus — India's Own Dinosaur' in the Jurassic Gallery.",
    "Online ticket booking is now available — skip the queue and book your visit in advance.",
    "Guided tours in Hindi and English available every hour from 10:30 AM.",
]

EMPLOYEES = [
    dict(name="Dr. Anjali Verma", designation="Director General", department="Administration",
         bio="Leads the museum's strategic vision and heritage conservation programmes, with over "
             "20 years of experience in archaeology and cultural policy.",
         display_order=1, email="director@nationalheritagemuseum.gov.in", phone="+91-11-2345-6790"),
    dict(name="Rajesh Kumar", designation="Chief Curator", department="Curatorial Affairs",
         bio="Oversees the acquisition, preservation and display of exhibits across all twelve "
             "galleries, specialising in Mauryan and Mughal-era artefacts.",
         display_order=2, email="curator@nationalheritagemuseum.gov.in", phone="+91-11-2345-6791"),
    dict(name="Dr. Fatima Sheikh", designation="Head of Education & Outreach", department="Public Programmes",
         bio="Designs guided tours, school programmes and the museum's digital learning initiatives, "
             "including the Heritage AI visitor assistant.",
         display_order=3, email="education@nationalheritagemuseum.gov.in", phone="+91-11-2345-6792"),
    dict(name="Vikram Singh", designation="Head of Visitor Services", department="Operations",
         bio="Manages ticketing, gallery occupancy and the day-to-day visitor experience across the "
             "museum complex.",
         display_order=4, email="visitorservices@nationalheritagemuseum.gov.in", phone="+91-11-2345-6793"),
]

PAGES = [
    dict(
        title="Accessibility Statement", slug="accessibility-statement", is_published=1,
        content=(
            "<p>The National Heritage Museum is committed to ensuring digital accessibility for all "
            "visitors. This website includes adjustable text size, a high-contrast display mode, and "
            "an integrated language translator supporting over a dozen languages.</p>"
            "<p>If you experience any difficulty accessing content on this site, please contact us via "
            "the form on our homepage and we will assist you promptly.</p>"
        ),
    ),
    dict(
        title="RTI & Citizen Charter", slug="rti-citizen-charter", is_published=1,
        content=(
            "<p>In the spirit of transparency and public accountability, the museum publishes its "
            "citizen charter outlining visitor rights, service standards and grievance redressal "
            "procedures.</p>"
            "<p>For formal Right to Information (RTI) requests, please write to the Public Information "
            "Officer at the address listed on our Contact page.</p>"
        ),
    ),
]

LINKS = [
    dict(label="Accessibility Statement", url="/page/accessibility-statement", location="footer", sort_order=1),
    dict(label="RTI & Citizen Charter", url="/page/rti-citizen-charter", location="footer", sort_order=2),
    dict(label="Our Team", url="/our-team", location="nav", sort_order=1),
]


def slugify(name: str) -> str:
    return (name.lower().replace("&", "and").replace("'", "").replace(",", "")
            .replace(".", "").replace("—", "-").replace(" ", "-"))


def seed_if_empty():
    from werkzeug.security import generate_password_hash
    from flask import current_app
    from . import models

    if models.count_galleries() == 0:
        for g in GALLERIES:
            models.create_gallery(slug=slugify(g["name"]), **g)

    if models.count_admins() == 0:
        username = current_app.config.get("ADMIN_USERNAME", "admin")
        password = current_app.config.get("ADMIN_PASSWORD", "admin123")
        models.create_admin(username, generate_password_hash(password))

    models.seed_default_settings()

    if not models.get_all_notices():
        for n in NOTICES:
            models.create_notice(n)

    if models.count_employees() == 0:
        for e in EMPLOYEES:
            models.create_employee(**e)

    if not models.get_pages(published_only=False):
        for p in PAGES:
            models.create_page(p["title"], p["slug"], p["content"], p["is_published"])

    if not models.get_links(active_only=False):
        for lk in LINKS:
            models.create_link(lk["label"], lk["url"], lk["location"], lk["sort_order"])
