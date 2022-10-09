# nork-town
I will write a description later


# What I did
- [x] Setup dev environment with docker (using vs-code remote-containers, but you can use raw docker-compose)
- [x] Using docker compose with as many volumes as it takes
- [x] Using Python's Flask Framework and any other library
- [x] Use any SQL Database (using Postgres)
- [x] Secure routes (there is a register/login route, where you can get a token to use in other requests)
- [x] Write tests
- [x] Doc with swagger
- [x] Use migrations to database versioning

# How to run:

```bash
  $ git clone https://github.com/WalyssonPaiva/nork-town
  $ cd nork-town
  
  # Using vs-code remote containers (recommended)
  # Install on vscode: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
  # Use: CTRL + SHIFT + P to open command palette and type ">dev Containers: Rebuild and Reopen in Container"
  # your dev environment are up, just run migrations with "make migrations" then migrate to db with "make migrate"

  # Using docker-compose
  $ docker-compose up -d
  $ docker exec -it CONTAINER_NAME bash
  $ make migrations
  $ make migrate
```
# Documentation
- Go to route /apidocs (ex: 127.0.0.1:5000/apidocs)
