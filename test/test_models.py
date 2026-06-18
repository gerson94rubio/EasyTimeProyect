import pytest
from faker import Faker
from usuarios.models import User
from inventario.models import Producto

fake = Faker()

@pytest.mark.django_db
def test_crear_usuario_random():
    user = User.objects.create_user(
        username=fake.user_name(),
        password="test1234",  # necesario para AbstractUser
        tipo_documento="CC",
        identificacion=fake.unique.random_number(digits=8),
        telefono=fake.msisdn()[:15],
        rol="CLIENTE"
    )
    assert user.username != ""
    assert len(user.telefono) <= 15
    assert user.tipo_documento in ["CC", "CE", "NIT", "PP", "TI", "PPT"]
    assert user.rol in ["ADMIN", "JEFE", "CLIENTE"]


@pytest.mark.django_db
def test_crear_producto_random():
    p = Producto.objects.create(
        nombre=fake.word(),
        descripcion=fake.text(),
        precio_venta=fake.random_number(digits=5), 
        stock_actual=fake.random_number(digits=2)
        )
    
    assert p.nombre != ""
    assert p.precio_venta > 0
    assert p.stock_actual >= 0


