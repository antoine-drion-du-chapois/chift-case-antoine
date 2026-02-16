import xmlrpc.client
from datetime import datetime
import socket
from app.core.config import settings
from app.schema.invoice import OdooInvoice
from app.schema.partners import OdooPartner
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

RETRYABLE_EXCEPTIONS = (
    socket.timeout,
    ConnectionError,
    xmlrpc.client.ProtocolError,
    xmlrpc.client.Fault,
)


def _get_uid():
    common = xmlrpc.client.ServerProxy(
        f"{settings.ODOO_URL}/xmlrpc/2/common",
        allow_none=True
    )

    uid = common.authenticate(
        settings.ODOO_DB,
        settings.ODOO_USERNAME,
        settings.ODOO_PASSWORD,
        {}
    )

    if not uid:
        raise Exception("Odoo authentication failed")

    return uid


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    reraise=True,
)
def _fetch_generic(model: str, last_sync: datetime, fields: list[str]):
    uid = _get_uid()

    models = xmlrpc.client.ServerProxy(
        f"{settings.ODOO_URL}/xmlrpc/2/object",
        allow_none=True
    )

    domain = [
        ("write_date", ">", last_sync.strftime("%Y-%m-%d %H:%M:%S"))
    ]

    return models.execute_kw(
        settings.ODOO_DB,
        uid,
        settings.ODOO_PASSWORD,
        model,
        "search_read",
        [domain],
        {
            "fields": fields,
            "context": {"active_test": False},
        },
    )
