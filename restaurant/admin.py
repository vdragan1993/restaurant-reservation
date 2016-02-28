from django.contrib import admin
from .models import Restaurant, MenuItem, Table, Guest, Manager, Friendship, Reservation, ReservedTables, Visit


admin.site.register(Restaurant)
admin.site.register(MenuItem)


# changing order of fields for tables
class TableAdmin(admin.ModelAdmin):
    fields = ['restaurant', 'number', 'row', 'column', 'currently_free']

admin.site.register(Table, TableAdmin)

admin.site.register(Guest)
admin.site.register(Manager)
admin.site.register(Friendship)


# changing order of fields for reservation
class ReservationAdmin(admin.ModelAdmin):
    fields = ['guest', 'restaurant', 'coming', 'duration']

admin.site.register(Reservation, ReservationAdmin)

admin.site.register(ReservedTables)


# changing order of fields for visit
class VisitAdmin(admin.ModelAdmin):
    fields = ['guest', 'reservation', 'ending_time', 'confirmed', 'grade']

admin.site.register(Visit, VisitAdmin)
