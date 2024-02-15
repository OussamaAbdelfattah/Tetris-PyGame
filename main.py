import pygame
import random

# Dimensions de la fenêtre du jeu
largeur_fenetre = 800
hauteur_fenetre = 600

# Dimensions de la grille du jeu
largeur_grille = 50
hauteur_grille = 20
taille_case = 30

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
COULEURS_PIECES = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 255), (128, 0, 128)]

# Initialisation de Pygame
pygame.init()
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
clock = pygame.time.Clock()
pygame.display.set_caption('Tetris')

# Classe pour les pièces du jeu
class Piece:
    def __init__(self, x, y, forme):
        self.x = x
        self.y = y
        self.forme = forme

    def deplacer(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotationner(self):
        self.forme = list(zip(*reversed(self.forme)))

    def dessiner(self):
        for i in range(len(self.forme)):
            for j in range(len(self.forme[i])):
                if self.forme[i][j]:
                    pygame.draw.rect(fenetre, COULEURS_PIECES[self.forme[i][j]], (self.x * taille_case + j * taille_case, self.y * taille_case + i * taille_case, taille_case, taille_case))

# Fonction pour générer une nouvelle pièce aléatoire
def generer_piece():
    formes_pieces = [
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]],
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1, 1], [0, 0, 1]]
    ]
    forme = random.choice(formes_pieces)
    x = (largeur_grille - len(forme[0])) // 2
    y = 0
    return Piece(x, y, forme)

# Fonction pour vérifier si une pièce est en collision avec la grille
def collision(grille, piece):
    for i in range(len(piece.forme)):
        for j in range(len(piece.forme[i])):
            if piece.forme[i][j] and (piece.x + j < 0 or piece.x + j >= largeur_grille or piece.y + i >= hauteur_grille or grille[piece.y + i][piece.x + j]):
                return True
    return False

def afficher_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, NOIR)
    fenetre.blit(text, (largeur_fenetre // 2 - text.get_width() // 2, hauteur_fenetre // 2 - text.get_height() // 2))
    pygame.display.flip()

# Fonction pour vérifier et supprimer les lignes complètes de la grille
def supprimer_lignes(grille):
    lignes_completees = []
    for i in range(hauteur_grille):
        if all(grille[i]):
            lignes_completees.append(i)
    for ligne in lignes_completees:
        del grille[ligne]
        grille.insert(0, [0] * largeur_grille)

# Initialisation de la grille du jeu
grille = [[0] * largeur_grille for _ in range(hauteur_grille)]

# Variables de jeu
piece_en_cours = generer_piece()
jeu_termine = False
timer = 0
vitesse_chute = 1000  # Temps en millisecondes entre chaque chute automatique de la pièce

# Boucle principale du jeu
while not jeu_termine:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu_termine = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                piece_en_cours.deplacer(-1, 0)
                if collision(grille, piece_en_cours):
                    piece_en_cours.deplacer(1, 0)
            elif event.key == pygame.K_RIGHT:
                piece_en_cours.deplacer(1, 0)
                if collision(grille, piece_en_cours):
                    piece_en_cours.deplacer(-1, 0)
            elif event.key == pygame.K_DOWN:
                piece_en_cours.deplacer(0, 1)
                if collision(grille, piece_en_cours):
                    piece_en_cours.deplacer(0, -1)
            elif event.key == pygame.K_UP:
                piece_en_cours.rotationner()
                if collision(grille, piece_en_cours):
                    piece_en_cours.rotationner()

    timer += clock.get_rawtime()
    clock.tick()
    if timer >= vitesse_chute:
        piece_en_cours.deplacer(0, 1)
        if collision(grille, piece_en_cours):
            piece_en_cours.deplacer(0, -1)
            for i in range(len(piece_en_cours.forme)):
                for j in range(len(piece_en_cours.forme[i])):
                    if piece_en_cours.forme[i][j]:
                        grille[piece_en_cours.y + i][piece_en_cours.x + j] = 1
            supprimer_lignes(grille)
            piece_en_cours = generer_piece()
            if collision(grille, piece_en_cours):
                jeu_termine = True
        timer = 0
        if jeu_termine:
            afficher_message("Vous avez perdu. Appuyez sur une touche pour quitter.")
            pygame.time.wait(2000)  # Attendre 2 secondes avant de quitter
            pygame.event.wait()  # Attendre un événement (par exemple, une touche pressée) pour quitter
            jeu_termine = True

    # Effacer l'écran
    fenetre.fill(BLANC)

    # Dessiner la grille
    for i in range(hauteur_grille):
        for j in range(largeur_grille):
            if grille[i][j]:
                pygame.draw.rect(fenetre, COULEURS_PIECES[grille[i][j]], (j * taille_case, i * taille_case, taille_case, taille_case))

    # Dessiner la pièce en cours
    piece_en_cours.dessiner()

    # Mettre à jour l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
