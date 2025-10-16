import json

# Fonction pour charger
def load_products():
    try:
        with open('stock.json', 'r') as f:
            return json.load(f)
    except:
        return []

# Fonction pour sauvegarder
def save_products():
    with open('stock.json', 'w') as f:
        json.dump(products, f, indent=2)

# Charger au démarrage
products = load_products()

def add_product():
    try:
        name = input("Veuillez entrée le nom de l'article: ")
        price = int(input(f"Veuillez rentrée le prix de {name}: "))
        quantity = int(input(f"Veuillez entrée la quantité a enregistré de {name}: "))
        products.append({
            "id": generate_new_id(),
            "nom": name,
            "prix": price,
            "quantite": quantity
        })
        print(f"✓ Produit {name} ajouté avec succès!")
        save_products()
        print("\nListe mise à jour:")
        show_all_product()  # Affiche directement après l'ajout
    except ValueError:
        print("Vous avez une erreur")
    return products

def delete_product():
    show_all_product()
    user_input = int(input("Quel l'objet que vous voulez supprimer"))
    for element in products:
        if element["id"] == user_input:
            confirmation_input = int(input("""
                                           Etes-vous sur ?\n
                                           1. Oui
                                           2. Non
                                           """))
            match confirmation_input: 
                case 1:
                    products.remove(element)
                    save_products()
                    print("✓ Produit supprimé!")
                    return
                case 2:
                    break
    print("❌ ID introuvable!")

def show_all_product():
        if len(products) == 0:
            print("Aucun produit en stock")
        print("\n--- Liste des produits ---")
        for value in products:
            print(f"ID: {value['id']} | Nom: {value['nom']} | Prix: {value['prix']}€ | Quantité: {value['quantite']}")
        print("-" * 50)

def generate_new_id():
    if len(products) == 0:
        return 0
    else :
        number_list = []
        for element in products:
            number_list.append(element['id'])
        max_id = max(number_list) 
        return max_id+1
    
while True:
    input_user = int(input("""Veuillez saisir le nombre liée a votre action\n
1. Ajouter un nouveaux produit\n
2. Supprimer un produit\n
3. Montrer tout les produits\n
4. Quitter l'application
    """))

    match input_user:
        case  1:
            print("Vous avez selectionner : add_product")
            add_product()
        case 2:
            print("Vous avez selectionner : delete_product")
            delete_product()
        case 3:
            print("vous avez selectionner : show_all_product")
            show_all_product()
        case 4:
            print("Au revoir!")
            break
        case _ :
            print("Choix invalide")