import os
import sys

# Add the current directory to the path so app can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from app import db, Fruit, Ability
    print("Successfully imported database models from app")
except ImportError as e:
    print(f"Import error: {e}")
    print("Current directory:", os.getcwd())
    print("Python path:", sys.path)
    sys.exit(1)

# Check if database exists
db_path = os.path.join(current_dir, 'fruit_battlegrounds.db')
if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}. Creating tables...")
    try:
        db.create_all()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        sys.exit(1)

try:
    # Check if these fruits already exist to avoid duplicates
    existing_fruits = [fruit.name for fruit in Fruit.query.all()]
    added_fruits = []

    print(f"Existing fruits: {existing_fruits}")

    # LeopardV2 (Update 20 - March 2025)
    if "LeopardV2" not in existing_fruits:
        leopardv2 = Fruit(
            name="LeopardV2",
            description="The upgraded version of Leopard fruit with enhanced abilities. Transform into a powerful leopard-human hybrid with devastating attacks, afterimage techniques, and superior agility.",
            rarity="Mythical",
            drop_rate=0.01,
            image="leopardv2.png"
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
            image="dragonv2.png"
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
            image="doughv2.png"
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
            image="opeope.png"
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

    # Soul (Update 15 - February 2024)
    if "Soul" not in existing_fruits:
        soul = Fruit(
            name="Soul",
            description="Allows the user to manipulate souls, stealing life force from others.",
            rarity="Mythical",
            drop_rate=0.025,
            image="soul.png"
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
            image="nika.png"
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
    print(f"Added the following mythical fruits: {', '.join(added_fruits) if added_fruits else 'None (all already exist)'}")
    print(f"Final list of fruits: {[fruit.name for fruit in Fruit.query.all()]}")

except Exception as e:
    print(f"Error executing database operations: {e}")
    db.session.rollback()
    sys.exit(1) 