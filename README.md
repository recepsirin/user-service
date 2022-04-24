# User Service
### Tech Stack 
* #### Python >= 3.7
* #### Django & DRF
* #### PostgreSQL
* #### Docker

---

### Install & Run


Build service 
```bash
docker-compose build
```

Run it
```bash
docker-compose up -d
```


---

## API Documentation

* [POST] /api/v1/users/
* [GET] /api/v1/users
* [DELETE] /api/v1/users/
* [POST] /api/v1/users/<int:id>/contact/
* [GET] /api/v1/users/<int:id>/contact
* [PUT] /api/v1/users/<int:id>/contact/
* [GET] /api/v1/users/<int:id>/contact/email/<int:id>
* [GET] /api/v1/users/<int:id>/contact/phone-number/<int:id>

#### [POST] /api/v1/users/
Create new user with contact info
```bash
{
    "lastname": "", # required 
    "firstname": "", # required
    "emails": [..], # required
    "phonenumbers": [..] # required
}
```

#### [GET] /api/v1/users
Get all users [can be filtered via id and firstname as demanded]

```bash
[ # an illustration of return data
    ...
    {
        "id": 6,
        "lastname": "",
        "firstname": "",
        "emails": [..],
        "phonenumbers": [..]
    },
    ...
]
```


#### [DELETE] /api/v1/users/
Delete a user
```bash
{
  "id": 1 # required 
}
```

#### [POST] /api/v1/users/<int:id>/contact/
Add additional contact info to a user
```bash
{
    "email": "example@domain.com", # required
    "phone_number": "+90 555 555 55 55" # required
}
```

#### [GET] /api/v1/users/<int:id>/contact
Get a user
```bash
{ # an illustration of return data
    "id": 15,
    "lastname": "",
    "firstname": "",
    "emails": {
        "15": "",
        "100": ""
    },
    "phonenumbers": {
        "15": "",
        "100": ""
    }
}
```

#### [PUT] /api/v1/users/<int:id>/contact/
Update a user's contact info
```bash
{
    "emails": ["..", ... ], # required
    "phonenumbers": ["..", ".."] # required
}
```

#### [GET] /api/v1/users/<int:id>/contact/email/<int:id>
Get a specific email of a user
```bash
{ # an illustration of return data
    "email": ""
}
```

#### [GET] /api/v1/users/<int:id>/contact/phone-number/<int:id>
Get a specific phone number of a user
```bash
{ # an illustration of return data
    "number": ""
}
```
