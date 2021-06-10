import graphene
import graphql_jwt

import products.schema
import users.schema

# Importing Product Relay schema
import products.schema_relay

# Import Cart SCHEMA
import cart.schema

# Import Order Schema
import neworders.schema

import allbilling.schema



class Query(users.schema.Query, products.schema.Query, cart.schema.Query, neworders.schema.Query, allbilling.schema.Query, products.schema_relay.RelayQuery, graphene.ObjectType):
    pass

# class Query(users.schema.Query, graphene.ObjectType):
#     pass

class Mutation(users.schema.Mutation, products.schema.Mutation, neworders.schema.Mutation, cart.schema.Mutation,allbilling.schema.Mutation,products.schema_relay.RelayMutation,graphene.ObjectType,):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation= Mutation)
