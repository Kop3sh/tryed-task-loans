# crispy-enigma

# SETUP

1. make sure that docker is installed and running
2. fill the .env file with relevant values
3. run `docker compse up --build -d`
4. run `docker exec -it crispy-enigma-web-1 sh`
5. run `python manage.py createsuperuser` to have access to db
6. open the web API on 127.0.0.1

# TODOS:

- [] test api endpoints and permissions
  - [x] create endpoint (any user can create loan request, serializer read-only fields)
  - [x] list all loan request (only admin can list all loan requests)
  - [x] retrieve single loan request detail (loan request owner or admin)
  - [x] update and delete (only loan request owner, only pending requests)
  - [x] approve/ reject loan request (admin only, cannot update other fields)
- [x] Github actions
- [x] deploy on railway
- [x] loan amortized schedule sheet
