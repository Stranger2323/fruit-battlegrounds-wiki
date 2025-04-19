from app import app, db, Fruit, Ability

with app.app_context():
    # Check if Dough exists
    dough = Fruit.query.filter_by(name="Dough").first()
    
    # If Dough doesn't exist, create it
    if not dough:
        print("Dough fruit not found. Creating it as Legendary...")
        dough = Fruit(
            name="Dough",
            description="Allows the user to create and control mochi, a sticky substance. Was downgraded to Legendary rarity when DoughV2 was introduced in Update 19.",
            rarity="Legendary",
            drop_rate=0.1,
            image="dough.png"
        )
        db.session.add(dough)
        db.session.flush()  # Generate ID
        
        # Add abilities
        db.session.add_all([
            Ability(name="Dough Ball", description="Create and throw a ball of dough that explodes on impact.", key="Z", fruit_id=dough.id),
            Ability(name="Mochi Mochi", description="Create a wave of sticky dough to trap opponents.", key="X", fruit_id=dough.id),
            Ability(name="Dough Thrust", description="Extend your arm as dough to grab and pull enemies.", key="C", fruit_id=dough.id),
            Ability(name="Mochi Barrage", description="Unleash a barrage of dough punches.", key="V", fruit_id=dough.id),
            Ability(name="Dough Mobility", description="Use dough to increase mobility and jump height.", key="F", fruit_id=dough.id),
        ])
        db.session.commit()
        print("Dough fruit added successfully!")
    else:
        print(f"Dough fruit already exists with rarity: {dough.rarity}")
        
        # If it exists but not as Legendary, update it
        if dough.rarity != "Legendary":
            dough.rarity = "Legendary"
            dough.drop_rate = 0.1
            db.session.commit()
            print("Updated Dough to Legendary rarity")
    
    # Check if Smoke exists
    smoke = Fruit.query.filter_by(name="Smoke").first()
    
    # If Smoke doesn't exist, create it
    if not smoke:
        print("Smoke fruit not found. Creating it as Uncommon...")
        smoke = Fruit(
            name="Smoke",
            description="Allows the user to split their body into pieces and control them. A Logia-type fruit based on the Moku-Moku no Mi from One Piece.",
            rarity="Uncommon",
            drop_rate=5.95,
            image="smoke.png"
        )
        db.session.add(smoke)
        db.session.flush()  # Generate ID
        
        # Add abilities based on Fruit Battlegrounds wiki
        db.session.add_all([
            Ability(name="White Blow", description="User fires a smoke blast in the direction of the cursor. Has low range, similar to Quake's first move.", key="Z", fruit_id=smoke.id),
            Ability(name="White Out", description="User throws a column of smoke which drags opponents away and up into the air.", key="X", fruit_id=smoke.id),
            Ability(name="Typhoon", description="User jumps into the air and spins forward while barraging the opponent with a series of smoke-imbued attacks. Can be held to increase the time attacking.", key="C", fruit_id=smoke.id),
            Ability(name="Firework", description="User crouches down, covering their arms in smoke before shooting high into the air, dragging opponents close by with them. The user then creates a huge smoke explosion, blasting everyone caught in the attack away.", key="V", fruit_id=smoke.id),
            Ability(name="Smoke Dash", description="Transform into smoke to travel quickly across the battlefield.", key="F", fruit_id=smoke.id),
        ])
        db.session.commit()
        print("Smoke fruit added successfully!")
    else:
        print(f"Smoke fruit already exists with rarity: {smoke.rarity}")
    
    # Check if Ash exists
    ash = Fruit.query.filter_by(name="Ash").first()
    
    # If Ash doesn't exist, create it
    if not ash:
        print("Ash fruit not found. Creating it as Rare...")
        ash = Fruit(
            name="Ash",
            description="Cloak the battlefield in a cloud of ash, demolishing enemies in its suffocating grasp. A Logia-type fruit added in Update 17.",
            rarity="Rare",
            drop_rate=1.04,
            image="ash.png"
        )
        db.session.add(ash)
        db.session.flush()  # Generate ID
        
        # Add abilities
        db.session.add_all([
            Ability(name="Ash Cloud", description="Create a cloud of ash that damages enemies within its area.", key="Z", fruit_id=ash.id),
            Ability(name="Ash Pillar", description="Send forth a pillar of ash to damage and knock back opponents.", key="X", fruit_id=ash.id),
            Ability(name="Ash Eruption", description="Cause an eruption of ash beneath enemies, launching them into the air.", key="C", fruit_id=ash.id),
            Ability(name="Volcanic Devastation", description="Create a massive explosion of ash that engulfs a wide area, dealing significant damage to all caught within.", key="V", fruit_id=ash.id),
            Ability(name="Ash Glide", description="Transform into ash to glide through the air, allowing for increased mobility.", key="F", fruit_id=ash.id),
        ])
        db.session.commit()
        print("Ash fruit added successfully!")
    else:
        print(f"Ash fruit already exists with rarity: {ash.rarity}")
    
    # List all fruits and their rarities
    print("\nCurrent fruits in database:")
    for fruit in Fruit.query.all():
        print(f"{fruit.name}: {fruit.rarity} (Drop rate: {fruit.drop_rate}%)") 