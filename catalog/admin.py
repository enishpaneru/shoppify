from django.contrib import admin

# Register your models here.
from .models import Type, Dress, booking, DressInstance,Order,OrderDetail,UserDetail,transaction,rentinfo

#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(Type)

#admin.site.register(BookInstance)
# Define the admin class
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name','type_pic')
    fields = ['name','type_pic','detail']

# Register the admin class with the associated model
admin.site.register(Type, TypeAdmin)

# Register the Admin classes for Book using the decorator
class transactionAdmin(admin.ModelAdmin):
    list_display = ('renter','dress')
    fields = ['renter','dress']
admin.site.register(transaction, transactionAdmin)
class rentinfoAdmin(admin.ModelAdmin):
    list_display = ('fine','insuranceclaimstatus')
    fields = ['fine','insuranceclaimstatus']
admin.site.register(rentinfo, rentinfoAdmin)
# Register the admin class with the associated model




class DressAdmin(admin.ModelAdmin):
    list_display = ('name', 'type','pk')
    class DressInstanceInline(admin.TabularInline):
        model = DressInstance
    inlines = [DressInstanceInline]

admin.site.register(Dress, DressAdmin)

# Register the Admin classes for BookInstance using the decorator


class DressInstanceAdmin(admin.ModelAdmin):
    list_display = ('dress',  'id')
    fieldsets = (
        (None, {
            'fields': ('dress','imprint', 'id')
        }),
    )
admin.site.register(DressInstance, DressInstanceAdmin)
class bookingAdmin(admin.ModelAdmin):
    list_display = ('dress',  'user','bookdate')
    fieldsets = (
        (None, {
            'fields': ('user','dress','booknovalue')
        }),
    )
admin.site.register(booking, bookingAdmin)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',  'orderdate','active')

admin.site.register(Order, OrderAdmin)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('dress',  'orderno','orderuser')

admin.site.register(OrderDetail, OrderDetailAdmin)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user',  'location')

admin.site.register(UserDetail, UserDetailAdmin)
