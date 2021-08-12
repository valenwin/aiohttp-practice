# Simple Microservice Example

## Requirements:
- Postgres >= 12.4
- Redis
- [Pyenv](https://github.com/pyenv/pyenv) is recommended

## Setup
### Copy config file and fill it with needed keys
```
$ cp local_example.yaml local.yaml
```
### Start project on your local machine
```
make setup
make run
```
## DB Migrations
### Create new db revision
```
make revision 
```
### Apply migrations
```
make db 
```
### Show migrations
```
make show
```
### Downgrade db migration
```
make downgrade
```
### Link to Swagger
```
/api-docs
```