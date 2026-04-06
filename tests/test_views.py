import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from vehicles.models import Vehicle, RentalOption
from applications.models import Application

User = get_user_model()

# Here, we create fixtures to facilitate test writing

# Fixture to simulate the creation of an user
@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="Testpass2026!",
        first_name="Jean",
        last_name="Test",
    )

# Fixture to simulate the creation of a vehicle
@pytest.fixture
def vehicle(db):
    return Vehicle.objects.create(
        brand="Peugeot", model="308", year=2023,
        mileage=25000, sale_price=18500, monthly_rental=299,
        vehicle_type=Vehicle.BOTH, is_active=True,
    )

# Fixture to get the test client to log in
@pytest.fixture
def client_logged_in(user):
    client = Client()
    client.login(username="testuser", password="Testpass2026!")
    return client



# =====================
# -- VEHICLE TESTING --
# =====================

# Tests for the catalog
@pytest.mark.django_db
class TestVehicleListView:

    def test_catalog_loads(self):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"))
        assert response.status_code == 200

    def test_catalog_shows_vehicles(self, vehicle):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"))
        assert b"Peugeot" in response.content

    def test_catalog_hides_inactive(self):
        Vehicle.objects.create(
            brand="Hidden", model="Car", year=2023,
            mileage=10000, sale_price=10000, is_active=False,
        )
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"))
        assert b"Hidden" not in response.content

    def test_filter_by_brand(self, vehicle):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"), {"brand": "Peugeot"})
        assert b"Peugeot" in response.content

    def test_filter_by_type_sale(self, vehicle):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"), {"type": "sale"})
        assert b"Peugeot" in response.content

    def test_filter_by_type_rental(self, vehicle):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"), {"type": "rental"})
        assert b"Peugeot" in response.content

    def test_filter_by_price_max(self, vehicle):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"), {"price_max": "20000"})
        assert b"Peugeot" in response.content

    def test_filter_by_km_max(self, vehicle):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"), {"km_max": "30000"})
        assert b"Peugeot" in response.content

    def test_filter_invalid_price(self):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"), {"price_max": "abc"})
        assert response.status_code == 200

    def test_filter_invalid_km(self):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_list"), {"km_max": "abc"})
        assert response.status_code == 200


# Tests for vehicle details page
@pytest.mark.django_db
class TestVehicleDetailView:

    def test_detail_loads(self, vehicle):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_detail", kwargs={"pk": vehicle.pk}))
        assert response.status_code == 200
        assert b"Peugeot" in response.content

    def test_detail_404_inactive(self):
        v = Vehicle.objects.create(
            brand="Ghost", model="Car", year=2023,
            mileage=10000, sale_price=10000, is_active=False,
        )
        client = Client()
        response = client.get(reverse("vehicles:vehicle_detail", kwargs={"pk": v.pk}))
        assert response.status_code == 404

    def test_detail_404_nonexistent(self):
        client = Client()
        response = client.get(reverse("vehicles:vehicle_detail", kwargs={"pk": 99999}))
        assert response.status_code == 404


# Tests for the rental options page
@pytest.mark.django_db
class TestRentalOptionsView:

    def test_page_loads(self):
        client = Client()
        response = client.get(reverse("vehicles:rental_options"))
        assert response.status_code == 200

    def test_shows_active_options(self):
        RentalOption.objects.create(name="Insurance", description="Test", monthly_price=89.90)
        client = Client()
        response = client.get(reverse("vehicles:rental_options"))
        assert b"Insurance" in response.content


# =====================
# -- ACCOUNT TESTING --
# =====================

# Tests for the signing up
@pytest.mark.django_db
class TestSignupView:

    def test_signup_page_loads(self):
        client = Client()
        response = client.get(reverse("accounts:signup"))
        assert response.status_code == 200

    def test_signup_success(self):
        client = Client()
        response = client.post(reverse("accounts:signup"), {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "Nouveau",
            "last_name": "Client",
            "phone": "06 99 88 77 66",
            "address": "1 rue Test",
            "password1": "SecurePass2026!",
            "password2": "SecurePass2026!",
        })
        assert response.status_code == 302
        assert User.objects.filter(username="newuser").exists()

    def test_signup_password_mismatch(self):
        client = Client()
        response = client.post(reverse("accounts:signup"), {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "Test",
            "last_name": "User",
            "phone": "06 11 22 33 44",
            "address": "Test",
            "password1": "SecurePass2026!",
            "password2": "DifferentPass2026!",
        })
        assert response.status_code == 200
        assert not User.objects.filter(username="newuser").exists()


# Tests for the logging in
@pytest.mark.django_db
class TestLoginView:

    def test_login_page_loads(self):
        client = Client()
        response = client.get(reverse("accounts:signin"))
        assert response.status_code == 200

    def test_login_success(self, user):
        client = Client()
        response = client.post(reverse("accounts:signin"), {
            "username": "testuser",
            "password": "Testpass2026!",
        })
        assert response.status_code == 302

    def test_login_wrong_password(self, user):
        client = Client()
        response = client.post(reverse("accounts:signin"), {
            "username": "testuser",
            "password": "WrongPass!",
        })
        assert response.status_code == 200


# Test for the logging out
@pytest.mark.django_db
class TestLogoutView:

    def test_logout(self, client_logged_in):
        response = client_logged_in.get(reverse("accounts:logout"))
        assert response.status_code == 302


# Tests for the user dashboard page
@pytest.mark.django_db
class TestDashboardView:

    def test_dashboard_requires_login(self):
        client = Client()
        response = client.get(reverse("accounts:dashboard"))
        assert response.status_code == 302

    def test_dashboard_loads(self, client_logged_in):
        response = client_logged_in.get(reverse("accounts:dashboard"))
        assert response.status_code == 200


# Tests for the user profile page
@pytest.mark.django_db
class TestProfileView:

    def test_profile_requires_login(self):
        client = Client()
        response = client.get(reverse("accounts:profile"))
        assert response.status_code == 302

    def test_profile_loads(self, client_logged_in):
        response = client_logged_in.get(reverse("accounts:profile"))
        assert response.status_code == 200

    def test_profile_update(self, client_logged_in, user):
        response = client_logged_in.post(reverse("accounts:profile"), {
            "first_name": "Updated",
            "last_name": "Name",
            "phone": "06 99 99 99 99",
            "address": "New address",
        })
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.first_name == "Updated"


# Test for the password resetting
@pytest.mark.django_db
class TestPasswordResetView:

    def test_password_reset_page_loads(self):
        client = Client()
        response = client.get(reverse("accounts:password_reset"))
        assert response.status_code == 200


# =====================
# -- APPLICATION TESTING --
# =====================

# Tests for the applying for purchase
@pytest.mark.django_db
class TestApplyPurchaseView:

    def test_requires_login(self, vehicle):
        client = Client()
        response = client.get(reverse("applications:apply_purchase", kwargs={"vehicle_pk": vehicle.pk}))
        assert response.status_code == 302

    def test_form_loads(self, client_logged_in, vehicle):
        response = client_logged_in.get(reverse("applications:apply_purchase", kwargs={"vehicle_pk": vehicle.pk}))
        assert response.status_code == 200

    def test_submit_application(self, client_logged_in, vehicle):
        response = client_logged_in.post(reverse("applications:apply_purchase", kwargs={"vehicle_pk": vehicle.pk}))
        assert response.status_code == 302
        app = Application.objects.filter(application_type=Application.PURCHASE).last()
        assert app is not None
        assert app.status == Application.PENDING


# Tests for the applying for rental
@pytest.mark.django_db
class TestApplyRentalView:

    def test_form_loads(self, client_logged_in, vehicle):
        response = client_logged_in.get(reverse("applications:apply_rental", kwargs={"vehicle_pk": vehicle.pk}))
        assert response.status_code == 200

    def test_submit_rental(self, client_logged_in, vehicle):
        response = client_logged_in.post(reverse("applications:apply_rental", kwargs={"vehicle_pk": vehicle.pk}), {
            "rental_duration": 24,
        })
        assert response.status_code == 302
        app = Application.objects.first()
        assert app.application_type == Application.RENTAL
        assert app.rental_duration == 24


# Tests for uploading documents
@pytest.mark.django_db
class TestUploadDocumentsView:

    def test_requires_login(self, vehicle, user):
        app = Application.objects.create(
            applicant=user, vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        client = Client()
        response = client.get(reverse("applications:upload_documents", kwargs={"pk": app.pk}))
        assert response.status_code == 302

    def test_page_loads(self, client_logged_in, vehicle, user):
        app = Application.objects.create(
            applicant=user, vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        response = client_logged_in.get(reverse("applications:upload_documents", kwargs={"pk": app.pk}))
        assert response.status_code == 200


# Tests for application details page
@pytest.mark.django_db
class TestApplicationDetailView:

    def test_requires_login(self, vehicle, user):
        app = Application.objects.create(
            applicant=user, vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        client = Client()
        response = client.get(reverse("applications:application_detail", kwargs={"pk": app.pk}))
        assert response.status_code == 302

    def test_detail_loads(self, client_logged_in, vehicle, user):
        app = Application.objects.create(
            applicant=user, vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        response = client_logged_in.get(reverse("applications:application_detail", kwargs={"pk": app.pk}))
        assert response.status_code == 200

    def test_other_user_cannot_access(self, vehicle, user):
        app = Application.objects.create(
            applicant=user, vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        other = User.objects.create_user(username="other", password="Test2026!")
        client = Client()
        client.login(username="other", password="Test2026!")
        response = client.get(reverse("applications:application_detail", kwargs={"pk": app.pk}))
        assert response.status_code == 404