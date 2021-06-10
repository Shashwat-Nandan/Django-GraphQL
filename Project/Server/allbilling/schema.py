import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType

from .models import BillingProfile



class BillingProfileType(DjangoObjectType):
    class Meta:
        model = BillingProfile

class Query(graphene.ObjectType):
    allBillingProfiles = graphene.List(BillingProfileType)
    billingprofile = graphene.Field(BillingProfileType, id=graphene.Int())

    def resolve_allBillingProfiles(self, info, **kwargs):
        return BillingProfile.objects.all()

    def resolve_billingprofile(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return BillingProfile.objects.get(pk=id)

        return None

class CreateBillingProfile(graphene.Mutation):
    user= graphene.Field(UserType)
    billingprofile = graphene.Field(BillingProfileType)

    class Arguments:

        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        address = graphene.String()
        city = graphene.String()
        postal_code = graphene.Int()

    def mutate(self, info, first_name, last_name, email, address, city, postal_code):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You must be logged in to create Orders!')


        billingprofile = BillingProfile(first_name=first_name, last_name=last_name, email=email,
                                    address=address, postal_code=postal_code, city=city, user=user)
        billingprofile.save()

        return CreateBillingProfile(billingprofile=billingprofile)



class Mutation(graphene.ObjectType):
    create_billingprofile = CreateBillingProfile.Field()
