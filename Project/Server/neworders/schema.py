import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from products.schema import ProductType
from cart.schema import CartItemType
from allbilling.schema import BillingProfileType

from .models import Order, OrderItem
from cart.models import Cart, CartItem
from allbilling.models import BillingProfile

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class Query(graphene.ObjectType):
    allorders = graphene.List(OrderType)
    order = graphene.Field(OrderType, id=graphene.Int())
    orderitems = graphene.List(OrderType)

    def resolve_allorders(self, info, **kwargs):
        return Order.objects.all()

    def resolve_order(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Order.objects.get(pk=id)

        return None

    def resolve_orderitems(self, info, **kwargs):
        return OrderItem.objects.all()


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem




# Creating Orders

class CreateOrder(graphene.Mutation):
    user= graphene.Field(UserType)
    product = graphene.Field(ProductType)
    order = graphene.Field(OrderType)
    cartitems = graphene.Field(CartItemType)
    orderitem = graphene.Field(OrderItemType)
    billingprofile = graphene.Field(BillingProfileType)


    class Arguments:

        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You must be logged in to create Orders!')

        cart = Cart.objects.get(user=user)

        cartitems = CartItem.objects.filter(cart=cart)

        if cartitems.count() != 0:
            # order = Order(first_name=first_name, last_name=last_name, email=email,
            #                             address=address, postal_code=postal_code, city=city, user=user)
            # order.save()
            billingprofile = BillingProfile.objects.get(pk=id)
            order = Order(user=user, billingprofile=billingprofile)
            for item in cartitems:
            # orderitem = OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])
             orderitem = OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
             cartitems.delete()

        else:
            raise Exception('You Cart is empty')


        return CreateOrder(order=order, orderitem=orderitem)

class UpdateOrder(graphene.Mutation):
    user= graphene.Field(UserType)

    order = graphene.Field(OrderType)

    class Arguments:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        address = graphene.String()
        city = graphene.String()
        postal_code = graphene.Int()

    def mutate(self, info, id, first_name, last_name, email, address, city, postal_code):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You must be logged in to create Orders!')

        order = Order.objects.get(pk=id)

        if first_name is not None:
            order.first_name = first_name

        if last_name is not None:
            order.last_name = last_name

        if email is not None:
            order.email = email

        if address is not None:
            order.address = address

        if city is not None:
            order.city = city

        if postal_code is not None:
            order.postal_code = postal_code
        order.save()

        return UpdateOrder(order=order)

class DeleteOrder(graphene.Mutation):
    user= graphene.Field(UserType)

    order = graphene.Field(OrderType)

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You must be logged in to create Orders!')

        order = Order.objects.get(pk=id)
        order.delete()

        return DeleteOrder(order=None)

# class createOrderItem(graphene.Mutation):
#     product = graphene.Field(ProductType)
#     order = graphene.Field(OrderType)
#
#     orderitem = graphene.Field(OrderItemType)
#
#     class Arguments:
#         quantity = graphene.Int()
#
#
#     def mutate(self,info,quantity, order, product):
#         order = info.context.order
#
#         orderitem = OrderItem.objects.create(quantity=quantity, order=order, product=product)
#
#         return createOrderItem(orderitem=orderitem)

class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    # create_order_item = createOrderItem.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()
