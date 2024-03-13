import azure.functions as func
from api.app import application
from pathlib import Path
import logging

def main(req: func.HttpRequest, context: func.Context, db: bytes) -> func.HttpResponse:
    with open('/tmp/list.db', 'wb') as f:
#    with open('C:\\Users\\youruser\\Documents\\code\\tnl-list\\list.db', 'wb') as f:
        f.write(db)

    return func.WsgiMiddleware(application).handle(req, context)