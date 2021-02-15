from datetime import date, datetime

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat(sep=' ')
        if isinstance(obj, date):
            return obj.isoformat()

        return JSONEncoder.default(self, obj)
