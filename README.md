En accèdant au site sans être connecté vous n'avez accès qu'aux actions de connexion et création de compte, vous pouverz vous connecter avec le superuser Linus (mdp: LinuxAir11).
Les principales routes sont accessible avec le header une fois connecté.
Dans la liste des items, les boutons à droite permettent la modfication, suppression et le partage.
Il faut cliquer sur les mots de passe pour les afficher.

Pour exécuter les tests, la commande est:
python manage.py test app.tests

Liste des routes :
accounts/register
create_item
items_list
share_item/<id>
shared_items
delete_shared/<id>
update_item/<id>
delete_item/<id>
display_password/<id>
changedmymind
history
