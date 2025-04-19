from app import app, db, Fruit

# Need to use app context when working with Flask-SQLAlchemy
with app.app_context():
    # Find Dough and change to Legendary
    dough = Fruit.query.filter_by(name="Dough").first()
    if dough:
        dough.rarity = "Legendary"
        dough.drop_rate = 0.1
        print(f"Updated Dough to Legendary rarity")
    else:
        print("Dough fruit not found")
    
    # Find Leopard and change to Legendary
    leopard = Fruit.query.filter_by(name="Leopard").first()
    if leopard:
        leopard.rarity = "Legendary"
        leopard.drop_rate = 0.1
        print(f"Updated Leopard to Legendary rarity")
    else:
        print("Leopard fruit not found")
    
    # Commit changes
    db.session.commit()
    print("Database updated successfully") 