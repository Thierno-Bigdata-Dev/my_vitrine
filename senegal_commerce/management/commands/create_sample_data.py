import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shops.models import Shop
from products.models import Category, Product

User = get_user_model()

class Command(BaseCommand):
    help = 'Créer des données d\'exemple pour l\'application'

    def handle(self, *args, **options):
        self.stdout.write('Création des données d\'exemple...')
        
        # Créer des utilisateurs vendeurs
        vendors = []
        for i in range(3):
            vendor, created = User.objects.get_or_create(
                username=f'vendeur{i+1}',
                defaults={
                    'email': f'vendeur{i+1}@senegalcommerce.sn',
                    'first_name': f'Vendeur{i+1}',
                    'last_name': 'Sénégal',
                    'user_type': 'vendor',
                    'phone': f'+221 77 123 456{i}',
                    'address': f'Dakar, Sénégal - Zone {i+1}'
                }
            )
            vendor.set_password('password123')
            vendor.save()
            vendors.append(vendor)
        
        # Créer des catégories
        categories_data = [
            'Artisanat', 'Mode et Vêtements', 'Alimentation',
            'Cosmétiques', 'Décoration', 'Accessoires'
        ]
        categories = []
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Produits de {cat_name} sénégalais'}
            )
            categories.append(category)
        
        # Créer des boutiques
        shops_data = [
            {
                'name': 'Boutique Teranga',
                'description': 'Artisanat traditionnel sénégalais',
                'city': 'Dakar',
                'phone': '+221 77 123 4560',
                'email': 'teranga@senegalcommerce.sn'
            },
            {
                'name': 'Mode Sahel',
                'description': 'Mode africaine contemporaine',
                'city': 'Saint-Louis',
                'phone': '+221 77 123 4561',
                'email': 'modesahel@senegalcommerce.sn'
            },
            {
                'name': 'Saveurs du Sénégal',
                'description': 'Produits alimentaires locaux',
                'city': 'Thiès',
                'phone': '+221 77 123 4562',
                'email': 'saveurs@senegalcommerce.sn'
            }
        ]
        
        shops = []
        for i, shop_data in enumerate(shops_data):
            shop, created = Shop.objects.get_or_create(
                name=shop_data['name'],
                defaults={
                    **shop_data,
                    'owner': vendors[i],
                    'address': f'Adresse de {shop_data["name"]}, {shop_data["city"]}'
                }
            )
            shops.append(shop)
        
        # Créer des produits
        products_data = [
            {
                'name': 'Boubou Traditionnel',
                'description': 'Boubou traditionnel sénégalais en bazin',
                'price': 45000,
                'category': categories[1],  # Mode
                'shop': shops[1],
                'stock_quantity': 15,
                'is_featured': True
            },
            {
                'name': 'Sac en Cuir Peul',
                'description': 'Sac artisanal en cuir traditionnel',
                'price': 25000,
                'category': categories[0],  # Artisanat
                'shop': shops[0],
                'stock_quantity': 8,
                'is_featured': True
            },
            {
                'name': 'Bissap en Poudre',
                'description': 'Bissap naturel en poudre, 500g',
                'price': 3500,
                'category': categories[2],  # Alimentation
                'shop': shops[2],
                'stock_quantity': 50,
                'is_featured': True
            },
            {
                'name': 'Collier en Perles',
                'description': 'Collier traditionnel en perles colorées',
                'price': 15000,
                'category': categories[5],  # Accessoires
                'shop': shops[0],
                'stock_quantity': 12
            },
            {
                'name': 'Huile de Baobab',
                'description': 'Huile naturelle de baobab, 100ml',
                'price': 8000,
                'category': categories[3],  # Cosmétiques
                'shop': shops[2],
                'stock_quantity': 25
            }
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                shop=product_data['shop'],
                defaults=product_data
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                'Données d\'exemple créées avec succès!\n'
                f'- {len(vendors)} vendeurs\n'
                f'- {len(categories)} catégories\n'
                f'- {len(shops)} boutiques\n'
                f'- {len(products_data)} produits'
            )
        )
