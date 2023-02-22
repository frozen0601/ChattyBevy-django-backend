# ChattyBevy-django-backend
A Back End Coding Test Project.

Here is the [Kanban board](https://github.com/users/frozen0601/projects/1) for tracking this project.

**Commits in this branch are constrained to work with [ChattyBevy-frontend](https://github.com/frozen0601/ChattyBevy-frontend). For further changes that might alter the JSON response, such as the paginated JSON response for returning messages, are commited to the branch [structuralChanges](https://github.com/frozen0601/ChattyBevy-django-backend/tree/structuralChanges)**

## Setup
1. Clone the project
2. Move to the project file
    
    - `cd ChattyBevy-django-backend/`
3. Create and activate a virtual environment

    - `python -m venv venv` or `python3 -m venv venv`
    
    - `source venv/bin/activate`
4. Install the requirements
    - `pip install -r requirements.txt`
    
5. Move to the django project file
    
    - `cd bevyApi/`

6. Run the server
    
    - `python manage.py runserver`
    
## APIs
The project's APIs are setup to run at localhost on port 8000.
The APIs can be seperated into three parts, **User Management**, **JWT authentication**, and **Messaging**.

### User Management
The User Management APIs leverages Tivix's repo [django-rest-auth](https://github.com/Tivix/django-rest-auth), which makes it extremely easy to manage user accounts.

- [POST] Login `/rest-auth/login/`
    - required fields:
        ```json
        {
            "username": "",
            "email": "",
            "password": ""
        }
        ```
        *choose one between username and email
        
   - return fields:
        ```json
        {
            "key": ""
        }
        ```

- [POST] Register `/rest-auth/registration/`
    - required fields:
        ```json
        {
            "username": "",
            "email": "",
            "password1": "",
            "password2": ""
        }
        ```
   - return fields:
        ```json
        {
            "key": ""
        }
        ```

    
### JWT authentication
Django REST framework comes with authentication methods such as session/token authentication. Yet, there are some benefits of using JWT authentication.

`
JWT authentication is good because it allows for stateless, secure transmission of information between client and server.
JWT tokens can be signed and encrypted for added security. They are also compact, allowing for efficient storage and transfer.
This makes JWT a suitable choice for RESTful API authentication.
` - openGPT

The APIs provided by [SimpleJWT](https://github.com/SimpleJWT/drf-SimpleJWT-React) is used to provide the required authentication services.

- [POST] Get tokens `/api/token/`
    - required fields:
        ```json
        {
            "username": "",
            "email": ""
        }
        ```
    - return fields:
        ```json
        {
            "refresh": "",
            "access": ""
        }
        ```
    
- [POST] Get refresh token `/api/token/refresh/`
    - required fields:
        ```json
        {
            "refresh": ""
        }
        ```
   - return fields:
        ```json
        {
            "refresh": ""
        }
        ```

### Messaging


- [GET] Get established contacts (room) `/messaging/room/`

   - return fields:
        ```json
        {
            "count": int,
            "next": href,
            "previous": href,
            "results": [
                {
                    "id": int,
                    "user1": str,
                    "user2": str
                },
            ]
        }
        ```

- [GET] Get chat room `/messaging/room/{room_id}`
   - return fields:
        ```json
        [
            {
                "id": int,
                "room_id": int,
                "sender": str,
                "recipient": str,
                "title": str,
                "body": str,
                "created_at": datetime
            },
        ]
        ```
    
- [POST] Send message `/messaging/room/{room_id}/message/`
    - required fields:
        ```json
        {
            "sender": str,
            "recipient": str,
            "title": str,
            "body": str
        }
        ```
   - return fields:
        ```json
        {
            "id": int,
            "room_id": int,
            "sender": str,
            "recipient": str,
            "title": str,
            "body": str,
            "created_at": str
        }
        ```

- [DELETE] Delete message `/messaging/room/{room_id}/message/{message_id}/`
    - return fields:
        ```json
            "message": {
            "message": "Item deleted successfully"
        }
        ```

 ## Features
 **Pagination, Throttling, Caching, and CORS** are the new terms/knowledge I picked up in this project.
 
 **Throttling** has been enabled throughout the APIs.
 
 **Caching** is used for storing user login session (JWT tokens).
 
 **Pagination** is applied on `/messaging/room/` but has not been done on `/messaging/room/{room_id}` yet.
 
 **Access Control** on composing/viewing/deleting messages should be protected thoroughly.
 
 **Uniform Error Return** is managed by an api exception handler.
 
 
 ## TODOs & notes & learned
 ### TODO Features
  - Applies pagination thoroughly.
  
 ### TODO Refactor
 - ~~Refactor code to handle malicious inputs.~~
    -  ~~POST with fields/fields value altered~~
    -  ~~Malformed hidden field~~
 - ~~Refactor message composing mechanism.~~
    ~~The current code check if room exists whenever a message is sent. Refactor it as:~~
        
    ```python
    if "room_id" not in request.POST:
        roomID = _createRoom(userA, userB)
    _composeMessage(roomID, message, ...)
    ```
        
 ### TODO Bug Fix
 - ~~Fix a bug related to deleting user.~~
 
 ### Others
 - Unit testing.
 - [freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/)
 - Database views
 - ...

Refer to the [Kanban board](https://github.com/users/frozen0601/projects/1) for more details on project status.
