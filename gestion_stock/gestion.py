from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import mysql.connector
# Créaction graphique
fenetre = Tk()
fenetre.title("Gestion de stock")
# Couleur du plan arrière
fenetre.configure(bg='cyan')
fenetre.geometry("500x500")
# Établir une connexion avec la base de données
connexion = mysql.connector.connect(host="localhost", user="root", 
    password="voltigeur21", database="boutique")
# Créer un curseur
curseur = connexion.cursor()
# Exécuter une requête SELECT pour récupérer les données de la table produits
curseur.execute("SELECT * FROM produit")
# Récupérer les résultats
resultats = curseur.fetchall()
# Zone de texte de bienvenue
haut = Label (fenetre,text = "PRODUITS")
haut.place(x=20,y=70)
zone_texte = Label (fenetre,text = 
    "Un tableau de bord de la gestion de voltigames")
zone_texte.config(state = DISABLED)
zone_texte.place(x=120,y=40)
# Créaction du mot nom
nom = Label(fenetre,text="Nom")
nom.place(x=40, y=100)
# Champs pour mettre l'écriture
entre_nom = Entry(fenetre,bd=8)
entre_nom.place(x=80,y=100)
# Créaction de la description a choisir
objet =["Bureautique","Appareil électronique",
    "Figurine","Carte cadeau","Jeux vidéos"]
# Créaction de description
description = Label(fenetre,text="Description")
description.place(x=250, y=100)
# Champs pour mettre la description
entre_description = ttk.Combobox(fenetre,values=objet)
entre_description.place(x=320, y=100)
# Créaction du mot prix
prix = Label(fenetre,text="Prix")
prix.place(x=40, y=150)
#  Champs pour mettre le prix
entre_prix = Entry(fenetre,bd=8)
entre_prix.place(x=80, y=150)
# Créaction du mot quantité
quantite = Label(fenetre, text="Quantité")
quantite.place(x=250, y=150)
# Créaction de la quantité a choisir
nombre =["1","2","3","4","5","6","7","8","9","10",
         "11","12","13","14","15","16",
         "17","18","19","20"] 
# Champs pour mettre quantité
entre_quantite = ttk.Combobox(fenetre,values=nombre)
entre_quantite.place(x=320, y=150)
# Créaction du mot id_catégorie
categorie = Label(fenetre,text="id_catégorie")
categorie.place(x=150, y=200)
# Champs pour mettre id_catégorie
entre_categorie = Entry(fenetre,bd=8)
entre_categorie.insert(0, "A mettre des chiffres")
entre_categorie.place(x=230, y=200)
# Créer le Treeview
tableau = ttk.Treeview(fenetre, columns=(0, 1, 2, 3, 4,5), show="headings")
tableau.place(x=50, y=290, width=400, height=200)
# Ajouter les en-têtes de colonne
tableau.heading(0, text="ID")
tableau.heading(1, text="Nom")
tableau.heading(2, text="Description")
tableau.heading(3, text="Prix")
tableau.heading(4, text="Quantité")
tableau.heading(5, text="Id_catégorie")
# redimensionner le tableau des colonnes
tableau.column(0,width=10)
tableau.column(1,width=10)
tableau.column(2,width=10)
tableau.column(3,width=10)
tableau.column(4,width=10)
tableau.column(5,width=10)
# Parcourir les résultats et ajouter chaque ligne au Treeview
for row in resultats:
    tableau.insert("", END,iid=row[0], values=row)
# Classe pour créer le bouton ajouter
class AjoutBouton(Button):
    def __init__(self, fenetre, tableau, entre_nom, entre_description, entre_prix, entre_quantite, entre_categorie):
        super().__init__(fenetre, text="Ajouter", command=self.ajouter)
        # créaction des attributs
        self.tableau = tableau
        self. entre_nom = entre_nom
        self.entre_description = entre_description
        self.entre_prix = entre_prix
        self.entre_quantite = entre_quantite
        self.entre_catégorie = entre_categorie
    # Une methode pour recuperer les saisies
    def ajouter(self):
        nom = self.entre_nom.get()
        description = self.entre_description.get()
        prix = self.entre_prix.get()
        quantite = self.entre_quantite.get()
        categorie = self.entre_catégorie.get()
        # Vérifier que les champs obligatoires ont été remplis
        if not nom or not prix or not quantite or not categorie:
            messagebox.showwarning("Erreur",
                "Le champs Nom,Prix,Quantité et Id_catégorie sont obligagatoire")
            return
        # Convertir les saisies en input
        prix = float(prix)
        quantite = int(quantite)
        categorie = int(categorie)
        # recommencer une nouvelle ligne dans la base de données
        try:
            connexion = mysql.connector.connect(host="localhost", user="root", 
                password="voltigeur21", database="boutique")
            curseur = connexion.cursor()
            curseur.execute("INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)",
                 (nom, description, prix, quantite, categorie))
            connexion.commit()
            curseur.close()
            connexion.close()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'insertion dans la base de données :\n{e}")
            return
        # Ajouter la nouvelle ligne dans le Treeview
        nouvelle_ligne=(curseur.lastrowid,nom,description,prix,quantite)
        self.tableau.insert("", END, values = nouvelle_ligne)
        # Effacer les saisies de l'utilisateur
        self.entre_nom.delete(0, END)
        self.entre_description.set("")
        self.entre_prix.delete(0, END)
        self.entre_quantite.set("")
# Créaction de la liaison du bouton ajouter au base de donnée
bout_ajouter = AjoutBouton (fenetre,tableau, entre_nom, entre_description, entre_prix, entre_quantite, entre_categorie)
bout_ajouter.place(x=100, y=250)
class SuprimerBouton(Button):
    def __init__(self, fenetre):
        super().__init__(fenetre, text="Suprimer", command=self.supprimer)
        
    def supprimer(self):
        id_produits = tableau.focus()
        if(str(id_produits) != ""):
            if messagebox.askyesno("suppression","supprimer?"):
                try:
                    connexion = mysql.connector.connect(host="localhost", user="root", 
                        password="voltigeur21", database="boutique")
                    curseur = connexion.cursor()
                    tableau.delete(id_produits)
                    curseur.execute("delete from produit where id = %s",(id_produits,))
                    connexion.commit()
                    curseur.close()
                    connexion.close()
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de l'insertion dans la base de données :\n{e}")           
# Créaction de la liaison du bouton suprimer au base de donnée
bout_ajouter = SuprimerBouton(fenetre)
bout_ajouter.place(x=200, y=250)
class ModifierBouton(Button):
    def __init__(self, fenetre):
        super().__init__(fenetre, text="Modifier", command=self.modifier)
        # créaction des attributs
        self.tableau = tableau
        self. entre_nom = entre_nom
        self.entre_description = entre_description
        self.entre_prix = entre_prix
        self.entre_quantite = entre_quantite
        self.entre_catégorie = entre_categorie
    # Une methode pour modifier les saisies
    def modifier(self):
            if messagebox.askyesno("Modification","Modifier?"):
                try:
                    connexion = mysql.connector.connect(host="localhost", user="root", 
                        password="voltigeur21", database="boutique")
                    curseur = connexion.cursor()
                    curseur.execute("UPDATE produit SET nom = %s WHERE id =%s",())
                    connexion.commit()
                    curseur.close()
                    connexion.close()
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de l'insertion dans la base de données :\n{e}")           
# Créaction de la liaison du bouton suprimer au base de donnée
bout_modifier = ModifierBouton(fenetre)
bout_modifier.place(x=310, y=250)
# Fermerture de la carte graphique
fenetre.mainloop()