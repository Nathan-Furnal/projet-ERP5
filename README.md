# Introduction

Ce document explique l'utilisation et le développement du projet d'ERP.  Dans la
première partie, j'aborderai le développement du module *realtor*, un module de
gestion de biens immobiliers, sous Odoo. Dans un deuxième, j'expliquerai
l'utilisation qu'on peut en faire. Enfin, je présenterai les liaisons possibles
avec Django.

La partie Odoo se trouve sous `odoo-app` et la partie Django sous
`realtorclient`.

# Odoo

## Mise en place

Tout d'abord, pour avoir un environnement de travail reproductible et portable,
nous utilisons des environnements *docker*. Leur installation et utilisation est
détaillée dans le cours.

Une fois les *containers* lancés, il faut aller dans le menu de l'application
après avoir enclenché le mode de déboguage (via `web?debug=True` dans l'URL) et
installer l'application `realtor`.

<!>**Attention**<!> à la création du compte/de la DB, il ne faut **pas** cocher
la section pour avoir des données de démonstration car elles interfèrent avec
mes données propres.

## *Business Objects*

La création de données par Odoo passe par l'utilisation de modèles qui sont
aussi liés à la base de données. Ils sont nommés *Business Objects* ou *BO* pour
faire simple.  Dans mon cas, on retrouve plusieurs objets.

- `Realtor Apartment` :: le produit principal de ce travail qui est un
appartement qui sera mis en vente via la plateforme.

- `Realtor Offer` :: Un objet qui permet de conserver une trace des offres
  faites pour chaque appartement.
- `Realtor Product` :: un *template* qui permet de lier l'appartement avec le
  système de stocks d'Odoo. C'est utile car on peut dès lors directement lier
  les inventaires et les factures à nos objets.
- `Res User` :: Qui étend simple l'utilisateur déjà existant en lui ajoutant un
  champ permettant de tenir compte des appartements détenus. Car dans notre
  système, seul les utilisateurs authentifiés peuvent mettre un appartement en
  vente.

## Vues

Les vues Odoo sont données en XML, elles se présentent sous différentes formes,
comme une arborescence ou bien un formulaire. Les groupes caractérisent des
données mises ensemble et les pages des onglets à l'intérieur d'une vue.

## Sécurité

Le fichier de sécurité `security.xml` permet d'ajouter des utilisateurs et de
les caractériser par des groupes, ce qui pratique pour créer des groupes au sein
d'une même entreprise ou d'un département.  On doit aussi donner les accès au
objets qu'on crée pour qu'ils puissent intéragir avec les autres objets et
surtout avec la base de données.

## Démo

Les fichiers de démonstration tels que le `demo.xml` ou `stock_demo.xml`
permettent d'ajouter des données fictives à titre de tests, dans la DB.  Le
premier est le `demo.xml` qui contient de l'information pour créer des
*partners* (ce sont des utilisateurs non authentifiés qui peuvent interagir en
partie avec la plateforme).  Ensuite, je crée des appartements fictifs qui
serviront durant tout le développement.

Le second fichier `stock_demo.xml` est nécessaire une fois qu'on a lié les
appartements à des produits. Il crée d'abord un stock d'inventaire unique dans
lesquels seront stockés les unités d'appartement. Ensuite, j'ajoute des
*templates* qui permettent de lier les produits aux appartements. Enfin, les
produits de l'inventaire font appel au *template* pour ajouter des unités avec
nombre donné, dans ce même inventaire.

# Django

Django et un *framework* web écrit en Python, on l'utilise pour afficher les
infomrations de l'application et interagir avec Odoo via XML-RPC. Ceci nécessite
d'avoir un serveur Odoo disponible pour pouvoir récupérer les données de la DB.

## Mise en place

Pour installer l'environnement virtuel, il est nécessaire d'utiliser `poetry` ou
un outil compatible avec le fichier `pyproject.toml`. Celui-ci défini les
dépendances nécessaires au projet. On peut simplement installer le projet avec
`poetry install` ou bien `pip install .` dans le répertoire
`realtorclient`. Ensuite, il faut activer l'environnement virtuel.

## Modèles

Comme les modèles sont déjà créés du côté d'Odoo, il y a peu ou pas de modèles
nécessaires.

## Connexion à Odoo via XML-RPC

La connexion passe par le fichier `xml_rpc.py` dans la section Django. Les
données de connexion sont entrées en dur pour faciliter l'implémentation.  Il y
a des fonctions qui permettent d'accéder aux données. La fonction la plus
complexe, qui permet d'ajouter des offres à un appartement et d'ajouter
l'utilisateur qui fait l'offre s'il n'est pas encore dans le système ; utilise
différents filtres sur les listes de dictionnaires qui sont rendues par Odoo.

## Vues

Les vues permettent d'afficher les données. Pour la connexion et les offres, je
passe par des formulaires qui permettent de tenir un fichier de connexion et
envoyer des informations au serveur Odoo, respectivement.

# Conclusion

Ce travail lie un module Odoo avec un site web écrit en Django. Il permet de
créer des modèles et générer des données fictives côté Odoo et d'offrir une vue
plus simple ainsi que de l'interaction, côté Django.

# N.B

Ce projet a été fait dans le cadre de mes études à l'ESI et n'a pas pour but
d'être utilisé pour des applications réelles dans un cadre professionnel.

<!-- Local Variables: --> 
<!-- jinx-languages: "fr" --> 
<!-- End: -->
