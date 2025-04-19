from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fruit_battlegrounds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Fruit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rarity = db.Column(db.String(20), nullable=False)  # Common, Uncommon, Rare, Epic, Legendary, Mythical
    drop_rate = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(20), nullable=True) # Logia, Paramecia, Zoan
    abilities = db.relationship('Ability', backref='fruit', lazy=True)
    
class Ability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    key = db.Column(db.String(10), nullable=False)  # Z, X, C, V, F
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)

class Boss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    health = db.Column(db.Integer, nullable=False)
    exp_reward = db.Column(db.Integer, nullable=False)
    gem_reward = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    fruit_drops = db.relationship('FruitDrop', backref='boss', lazy=True)

class FruitDrop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boss_id = db.Column(db.Integer, db.ForeignKey('boss.id'), nullable=False)
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)
    drop_rate = db.Column(db.Float, nullable=False)  # Usually 1%
    fruit = db.relationship('Fruit')

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level_requirement = db.Column(db.Integer, nullable=True)
    exp_multiplier = db.Column(db.Float, nullable=True)
    image = db.Column(db.String(100), nullable=True)

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False, unique=True)
    reward = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_released = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fruits')
def fruits():
    all_fruits = Fruit.query.all()
    
    # Define rarity order for sorting
    rarity_order = {
        'Common': 1,
        'Uncommon': 2,
        'Rare': 3,
        'Epic': 4,
        'Legendary': 5,
        'Mythical': 6
    }
    
    # Debug output for console to see what's in the database
    print("Found", len(all_fruits), "fruits in database:")
    for fruit in all_fruits:
        print(f"- {fruit.name} ({fruit.rarity})")
    
    # Sort fruits by rarity in ascending order
    all_fruits = sorted(all_fruits, key=lambda x: rarity_order.get(x.rarity, 0))
    
    return render_template('fruits.html', fruits=all_fruits)

@app.route('/fruit/<int:fruit_id>')
def fruit_detail(fruit_id):
    fruit = Fruit.query.get_or_404(fruit_id)
    return render_template('fruit_detail.html', fruit=fruit)

@app.route('/bosses')
def bosses():
    all_bosses = Boss.query.all()
    return render_template('bosses.html', bosses=all_bosses)

@app.route('/boss/<int:boss_id>')
def boss_detail(boss_id):
    boss = Boss.query.get_or_404(boss_id)
    return render_template('boss_detail.html', boss=boss)

@app.route('/maps')
def maps():
    all_maps = Map.query.all()
    return render_template('maps.html', maps=all_maps)

@app.route('/codes')
def codes():
    active_codes = Code.query.filter_by(is_active=True).all()
    return render_template('codes.html', codes=active_codes)

@app.route('/updates')
def updates():
    all_updates = Update.query.order_by(Update.date_released.desc()).all()
    return render_template('updates.html', updates=all_updates)

@app.route('/leveling-guide')
def leveling_guide():
    return render_template('leveling_guide.html')

@app.route('/mechanics')
def mechanics():
    return render_template('mechanics.html')

@app.route('/pvp')
def pvp():
    return render_template('pvp.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('home'))
    
    fruits = Fruit.query.filter(Fruit.name.ilike(f'%{query}%')).all()
    bosses = Boss.query.filter(Boss.name.ilike(f'%{query}%')).all()
    maps = Map.query.filter(Map.name.ilike(f'%{query}%')).all()
    codes = Code.query.filter(Code.code.ilike(f'%{query}%')).all()
    
    return render_template('search_results.html', query=query, fruits=fruits, bosses=bosses, maps=maps, codes=codes)

# Add missing mythical fruits from Update 20
@app.route('/add-mythical-fruits')
def add_mythical_fruits():
    # Check if these fruits already exist to avoid duplicates
    existing_fruits = [fruit.name for fruit in Fruit.query.all()]
    added_fruits = []
    
    # LeopardV2 (Update 20 - March 2025)
    if "LeopardV2" not in existing_fruits:
        leopardv2 = Fruit(
            name="LeopardV2",
            description="The upgraded version of Leopard fruit with enhanced abilities. Transform into a powerful leopard-human hybrid with devastating attacks, afterimage techniques, and superior agility.",
            rarity="Mythical",
            drop_rate=0.01,
            image="leopardv2.png",
            type="Zoan"
        )
        db.session.add(leopardv2)
        added_fruits.append("LeopardV2")
        
        # Add abilities if the fruit was added
        db.session.flush()  # Generate ID for the new fruit
        db.session.add_all([
            Ability(name="Leopard Transformation", description="Transform into a powerful leopard-human hybrid with enhanced abilities.", key="V", fruit_id=leopardv2.id),
            Ability(name="Afterimage Assault", description="Create afterimages to confuse opponents and deliver rapid strikes.", key="C", fruit_id=leopardv2.id),
            Ability(name="Spiral Kick", description="Launch a powerful spinning kick that sends enemies flying.", key="X", fruit_id=leopardv2.id),
            Ability(name="Finger Revolver", description="Fire compressed air bullets from your fingers at high speed.", key="Z", fruit_id=leopardv2.id),
            Ability(name="Predator's Leap", description="Leap forward with incredible speed to close distance or escape.", key="F", fruit_id=leopardv2.id),
        ])
    
    # DragonV2 (Update 17 - October 2023)
    if "Dragon V2" not in existing_fruits:
        dragonv2 = Fruit(
            name="Dragon V2",
            description="An advanced version of the Dragon fruit with even more devastating abilities.",
            rarity="Mythical",
            drop_rate=0.025,
            image="dragonv2.png",
            type="Zoan"
        )
        db.session.add(dragonv2)
        added_fruits.append("Dragon V2")
        
        # Add abilities
        db.session.flush()
        db.session.add_all([
            Ability(name="Dragon Transformation", description="Transform into a powerful dragon hybrid with enhanced abilities.", key="V", fruit_id=dragonv2.id),
            Ability(name="Thunder Bagua", description="Deliver a devastating blow with immense power.", key="C", fruit_id=dragonv2.id),
            Ability(name="Dragon's Demolition", description="Create a powerful blast wave that damages everything in its path.", key="X", fruit_id=dragonv2.id),
            Ability(name="Wind Blade", description="Slash with powerful wind blades that cut through defenses.", key="Z", fruit_id=dragonv2.id),
            Ability(name="Dragon Flight", description="Soar through the sky with dragon wings.", key="F", fruit_id=dragonv2.id),
        ])
    
    # DoughV2 (Update 19 - December 2024)
    if "DoughV2" not in existing_fruits:
        doughv2 = Fruit(
            name="DoughV2",
            description="Enhanced version of the Dough fruit with advanced mochi manipulation abilities and superior combat potential.",
            rarity="Mythical",
            drop_rate=0.02,
            image="doughv2.png",
            type="Paramecia"
        )
        db.session.add(doughv2)
        added_fruits.append("DoughV2")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Power Dough", description="Enhance your strikes with hardened mochi for devastating damage.", key="Z", fruit_id=doughv2.id),
            Ability(name="Scorching Buzzcut", description="Create a buzzsaw of mochi that cuts through enemies and carries them along.", key="X", fruit_id=doughv2.id),
            Ability(name="Elastic Lasso", description="Extends a mochi arm to grab enemies and pull them toward you.", key="C", fruit_id=doughv2.id),
            Ability(name="Dough Pummel", description="Rapidly punch enemies with extending mochi fists.", key="V", fruit_id=doughv2.id),
            Ability(name="Mochi Glide", description="Create wings of mochi to glide through the air.", key="F", fruit_id=doughv2.id),
        ])
    
    # Ope-Ope (Update 10 - June 2023)
    if "Ope-Ope" not in existing_fruits:
        opeope = Fruit(
            name="Ope-Ope",
            description="Grants the user the ability to create a 'Room' where they have complete control over everything within its boundaries.",
            rarity="Mythical",
            drop_rate=0.02,
            image="opeope.png",
            type="Paramecia"
        )
        db.session.add(opeope)
        added_fruits.append("Ope-Ope")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Room", description="Create a spherical space where the user can manipulate anything within.", key="Z", fruit_id=opeope.id),
            Ability(name="Shambles", description="Instantly swap positions of objects within the Room.", key="X", fruit_id=opeope.id),
            Ability(name="Gamma Knife", description="Create a blade of energy that causes internal damage to targets.", key="C", fruit_id=opeope.id),
            Ability(name="Counter Shock", description="Emit an electrical charge that damages opponents.", key="V", fruit_id=opeope.id),
            Ability(name="Takt", description="Levitate objects or people within the Room.", key="F", fruit_id=opeope.id),
        ])
    
    # Okuchi (Wolf)
    if "Okuchi" not in existing_fruits:
        okuchi = Fruit(
            name="Okuchi",
            description="Allows the user to gain the traits and abilities of the Mythological Wolf: Okuchi no Makami",
            rarity="Mythical",
            drop_rate=0.01,
            image="okuchi.png",
            type="Zoan"
        )
        db.session.add(okuchi)
        added_fruits.append("Okuchi")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Wolf Fang", description="Bite with powerful mythical fangs.", key="Z", fruit_id=okuchi.id),
            Ability(name="Mythical Howl", description="Release a powerful howl that damages enemies.", key="X", fruit_id=okuchi.id),
            Ability(name="Wolf Rush", description="Rush forward with incredible speed.", key="C", fruit_id=okuchi.id),
            Ability(name="Wolf Form", description="Transform into the mythical wolf form.", key="V", fruit_id=okuchi.id),
            Ability(name="Spirit Run", description="Move with supernatural speed.", key="F", fruit_id=okuchi.id)
        ])
    
    # Soul (Update 15 - February 2024)
    if "Soul" not in existing_fruits:
        soul = Fruit(
            name="Soul",
            description="Allows the user to manipulate souls, stealing life force from others.",
            rarity="Mythical",
            drop_rate=0.025,
            image="soul.png",
            type="Paramecia"
        )
        db.session.add(soul)
        added_fruits.append("Soul")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Soul Pocus", description="Extract souls from enemies who show fear.", key="Z", fruit_id=soul.id),
            Ability(name="Soul Parade", description="Summon souls to attack enemies in a wide area.", key="X", fruit_id=soul.id),
            Ability(name="Soul Grab", description="Capture an enemy's soul to drain their energy.", key="C", fruit_id=soul.id),
            Ability(name="Incarnation", description="Create powerful manifestations from collected souls.", key="V", fruit_id=soul.id),
            Ability(name="Soul Levitation", description="Use soul energy to float and move through the air.", key="F", fruit_id=soul.id),
        ])
    
    # Nika (Update 14 - September 2023)
    if "Nika" not in existing_fruits:
        nika = Fruit(
            name="Nika",
            description="The legendary Sun God fruit, granting the user enhanced physical abilities and freedom of movement.",
            rarity="Mythical",
            drop_rate=0.01,
            image="nika.png",
            type="Zoan"
        )
        db.session.add(nika)
        added_fruits.append("Nika")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Awakening", description="Awaken the powers of the Sun God for enhanced abilities.", key="V", fruit_id=nika.id),
            Ability(name="Bajrang Gun", description="Deliver a massive punch with tremendous destructive power.", key="X", fruit_id=nika.id),
            Ability(name="Gomu Hydra", description="Create multiple stretching limbs to attack from all directions.", key="C", fruit_id=nika.id),
            Ability(name="Culverin", description="Launch a powerful punch that can change direction to track enemies.", key="Z", fruit_id=nika.id),
            Ability(name="Sky Walk", description="Jump and move through the air as if running on solid ground.", key="F", fruit_id=nika.id),
        ])
    
    db.session.commit()
    
    return f"Added the following mythical fruits: {', '.join(added_fruits) if added_fruits else 'None (all already exist)'}"

# Database initialization and sample data
@app.route('/init-db')
def init_db():
    # Drop all tables first to ensure a clean slate
    db.drop_all()
    db.create_all()
    
    # Define all fruits
    # Mythical
    lightning = Fruit(name="Lightning", description="Allows the user to create, control, and transform into lightning.", rarity="Mythical", drop_rate=0.03, image="lightning.png", type="Logia")
    leopardv2 = Fruit(name="LeopardV2", description="The upgraded version of Leopard fruit. Transform into a powerful leopard-human hybrid.", rarity="Mythical", drop_rate=0.01, image="leopardv2.png", type="Zoan")
    dragonv2 = Fruit(name="Dragon V2", description="An advanced version of the Dragon fruit.", rarity="Mythical", drop_rate=0.025, image="dragonv2.png", type="Zoan")
    doughv2 = Fruit(name="DoughV2", description="Enhanced version of the Dough fruit.", rarity="Mythical", drop_rate=0.02, image="doughv2.png", type="Paramecia")
    opeope = Fruit(name="Ope-Ope", description="Create a 'Room' to control space.", rarity="Mythical", drop_rate=0.02, image="opeope.png", type="Paramecia")
    soul = Fruit(name="Soul", description="Manipulate souls, stealing life force.", rarity="Mythical", drop_rate=0.025, image="soul.png", type="Paramecia")
    nika = Fruit(name="Nika", description="The legendary Sun God fruit.", rarity="Mythical", drop_rate=0.01, image="nika.png", type="Zoan")
    okuchi = Fruit(name="Okuchi", description="Mythological Wolf: Okuchi no Makami powers.", rarity="Mythical", drop_rate=0.01, image="okuchi.png", type="Zoan")
    darkquake = Fruit(name="DarkXQuake", description="Harness the power of two powerful fruits!", rarity="Mythical", drop_rate=0.01, image="darkxquake.png", type="Logia")

    # Legendary
    phoenix = Fruit(name="Phoenix", description="Transform into a phoenix with healing powers.", rarity="Legendary", drop_rate=0.02, image="phoenix.png", type="Zoan")
    dragon = Fruit(name="Dragon", description="Transform into a dragon with immense power.", rarity="Legendary", drop_rate=0.02, image="dragon.png", type="Zoan")
    leopard = Fruit(name="Leopard", description="Turn into a leopard. Was Mythical.", rarity="Legendary", drop_rate=0.1, image="leopard.png", type="Zoan")
    dough = Fruit(name="Dough", description="Create and control mochi. Was Mythical.", rarity="Legendary", drop_rate=0.1, image="dough.png", type="Paramecia")
    quake = Fruit(name="Quake", description="Generate intense vibrations and earthquakes.", rarity="Legendary", drop_rate=0.17, image="quake.png", type="Paramecia")
    gravity = Fruit(name="Gravity", description="Allows the user to control gravity.", rarity="Legendary", drop_rate=0.14, image="gravity.png", type="Paramecia")
    metal = Fruit(name="Metal", description="Control and manipulate metals.", rarity="Legendary", drop_rate=0.15, image="metal.png", type="Paramecia")
    venom = Fruit(name="Venom", description="Emit and control venom.", rarity="Legendary", drop_rate=0.07, image="venom.png", type="Paramecia")
    flamev2 = Fruit(name="FlameV2", description="Harness fierce flames to engulf and overwhelm adversaries.", rarity="Legendary", drop_rate=0.14, image="flamev2.png", type="Logia") # Added FlameV2
    icev2 = Fruit(name="Ice V2", description="Unleash the true potential of ice.", rarity="Legendary", drop_rate=0.14, image="icev2.png", type="Logia")
    magmav2 = Fruit(name="Magma V2", description="Unleash the true potential of magma.", rarity="Legendary", drop_rate=0.14, image="magmav2.png", type="Logia")
    rubberv2 = Fruit(name="Rubber V2", description="Stronger version of rubber (Post Timeskip).", rarity="Legendary", drop_rate=0.10, image="rubberv2.png", type="Paramecia")

    # Epic
    light = Fruit(name="Light", description="Create, control, and transform into light.", rarity="Epic", drop_rate=0.92, image="light.png", type="Logia")
    magma = Fruit(name="Magma", description="Create, control, and transform into magma.", rarity="Epic", drop_rate=0.85, image="magma.png", type="Logia")
    snow = Fruit(name="Snow", description="Smother the battlefield in cold snow.", rarity="Epic", drop_rate=0.92, image="snow.png", type="Logia")
    flame_epic = Fruit(name="Flame", description="Create, control and transform fire.", rarity="Epic", drop_rate=0.85, image="flame.png", type="Logia")
    love = Fruit(name="Love", description="Wield the powerful force of love.", rarity="Epic", drop_rate=0.59, image="love.png", type="Paramecia")
    string = Fruit(name="String", description="Create and manipulate strings.", rarity="Epic", drop_rate=0.68, image="string.png", type="Paramecia")
    paw = Fruit(name="Paw", description="Superhuman ability to repel anything touched.", rarity="Epic", drop_rate=0.76, image="paw.png", type="Paramecia")

    # Rare
    ice = Fruit(name="Ice", description="Create, control, and transform into ice.", rarity="Rare", drop_rate=2.8, image="ice.png", type="Logia")
    darkness = Fruit(name="Darkness", description="Create and control darkness.", rarity="Rare", drop_rate=2.5, image="darkness.png", type="Logia")
    bomb = Fruit(name="Bomb", description="Explode anything touched.", rarity="Rare", drop_rate=2.33, image="bomb.png", type="Paramecia")
    ash = Fruit(name="Ash", description="Cloak the battlefield in ash.", rarity="Rare", drop_rate=1.04, image="ash.png", type="Logia")

    # Uncommon
    falcon = Fruit(name="Falcon", description="Transform into a falcon.", rarity="Uncommon", drop_rate=7.2, image="falcon.png", type="Zoan")
    gas = Fruit(name="Gas", description="Create and control poisonous gas.", rarity="Uncommon", drop_rate=6.8, image="gas.png", type="Logia")
    rubber = Fruit(name="Rubber", description="Grants the user properties of rubber.", rarity="Uncommon", drop_rate=6.05, image="rubber.png", type="Paramecia")
    smoke = Fruit(name="Smoke", description="Create, control, and transform into smoke.", rarity="Uncommon", drop_rate=8.34, image="smoke.png", type="Logia")

    # Common
    barrier = Fruit(name="Barrier", description="Generate defensive and offensive barriers.", rarity="Common", drop_rate=21.1, image="barrier.png", type="Paramecia")
    chop_common = Fruit(name="Chop", description="Slice through objects and create air slashes.", rarity="Common", drop_rate=22.5, image="chop.png", type="Paramecia")
    sand = Fruit(name="Sand", description="Create, control, and transform into sand.", rarity="Common", drop_rate=21.1, image="sand.png", type="Logia")

    # Add fruits to session
    db.session.add_all([
        # Mythical
        lightning, leopardv2, dragonv2, doughv2, opeope, soul, nika, okuchi, darkquake,
        # Legendary
        phoenix, dragon, leopard, dough, quake, gravity, metal, venom, icev2, magmav2, rubberv2,
        flamev2, # Added FlameV2
        # Epic
        light, magma, snow, flame_epic, love, string, paw,
        # Rare
        ice, darkness, bomb, ash,
        # Uncommon
        falcon, gas, rubber, smoke,
        # Common
        barrier, chop_common, sand
    ])
    db.session.commit()
    
    # Fetch IDs for fruits after commit
    # We need IDs to link abilities correctly
    # Re-fetch fruits by name to ensure we have the correct objects with IDs
    fruits_map = {f.name: f for f in Fruit.query.all()}
    
    # Define Abilities list
    abilities_to_add = []
    
    # Helper to safely add abilities
    def add_ability(fruit_name, name, description, key):
        fruit = fruits_map.get(fruit_name)
        if fruit:
            abilities_to_add.append(Ability(name=name, description=description, key=key, fruit_id=fruit.id))
        else:
            print(f"Warning: Fruit '{fruit_name}' not found when adding ability '{name}'")

    # Add abilities for each fruit
    # Mythical Abilities
    add_ability("Lightning", "Lightning Ray", "Low cooldown, very spammable.", "Z")
    add_ability("Lightning", "Raigo", "Powerful lightning attack with large AoE.", "X")
    add_ability("Lightning", "Thunder Spear", "Fast lightning projectile.", "C")
    add_ability("Lightning", "El Thor", "Summons a huge lightning bolt.", "V")
    add_ability("Lightning", "Light Flight", "Second fastest flight.", "F")
    add_ability("LeopardV2", "Finger Revolver", "Fire compressed air bullets.", "Z")
    add_ability("LeopardV2", "Spiral Kick", "Powerful spinning kick.", "X")
    add_ability("LeopardV2", "Afterimage Assault", "Create afterimages for rapid strikes.", "C")
    add_ability("LeopardV2", "Leopard Transformation", "Transform into leopard-human hybrid.", "V")
    add_ability("LeopardV2", "Predator's Leap", "Leap forward with incredible speed.", "F")
    add_ability("Dragon V2", "Wind Blade", "Slash with powerful wind blades.", "Z")
    add_ability("Dragon V2", "Dragon's Demolition", "Create a powerful blast wave.", "X")
    add_ability("Dragon V2", "Thunder Bagua", "Deliver a devastating blow.", "C")
    add_ability("Dragon V2", "Dragon Transformation", "Transform into dragon hybrid.", "V")
    add_ability("Dragon V2", "Dragon Flight", "Soar through the sky.", "F")
    add_ability("DoughV2", "Power Dough", "Enhance strikes with hardened mochi.", "Z")
    add_ability("DoughV2", "Scorching Buzzcut", "Create a buzzsaw of mochi.", "X")
    add_ability("DoughV2", "Elastic Lasso", "Extend mochi arm to grab enemies.", "C")
    add_ability("DoughV2", "Dough Pummel", "Rapidly punch with extending mochi fists.", "V")
    add_ability("DoughV2", "Mochi Glide", "Create mochi wings to glide.", "F")
    add_ability("Ope-Ope", "Room", "Create a spherical space for manipulation.", "Z")
    add_ability("Ope-Ope", "Shambles", "Instantly swap positions within Room.", "X")
    add_ability("Ope-Ope", "Gamma Knife", "Create energy blade for internal damage.", "C")
    add_ability("Ope-Ope", "Counter Shock", "Emit an electrical charge.", "V")
    add_ability("Ope-Ope", "Takt", "Levitate objects within Room.", "F")
    add_ability("Soul", "Soul Pocus", "Extract souls from enemies showing fear.", "Z")
    add_ability("Soul", "Soul Parade", "Summon souls to attack.", "X")
    add_ability("Soul", "Soul Grab", "Capture enemy soul to drain energy.", "C")
    add_ability("Soul", "Incarnation", "Create powerful manifestations from souls.", "V")
    add_ability("Soul", "Soul Levitation", "Float using soul energy.", "F")
    add_ability("Nika", "Culverin", "Launch powerful tracking punch.", "Z")
    add_ability("Nika", "Bajrang Gun", "Deliver a massive punch.", "X")
    add_ability("Nika", "Gomu Hydra", "Create multiple stretching limbs.", "C")
    add_ability("Nika", "Awakening", "Awaken Sun God powers.", "V")
    add_ability("Nika", "Sky Walk", "Move through the air.", "F")
    add_ability("Okuchi", "Wolf Fang", "Bite with mythical fangs.", "Z")
    add_ability("Okuchi", "Mythical Howl", "Powerful damaging howl.", "X")
    add_ability("Okuchi", "Wolf Rush", "Rush forward with speed.", "C")
    add_ability("Okuchi", "Wolf Form", "Transform into mythical wolf.", "V")
    add_ability("Okuchi", "Spirit Run", "Move with supernatural speed.", "F")
    add_ability("DarkXQuake", "Dark Tremor", "Combine darkness and quake.", "Z")
    add_ability("DarkXQuake", "Void Quake", "Black hole with seismic power.", "X")
    add_ability("DarkXQuake", "Dark Tsunami", "Wave of darkness and quake.", "C")
    add_ability("DarkXQuake", "World Ender", "Ultimate dark/quake combo.", "V")
    add_ability("DarkXQuake", "Shadow Quake", "Travel through shadows with quake.", "F")

    # Legendary Abilities
    add_ability("Phoenix", "Phoenix Fire", "Launch blue flames.", "Z")
    add_ability("Phoenix", "Phoenix Regeneration", "Heal with phoenix flames.", "X")
    add_ability("Phoenix", "Talons of the Phoenix", "Strike with powerful talons.", "C")
    add_ability("Phoenix", "Phoenix Transformation", "Transform into a phoenix.", "V")
    add_ability("Phoenix", "Phoenix Flight", "Fly with phoenix wings.", "F")
    add_ability("Dragon", "Dragon Breath", "Breathe fire.", "Z")
    add_ability("Dragon", "Dragon Claw", "Strike with dragon claws.", "X")
    add_ability("Dragon", "Dragon Twister", "Create a damaging tornado.", "C")
    add_ability("Dragon", "Dragon Form", "Transform into a dragon.", "V")
    add_ability("Dragon", "Dragon Flight", "Fly with dragon wings.", "F")
    add_ability("Leopard", "Feral Dash", "Dash forward with increased speed.", "Z")
    add_ability("Leopard", "Leopard Claw", "Slash enemies with sharp claws.", "X")
    add_ability("Leopard", "Pounce", "Leap at target with speed.", "C")
    add_ability("Leopard", "Leopard Form", "Transform into leopard-human hybrid.", "V")
    add_ability("Leopard", "Predator Sense", "Enhance senses to detect enemies.", "F")
    add_ability("Dough", "Dough Ball", "Throw exploding dough ball.", "Z")
    add_ability("Dough", "Mochi Mochi", "Create wave of sticky dough.", "X")
    add_ability("Dough", "Dough Thrust", "Extend dough arm to grab.", "C")
    add_ability("Dough", "Mochi Barrage", "Barrage of dough punches.", "V")
    add_ability("Dough", "Dough Mobility", "Increase mobility.", "F")
    add_ability("Quake", "Quake Punch", "Devastating quake punch.", "Z")
    add_ability("Quake", "Tsunami", "Create massive tsunami wave.", "X")
    add_ability("Quake", "Tremor", "Create earthquakes.", "C")
    add_ability("Quake", "Seismic Wave", "Release powerful seismic wave.", "V")
    add_ability("Quake", "Ground Shatter", "Shatter the ground.", "F")
    add_ability("Gravity", "Gravity Push", "Push enemies away.", "Z")
    add_ability("Gravity", "Gravity Pull", "Pull enemies toward you.", "X")
    add_ability("Gravity", "Gravity Crush", "Crush enemies with gravity.", "C")
    add_ability("Gravity", "Zero Gravity", "Remove gravity.", "V")
    add_ability("Gravity", "Gravity Flight", "Fly by controlling gravity.", "F")
    add_ability("Metal", "Metal Spikes", "Launch metal spikes.", "Z")
    add_ability("Metal", "Metal Shield", "Form protective metal shield.", "X")
    add_ability("Metal", "Metal Storm", "Rain down metal projectiles.", "C")
    add_ability("Metal", "Metal Body", "Transform into living metal.", "V")
    add_ability("Metal", "Metal Movement", "Create metal structures to move.", "F")
    add_ability("Venom", "Venom Shot", "Fire deadly venom.", "Z")
    add_ability("Venom", "Venom Wave", "Create toxic venom wave.", "X")
    add_ability("Venom", "Toxic Cloud", "Release poisonous gas cloud.", "C")
    add_ability("Venom", "Venom Hydra", "Create venom hydra.", "V")
    add_ability("Venom", "Venom Movement", "Move using venom propulsion.", "F")
    add_ability("Flash", "Flash Bang", "Create blinding flash.", "Z")
    add_ability("Flash", "Flash Step", "Move at blinding speed.", "X")
    add_ability("Flash", "Flash Storm", "Create multiple flashes.", "C")
    add_ability("Flash", "Flash Form", "Transform into light energy.", "V")
    add_ability("Flash", "Flash Movement", "Move at light speed.", "F")
    add_ability("Flame", "Flame Emperor", "Massive flame explosion.", "Z")
    add_ability("Flame", "Flame Pillar", "Towering flame pillar.", "X")
    add_ability("Flame", "Phoenix Mode", "Transform into flame phoenix.", "C")
    add_ability("Flame", "Flame Body", "Transform into living flames.", "V")
    add_ability("Flame", "Flame Dash", "Dash using flame propulsion.", "F")
    add_ability("Ice V2", "Ice Age V2", "Enhanced ice age attack.", "Z")
    add_ability("Ice V2", "Ice Wolf", "Summon ice wolf.", "X")
    add_ability("Ice V2", "Frozen World", "Freeze large area.", "C")
    add_ability("Ice V2", "Ice Awakening", "Awaken true ice powers.", "V")
    add_ability("Ice V2", "Ice Glide V2", "Enhanced ice movement.", "F")
    add_ability("Magma V2", "Magma Eruption", "Massive magma eruption.", "Z")
    add_ability("Magma V2", "Magma Dragon", "Summon magma dragon.", "X")
    add_ability("Magma V2", "Volcanic Field", "Turn battlefield volcanic.", "C")
    add_ability("Magma V2", "Magma Awakening", "Awaken true magma powers.", "V")
    add_ability("Magma V2", "Magma Surf V2", "Enhanced magma movement.", "F")
    add_ability("Rubber V2", "Red Hawk", "Powerful fire-enhanced punch.", "Z")
    add_ability("Rubber V2", "Elephant Gun", "Giant hardened punch.", "X")
    add_ability("Rubber V2", "Kong Gun", "Powerful Gear 4 punch.", "C")
    add_ability("Rubber V2", "Gear 4", "Transform into Gear 4 Boundman.", "V")
    add_ability("Rubber V2", "Python", "Controllable stretching attack.", "F")
    add_ability("FlameV2", "Scorching Fist", "Create a beam of fire, scorching the enemy.", "Z")
    add_ability("FlameV2", "Twisting Claw", "Lunge forward, grab, launch, and explode enemy.", "X")
    add_ability("FlameV2", "Blazing Meteor", "Turn into a ball of fire and fly towards cursor.", "C")
    add_ability("FlameV2", "Crimson Body", "Cover body in flames, dealing passive damage.", "V")
    add_ability("FlameV2", "Supernova", "Summon a giant ball of fire and throw it down.", "F")

    # Epic Abilities
    add_ability("Light", "Light Beam", "Instant light beam.", "Z")
    add_ability("Light", "Light Explosion", "Explosion of light.", "X")
    add_ability("Light", "Light Sword", "Create light sword.", "C")
    add_ability("Light", "Light Transformation", "Transform into light.", "V")
    add_ability("Light", "Light Speed", "Travel at light speed.", "F")
    add_ability("Magma", "Magma Fist", "Launch exploding magma fist.", "Z")
    add_ability("Magma", "Great Eruption", "Massive magma eruption.", "X")
    add_ability("Magma", "Meteor Volcano", "Rain down magma meteors.", "C")
    add_ability("Magma", "Magma Body", "Transform body into magma.", "V")
    add_ability("Magma", "Magma Movement", "Propel with magma.", "F")
    add_ability("Snow", "Snow Shot", "Fire freezing snow ball.", "Z")
    add_ability("Snow", "Blizzard", "Create damaging blizzard.", "X")
    add_ability("Snow", "Snow Sword", "Create ice/snow sword.", "C")
    add_ability("Snow", "Snow Body", "Transform into snow.", "V")
    add_ability("Snow", "Snow Glide", "Glide on snow path.", "F")
    add_ability("Fire", "Fire Ball", "Launch fire ball.", "Z")
    add_ability("Fire", "Fire Pillar", "Create flame pillar.", "X")
    add_ability("Fire", "Fire Dragon", "Create flame dragon.", "C")
    add_ability("Fire", "Fire Body", "Transform into fire.", "V")
    add_ability("Fire", "Fire Flight", "Fly using fire.", "F")
    add_ability("Love", "Love Beam", "Fire love energy beam.", "Z")
    add_ability("Love", "Healing Heart", "Heal self and allies.", "X")
    add_ability("Love", "Love Slave", "Charm enemies.", "C")
    add_ability("Love", "Love Aura", "Create love energy aura.", "V")
    add_ability("Love", "Love Float", "Float using love energy.", "F")
    add_ability("String", "String Shot", "Fire damaging string.", "Z")
    add_ability("String", "String Fence", "Create damaging string fence.", "X")
    add_ability("String", "Overheat", "Create string whip.", "C")
    add_ability("String", "String Cocoon", "Protective string cocoon.", "V")
    add_ability("String", "Sky Path", "Swing through air.", "F")
    add_ability("Paw", "Pressure Cannon", "Teleport punch with shockwave.", "Z")
    add_ability("Paw", "Sonic Stomp", "Teleport stomp with AOE damage.", "X")
    add_ability("Paw", "Sumo Thrust Barrage", "Fire paw-shaped bullets.", "C")
    add_ability("Paw", "Torture", "Stun target with red paw.", "V")
    add_ability("Paw", "Ursus Shock", "Giant paw explosion.", "F")

    # Rare Abilities
    add_ability("Ice", "Ice Shard", "Fire sharp ice shards.", "Z")
    add_ability("Ice", "Ice Age", "Freeze ground around you.", "X")
    add_ability("Ice", "Ice Sword", "Create ice sword.", "C")
    add_ability("Ice", "Ice Time", "Freeze self for defense.", "V")
    add_ability("Ice", "Ice Path", "Create ice path.", "F")
    add_ability("Darkness", "Dark Matter", "Fire darkness ball.", "Z")
    add_ability("Darkness", "Black Hole", "Create black hole.", "X")
    add_ability("Darkness", "Liberation", "Release stored enemies.", "C")
    add_ability("Darkness", "Dark Vortex", "Whirlwind of darkness.", "V")
    add_ability("Darkness", "Shadow Travel", "Travel through shadow.", "F")
    add_ability("Bomb", "Explosion", "Create powerful explosion.", "Z")
    add_ability("Bomb", "Landmine", "Place explosive trap.", "X")
    add_ability("Bomb", "Blast Wave", "Release explosive wave.", "C")
    add_ability("Bomb", "Explosion Body", "Explosive form.", "V")
    add_ability("Ash", "Ash Cloud", "Suffocating ash cloud.", "Z")
    add_ability("Ash", "Ash Storm", "Burning ash storm.", "X")
    add_ability("Ash", "Ash Burial", "Bury enemies in ash.", "C")
    add_ability("Ash", "Ash Form", "Transform into ash.", "V")
    add_ability("Ash", "Ash Movement", "Move using ash.", "F")

    # Uncommon Abilities
    add_ability("Falcon", "Talon Strike", "Swift talon strike.", "Z")
    add_ability("Falcon", "Wing Slash", "Create wind blade.", "X")
    add_ability("Falcon", "Aerial Dive", "Powerful aerial dive.", "C")
    add_ability("Falcon", "Falcon Form", "Transform into falcon.", "V")
    add_ability("Falcon", "Falcon Flight", "Fly with falcon wings.", "F")
    add_ability("Gas", "Gas Cloud", "Poisonous gas cloud.", "Z")
    add_ability("Gas", "Toxic Shot", "Concentrated poison gas.", "X")
    add_ability("Gas", "Gas Explosion", "Explosion of gas.", "C")
    add_ability("Gas", "Gas Form", "Transform into gas.", "V")
    add_ability("Gas", "Gas Stream", "Propel with gas.", "F")
    add_ability("Rubber", "Gum Pistol", "Long-range punch.", "Z")
    add_ability("Rubber", "Gum Bazooka", "Powerful two-arm attack.", "X")
    add_ability("Rubber", "Gum Balloon", "Bounce back attacks.", "C")
    add_ability("Rubber", "Gear Second", "Increase speed.", "V")
    add_ability("Rubber", "Rubber Stretch", "Stretch to move.", "F")
    add_ability("Chop", "Air Slash", "Flying slash attack.", "Z")
    add_ability("Chop", "Cross Chop", "X-shaped slash.", "X")
    add_ability("Chop", "Chop Wave", "Wave of slashing energy.", "C")
    add_ability("Chop", "Chop Form", "Enhance cutting.", "V")
    add_ability("Chop", "Quick Slash", "Dash forward with slash.", "F")

    # Common Abilities
    add_ability("Barrier", "Barrier Wall", "Protective barrier wall.", "Z")
    add_ability("Barrier", "Surprise Attack", "Escape move.", "X")
    add_ability("Barrier", "Barrier Prison", "Immunity inside.", "C")
    add_ability("Barrier", "Barrier Towers", "Blocking wall.", "V")
    add_ability("Chop", "Air Slash", "Create a flying slash attack.", "Z") 
    add_ability("Chop", "Cross Chop", "Create an X-shaped slash.", "X")
    add_ability("Chop", "Chop Slam", "Jump and slam down.", "C")
    add_ability("Chop", "Sword Dance", "Spin with slashes.", "V")
    add_ability("Smoke", "Smoke Shot", "Fire smoke ball.", "Z")
    add_ability("Smoke", "Smoke Screen", "Obscure vision.", "X")
    add_ability("Smoke", "Smoke Dash", "Dash forward as smoke.", "C")
    add_ability("Smoke", "Smoke Form", "Transform into smoke.", "V")
    add_ability("Smoke", "Smoke Glide", "Glide as smoke.", "F")
    add_ability("Split", "Split Shot", "Fire body parts.", "Z")
    add_ability("Split", "Split Rush", "Rush while splitting.", "X")
    add_ability("Split", "Split Defense", "Split to avoid damage.", "C")
    add_ability("Split", "Split Form", "Transform into split form.", "V")
    add_ability("Sand", "Sand Blast", "Launch sand blast.", "Z")
    add_ability("Sand", "Sand Tomb", "Trap enemies in sand.", "X")
    add_ability("Sand", "Desert Spada", "Extend sand blade.", "C")
    add_ability("Sand", "Sand Dispersal", "Transform into sand.", "V")
    add_ability("Sand", "Sand Glide", "Glide on sand.", "F")

    # Add all abilities to the session
    db.session.add_all(abilities_to_add)

    # Add some bosses (Updating health to reflect phases)
    marco = Boss(name="Marco", description="The Phoenix, First Commander.", location="Flower Hill (Dressrosa)", health=8000, exp_reward=15000, gem_reward=450, image="marco.png")
    kaido = Boss(name="Kaido", description="King of the Beasts.", location="Onigashima", health=15000, exp_reward=24000, gem_reward=550, image="kaido.jpg")
    cake_queen = Boss(name="Cake Queen", description="Captain of the Big Mom Pirates.", location="Cake Lair (Whole Cake)", health=11600, exp_reward=20000, gem_reward=480, image="cake_queen.png")
    katakuri = Boss(name="Katakuri", description="Sweet Commander.", location="Mirror World", health=10000, exp_reward=18000, gem_reward=460, image="katakuri.png")
                    
    db.session.add_all([marco, kaido, cake_queen, katakuri])
    db.session.commit()

    # Add Fruit Drops (Fetch fruits again after commit to be safe)
    fruits_map = {f.name: f for f in Fruit.query.all()}
    
    phoenix_db = fruits_map.get("Phoenix")
    dragon_db = fruits_map.get("Dragon")
    soul_db = fruits_map.get("Soul")
    dough_db = fruits_map.get("Dough") # Katakuri drops base Dough
    # doughv2_db = fruits_map.get("DoughV2") # Optional DoughV2 drop
    
    if phoenix_db:
        db.session.add(FruitDrop(boss_id=marco.id, fruit_id=phoenix_db.id, drop_rate=1.0))
    if dragon_db:
        db.session.add(FruitDrop(boss_id=kaido.id, fruit_id=dragon_db.id, drop_rate=1.0))
    if soul_db:
        db.session.add(FruitDrop(boss_id=cake_queen.id, fruit_id=soul_db.id, drop_rate=1.0))
    if dough_db:
         db.session.add(FruitDrop(boss_id=katakuri.id, fruit_id=dough_db.id, drop_rate=1.0))
    # if doughv2_db: 
        # db.session.add(FruitDrop(boss_id=katakuri.id, fruit_id=doughv2_db.id, drop_rate=0.5))
    
    # Add maps, codes, updates etc...
    db.session.add(Map(name="Dressrosa", description="Starting area.", level_requirement=None, exp_multiplier=1.0, image="map_dressrosa.jpg"))
    db.session.add(Map(name="Whole Cake", description="Mid-game area.", level_requirement=100, exp_multiplier=1.75, image="map_whole_cake.jpg"))
    db.session.add(Map(name="Mirror World", description="Accessed through Whole Cake.", level_requirement=100, exp_multiplier=1.75, image="map_mirror_world.jpg"))
    db.session.add(Map(name="Onigashima (Wano)", description="Highest level area.", level_requirement=200, exp_multiplier=2.5, image="map_onigashima.jpg"))
    db.session.add(Map(name="Tournament", description="PvP arena.", level_requirement=0, exp_multiplier=1.0, image="map_tournament.jpg"))
    
    db.session.add(Code(code="OMG9HUNDRED!", reward="700 Gems"))
    db.session.add(Code(code="MAGNIFICENT890K!!", reward="500 Gems"))
    db.session.add(Code(code="BIGDAY", reward="350 Gems"))
    
    db.session.add(Update(version="v20", title="Update 20: Leopard V2", date_released=datetime(2025, 3, 17),
                           description="LeopardV2, Snow, Rebirth added.")) # Simplified description
    db.session.add(Update(version="v19", title="Update 19: Dough V2", date_released=datetime(2024, 12, 20),
                           description="DoughV2, Mirror World, Katakuri, Ranked PvP added.")) # Simplified description
    db.session.add(Update(version="v18", title="Update 18: FlameV2 + Ash", date_released=datetime(2024, 7, 2),
                           description="FlameV2, Ash Fruit, M1 System Changes, New PvP Mechanics, Balance Changes"))
    # Add other updates if needed...
    
    # Commit all changes
    db.session.commit()
    
    # Recount fruits after adding all
    final_fruit_count = Fruit.query.count()
    
    return f"Database initialized with sample data! Total fruits: {final_fruit_count}"

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Route to check all mythical fruits
@app.route('/check-mythical-fruits')
def check_mythical_fruits():
    mythical_fruits = Fruit.query.filter_by(rarity="Mythical").all()
    fruit_info = []
    for fruit in mythical_fruits:
        fruit_info.append({
            "name": fruit.name,
            "drop_rate": fruit.drop_rate,
            "abilities": [a.name for a in fruit.abilities]
        })
    return str(fruit_info)

# Route to add missing fruits from wiki
@app.route('/add-missing-fruits')
def add_missing_fruits():
    # Check existing fruits to avoid duplicates
    existing_fruits = [fruit.name for fruit in Fruit.query.all()]
    added_fruits = []
    
    # Common Fruits (63.6% total)
    if "Split" not in existing_fruits:
        split = Fruit(
            name="Split",
            description="Allows the player to split their body into pieces and control them.",
            rarity="Common",
            drop_rate=21.1,
            image="split.png",
            type="Paramecia"
        )
        db.session.add(split)
        added_fruits.append("Split")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Split Shot", description="Fire body parts as projectiles.", key="Z", fruit_id=split.id),
            Ability(name="Split Rush", description="Rush forward while splitting into pieces.", key="X", fruit_id=split.id),
            Ability(name="Split Defense", description="Split apart to avoid damage.", key="C", fruit_id=split.id),
            Ability(name="Split Form", description="Transform into split form.", key="V", fruit_id=split.id)
        ])

    # Uncommon Fruits (25.8% total)
    if "Rubber" not in existing_fruits:
        rubber = Fruit(
            name="Rubber",
            description="Grants the user properties of rubber, turning them into a rubber human.",
            rarity="Uncommon",
            drop_rate=6.05,
            image="rubber.png",
            type="Paramecia"
        )
        db.session.add(rubber)
        added_fruits.append("Rubber")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Gum Pistol", description="Stretch your arm for a long-range punch.", key="Z", fruit_id=rubber.id),
            Ability(name="Gum Bazooka", description="Launch both arms for a powerful attack.", key="X", fruit_id=rubber.id),
            Ability(name="Gum Balloon", description="Inflate yourself to bounce back attacks.", key="C", fruit_id=rubber.id),
            Ability(name="Gear Second", description="Increase attack speed and mobility.", key="V", fruit_id=rubber.id),
            Ability(name="Rubber Stretch", description="Stretch to move quickly.", key="F", fruit_id=rubber.id)
        ])

    # Rare Fruits additions
    if "Bomb" not in existing_fruits:
        bomb = Fruit(
            name="Bomb",
            description="Gives the player the ability to explode anything they touch.",
            rarity="Rare",
            drop_rate=2.33,
            image="bomb.png",
            type="Paramecia"
        )
        db.session.add(bomb)
        added_fruits.append("Bomb")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Explosion", description="Create a powerful explosion.", key="Z", fruit_id=bomb.id),
            Ability(name="Landmine", description="Place an explosive trap.", key="X", fruit_id=bomb.id),
            Ability(name="Blast Wave", description="Release an explosive wave.", key="C", fruit_id=bomb.id),
            Ability(name="Explosion Body", description="Transform into an explosive form.", key="V", fruit_id=bomb.id)
        ])

    # Legendary Fruits additions
    if "Quake" not in existing_fruits:
        quake = Fruit(
            name="Quake",
            description="Generate intense vibrations and earthquakes to unleash devastating attacks.",
            rarity="Legendary",
            drop_rate=0.17,
            image="quake.png",
            type="Paramecia"
        )
        db.session.add(quake)
        added_fruits.append("Quake")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Quake Punch", description="Unleash a devastating quake punch.", key="Z", fruit_id=quake.id),
            Ability(name="Tsunami", description="Create a massive tsunami wave.", key="X", fruit_id=quake.id),
            Ability(name="Tremor", description="Create earthquakes in an area.", key="C", fruit_id=quake.id),
            Ability(name="Seismic Wave", description="Release a powerful seismic wave.", key="V", fruit_id=quake.id),
            Ability(name="Ground Shatter", description="Shatter the ground beneath you.", key="F", fruit_id=quake.id)
        ])

    if "Gravity" not in existing_fruits:
        gravity = Fruit(
            name="Gravity",
            description="Allows the user to control gravity at will.",
            rarity="Legendary",
            drop_rate=0.14,
            image="gravity.png",
            type="Paramecia"
        )
        db.session.add(gravity)
        added_fruits.append("Gravity")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Gravity Push", description="Push enemies away with gravity.", key="Z", fruit_id=gravity.id),
            Ability(name="Gravity Pull", description="Pull enemies toward you.", key="X", fruit_id=gravity.id),
            Ability(name="Gravity Crush", description="Crush enemies with increased gravity.", key="C", fruit_id=gravity.id),
            Ability(name="Zero Gravity", description="Remove gravity in an area.", key="V", fruit_id=gravity.id),
            Ability(name="Gravity Flight", description="Fly by controlling gravity.", key="F", fruit_id=gravity.id)
        ])

    # Mythical Fruits additions
    if "Okuchi" not in existing_fruits:
        okuchi = Fruit(
            name="Okuchi",
            description="Allows the user to gain the traits and abilities of the Mythological Wolf: Okuchi no Makami",
            rarity="Mythical",
            drop_rate=0.01,
            image="okuchi.png",
            type="Zoan"
        )
        db.session.add(okuchi)
        added_fruits.append("Okuchi")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Wolf Fang", description="Bite with powerful mythical fangs.", key="Z", fruit_id=okuchi.id),
            Ability(name="Mythical Howl", description="Release a powerful howl that damages enemies.", key="X", fruit_id=okuchi.id),
            Ability(name="Wolf Rush", description="Rush forward with incredible speed.", key="C", fruit_id=okuchi.id),
            Ability(name="Wolf Form", description="Transform into the mythical wolf form.", key="V", fruit_id=okuchi.id),
            Ability(name="Spirit Run", description="Move with supernatural speed.", key="F", fruit_id=okuchi.id)
        ])

    if "DarkXQuake" not in existing_fruits:
        darkquake = Fruit(
            name="DarkXQuake",
            description="Harness the power of two powerful fruits! Crush your opponents with Quake and engulf them in your darkness.",
            rarity="Mythical",
            drop_rate=0.01,
            image="darkxquake.png",
            type="Logia"
        )
        db.session.add(darkquake)
        added_fruits.append("DarkXQuake")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Dark Tremor", description="Combine darkness and quake powers.", key="Z", fruit_id=darkquake.id),
            Ability(name="Void Quake", description="Create a black hole with seismic power.", key="X", fruit_id=darkquake.id),
            Ability(name="Dark Tsunami", description="Launch a wave of darkness and quake energy.", key="C", fruit_id=darkquake.id),
            Ability(name="World Ender", description="Ultimate combination of darkness and quake.", key="V", fruit_id=darkquake.id),
            Ability(name="Shadow Quake", description="Travel through shadows with quake power.", key="F", fruit_id=darkquake.id)
        ])
    
    # Epic Fruits additions
    if "Fire" not in existing_fruits:
        fire = Fruit(
            name="Fire",
            description="Gives the player the ability to create, control and transform fire at their will.",
            rarity="Epic",
            drop_rate=0.85,
            image="fire.png",
            type="Logia"
        )
        db.session.add(fire)
        added_fruits.append("Fire")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Fire Ball", description="Launch a ball of fire.", key="Z", fruit_id=fire.id),
            Ability(name="Fire Pillar", description="Create a pillar of flames.", key="X", fruit_id=fire.id),
            Ability(name="Fire Dragon", description="Create a dragon made of flames.", key="C", fruit_id=fire.id),
            Ability(name="Fire Body", description="Transform into fire.", key="V", fruit_id=fire.id),
            Ability(name="Fire Flight", description="Fly using fire propulsion.", key="F", fruit_id=fire.id)
        ])

    if "Love" not in existing_fruits:
        love = Fruit(
            name="Love",
            description="Wield the powerful force of love and its various elements to heal, subdue, and attack.",
            rarity="Epic",
            drop_rate=0.59,
            image="love.png",
            type="Paramecia"
        )
        db.session.add(love)
        added_fruits.append("Love")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Love Beam", description="Fire a beam of love energy.", key="Z", fruit_id=love.id),
            Ability(name="Healing Heart", description="Heal yourself and nearby allies.", key="X", fruit_id=love.id),
            Ability(name="Love Slave", description="Charm enemies to fight for you.", key="C", fruit_id=love.id),
            Ability(name="Love Aura", description="Create an aura of love energy.", key="V", fruit_id=love.id),
            Ability(name="Love Float", description="Float using love energy.", key="F", fruit_id=love.id)
        ])

    # Legendary Fruits additions
    if "Metal" not in existing_fruits:
        metal = Fruit(
            name="Metal",
            description="Allows the user to control and manipulate metals with ease.",
            rarity="Legendary",
            drop_rate=0.15,
            image="metal.png",
            type="Paramecia"
        )
        db.session.add(metal)
        added_fruits.append("Metal")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Metal Spikes", description="Create and launch metal spikes.", key="Z", fruit_id=metal.id),
            Ability(name="Metal Shield", description="Form a protective metal shield.", key="X", fruit_id=metal.id),
            Ability(name="Metal Storm", description="Rain down metal projectiles.", key="C", fruit_id=metal.id),
            Ability(name="Metal Body", description="Transform into living metal.", key="V", fruit_id=metal.id),
            Ability(name="Metal Movement", description="Create metal structures to move on.", key="F", fruit_id=metal.id)
        ])

    if "Venom" not in existing_fruits:
        venom = Fruit(
            name="Venom",
            description="Allows the player to emit and control venom from their body.",
            rarity="Legendary",
            drop_rate=0.07,
            image="venom.png",
            type="Paramecia"
        )
        db.session.add(venom)
        added_fruits.append("Venom")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Venom Shot", description="Fire a shot of deadly venom.", key="Z", fruit_id=venom.id),
            Ability(name="Venom Wave", description="Create a wave of toxic venom.", key="X", fruit_id=venom.id),
            Ability(name="Toxic Cloud", description="Release a cloud of poisonous gas.", key="C", fruit_id=venom.id),
            Ability(name="Venom Hydra", description="Create a hydra made of venom.", key="V", fruit_id=venom.id),
            Ability(name="Venom Movement", description="Move using venom propulsion.", key="F", fruit_id=venom.id)
        ])

    if "Flash" not in existing_fruits:
        flash = Fruit(
            name="Flash",
            description="Channel your energy to emit powerful flashes that stun and dazzle enemies",
            rarity="Legendary",
            drop_rate=0.15,
            image="flash.png",
            type="Paramecia"
        )
        db.session.add(flash)
        added_fruits.append("Flash")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Flash Bang", description="Create a blinding flash of light.", key="Z", fruit_id=flash.id),
            Ability(name="Flash Step", description="Move at blinding speeds.", key="X", fruit_id=flash.id),
            Ability(name="Flash Storm", description="Create multiple flashes of light.", key="C", fruit_id=flash.id),
            Ability(name="Flash Form", description="Transform into pure light energy.", key="V", fruit_id=flash.id),
            Ability(name="Flash Movement", description="Move at the speed of light.", key="F", fruit_id=flash.id)
        ])

    if "Flame" not in existing_fruits:
        flame = Fruit(
            name="Flame",
            description="Harness your fierce flames to engulf and overwhelm your adversaries.",
            rarity="Legendary",
            drop_rate=0.14,
            image="flame.png",
            type="Logia"
        )
        db.session.add(flame)
        added_fruits.append("Flame")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Flame Emperor", description="Create a massive explosion of flames.", key="Z", fruit_id=flame.id),
            Ability(name="Flame Pillar", description="Create a towering pillar of flames.", key="X", fruit_id=flame.id),
            Ability(name="Phoenix Mode", description="Transform into a phoenix of flames.", key="C", fruit_id=flame.id),
            Ability(name="Flame Body", description="Transform into living flames.", key="V", fruit_id=flame.id),
            Ability(name="Flame Dash", description="Dash using flame propulsion.", key="F", fruit_id=flame.id)
        ])

    # Add more fruits here...
    
    # Legendary V2 Fruits
    if "Ice V2" not in existing_fruits:
        icev2 = Fruit(
            name="Ice V2",
            description="Unleash the true potential of your inner ice abilities",
            rarity="Legendary",
            drop_rate=0.14,
            image="icev2.png",
            type="Logia"
        )
        db.session.add(icev2)
        added_fruits.append("Ice V2")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Ice Age V2", description="Create an enhanced ice age attack.", key="Z", fruit_id=icev2.id),
            Ability(name="Ice Wolf", description="Summon a wolf made of ice.", key="X", fruit_id=icev2.id),
            Ability(name="Frozen World", description="Freeze everything in a large area.", key="C", fruit_id=icev2.id),
            Ability(name="Ice Awakening", description="Awaken your true ice powers.", key="V", fruit_id=icev2.id),
            Ability(name="Ice Glide V2", description="Enhanced ice movement abilities.", key="F", fruit_id=icev2.id)
        ])

    if "Magma V2" not in existing_fruits:
        magmav2 = Fruit(
            name="Magma V2",
            description="Unleash the true potential of your inner magma abilities",
            rarity="Legendary",
            drop_rate=0.14,
            image="magmav2.png",
            type="Logia"
        )
        db.session.add(magmav2)
        added_fruits.append("Magma V2")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Magma Eruption", description="Create a massive magma eruption.", key="Z", fruit_id=magmav2.id),
            Ability(name="Magma Dragon", description="Summon a dragon made of magma.", key="X", fruit_id=magmav2.id),
            Ability(name="Volcanic Field", description="Turn the battlefield into a volcanic zone.", key="C", fruit_id=magmav2.id),
            Ability(name="Magma Awakening", description="Awaken your true magma powers.", key="V", fruit_id=magmav2.id),
            Ability(name="Magma Surf V2", description="Enhanced magma movement abilities.", key="F", fruit_id=magmav2.id)
        ])

    # Rare Fruits
    if "Ash" not in existing_fruits:
        ash = Fruit(
            name="Ash",
            description="Cloak the battlefield in a cloud of ash, demolishing enemies in its suffocating grasp.",
            rarity="Rare",
            drop_rate=1.04,
            image="ash.png",
            type="Logia"
        )
        db.session.add(ash)
        added_fruits.append("Ash")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Ash Cloud", description="Create a cloud of suffocating ash.", key="Z", fruit_id=ash.id),
            Ability(name="Ash Storm", description="Create a storm of burning ash.", key="X", fruit_id=ash.id),
            Ability(name="Ash Burial", description="Bury enemies in ash.", key="C", fruit_id=ash.id),
            Ability(name="Ash Form", description="Transform into ash.", key="V", fruit_id=ash.id),
            Ability(name="Ash Movement", description="Move using ash propulsion.", key="F", fruit_id=ash.id)
        ])

    # Uncommon Fruits
    if "Chop" not in existing_fruits:
        chop = Fruit(
            name="Chop",
            description="Allows the player to split their body into pieces and control them.",
            rarity="Uncommon",
            drop_rate=8.07,
            image="chop.png",
            type="Paramecia"
        )
        db.session.add(chop)
        added_fruits.append("Chop")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Air Slash", description="Create a flying slash attack.", key="Z", fruit_id=chop.id),
            Ability(name="Cross Chop", description="Create an X-shaped slash attack.", key="X", fruit_id=chop.id),
            Ability(name="Chop Wave", description="Create a wave of slashing energy.", key="C", fruit_id=chop.id),
            Ability(name="Chop Form", description="Enhance your cutting abilities.", key="V", fruit_id=chop.id),
            Ability(name="Quick Slash", description="Dash forward with a quick slash.", key="F", fruit_id=chop.id)
        ])

    # Legendary Fruits
    if "Rubber V2" not in existing_fruits:
        rubberv2 = Fruit(
            name="Rubber V2",
            description="A much more stronger version of the rubber fruit (Post Timeskip).",
            rarity="Legendary",
            drop_rate=0.10,
            image="rubberv2.png",
            type="Paramecia"
        )
        db.session.add(rubberv2)
        added_fruits.append("Rubber V2")
        
        db.session.flush()
        db.session.add_all([
            Ability(name="Red Hawk", description="Powerful fire-enhanced punch.", key="Z", fruit_id=rubberv2.id),
            Ability(name="Elephant Gun", description="Giant hardened punch attack.", key="X", fruit_id=rubberv2.id),
            Ability(name="Kong Gun", description="Powerful bound punch in Gear 4.", key="C", fruit_id=rubberv2.id),
            Ability(name="Gear 4", description="Transform into Gear 4 Boundman.", key="V", fruit_id=rubberv2.id),
            Ability(name="Python", description="Controllable stretching attack.", key="F", fruit_id=rubberv2.id)
        ])
    
    db.session.commit()
    return f"Added the following fruits: {', '.join(added_fruits) if added_fruits else 'None (all already exist)'}"

# Add the Mirror World map to the database
@app.route('/add-mirror-world')
def add_mirror_world():
    # Check if the Mirror World map already exists
    existing_maps = [map.name for map in Map.query.all()]
    message = []
    
    if "Mirror World" not in existing_maps:
        # Add Mirror World to the database
        mirror_world = Map(
            name="Mirror World",
            description="A distorted, mirror-like environment accessed through a portal in Whole Cake Island. Home to Katakuri who drops Dough or DoughV2 fruits.",
            level_requirement=100,  # Updated level requirement
            exp_multiplier=1.75,  # Updated exp multiplier
            image="map_mirror_world.jpg"
        )
        db.session.add(mirror_world)
        db.session.commit()
        message.append("✅ Mirror World map added successfully to the database!")
    else:
        message.append("⚠️ Mirror World map already exists in the database.")
    
    # Provide information about adding the image
    map_image_path = os.path.join(app.static_folder, 'images', 'maps', 'map_mirror_world.jpg')
    if not os.path.exists(map_image_path):
        message.append("⚠️ Important: You need to add an image file at: static/images/maps/map_mirror_world.jpg")
    else:
        message.append("✅ Mirror World map image is already present.")
        
    # Return HTML response with instructions
    response = f"""
    <html>
    <head>
        <title>Add Mirror World Map</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #0075ff; }}
            .message {{ margin-bottom: 10px; }}
            .instructions {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }}
            .instructions h2 {{ margin-top: 0; }}
            .code {{ background-color: #f1f1f1; padding: 10px; border-radius: 3px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <h1>Mirror World Map Status</h1>
        
        <div class="messages">
            {"<br>".join(message)}
        </div>
        
        <div class="instructions">
            <h2>Next Steps</h2>
            <p>To fully implement Mirror World, make sure to:</p>
            <ol>
                <li>Add an image file at: <code>static/images/maps/map_mirror_world.jpg</code></li>
                <li>Refresh the Maps page to see the new Mirror World entry</li>
                <li>Consider adding a Katakuri boss entry if not already present</li>
            </ol>
        </div>
        
        <p><a href="/maps">Go to Maps Page</a></p>
    </body>
    </html>
    """
    return response

# Add the Tournament map to the database
@app.route('/add-tournament')
def add_tournament():
    # Check if the Tournament map already exists
    existing_maps = [map.name for map in Map.query.all()]
    message = []
    
    if "Tournament" not in existing_maps:
        # Add Tournament to the database
        tournament = Map(
            name="Tournament",
            description="A special PvP arena accessed through Gatz at the Corrida Colosseum in Dressrosa. Players compete in 1v1 brackets for rewards.",
            level_requirement=0,  # No level requirement
            exp_multiplier=1.0,   # Standard exp multiplier
            image="map_tournament.jpg"
        )
        db.session.add(tournament)
        db.session.commit()
        message.append("✅ Tournament map added successfully to the database!")
    else:
        message.append("⚠️ Tournament map already exists in the database.")
    
    # Provide information about adding the image
    map_image_path = os.path.join(app.static_folder, 'images', 'maps', 'map_tournament.jpg')
    if not os.path.exists(map_image_path):
        message.append("⚠️ Important: You need to add an image file at: static/images/maps/map_tournament.jpg")
    else:
        message.append("✅ Tournament map image is already present.")
        
    # Return HTML response with instructions
    response = f"""
    <html>
    <head>
        <title>Add Tournament Map</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #0075ff; }}
            .message {{ margin-bottom: 10px; }}
            .instructions {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }}
            .instructions h2 {{ margin-top: 0; }}
            .code {{ background-color: #f1f1f1; padding: 10px; border-radius: 3px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <h1>Tournament Map Status</h1>
        
        <div class="messages">
            {"<br>".join(message)}
        </div>
        
        <div class="instructions">
            <h2>Next Steps</h2>
            <p>To fully implement Tournament, make sure to:</p>
            <ol>
                <li>Add an image file at: <code>static/images/maps/map_tournament.jpg</code></li>
                <li>Refresh the Maps page to see the new Tournament entry</li>
            </ol>
        </div>
        
        <p><a href="/maps">Go to Maps Page</a></p>
    </body>
    </html>
    """
    return response

if __name__ == '__main__':
    app.run(debug=True) 