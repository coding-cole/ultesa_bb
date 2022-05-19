USERS = "users"
POSTS = "posts"

USERS_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["email", "first_name", "middle_name", "last_name", "school", "department" "gender", "phone_number",
                     "username", "password", "profile_img", "verified", "following", "followers", "posts"],
        "properties": {
            "email": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "first_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "middle_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "last_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "school": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "department": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "gender": {
                "enum": ["m", "f"],
                "description": "must be 'm' or 'f  and is required"
            },
            "phone_number": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "password": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "profile_img": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "verified": {
                "bsonType": "boolean",
                "description": "must be a boolean and is required"
            },
            "following": {
                "bsonType": "array",
                "description": "must be a array and is required"
            },
            "followers": {
                "bsonType": "array",
                "description": "must be a array and is required"
            },
            "posts": {
                "bsonType": "array",
                "description": "must be a array and is required"
            }
        }
    }
}

POSTS_VALIDATOR = {

}
