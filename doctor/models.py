from django.db import models

class DoctorHisob(models.Model):
    Oqigan_manzili  = models.CharField(max_length=100)
    Oqigan_joyi_nomi = models.CharField(max_length=100)
    Yonalishi = models.CharField(max_length=100)
    Diplom_raqami = models.CharField(max_length=20)
    Diplom_fayli = models.FileField()




class DoctorTajriba(models.Model):
    Ish_manzili = models.CharField(max_length=100)
    Ish_joyi_nomi = models.CharField(max_length=100)
    Ish_lavozimi = models.CharField(max_length=100)
    Ishga_kirgan_sanasi = models.IntegerField()
    