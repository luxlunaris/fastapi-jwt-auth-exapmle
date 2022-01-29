# FastAPI JWT auth example

Auth service built with FastAPI and deployed in Docker.

## Setup

From root repo folder:

`docker-compose up --build`

## Environment variables

Application uses bunch of environment variables, all of them should be placed in .env file inside root repo folder.

Database usage requires 3 environment variables:

1. USERS_PG_USER (postgreql username)
2. USERS_PG_PASS (postgreql password)
3. USERS_PG_DB (postgresql DB name)

Also, you should have following environment variables for JWT asymmetric algorithm usage in auth service:

1. JWT_SECRET_KEY (some secret string, might be hash, or might be 12MB string of your sins confession)
2. JWT_PUBLIC_KEY (RSA512 public key)
3. JWT_PRIVATE_KEY (RSA512 private key)

## Service availability

It is available at port 8001, documentation (Swagger) is available at /api endpoint.
However, please note that API test through swagger won't work correctly because one of cookies you get has to be sent as HTTP header.
You may test service with curl or watch autotests completion.

### Autotests

`docker-compose run --rm auth bash`

`pytest -vv --cov=app tests/`

### Debugging

There is remote debugger configured for VSCode. You can access debugging with:

`docker-compose -f docker-compose-debug.yml up`

then, go to VSCode and press F5. Put breakpoints and enjoy.
