Application en python utilisant le framework Django

Appli fait appel à :
    -une base de donnée sqlite
    -la librairie BOOTSTRAP
    -le pacakge tkinter
    -xlswriter pour l'export d'un fichier excel

Objectif: 
   - permettre la génération d'une liste de point à partir des éléments constituant une Chaufferie ou Sous Station dans le but de dimensionner l'automate de régulation

AVANT L'UTILISATION:
 1) Installer DJANGO : pip install django
 2) Installer BOOTSTRAP5 : pip install django-bootstrap5
 3) Installer XLSXWRITER : pip install xlsxwriter
 4) Installer IMPORT-EXPORT : pip install django-import-export

Pour la mise en place sur le serveur:
 1) Dans le fichier settings.py, placer DEBUG à FALSE
 2) Dans le fichier settings.py, commenter la ligne ALLOWED_HOSTS = []
 3) Dans le fichier settings.py, Décommenter la ligne # ALLOWED_HOSTS = ['xxxxx.xxxxx.com']

Si une modification est faite dans un fichier CSS, penser à recharger les fichiers statiques:  python manage.py collectstatic
