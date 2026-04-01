from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from vehicles.models import Vehicle, RentalOption

User = get_user_model()


class Command(BaseCommand):
    help = "Populate database with demo data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Admin user
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@m-motors.fr",
                password="Admin2026!",
                first_name="Admin",
                last_name="M-Motors",
            )
            self.stdout.write(self.style.SUCCESS("  Admin created (admin / Admin2026!)"))

        # Demo client
        if not User.objects.filter(username="client").exists():
            User.objects.create_user(
                username="client",
                email="client@example.com",
                password="Client2026!",
                first_name="Jean",
                last_name="Dupont",
                phone="06 12 34 56 78",
                address="269 rue Vendôme, 69003 Lyon",
            )
            self.stdout.write(self.style.SUCCESS("  Client created (client / Client2026!)"))

        # Rental options
        options_data = [
            ("Insurance", "Full coverage including theft, fire, glass breakage and all damages.", 89.90),
            ("Roadside assistance", "24/7 roadside assistance including towing and replacement vehicle.", 29.90),
            ("Maintenance", "Routine maintenance: oil change, brakes, tires, manufacturer servicing.", 59.90),
            ("Technical inspection", "Coverage of technical inspection and any re-inspections.", 9.90),
        ]
        for name, desc, price in options_data:
            obj, created = RentalOption.objects.get_or_create(
                name=name,
                defaults={"description": desc, "monthly_price": price},
            )
            if created:
                self.stdout.write(f"  Option: {obj.name}")

        # Vehicles
        vehicles_data = [
            {"brand": "Peugeot", "model": "308", "year": 2022, "mileage": 25000, "sale_price": 18500, "monthly_rental": 299, "vehicle_type": "both", "description": "Compact sedan in excellent condition, low mileage."},
            {"brand": "Renault", "model": "Clio V", "year": 2023, "mileage": 12000, "sale_price": 16900, "monthly_rental": 249, "vehicle_type": "both", "description": "Versatile city car, ideal for urban driving."},
            {"brand": "Citroen", "model": "C3 Aircross", "year": 2021, "mileage": 45000, "sale_price": 15200, "monthly_rental": 269, "vehicle_type": "both", "description": "Compact urban SUV, spacious interior."},
            {"brand": "Volkswagen", "model": "Golf VIII", "year": 2022, "mileage": 30000, "sale_price": 24500, "monthly_rental": 389, "vehicle_type": "both", "description": "Premium compact hybrid, high-end finish."},
            {"brand": "Toyota", "model": "Yaris Cross", "year": 2023, "mileage": 8000, "sale_price": 22800, "monthly_rental": 349, "vehicle_type": "rental", "description": "Compact hybrid SUV, exceptional fuel economy."},
            {"brand": "Dacia", "model": "Sandero", "year": 2022, "mileage": 35000, "sale_price": 11500, "monthly_rental": None, "vehicle_type": "sale", "description": "Budget-friendly sedan, unbeatable value."},
            {"brand": "BMW", "model": "320d", "year": 2021, "mileage": 55000, "sale_price": 29900, "monthly_rental": 449, "vehicle_type": "both", "description": "Sporty premium sedan, powerful diesel engine."},
            {"brand": "Tesla", "model": "Model 3", "year": 2023, "mileage": 15000, "sale_price": 35900, "monthly_rental": 549, "vehicle_type": "both", "description": "100% electric sedan, 500 km range."},
            {"brand": "Fiat", "model": "500 Electric", "year": 2023, "mileage": 5000, "sale_price": 21000, "monthly_rental": 329, "vehicle_type": "rental", "description": "Iconic electric city car, 320 km range."},
            {"brand": "Mercedes", "model": "A 200", "year": 2022, "mileage": 20000, "sale_price": 28500, "monthly_rental": 429, "vehicle_type": "both", "description": "Premium compact, AMG Line finish."},
            {"brand": "Peugeot", "model": "3008", "year": 2021, "mileage": 60000, "sale_price": 22000, "monthly_rental": 359, "vehicle_type": "both", "description": "Family SUV, next-gen i-Cockpit."},
            {"brand": "Renault", "model": "Captur", "year": 2023, "mileage": 10000, "sale_price": 24200, "monthly_rental": 379, "vehicle_type": "both", "description": "Plug-in hybrid crossover, 50 km electric range."},
        ]
        # If a vehicle exists, it is retrieved. Else, it is created.
        for v in vehicles_data:
            obj, created = Vehicle.objects.get_or_create(
                brand=v["brand"],
                model=v["model"],
                year=v["year"],
                defaults=v,
            )
            if created:
                self.stdout.write(f"  Vehicle: {obj}")

        self.stdout.write(self.style.SUCCESS(f"\nDone! {Vehicle.objects.count()} vehicles, {RentalOption.objects.count()} options, {User.objects.count()} users."))