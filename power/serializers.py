from .models import DemandReport
from rest_framework import serializers


class DemandReportSerializer(serializers.ModelSerializer):
    demand = serializers.ListField(write_only=True)
        
    class Meta:
        model = DemandReport
        fields = '__all__'
        read_only_fields = tuple(i.name for i in model._meta.fields)
        
    def create(self, validated_data):
        """
        If the object exists, update it, otherwise create it
        
        :param validated_data: The data that has been validated by the serializer
        :return: Nothing is being returned.
        """
        demand = validated_data.pop('demand')
        objs = DemandReport.objects.all()
        if not objs.exists():
            obj = DemandReport(**demand[0])
            obj.market_peak_day = True
            obj.market_peak_month = True
            obj.ontario_peak_day = True
            obj.ontario_peak_month = True
            obj.save()
            demand = demand[1:]

        for row in demand:
            try:
                obj = DemandReport.objects.get(date=row['date'], hour=row['hour'])
                obj.market_demand = row['market_demand']
                obj.ontario_demand = row['ontario_demand']
            except DemandReport.DoesNotExist:
                obj = DemandReport(**row)

            month = row['date'][:7]
            market_demand_day = DemandReport.objects.filter(
                date=row['date'], market_peak_day=True, market_demand__lte=row['market_demand'])
            ontario_demand_day = DemandReport.objects.filter(
                date=row['date'], ontario_peak_day=True, ontario_demand__lte=row['ontario_demand'])

            market_demand_month = DemandReport.objects.filter(
                date__startswith=month, market_peak_month=True, market_demand__lte=row['market_demand'])

            ontario_demand_month = DemandReport.objects.filter(
                date__startswith=month, ontario_peak_month=True, ontario_demand__lte=row['ontario_demand'])

            if market_demand_day.exists():
                obj.market_peak_day = True
                market_demand_day.update(market_peak_day=False)
            else:
                obj.market_peak_day = False
            
            if ontario_demand_day.exists():
                obj.ontario_peak_day = True
                ontario_demand_day.update(ontario_peak_day=False)
            else:
                obj.ontario_peak_day = False
            
            if market_demand_month.exists():
                obj.market_peak_month = True
                market_demand_month.update(market_peak_month=False)
            else:
                obj.market_peak_month = False
            
            if ontario_demand_month.exists():
                obj.ontario_peak_month = True
                ontario_demand_month.update(ontario_peak_month=False)
            else:
                obj.ontario_peak_month = False
            
            obj.save()

        return len(demand)
    
    def save(self, **kwargs):
        """
        This method is not being used.
        """
        return self.create(self.validated_data)