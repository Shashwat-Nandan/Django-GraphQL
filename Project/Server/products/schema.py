import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from django.db.models import Q
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id

from .models import Product, Store


class StoreType(DjangoObjectType):
    class Meta:
        model = Store

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class Query(graphene.ObjectType):
    stores = graphene.List(StoreType, search=graphene.String())
    store = graphene.Field(StoreType, id=graphene.Int())
    product = graphene.Field(ProductType, id=graphene.Int())
    productlist_by_store = graphene.Field(ProductType)
    products = graphene.List(ProductType, search=graphene.String())

    def resolve_stores(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(name__icontains=search)
            )
            return Store.objects.filter(filter)
        return Store.objects.all()

    def resolve_store(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Store.objects.get(pk=id)

        return None

    def resolve_productlist_by_store(self,info):
        user = info.context.user

        # if user.kind == "RETAILER"
        store = Store.objects.get(user=user)
        products = Product.objects.filter(store=store)

        # newList = [dict(storeProduct) for storeProduct in products]
        # newArr = list(products)

        return products[0]


    def resolve_product(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Product.objects.get(pk=id)

        return None

    def resolve_products(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(name__icontains=search)
            )
            return Product.objects.filter(filter)

        return Product.objects.all()




#Creating Store

class CreateStore(graphene.Mutation):
    user= graphene.Field(UserType)

    id = graphene.Int()
    name = graphene.String()
    slug = graphene.String()
    location_area = graphene.String()
    pin_code = graphene.Int()


    #2
    class Arguments:

        name = graphene.String()
        slug = graphene.String()
        location_area = graphene.String()
        pin_code = graphene.Int()


    #3
    def mutate(self, info, name, slug, location_area, pin_code):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You must be logged in to create Store!')

        store = Store(name=name, slug=slug, location_area=location_area, pin_code=pin_code, user=user)
        store.save()

        return CreateStore(
            id=store.id,
            name=store.name,
            slug=store.slug,
            location_area = store.location_area,
            pin_code = store.pin_code,
        )


#Creating Product
class CreateProduct(graphene.Mutation):
    store= graphene.Field(StoreType)
    user= graphene.Field(UserType)

    id = graphene.Int()
    name = graphene.String()
    # slug = graphene.String()
    sku_size = graphene.String()
    brand = graphene.String()
    description = graphene.String()
    price = graphene.Float()
    image = graphene.String()

    #2
    class Arguments:

        name = graphene.String()
        # slug = graphene.String()
        sku_size = graphene.String()
        brand = graphene.String()
        description = graphene.String()
        price = graphene.Float()



    #3
    def mutate(self, info, name, sku_size, brand, description,price):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You have to be logged in to do this operation')


        store = Store.objects.filter(user=user) #Returns a Queryset, so we will have to extract the value by taking the 0 index
        if not store:
            raise Exception('You are not authorized to do this operation')

        product = Product(name=name, sku_size=sku_size, brand=brand, description=description, price=price, store=store[0])
        product.save()

        return CreateProduct(
            id=product.id,
            store = store,
            name=product.name,
            # slug=product.slug,
            sku_size = product.sku_size,
            brand = product.brand,
            description = product.description,
            price = product.price,
        )

class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        # slug = graphene.String()
        sku_size = graphene.String(required=False)
        brand = graphene.String(required=False)
        description = graphene.String(required=False)
        price = graphene.Float(required=False)
        image = graphene.String(required=False)
        available = graphene.Boolean(required=False)

    def mutate(self, info, id, name, sku_size, brand, description, price, image, available):

        product = Product.objects.get(pk=from_global_id(id)[1])

        if name is not None:
            product.name = name

        if sku_size is not None:
            product.sku_size = sku_size

        if brand is not None:
            product.brand = brand

        if description is not None:
            product.description = description

        if price is not None:
            product.price = price

        if image is not None:
            product.image = image

        if available is not None:
            product.available = available
        product.save()

        return UpdateProduct(product=product)

class DeleteProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        id = graphene.ID(required=True)
        # newId = from_global_id(id)[1]


    def mutate(self, info, id):

        product = Product.objects.get(pk=from_global_id(id)[1])
        product.delete()

        return DeleteProduct(product=None)

#4
class Mutation(graphene.ObjectType):
    create_store = CreateStore.Field()
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
