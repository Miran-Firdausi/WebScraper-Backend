from django.db import models


class ScrapedData(models.Model):
    job_id = models.UUIDField()
    coin_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    price_change = models.DecimalField(max_digits=20, decimal_places=10)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap_rank = models.IntegerField()
    volume = models.DecimalField(max_digits=20, decimal_places=2)
    volume_rank = models.IntegerField()
    volume_change = models.DecimalField(max_digits=10, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2)
    total_supply = models.DecimalField(max_digits=20, decimal_places=2)
    diluted_market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    contracts = models.JSONField()
    official_links = models.JSONField()
    socials = models.JSONField()

    def __str__(self):
        return str(self.coin_name) + " - " + str(self.job_id)

