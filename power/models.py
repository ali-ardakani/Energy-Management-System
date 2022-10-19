from django.db import models

class DemandReport(models.Model):
    date = models.CharField(max_length=10)
    hour = models.IntegerField()
    market_demand = models.IntegerField()
    ontario_demand = models.IntegerField()
    market_peak_day = models.BooleanField()
    ontario_peak_day = models.BooleanField()
    market_peak_month = models.BooleanField()
    ontario_peak_month = models.BooleanField()

    class Meta:
        ordering = ['date', 'hour']