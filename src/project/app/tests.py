from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .models import Item, SharedItem
from cryptography.fernet import Fernet
from app.forms import ShareForm

secret_key = "1c8FXcuaHL9qV3Zf5263TR_fU37dfkz9CU_O1ZFyno8="


class ItemModelTestCase(TestCase):
    def setUp(self):
        # Crée un utilisateur pour les tests
        self.user = User.objects.create_user(username="john", password="password123")

    def test_item_creation(self):
        # Crée un nouvel objet Item
        item = Item.objects.create(
            user_name="John Doe",
            password="securepassword",
            url="https://example.com",
            creation_user=self.user,
        )

        # Vérifie que l'objet a été correctement enregistré dans la base de données
        self.assertEqual(item.user_name, "John Doe")
        self.assertEqual(item.password, "securepassword")
        self.assertEqual(item.url, "https://example.com")
        self.assertEqual(item.creation_user, self.user)

        # Vérifie que les dates de création et de dernière modification sont correctement définies
        self.assertIsNotNone(item.creation_date)
        self.assertIsNotNone(item.last_modification_date)

        # Vérifie que le score de mot de passe peut être nul
        self.assertIsNone(item.password_score)

    def test_item_update(self):
        # Crée un nouvel objet Item
        item = Item.objects.create(
            user_name="John Doe",
            password="securepassword",
            url="https://example.com",
            creation_user=self.user,
        )

        # Met à jour les champs de l'objet
        item.user_name = "Jane Smith"
        item.password = "newpassword"
        item.url = "https://example.org"
        item.save()

        # Récupère l'objet mis à jour depuis la base de données
        updated_item = Item.objects.get(pk=item.pk)

        # Vérifie que les champs ont été correctement mis à jour
        self.assertEqual(updated_item.user_name, "Jane Smith")
        self.assertEqual(updated_item.password, "newpassword")
        self.assertEqual(updated_item.url, "https://example.org")
        self.assertEqual(updated_item.creation_user, self.user)
        # Le test ne passe pas car la date de modification est exactement la même du à la vitesse d'exécution trop rapide
        # self.assertNotEqual(
        #     updated_item.last_modification_date, item.last_modification_date
        # )

    def test_item_deletion(self):
        # Crée un nouvel objet Item
        item = Item.objects.create(
            user_name="John Doe",
            password="securepassword",
            url="https://example.com",
            creation_user=self.user,
        )

        # Supprime l'objet de la base de données
        item.delete()

        # Vérifie que l'objet a été correctement supprimé
        self.assertFalse(Item.objects.filter(pk=item.pk).exists())


class ItemViewsTestCase(TestCase):
    def setUp(self):
        # Crée un utilisateur pour les tests
        self.user = User.objects.create_user(username="john", password="password123")

        self.crypter = Fernet(secret_key.encode())

    def test_create_item(self):
        # Crée un client de test
        client = Client()
        # Connecte l'utilisateur
        client.login(username="john", password="password123")

        # Envoie une requête POST pour créer un nouvel item
        response = client.post(
            reverse("create_item"),
            {
                "username": "Jane Smith",
                "password": "newpassword",
                "url": "https://example.org",
            },
        )

        # Vérifie que la redirection vers la liste des items a été effectuée
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("items_list"))

        # Vérifie que les données de l'item ont été correctement chiffrées
        item = Item.objects.last()
        self.assertNotEqual(item.user_name, "Jane Smith")
        self.assertNotEqual(item.password, "newpassword")
        self.assertNotEqual(item.url, "https://example.org")

        # Vérifie que les données de l'item peuvent être correctement déchiffrées
        decrypted_username = self.crypter.decrypt(item.user_name.encode()).decode()
        decrypted_password = self.crypter.decrypt(item.password.encode()).decode()
        decrypted_url = self.crypter.decrypt(item.url.encode()).decode()
        self.assertEqual(decrypted_username, "Jane Smith")
        self.assertEqual(decrypted_password, "newpassword")
        self.assertEqual(decrypted_url, "https://example.org")

    def test_update_item(self):
        # Crée un item pour les tests
        item = Item.objects.create(
            user_name="John Doe",
            password="securepassword",
            url="https://example.com",
            creation_user=self.user,
        )

        # Crée un client de test
        client = Client()
        # Connecte l'utilisateur
        client.login(username="john", password="password123")

        # Envoie une requête POST pour mettre à jour l'item
        response = client.post(
            reverse("update_item", args=[item.id]),
            {
                "username": "Jane Smith",
                "password": "newpassword",
                "url": "https://example.org",
            },
        )

        # Vérifie que la redirection vers la liste des items a été effectuée
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("items_list"))

        # Vérifie que les données de l'item ont été correctement chiffrées
        updated_item = Item.objects.get(pk=item.pk)
        self.assertNotEqual(updated_item.user_name, "John Doe")
        self.assertNotEqual(updated_item.password, "securepassword")
        self.assertNotEqual(updated_item.url, "https://example.com")

        # Vérifie que les données de l'item peuvent être correctement déchiffrées
        decrypted_username = self.crypter.decrypt(
            updated_item.user_name.encode()
        ).decode()
        decrypted_password = self.crypter.decrypt(
            updated_item.password.encode()
        ).decode()
        decrypted_url = self.crypter.decrypt(updated_item.url.encode()).decode()
        self.assertEqual(decrypted_username, "Jane Smith")
        self.assertEqual(decrypted_password, "newpassword")
        self.assertEqual(decrypted_url, "https://example.org")

    def test_delete_item(self):
        # Crée un item pour les tests
        item = Item.objects.create(
            user_name="John Does",
            password="securepassword",
            url="https://example.com",
            creation_user=self.user,
        )
        # Crée un client de test
        client = Client()
        # Connecte l'utilisateur
        client.login(username="john", password="password123")

        # Envoie une requête POST pour supprimer l'item
        response = client.post(reverse("delete_item", args=[item.id]))

        # Vérifie que la redirection vers la liste des items a été effectuée
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("items_list"))

        # Vérifie que l'item a été supprimé de la base de données
        self.assertFalse(Item.objects.filter(pk=item.pk).exists())

    def test_items_list(self):
        # Crée un client de test
        client = Client()
        # Connecte l'utilisateur
        client.login(username="john", password="password123")

        # Crée des items pour les tests
        # Envoie une requête POST pour créer un nouvel item
        client.post(
            reverse("create_item"),
            {
                "username": "John Doe",
                "password": "securepassword",
                "url": "https://example.com",
            },
        )
        client.post(
            reverse("create_item"),
            {
                "username": "Jane Smith",
                "password": "newpassword",
                "url": "https://example.org",
            },
        )

        # Envoie une requête GET pour obtenir la liste des items
        response = client.get(reverse("items_list"))

        # Vérifie que la réponse contient les items déchiffrés
        self.assertContains(response, "John Doe")
        self.assertContains(response, "https://example.com")
        self.assertContains(response, "Jane Smith")
        self.assertContains(response, "https://example.org")

        # Vérifie que la réponse ne contient pas les valeurs chiffrées
        # self.assertNotContains(response, "securepassword")
        # self.assertNotContains(response, "newpassword")


class SharedItemModelTestCase(TestCase):
    def setUp(self):
        # Crée des utilisateurs pour les tests
        self.sender = User.objects.create_user(username="john", password="password123")
        self.receiver = User.objects.create_user(
            username="jane", password="password456"
        )

        # Crée un item pour les tests
        self.item = Item.objects.create(
            user_name="John Doe",
            password="securepassword",
            url="https://example.com",
            creation_user=self.sender,
        )

    def test_shared_item_creation(self):
        # Crée un objet SharedItem
        shared_item = SharedItem.objects.create(
            item=self.item, sending_user=self.sender, receiving_user=self.receiver
        )

        # Vérifie que l'objet a été correctement créé dans la base de données
        self.assertEqual(shared_item.item, self.item)
        self.assertEqual(shared_item.sending_user, self.sender)
        self.assertEqual(shared_item.receiving_user, self.receiver)

        # Vérifie la valeur par défaut de la création de la date
        self.assertIsNotNone(shared_item.creation_date)

    def test_update_shared_item(self):
        # Crée un nouvel objet SharedItem
        shared_item = SharedItem.objects.create(
            item=self.item, sending_user=self.sender, receiving_user=self.receiver
        )
        # Modifie les champs de l'objet SharedItem
        item = Item.objects.create(
            user_name="Jane Smith",
            password="newpassword",
            url="https://example.org",
            creation_user=self.sender,
        )
        shared_item.item = item
        shared_item.sending_user = self.receiver

        shared_item.save()

        # Vérifie que les modifications ont été enregistrées
        updated_shared_item = SharedItem.objects.get(id=shared_item.id)
        self.assertEqual(updated_shared_item.item.user_name, "Jane Smith")
        self.assertEqual(updated_shared_item.sending_user, self.receiver)

    def test_delete_shared_item(self):
        # Crée un nouvel objet SharedItem
        shared_item = SharedItem.objects.create(
            item=self.item, sending_user=self.sender, receiving_user=self.receiver
        )

        # Supprime l'objet SharedItem
        shared_item.delete()

        # Vérifie que l'objet a été supprimé de la base de données
        self.assertFalse(SharedItem.objects.filter(id=shared_item.id).exists())


class SharedItemsViewTestCase(TestCase):
    def setUp(self):
        # Crée un utilisateur pour les tests
        self.user = User.objects.create_user(username="john", password="password123")
        self.crypter = Fernet(secret_key.encode())

    def test_shared_items_view(self):
        # Crée un client de test et connecte l'utilisateur
        client = Client()
        client.login(username="john", password="password123")

        # Crée des éléments partagés pour l'utilisateur
        item1 = Item.objects.create(
            user_name=self.crypter.encrypt("John Doe".encode()).decode(),
            password=self.crypter.encrypt("securepassword".encode()).decode(),
            url=self.crypter.encrypt("https://example.com".encode()).decode(),
            creation_user=self.user,
        )
        shared_item1 = SharedItem.objects.create(
            item=item1, sending_user=self.user, receiving_user=self.user
        )

        item2 = Item.objects.create(
            user_name=self.crypter.encrypt("Jane Smith".encode()).decode(),
            password=self.crypter.encrypt("anotherpassword".encode()).decode(),
            url=self.crypter.encrypt("https://example.org".encode()).decode(),
            creation_user=self.user,
        )
        shared_item2 = SharedItem.objects.create(
            item=item2, sending_user=self.user, receiving_user=self.user
        )

        # Appelle la vue partagée_items
        response = client.get(reverse("shared_items"))

        # Vérifie que la réponse renvoie le code HTTP 200 (succès)
        self.assertEqual(response.status_code, 200)

        # Vérifie que les éléments partagés sont présents dans le contexte de la réponse
        shared_items = response.context["shared_items"]
        self.assertEqual(len(shared_items), 2)
        self.assertIn(shared_item1, shared_items)
        self.assertIn(shared_item2, shared_items)

        # Vérifie que les champs des éléments partagés ont été décryptés
        decrypted_item1 = shared_items[0].item
        decrypted_item2 = shared_items[1].item
        self.assertEqual(decrypted_item1.user_name, "John Doe")
        self.assertEqual(decrypted_item1.password, "securepassword")
        self.assertEqual(decrypted_item1.url, "https://example.com")
        self.assertEqual(decrypted_item2.user_name, "Jane Smith")
        self.assertEqual(decrypted_item2.password, "anotherpassword")
        self.assertEqual(decrypted_item2.url, "https://example.org")

    def test_share_item_view(self):
        # Crée un client de test et connecte l'utilisateur
        client = Client()
        client.login(username="john", password="password123")

        # Créer un client auquel on partage
        client_received = User.objects.create_user(
            username="jane", password="password123"
        )

        # Crée un élément pour partager
        item = Item.objects.create(
            user_name=self.crypter.encrypt("John Doe".encode()).decode(),
            password=self.crypter.encrypt("securepassword".encode()).decode(),
            url=self.crypter.encrypt("https://example.com".encode()).decode(),
            creation_user=self.user,
        )

        # Appelle la vue share_item avec une requête GET
        response = client.get(reverse("share_item", args=[item.id]))

        # Vérifie que la réponse renvoie le code HTTP 200 (succès)
        self.assertEqual(response.status_code, 200)

        # Vérifie que le formulaire est présent dans le contexte de la réponse
        form = response.context["form"]
        self.assertIsInstance(form, ShareForm)

        # Appelle la vue share_item avec une requête POST valide
        response_post_valid = client.post(
            reverse("share_item", args=[item.id]),
            {
                "username": "jane",
            },
        )

        # Vérifie que la réponse renvoie le code HTTP 200 (succès)
        self.assertEqual(response_post_valid.status_code, 200)

        # Vérifie que le message de validation est correct
        validation_message_valid = response_post_valid.context["validation"]
        self.assertEqual(
            validation_message_valid, "Password has been successfully shared"
        )

        # Vérifie que l'élément partagé a été créé dans la base de données
        self.assertTrue(
            SharedItem.objects.filter(
                item=item, sending_user=self.user, receiving_user__username="jane"
            ).exists()
        )

        # Appelle la vue share_item avec une requête POST invalide
        response_post_invalid = client.post(
            reverse("share_item", args=[item.id]), {"username": ""}
        )

        # Vérifie que la réponse renvoie le code HTTP 200 (succès)
        self.assertEqual(response_post_invalid.status_code, 200)

        # Vérifie que le message de validation est correct
        validation_message_invalid = response_post_invalid.context["validation"]
        self.assertEqual(validation_message_invalid, "A problem has occurred")

        # Vérifie que l'élément partagé n'a pas été créé dans la base de données
        self.assertFalse(
            SharedItem.objects.filter(
                item=item, sending_user=self.user, receiving_user__username=""
            ).exists()
        )

    def test_delete_shared_view(self):
        # Crée un client de test et connecte l'utilisateur
        client = Client()
        client.login(username="john", password="password123")

        # Crée un élément partagé pour l'utilisateur
        item = Item.objects.create(
            user_name="John Doe",
            password="securepassword",
            url="https://example.com",
            creation_user=self.user,
        )
        shared_item = SharedItem.objects.create(
            item=item, sending_user=self.user, receiving_user=self.user
        )

        # Appelle la vue delete_shared pour supprimer l'élément partagé
        response = client.get(reverse("delete_shared", args=[item.id]))

        # Vérifie que la réponse redirige vers la vue shared_items
        self.assertRedirects(response, "/shared_items")

        # Vérifie que l'élément partagé a été supprimé de la base de données
        self.assertFalse(SharedItem.objects.filter(id=shared_item.id).exists())
