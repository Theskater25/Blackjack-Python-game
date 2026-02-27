import pgzrun
import random

# Configuration de la fenêtre
WIDTH = 1200
HEIGHT = 800
TITLE = "Blackjack 21"

# Variables du jeu
deck = []
player_hand = []
dealer_hand = []
player_score = 0
dealer_score = 0
game_over = False
dealer_turn = False
message = ""
dealer_hidden = True

# Positions des cartes
DEALER_START_X = WIDTH // 2 - 150
DEALER_START_Y = 150
PLAYER_START_X = WIDTH // 2 - 150
PLAYER_START_Y = HEIGHT - 300
CARD_SPACING = 120

def create_deck():
    """Crée un jeu de 52 cartes"""
    global deck
    deck = []
    suits = ['heart', 'diamond', 'club', 'spade']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    for suit in suits:
        for rank in ranks:
            # Nom du fichier de la carte
            filename = f"{rank}_of_{suit}.png"

            # Valeur de la carte
            if rank in ['jack', 'queen', 'king']:
                value = 10
            elif rank == 'ace':
                value = 11  # On commence avec 11, on ajustera si nécessaire
            else:
                value = int(rank)

            deck.append({
                'filename': filename,
                'value': value,
                'rank': rank,
                'suit': suit
            })

    random.shuffle(deck)

def calculate_score(hand):
    """Calcule le score d'une main en gérant les As"""
    score = sum(card['value'] for card in hand)
    aces = sum(1 for card in hand if card['rank'] == 'ace')

    # Ajuster la valeur des As si nécessaire
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1

    return score

def deal_card(hand):
    """Distribue une carte à une main"""
    if deck:
        card = deck.pop()
        hand.append(card)
        return card
    return None

def start_new_game():
    """Initialise une nouvelle partie"""
    global player_hand, dealer_hand, player_score, dealer_score
    global game_over, dealer_turn, message, dealer_hidden

    # Réinitialiser les variables
    player_hand = []
    dealer_hand = []
    game_over = False
    dealer_turn = False
    message = ""
    dealer_hidden = True

    # Créer et mélanger le deck
    create_deck()

    # Distribuer les cartes initiales
    for _ in range(2):
        deal_card(player_hand)
        deal_card(dealer_hand)

    # Calculer les scores initiaux
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    # Vérifier le blackjack initial
    if player_score == 21:
        dealer_hidden = False
        if dealer_score == 21:
            message = "ÉGALITÉ - Deux Blackjacks!"
        else:
            message = "BLACKJACK! Vous avez gagné!"
        game_over = True

def player_hit():
    """Le joueur tire une carte"""
    global player_score, game_over, message, dealer_hidden

    if not game_over and not dealer_turn:
        deal_card(player_hand)
        player_score = calculate_score(player_hand)

        if player_score > 21:
            game_over = True
            dealer_hidden = False
            message = "BUST! Vous avez perdu!"

def player_stand():
    """Le joueur s'arrête et c'est au tour du croupier"""
    global dealer_turn, dealer_score, game_over, message, dealer_hidden

    if not game_over and not dealer_turn:
        dealer_turn = True
        dealer_hidden = False

        # Le croupier joue
        while dealer_score < 17:
            deal_card(dealer_hand)
            dealer_score = calculate_score(dealer_hand)

        # Déterminer le gagnant
        if dealer_score > 21:
            message = "Le croupier a dépassé 21! Vous avez gagné!"
        elif dealer_score > player_score:
            message = "Le croupier gagne!"
        elif player_score > dealer_score:
            message = "Vous avez gagné!"
        else:
            message = "Égalité!"

        game_over = True

def draw():
    """Dessine tous les éléments du jeu"""
    # Dessiner le fond (table de jeu)
    try:
        screen.blit('tabledejeu', (0, 0))
    except:
        # Si l'image n'est pas trouvée, utiliser un fond vert
        screen.fill((0, 100, 0))

    # Titre
    screen.draw.text("BLACKJACK 21",
                     center=(WIDTH // 2, 50),
                     fontsize=60,
                     color="gold",
                     shadow=(2, 2),
                     scolor="black")

    # Dessiner les cartes du croupier
    screen.draw.text("Croupier",
                     (DEALER_START_X, DEALER_START_Y - 40),
                     fontsize=30,
                     color="white")

    for i, card in enumerate(dealer_hand):
        x = DEALER_START_X + (i * CARD_SPACING)
        y = DEALER_START_Y

        if i == 1 and dealer_hidden:
            # Cacher la deuxième carte du croupier
            try:
                screen.blit('verso', (x, y))
            except:
                # Si l'image n'existe pas, dessiner un rectangle
                screen.draw.filled_rect(Rect((x, y), (100, 140)), "darkblue")
                screen.draw.text("?", center=(x + 50, y + 70), fontsize=40, color="white")
        else:
            # Afficher la carte
            try:
                screen.blit(card['filename'].replace('.png', ''), (x, y))
            except:
                # Si l'image n'existe pas, afficher une carte simple
                screen.draw.filled_rect(Rect((x, y), (100, 140)), "white")
                screen.draw.rect(Rect((x, y), (100, 140)), "black")
                screen.draw.text(f"{card['rank'][:1].upper()}",
                                center=(x + 50, y + 50),
                                fontsize=30,
                                color="black")
                screen.draw.text(f"{card['suit'][:1].upper()}",
                                center=(x + 50, y + 90),
                                fontsize=20,
                                color="red" if card['suit'] in ['heart', 'diamond'] else "black")

    # Afficher le score du croupier
    if not dealer_hidden:
        screen.draw.text(f"Score: {dealer_score}",
                        (DEALER_START_X, DEALER_START_Y + 160),
                        fontsize=25,
                        color="yellow")

    # Dessiner les cartes du joueur
    screen.draw.text("Joueur",
                     (PLAYER_START_X, PLAYER_START_Y - 40),
                     fontsize=30,
                     color="white")

    for i, card in enumerate(player_hand):
        x = PLAYER_START_X + (i * CARD_SPACING)
        y = PLAYER_START_Y

        try:
            screen.blit(card['filename'].replace('.png', ''), (x, y))
        except:
            # Si l'image n'existe pas, afficher une carte simple
            screen.draw.filled_rect(Rect((x, y), (100, 140)), "white")
            screen.draw.rect(Rect((x, y), (100, 140)), "black")
            screen.draw.text(f"{card['rank'][:1].upper()}",
                            center=(x + 50, y + 50),
                            fontsize=30,
                            color="black")
            screen.draw.text(f"{card['suit'][:1].upper()}",
                            center=(x + 50, y + 90),
                            fontsize=20,
                            color="red" if card['suit'] in ['heart', 'diamond'] else "black")

    # Afficher le score du joueur
    screen.draw.text(f"Score: {player_score}",
                    (PLAYER_START_X, PLAYER_START_Y + 160),
                    fontsize=25,
                    color="yellow")

    # Afficher les contrôles
    if not game_over:
        controls_y = HEIGHT - 80
        screen.draw.text("[ESPACE] Tirer une carte    [ENTRÉE] Rester",
                        center=(WIDTH // 2, controls_y),
                        fontsize=24,
                        color="white",
                        background="black")
    else:
        screen.draw.text("[R] Nouvelle partie",
                        center=(WIDTH // 2, HEIGHT - 80),
                        fontsize=24,
                        color="white",
                        background="black")

    # Afficher le message de fin de partie
    if message:
        # Fond semi-transparent pour le message
        msg_rect = Rect((WIDTH // 2 - 300, HEIGHT // 2 - 60), (600, 120))
        screen.draw.filled_rect(msg_rect, (0, 0, 0, 200))
        screen.draw.rect(msg_rect, "gold")

        # Message
        screen.draw.text(message,
                        center=(WIDTH // 2, HEIGHT // 2),
                        fontsize=40,
                        color="gold")

def on_key_down(key):
    """Gestion des touches du clavier"""
    global game_over

    if key == keys.SPACE:
        player_hit()
    elif key == keys.RETURN:
        player_stand()
    elif key == keys.R:
        start_new_game()

# Initialiser le jeu au démarrage
start_new_game()

# Lancer Pygame Zero
pgzrun.go()
