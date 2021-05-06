import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from products.schema import ProductType

from .models import Cart, CartItem

from products.models import Product


class CartType(DjangoObjectType):
    class Meta:
        model = Cart

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem

class Query(graphene.ObjectType):
    carts = graphene.Field(CartType)
    cartitems = graphene.List(CartItemType)

    def resolve_carts(self, info, **kwargs):
        user = info.context.user

        if not user.is_authenticated:
           raise GraphQLError('User is not authenticated')
        return user.cart

    def resolve_cartitems(self,info):
        return CartItem.objects.all()

class CreateCart(graphene.Mutation):
    user= graphene.Field(UserType)
    product = graphene.Field(ProductType)
    cart = graphene.Field(CartType)
    cartitems = graphene.Field(CartItemType)

    class Arguments:
        quantity = graphene.Int()
        id = graphene.ID(required=True)

    def mutate(self, info, id, quantity):
        user = info.context.user
        product = Product.objects.get(pk=id)


        cart = cart.objects.create(user=user)

        # if (cart.DOESNOTEXIST):
        #     cart = Cart.objects.create(user=user)

        cartitems = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return CreateCart(cart=cart, cartitems=cartitems)



class Mutation(graphene.ObjectType):
    create_cart = CreateCart.Field()
