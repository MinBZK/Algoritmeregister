
# Steps to migrate from current system to keycloak API with multiple roles, organisations
## Scripts for keycloak
### Prepare keycloak with roles & groups attributes
The `roles` and `groups` attributes are used to store role and group data for each user. This needs to be reported in the token, such that the backend can identify the user properly.

1. go to `Clients` -> `authentication-client` in Keycloak
2. go to `client scopes` -> `authentication-client-dedicated`
3. `Add mapper` -> `By configuration` -> `User Attribute`
4. `Name`, `User Attribute` and `Token Claim Name`: enter all these fields with `roles`
5. All switches are `true` except for `Add to lightweight acces token`.

- Repeat these steps for the `groups` attribute

### Migrate group memberships to 'groups' attribute
Run script to
1. Get members for each group
2. Update those user to retrieve that group as an attribute.

`python -m scripts.keycloak_migration_groups`

### Migrate role to roles attribute
Run script to 
1. retrieve all users, 
2. update their `role` to `roles` attribute.

`python -m scripts.keycloak_migration_roles`

## PostgreSQL scripts
### Prepare the organisation table for new system
Run script to
1. retrieve all groups,
2. Report on missing organisations.

`python -m scripts.database_migration_groups`


### Migrate to new publication flow system
Run script to
1. Update flow column based on 'released' and 'published' column.

`python -m scripts.database_migration_state`


### Migrate action history to new names for actions
Run script to
1. Update the operation names to new ones, namely removing 'released' and replacing it with 'state-update'

### Remove old and unused mappers (only when you know this keycloak realm is no longer used in the old fashion).
- Remove `role` & `group` mapper 
- Remove `released` & `published` columns


