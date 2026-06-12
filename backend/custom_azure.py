from storages.backends.azure_storage import AzureStorage
from clearance import settings

class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.STORAGE_ACCOUNT_KEY
    azure_container = 'media'
    expiration_secs = 3600
    
    def url(self, name, expire=None):
        if expire is None:
            expire = self.expiration_secs
        return super().url(name, expire)

class AzureStaticStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.STORAGE_ACCOUNT_KEY
    azure_container = 'static'
    expiration_secs = None