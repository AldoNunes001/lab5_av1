import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from store.models import Product, Collection
from core.models import User  


@pytest.mark.django_db
def test_create_product():
    client = APIClient()

    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

    client.force_authenticate(user=admin_user)

    collection = Collection.objects.create(title="Coleção Teste")

    data = {
        "title": "Produto Teste",
        "unit_price": 10.0,
        "inventory": 100,
        "slug": "produto-teste",
        "collection": collection.id
    }

    url = reverse('products-list')
    response = client.post(url, data, format='json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_update_product():
    client = APIClient()

    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

    client.force_authenticate(user=admin_user)

    collection = Collection.objects.create(title="Coleção Teste")

    product = Product.objects.create(
        title="Produto Teste",
        unit_price=10.0,
        inventory=100,
        slug="produto-teste",
        collection=collection
    )

    data = {
        "title": "Produto Atualizado",
        "unit_price": 20.0,
        "inventory": 50,
        "slug": "produto-atualizado",
        "collection": collection.id
    }

    url = reverse('products-detail', args=[product.id])
    response = client.patch(url, data, format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_product():
    client = APIClient()

    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

    client.force_authenticate(user=admin_user)

    collection = Collection.objects.create(title="Coleção Teste")

    product = Product.objects.create(
        title="Produto Teste",
        unit_price=10.0,
        inventory=100,
        slug="produto-teste",
        collection=collection
    )

    url = reverse('products-detail', args=[product.id])
    response = client.delete(url)

    assert response.status_code == 204


# Testar listar produtos
@pytest.mark.django_db
def test_list_products():
    client = APIClient()

    collection = Collection.objects.create(title="Coleção Teste")
    Product.objects.create(
        title="Produto Teste",
        unit_price=10.0,
        inventory=100,
        slug="produto-teste",
        collection=collection
    )

    url = reverse('products-list')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) > 0  


# Testar ver detalhes de um produto
@pytest.mark.django_db
def test_retrieve_product():
    client = APIClient()

    collection = Collection.objects.create(title="Coleção Teste")
    product = Product.objects.create(
        title="Produto Teste",
        unit_price=10.0,
        inventory=100,
        slug="produto-teste",
        collection=collection
    )

    url = reverse('products-detail', args=[product.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data['title'] == product.title  