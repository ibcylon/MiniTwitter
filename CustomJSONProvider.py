from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        # Safely handle sets by converting them to lists
        if isinstance(obj, set):
            return list(obj)
        # Delegate encoding to the parent class for other types
        return super().default(obj)