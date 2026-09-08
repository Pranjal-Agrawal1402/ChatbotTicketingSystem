import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import serverless_wsgi  # noqa: E402
from app import create_app  # noqa: E402

flask_app = create_app()


def handler(event, context):
    return serverless_wsgi.handle_request(flask_app, event, context)
