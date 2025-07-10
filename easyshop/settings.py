TORTOISE_ORM = {
    "connections": {"default": "sqlite://easyshop.db"},
    "apps": {
        "models": {
            "models": ["models.models"],
            "default_connection": "default"
        }
    }
}
# Secret key for session management