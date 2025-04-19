from app import app, db, Fruit

with app.app_context():
    # Try to find Leopard
    leopard = Fruit.query.filter_by(name="Leopard").first()
    
    if leopard:
        print(f"Leopard details:")
        print(f"  - ID: {leopard.id}")
        print(f"  - Rarity: {leopard.rarity}")
        print(f"  - Drop Rate: {leopard.drop_rate}%")
        print(f"  - Description: {leopard.description[:50]}...")
        print(f"  - Abilities:")
        for ability in leopard.abilities:
            print(f"    - {ability.name} ({ability.key}): {ability.description[:30]}...")
    else:
        print("Leopard fruit not found in the database")
    
    # Try to find Dough
    dough = Fruit.query.filter_by(name="Dough").first()
    
    if dough:
        print(f"\nDough details:")
        print(f"  - ID: {dough.id}")
        print(f"  - Rarity: {dough.rarity}")
        print(f"  - Drop Rate: {dough.drop_rate}%")
        print(f"  - Description: {dough.description[:50]}...")
        print(f"  - Abilities:")
        for ability in dough.abilities:
            print(f"    - {ability.name} ({ability.key}): {ability.description[:30]}...")
    else:
        print("\nDough fruit not found in the database") 