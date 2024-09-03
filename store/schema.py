import graphene
from graphene_django.types import DjangoObjectType
from .models import Product, Collection, Customer, Order, OrderItem, Cart, CartItem, Review
from django.core.exceptions import ObjectDoesNotExist

# Definição dos tipos (DjangoObjectType) baseados nos modelos
class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class CollectionType(DjangoObjectType):
    class Meta:
        model = Collection

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem

class CartType(DjangoObjectType):
    class Meta:
        model = Cart

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem

class ReviewType(DjangoObjectType):
    class Meta:
        model = Review

# Definição das Queries
class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    all_collections = graphene.List(CollectionType)
    all_customers = graphene.List(CustomerType)
    all_orders = graphene.List(OrderType)
    all_cart_items = graphene.List(CartItemType)

    product = graphene.Field(ProductType, id=graphene.Int())
    collection = graphene.Field(CollectionType, id=graphene.Int())
    customer = graphene.Field(CustomerType, id=graphene.Int())
    order = graphene.Field(OrderType, id=graphene.Int())
    cart_item = graphene.Field(CartItemType, id=graphene.Int())

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_all_collections(self, info, **kwargs):
        return Collection.objects.all()

    def resolve_all_customers(self, info, **kwargs):
        return Customer.objects.all()

    def resolve_all_orders(self, info, **kwargs):
        return Order.objects.all()

    def resolve_all_cart_items(self, info, **kwargs):
        return CartItem.objects.all()

    def resolve_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    def resolve_collection(self, info, id):
        try:
            return Collection.objects.get(pk=id)
        except Collection.DoesNotExist:
            return None

    def resolve_customer(self, info, id):
        try:
            return Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return None

    def resolve_order(self, info, id):
        try:
            return Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return None

    def resolve_cart_item(self, info, id):
        try:
            return CartItem.objects.get(pk=id)
        except CartItem.DoesNotExist:
            return None

# Mutações

class CreateProduct(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        slug = graphene.String(required=True)
        description = graphene.String()
        unit_price = graphene.Decimal(required=True)
        inventory = graphene.Int(required=True)
        collection_id = graphene.Int(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, title, slug, unit_price, inventory, collection_id, description=None):
        try:
            collection = Collection.objects.get(pk=collection_id)
            product = Product(
                title=title,
                slug=slug,
                unit_price=unit_price,
                inventory=inventory,
                collection=collection,
                description=description
            )
            product.save()
            return CreateProduct(product=product)
        except ObjectDoesNotExist:
            raise Exception("Collection not found")

class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        slug = graphene.String()
        description = graphene.String()
        unit_price = graphene.Decimal()
        inventory = graphene.Int()
        collection_id = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, id, title=None, slug=None, description=None, unit_price=None, inventory=None, collection_id=None):
        try:
            product = Product.objects.get(pk=id)

            if title:
                product.title = title
            if slug:
                product.slug = slug
            if description:
                product.description = description
            if unit_price:
                product.unit_price = unit_price
            if inventory:
                product.inventory = inventory
            if collection_id:
                try:
                    collection = Collection.objects.get(pk=collection_id)
                    product.collection = collection
                except ObjectDoesNotExist:
                    raise Exception("Collection not found")
            
            product.save()
            return UpdateProduct(product=product)
        except ObjectDoesNotExist:
            raise Exception("Product not found")

class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            product = Product.objects.get(pk=id)
            product.delete()
            return DeleteProduct(success=True)
        except ObjectDoesNotExist:
            raise Exception("Product not found")

# Adicionar as mutações ao schema
class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

# Atualizar o schema com as novas mutações
schema = graphene.Schema(query=Query, mutation=Mutation)