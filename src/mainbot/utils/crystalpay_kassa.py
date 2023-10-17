from .crystalpay_sdk import CrystalPAY, InvoiceType
from src.core.config import settings


class CrystalpayKassa:
    def __init__(self):
        self.crystalpayAPI = CrystalPAY(
            settings.CRYSTALPAY_LOGIN,
            settings.CRYSTALPAY_SECRET,
            settings.CRYSTALPAY_SALT,
        )

    def create_payment(self, pay_sum):
        return self.crystalpayAPI.Invoice.create(pay_sum, InvoiceType.purchase, 15)

    def check_payment(self, idpay):
        return self.crystalpayAPI.Invoice.getinfo(idpay)

    def get_ticker(self, arrname):
        return self.crystalpayAPI.Ticker.get(arrname)

    def get_info(self):
        return self.crystalpayAPI.Balance.getinfo(hide_empty=False)
