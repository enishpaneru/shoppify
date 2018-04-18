from django.conf.urls import url
from django.contrib import admin

from . import views


urlpatterns = [
url(r'^$', views.index, name='index'),
 url(r'^dresses/$', views.DressListView, name='dresses'),
  url(r'^userdresses/$', views.DressListViewuser, name='user-dresses'),
    url(r'^owner/dresses/$', views.DressListViewowner, name='dressesowner'),
    url(r'^owner/types/$', views.TypeListViewowner, name='typesowner'),
    url(r'^owner/users/$', views.UsersListViewowner, name='users'),
url(r'^owner/$', views.ownerview, name='owner'),
 url(r'^dressessearch/$', views.DressListsearchView, name='dressessearch'),
  url(r'^imagesearch/$', views.imagesearchView, name='imagesearch'),
 url(r'^types/$', views.TypeListView, name='types'),
  url(r'^transactions/(?P<obj>\w+)$', views.transactionListView, name='transactions'),
  url(r'^rentinfos/$', views.rentinfoListView, name='rentinfo'),
  url(r'^transactionselect/$', views.transactionselectView, name='transactionselect'),
 url(r'^dress/(?P<pk>\d+)$', views.DressDetailView.as_view(), name='dress-detail'),
  url(r'^final/(?P<pk>\d+)$', views.final, name='final'),
url(r'^owner/dress/(?P<pk>\d+)$', views.DressDetailownerView.as_view(), name='dress-detail-owner'),
url(r'^user/dress/(?P<pk>\d+)$', views.DressDetailuserView, name='dress-detail-user'),

url(r'^owner/user/(?P<pk>\d+)$', views.UserDetailownerView.as_view(), name='user-detail-owner'),
url(r'^user/(?P<pk>\d+)$', views.UserDetailView, name='user-detail'),
url(r'^transaction/(?P<pk>\d+)$', views.transactionDetailView, name='transaction-detail'),

 url(r'^type/(?P<pk>\d+)$', views.TypeDetailView, name='type-detail'),
  url(r'^owner/type/(?P<pk>\d+)$', views.TypeDetailOwnerView, name='type-detail-owner'),
  url(r'^givebid/(?P<pk>\d+)$', views.givebid, name='givebid'),
url(r'^delete/(?P<pk>\d+)/(?P<obj>\w+)$', views.deleteobject, name='delete-object'),
url(r'^owner/adddress$', views.DressAdd, name='adddress'),
url(r'^owner/addType$', views.TypeAdd, name='addtype'),
url(r'^ordercomplete$', views.completeorder, name='ordercomplete'),
url(r'^orderconfirm$', views.confirmorder, name='orderconfirm'),

   url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

url(r'^owner/editdress/(?P<pk>\d+)$', views.DressEdit, name='editdress'),

]

urlpatterns += [
    url(r'^mydresses/$', views.LoanedDressesByUserListView, name='my-booked'),
        url(r'^mycart/$', views.mycart, name='my-cart'),
        url(r'^myprofile/$', views.myprofile, name='my-profile'),
        url(r'^myordered/$', views.myordered, name='my-ordered'),
]
urlpatterns += [

    url(r'^dress/(?P<pk>\d+)/book$', views.book_a_dress, name='to-book'),
]
urlpatterns += [

    url(r'^about$', views.about, name='about'),
    url(r'^showbid/(?P<pk>\d+)/$', views.showbid, name='showbid'),
]
urlpatterns += [

    url(r'^dress/(?P<pk>\d+)/buy$', views.buy_a_dress, name='to-buy'),
    url(r'^addtransaction/(?P<pk>\d+)$', views.addtransaction, name='addtransaction'),
]
urlpatterns += [
    url(r'^user/create/$', views.UserCreate.as_view(), name='user_create'),
    url(r'^user/(?P<pk>\d+)/update/$', views.UserUpdate.as_view(), name='user_update'),
    url(r'^userinfochange/$', views.userinfochange, name='userinfochange'),
    url(r'^user/(?P<pk>\d+)/delete/$', views.UserDelete.as_view(), name='user_delete'),
]
