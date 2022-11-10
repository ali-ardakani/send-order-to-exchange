# Simulator project of sending an order to the exchange
This project is a simulator of sending an order to the exchange.

## How to run
1. Install [Docker](https://docs.docker.com/install/)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)
3. Run `docker-compose up --build` in the project root directory

## How to use
### Send an order
1. Login to the simulator
2. Send an order to /order/ endpoint

Note: The order will be sent to the exchange when the total value of orders for the symbol is greater than 10$.

## Notes
- The project is written in [Python](https://www.python.org/) and uses [Django](https://www.djangoproject.com/) framework.
- The project uses [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) for development and deployment.
- The project uses [PostgreSQL](https://www.postgresql.org/) as a database.


