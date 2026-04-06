import pytest
from django.contrib.auth import get_user_model
from vehicles.models import Vehicle, RentalOption
from applications.models import Application

User = get_user_model()

# Here, we are testing the Vehicle Model
@pytest.mark.django_db
class TestVehicleModel:

    # Vehicle creation
    def test_create_vehicle(self):
        vehicle = Vehicle.objects.create(
            brand="Peugeot",
            model="308",
            year=2023,
            mileage=25000,
            sale_price=18500,
        )
        assert vehicle.pk is not None
        assert str(vehicle) == "Peugeot 308 (2023)"

    # "For Sale" status
    def test_is_for_sale(self):
        vehicle = Vehicle.objects.create(
            brand="Test", model="Sale", year=2023,
            mileage=10000, sale_price=15000,
            vehicle_type=Vehicle.SALE,
        )
        assert vehicle.is_for_sale is True
        assert vehicle.is_for_rental is False

    # "Rental" status
    def test_is_for_rental(self):
        vehicle = Vehicle.objects.create(
            brand="Test", model="Rental", year=2023,
            mileage=10000, monthly_rental=299,
            vehicle_type=Vehicle.RENTAL,
        )
        assert vehicle.is_for_sale is False
        assert vehicle.is_for_rental is True

    # Both "For Sale" and "Rental" statuses
    def test_is_for_both(self):
        vehicle = Vehicle.objects.create(
            brand="Test", model="Both", year=2023,
            mileage=10000, sale_price=15000, monthly_rental=299,
            vehicle_type=Vehicle.BOTH,
        )
        assert vehicle.is_for_sale is True
        assert vehicle.is_for_rental is True

    # Inactive vehicles
    def test_inactive_vehicle(self):
        Vehicle.objects.create(
            brand="Hidden", model="Car", year=2023,
            mileage=10000, sale_price=10000, is_active=False,
        )
        active = Vehicle.objects.filter(is_active=True)
        assert active.count() == 0


# Here, we are testing the Rental Options Model
@pytest.mark.django_db
class TestRentalOptionModel:

    # Option creation
    def test_create_option(self):
        option = RentalOption.objects.create(
            name="Insurance",
            description="Full coverage",
            monthly_price=89.90,
        )
        assert option.pk is not None
        assert "Insurance" in str(option)


# Here, we are testing the User Model
@pytest.mark.django_db
class TestUserModel:

    # User creation
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Testpass2026!",
            first_name="Jean",
            last_name="Test",
            phone="06 11 22 33 44",
        )
        assert user.pk is not None
        assert "Jean" in str(user)


# Here, we are testing the Application Model
@pytest.mark.django_db
class TestApplicationModel:

    # Application creation
    def test_create_application(self):
        user = User.objects.create_user(
            username="applicant", password="Test2026!"
        )
        vehicle = Vehicle.objects.create(
            brand="Renault", model="Clio", year=2023,
            mileage=10000, sale_price=16000,
        )
        app = Application.objects.create(
            applicant=user,
            vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        assert app.pk is not None
        assert app.status == Application.PENDING
        assert "Renault Clio" in str(app)


    


