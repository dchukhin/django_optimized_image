from django.db import models


class OptimizedNotOptimized(models.Model):
    instance_model = models.CharField(max_length=100)
    instance_pk = models.IntegerField()
    field_name = models.CharField(max_length=100)
    url = models.URLField()
    optimized_url = models.URLField()

    def __str__(self):
        return "{} pk {} optimized field {}".format(self.instance_model, self.instance_pk, self.field_name)
