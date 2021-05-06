import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Product, Store


#1
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'description', 'brand']


#2
class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        #3
        interfaces = (graphene.relay.Node, )


class StoreNode(DjangoObjectType):
    class Meta:
        model = Store
        interfaces = (graphene.relay.Node,)


class RelayQuery(graphene.ObjectType):
    #4
    relay_product = graphene.relay.Node.Field(ProductNode)
    #5
    relay_products = DjangoFilterConnectionField(ProductNode, filterset_class=ProductFilter)


class RelayCreateProduct(graphene.relay.ClientIDMutation):
    product = graphene.Field(ProductNode)

    class Input:
        name = graphene.String()
        slug = graphene.String()
        sku_size = graphene.String()
        brand = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        image = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You have to be logged in to do this operation')


        store = Store.objects.filter(user=user) #Returns a Queryset, so we will have to extract the value by taking the 0 index
        if not store:
            raise Exception('You are not authorized to do this operation')

        product = Product(name=input.get('name'), slug=input.get('slug'),
                        sku_size=input.get('sku_size'), brand=input.get('brand'),
                        description=input.get('description'), price=input.get('price'), image= input.get('image'), store=store[0])
        product.save()

        return RelayCreateProduct(product= product)


class RelayMutation(graphene.AbstractType):
    relay_create_product = RelayCreateProduct.Field()
