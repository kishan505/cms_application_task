# cms_application_task

## Setup

Following documentation demonstrates installation and set up of cms application on Ubuntu system

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/kishan505/cms_application_task.git
$ cd cms_application_task
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```

Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `python3`.

Once `pip` has finished downloading the dependencies:

create superuser for access admin pannel

```sh
(venv)$ python manage.py createsuperuser
```

then run project

```sh
(venv)$ python manage.py runserver
```

Once the server is running, import CMS_application_postman_collection.json in POSTMAN

To open admin panel navigate to `http://127.0.0.1:8000/admin` Url.

## API Reference

#### User sign up

```http
  POST /sign_up
```

| Parameter          | Type     | Description                                      |
| :----------------- | :------- | :----------------------------------------------- |
| `username`         | `string` | **Required**. enter username                     |
| `email`            | `string` | **Required**. enter valid email address          |
| `password`         | `string` | **Required**. enter password must be 6 character |

#### User login

```http
  POST /login
```

| Parameter  | Type     | Description                       |
| :--------- | :------- | :-------------------------------- |
| `username` | `string` | **Required**. enter your username |
| `password` | `string` | **Required**. enter your password |

#### Create Post

```http
  POST /create_post
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |

| Parameter       | Type      | Description                              |
| :-------------- | :-------- | :--------------------------------------- |
| `title`       | `string` | **Required**. enter title for post |
| `description` | `string`    | **Required**. enter description for post |
| `content`      | `string`  | **Required**. enter content for post |
| `author_id`   | `integer`  | **Required**. enter author_id for get user |
| `is_public_post`   | `string`  | enter is_public_post true or false for post public or not Default: Public |


#### Update Post

```http
  PUT /update_post
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |

| Parameter       | Type      | Description                              |
| :-------------- | :-------- | :--------------------------------------- |
| `post_id`       | `integer` | **Required**. enter post_id to fetch post |
| `title`       | `string` | enter title for update post |
| `description` | `string`    | enter description for update post |
| `content`      | `string`  | enter content for update post |
| `is_public_post`   | `string`  | enter is_public_post true or false for update post|

#### Delete Post

```http
  DELETE /delete_post
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |

| Parameter       | Type      | Description                              |
| :-------------- | :-------- | :--------------------------------------- |
| `post_id`       | `integer` | **Required**. enter post_id to delete post |

#### Get Post By Id

```http
  GET /get_post_by_id
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |

| Parameter       | Type      | Description                              |
| :-------------- | :-------- | :--------------------------------------- |
| `post_id`       | `integer` | **Required**. enter post_id to get post |


#### User All Posts

```http
  GET /user_all_posts
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |


#### Get All Posts

```http
  GET /get_all_posts
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |

#### Post Like or Dislike

```http
  POST /post_like_dislike
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |

| Parameter       | Type      | Description                              |
| :-------------- | :-------- | :--------------------------------------- |
| `post_id`       | `integer` | **Required**. enter post_id to get post |


#### Update Profile

```http
  PUT /update_profile
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |

| Parameter          | Type     | Description                                      |
| :----------------- | :------- | :----------------------------------------------- |
| `email`            | `string` | enter email for update |
| `mobile_no`        | `string` | enter valid Mobile No |
| `city`             | `string` | enter city name |
| `country`          | `string` | enter country name |


#### Delete Profile

```http
  DELETE /delete_profile
```

| Request Headers            | Description                |
| :--------------------------| :------------------------- |
| `Authorization`            | Token {your-token}         |

| Parameter          | Type     | Description                                      |
| :----------------- | :------- | :----------------------------------------------- |
| `user_id`          | `integer` | **Required**. enter user_id for delete user |

