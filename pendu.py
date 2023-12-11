import pygame
import pygame_menu
import random
pygame.init()
# Initialisation de la fenêtre de jeu
winHeight = 480
winWidth = 700
win=pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("Jeu du Pendu")
# Définition des couleurs utilisées dans le jeu
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)
# Définition des polices utilisées
btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
# Initialisation des variables globales
difficulty = 1 
mot = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('images/hangman0.png'), pygame.image.load('images/hangman1.png'), pygame.image.load('images/hangman2.png'), pygame.image.load('images/hangman3.png'), pygame.image.load('images/hangman4.png'), pygame.image.load('images/hangman5.png'), pygame.image.load('images/hangman6.png'), pygame.image.load('images/hangman7.png'), pygame.image.load('images/hangman8.png'), pygame.image.load('images/hangman9.png'), pygame.image.load('images/hangman10.png')]
limbs = 0
player_name = ''
def sauvegarder_score(nom_joueur, score):
    with open('scores.txt', 'a') as file:
        file.write(f'{nom_joueur}: {score}\n')
# Fonction pour afficher les scores        
def afficher_scores():
    win.fill(WHITE)
    scores = []
    with open('scores.txt', 'r') as file:
        scores = file.readlines()
    if scores:
        y_offset = 50
        for score in scores:
            score_text = guess_font.render(score.strip(), True, BLACK)
            win.blit(score_text, (winWidth / 2 - score_text.get_width() / 2, y_offset))
            y_offset += 30
    else:
        no_scores_text = guess_font.render('Aucun score enregistré pour le moment.', True, BLACK)
        win.blit(no_scores_text, (winWidth / 2 - no_scores_text.get_width() / 2, winHeight / 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()        
# Fonction pour choisir aléatoirement un mot dans un fichier texte
def randomWord():
    file = open('mots.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)
    return f[i][:-1]
# La fonction redraw_game_window() met à jour l'affichage du jeu à chaque itération
def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(WHITE)
    # Affichage des boutons pour les lettres    
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))
# Affichage des lettres devinées et non devinées dans le mot à deviner
    spaced = spacedOut(mot, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    win.blit(label1,(winWidth/2 - length/2, 400))
# Affichage de l'image du pendu correspondant au nombre d'erreurs
    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()
# Fonction pour vérifier si la lettre devinée ne fait pas partie du mot
def hang(guess):
    global mot
    if guess.lower() not in mot.lower():
        return True
    else:
        return False
# Fonction pour afficher les lettres devinées et non devinées dans le mot à deviner
def spacedOut(mot, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(mot)):
        if mot[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if mot[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += mot[x].upper() + ' '
        elif mot[x] == ' ':
            spacedWord += ' '
    return spacedWord
# Fonction pour vérifier si un bouton a été cliqué
def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None
# Fonction pour afficher l'écran de fin de partie (gagnée ou perdue)
def end(winner=False):
    global limbs, guessed, mot
    lostTxt = 'PERDU!,tapez pour rejouer'
    winTxt = 'GAGNER!,tapez pour rejouer'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(GREEN)
    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)
    wordTxt = lost_font.render(mot.upper(), 1, BLACK)
    wordWas = lost_font.render('Le mot était: ', 1, BLACK)
    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    pygame.time.wait(1000)
    score = 100 - (limbs * 10)  # Vous pouvez ajuster la logique de calcul du score
    player_name = getattr(menu, 'player_name', '')  # Récupère le nom stocké dans la classe menu
    if player_name:
        sauvegarder_score(player_name, score)
    else:
        sauvegarder_score('', score)    

    pygame.time.wait(3000)  # Attendre un peu pour afficher le score
    menu.mainloop(win)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                reset()
                menu.mainloop(win) 
# Fonction pour réinitialiser le jeu
def reset():
    global limbs
    global guessed
    global buttons
    global mot
    for i in range(len(buttons)):
        buttons[i][4] = True
    limbs = 0
    guessed = []
    mot = randomWord()
# Création des boutons pour les lettres de l'alphabet
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
# Sélection aléatoire du mot à deviner
mot = randomWord()
inPlay = True    
def get_word_by_difficulty(difficulty):
    file = open('mots.txt')
    f = file.readlines()
    words = [word.strip() for word in f]
    if difficulty == 1:  # Niveau Facile
        filtered_words = [word for word in words if len(word) <= 4]
    elif difficulty == 2:  # Niveau Moyen
        filtered_words = [word for word in words if 5 <= len(word) <= 8]
    else:  # Niveau Difficile
        filtered_words = [word for word in words if len(word) >= 9]
    if filtered_words:
        return random.choice(filtered_words)
    else:
        return random.choice(words)
# Fonction pour définir la difficulté du jeu    
def set_difficulty(value, difficulty_selector):
    global difficulty
    difficulty = difficulty_selector
    mot = get_word_by_difficulty(difficulty)      
# Fonction pour démarrer le jeu
def demarrer_jeu():
    global buttons, guessed, limbs, mot, player_name
    guessed = []
    limbs = 0
    for i in range(len(buttons)):
        buttons[i][4] = True
    mot = get_word_by_difficulty(difficulty)  # Utiliser le mot correspondant à la difficulté choisie
    player_name = getattr(menu, 'player_name', '')
# Boucle principale du jeu    
    while True:
        redraw_game_window()
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key).upper()
                    if letter not in guessed:
                        guessed.append(letter)
                        for button in buttons:
                            if button[5] == ord(letter):
                                button[4] = False
                        if hang(letter):
                            if limbs != 9:
                                limbs += 1
                            else:
                                end()
                        else:
                            print(spacedOut(mot, guessed))
                            if spacedOut(mot, guessed).count('_') == 0:
                                end(True)
        if len(guessed) == 26:
            end(True)  # Si toutes les lettres sont devinées, le joueur a gagné
# Fonction pour ajouter un nouveau mot dans le fichier texte
def ajouter_mot():
    nouveau_mot = ""
    ajout_termine = False
    while not ajout_termine:
        win.fill(WHITE)  # Efface l'écran à chaque itération
        affichage_texte = btn_font.render("Ajouter un nouveau mot :", True, RED)
        win.blit(affichage_texte, (winWidth // 2 - affichage_texte.get_width() // 2, winHeight // 2 - 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ajout_termine = True
                elif event.key == pygame.K_BACKSPACE:
                    nouveau_mot = nouveau_mot[:-1]
                elif event.unicode.isalpha():
                    nouveau_mot += event.unicode
        affichage_nouveau_mot = btn_font.render(nouveau_mot, True, RED)
        text_width, text_height = btn_font.size(nouveau_mot)
        win.blit(affichage_nouveau_mot, (winWidth // 2 - text_width // 2, winHeight // 2 + 50))
        pygame.display.flip()
    with open("mots.txt", 'a') as fichier:
        fichier.write(nouveau_mot + "\n")
    print("Mot ajouté avec succès !")   
# Création du menu principal du jeu                         
menu = pygame_menu.Menu('JEU DU PENDU', 700, 480,
                       theme=pygame_menu.themes.THEME_ORANGE)
menu.add.text_input('Nom :', default='', onchange=lambda name: setattr(menu, 'player_name', name))
menu.add.selector('Difficulté: :', [('',0),('Facile', 1),('Moyen', 2), ('Difficile', 3)], onchange=set_difficulty)
menu.add.button('Jouer', demarrer_jeu)
menu.add.button('Insérer un mot ',ajouter_mot)
menu.add.button('Afficher les scores', afficher_scores)
menu.add.button('Quitter', pygame_menu.events.EXIT)
menu.mainloop(win)
pygame.quit()