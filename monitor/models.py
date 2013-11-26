from django.db import models

# Create your models here.

class Box(models.Model):
    ip = models.IPAddressField(max_length="200")
    box_name = models.CharField(max_length="200")
    
    class Meta:
        verbose_name_plural="boxes"
    
    def __unicode__(self):
        return self.ip
    
    
class Service(models.Model):
    service_name = models.CharField(max_length="250")
    daemon = models.CharField(max_length="250")
    service_port = models.IntegerField(max_length="200")
    box = models.ForeignKey(Box)
    
    class Meta:
        verbose_name_plural="services"
    
    def __unicode__(self):
        return self.service_name
    
