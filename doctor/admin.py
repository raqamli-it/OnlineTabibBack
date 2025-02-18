from django.contrib import admin
from .models import DoctorHisob, DoctorTajriba

class DoctorHisobAdmin(admin.ModelAdmin):
    list_display = ('Oqigan_manzili', 'Oqigan_joyi_nomi', 'Yonalishi', 'Diplom_raqami', 'Diplom_fayli')
    search_fields = ('Oqigan_manzili', 'Oqigan_joyi_nomi')

class DoctorTajribaAdmin(admin.ModelAdmin):
    list_display = ('Ish_manzili', 'Ish_joyi_nomi', 'Ish_lavozimi', 'Ishga_kirgan_sanasi')
    search_fields = ('Ish_manzili', 'Ish_joyi_nomi')

admin.site.register(DoctorHisob, DoctorHisobAdmin)
admin.site.register(DoctorTajriba, DoctorTajribaAdmin)
