from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SuperuserRequiredMixin
# Create your views here.
from .models import Dress, Type, DressInstance,booking,Order,OrderDetail,UserDetail,transaction,rentinfo,tempimage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
import cv2
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import tensorflow as tf
import operator
from threading import Thread
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .newim import PreProcessing
from .project import FeatureExtraction
from .test import use_neural_network,train_neural_network
from .forms import BookDressForm,AddDressForm,UserCreateForm,AddTypeForm,BuyDressForm,UserinfoChangeForm,SignupForm,AddTransactionForm,AddFinalForm
def new_thread(idno):
    m1=get_object_or_404(Dress,pk=idno)
    image=m1.dress_pic.url
    imageurl= 'project'+image

    img = cv2.imread(imageurl,0)

    raw_data=[]
    raw_data += [cv2.resize(img, (30, 30), interpolation=cv2.INTER_AREA)]

    obj = PreProcessing()
    data=obj.convert_data(raw_data)
    index=use_neural_network(data)
    print (index[0])
    print (index[1])
    m1.search_index=index[0]
    m1.search_indexval=index[1]

    print(m1.search_index)
    print(m1.search_indexval)
    m1.save()


def index(request):
    """
    View function for home page of site.
    """

    return render(
        request,
        'index.html'

    )
def about(request):
    """
    View function for home page of site.
    """

    return render(
        request,
        'about.html'

    )
from django.views import generic

def DressListView(request):
    page = request.GET.get('page', 1)
    print(page)
    search =request.GET.get('searchvalue',None)
    print(search)
    if "search"  in request.GET or search != None :
        if search != None:
            searchval = search
        else:
            searchval=request.GET['search']
        print("in search")
        print (searchval)


        dresslist= Dress.objects.filter((Q(name__icontains=searchval)|Q(type__name__icontains=searchval))&Q(active=True))
        paginator = Paginator(dresslist,8)
        try:
            dress_list = paginator.page(page)
        except PageNotAnInteger:
            dress_list = paginator.page(1)
        except EmptyPage:
            dress_list = paginator.page(paginator.num_pages)
        return render(request, 'catalog/dress_list.html', {'dress_list': dress_list,'searchvalue':searchval})

    else:

        dresslist= Dress.objects.filter(active=True)
        paginator = Paginator(dresslist,8)

        try:
            dress_list = paginator.page(page)
        except PageNotAnInteger:
            dress_list = paginator.page(1)
        except EmptyPage:
            dress_list = paginator.page(paginator.num_pages)
        return render(request, 'catalog/dress_list.html', {'dress_list': dress_list})
def DressListViewuser(request):
    page = request.GET.get('page', 1)


    if "search" in request.GET:

        dresslist= Dress.objects.filter(Q(name__icontains=request.GET["search"])|Q(type__name__icontains=request.GET["search"]))
        paginator = Paginator(dresslist,8)
        try:
            dress_list = paginator.page(page)
        except PageNotAnInteger:
            dress_list = paginator.page(1)
        except EmptyPage:
            dress_list = paginator.page(paginator.num_pages)
        return render(request, 'catalog/dress_list_user.html', {'dress_list': dress_list,'searchvalue':request.GET["search"]})

    else:

        dresslist= Dress.objects.filter(user=request.user)
        paginator = Paginator(dresslist,8)

        try:
            dress_list = paginator.page(page)
        except PageNotAnInteger:
            dress_list = paginator.page(1)
        except EmptyPage:
            dress_list = paginator.page(paginator.num_pages)
        return render(request, 'catalog/dress_list_user.html', {'dress_list': dress_list})
def DressListsearchView(request):
    page = request.GET.get('page', 1)

    image=request.FILES.get('image')
    m1=tempimage(dress_pic=image)
    m1.save()
    imageurl= 'project'+m1.dress_pic.url

    img = cv2.imread(imageurl,0)


    raw_data=[]
    raw_data += [cv2.resize(img, (30, 30), interpolation=cv2.INTER_AREA)]

    obj = PreProcessing()
    data=obj.convert_data(raw_data)
    index=use_neural_network(data)
    print (index[0])
    new = index[1]

    m1.delete()
    dressdict={}
    sortedlist=[]
    dresslist= Dress.objects.filter(Q(search_index=index[0])).order_by('search_indexval')
    for x in dresslist:
        dressdict[x]=abs(new-x.search_indexval)
    print (dressdict)
    dressdict=sorted(dressdict.items(),key=operator.itemgetter(1))
    print (dressdict)
    for value in dressdict:
        sortedlist.append(value[0])
    paginator = Paginator(dresslist,8)
    dress_list = paginator.page(page)
    return render(request, 'catalog/dress_list_search.html', {'dress_list': sortedlist})

def imagesearchView(request):

    return render(request, 'catalog/imageupload.html',)

def TypeListView(request):
    page = request.GET.get('page',1)
    if "search" in request.GET:

        typelist= Type.objects.filter(name__icontains=request.GET["search"])
        paginator = Paginator(typelist,8)
        try:
            type_list = paginator.page(page)
        except PageNotAnInteger:
            type_list = paginator.page(1)
        except EmptyPage:
            type_list = paginator.page(paginator.num_pages)

    else:
        typelist= Type.objects.all()
        paginator = Paginator(typelist,8)
        try:
            type_list = paginator.page(page)
        except PageNotAnInteger:
            type_list = paginator.page(1)
        except EmptyPage:
            type_list = paginator.page(paginator.num_pages)

    return render(request, 'catalog/type_list.html', {'type_list': type_list})
def transactionListView(request,obj):

    if obj=="active":
        transactionlist= transaction.objects.filter(Q(active=True)&Q(completion=False))
    if obj=="notactive":
        transactionlist= transaction.objects.filter(Q(active=False)&Q(completion=False))

    return render(request, 'catalog/transaction_list.html', {'transaction_list': transactionlist})
def rentinfoListView(request):


    rentinfolist= rentinfo.objects.filter()


    return render(request, 'catalog/rentinfo_list.html', {'rentinfo_list': rentinfolist})
def transactionselectView(request):


    return render(request, 'catalog/transaction_select.html')
class DressDetailView(generic.DetailView):
    model = Dress
class DressDetailownerView(SuperuserRequiredMixin,generic.DetailView):
    model = Dress
    template_name = 'catalog/dress_detailowner.html'
def DressDetailuserView(request,pk):
    dress = get_object_or_404(Dress,pk=pk)
    if request.method=="POST":
        if request.POST["activestatus"]=="SetActive":
            dress.active=True
            transact.save()


        if request.POST["activestatus"]=="SetInactive":
            dress.active=False
            dress.save()
    return render(request,'catalog/dress_detailuser.html',{'dress':dress})
class UserDetailownerView(SuperuserRequiredMixin,generic.DetailView):
    model = User
    template_name = 'catalog/user_detailowner.html'
def UserDetailView(request,pk):
    user=get_object_or_404(User,pk=pk)
    detail=get_object_or_404(UserDetail,user=user)
    return render(request,'catalog/user_detail.html',{'user':user,'detail':detail})
def transactionDetailView(request,pk):

    transact=get_object_or_404(transaction,pk=pk)
    if request.method=="POST":
        if request.POST["activestatus"]=="SetActive":
            transact.active=True
            transact.save()
            dressobj=transact.dress
            dressobj.active=False
            dressobj.save()
            bookings=booking.objects.filter(dress=dressobj)
            bookings.delete()

        if request.POST["activestatus"]=="SetInactive":
            transact.active=False
            transact.save()

        return HttpResponseRedirect(reverse('transactionselect') )
    return render(request,'catalog/transaction_detail.html',{'transaction':transact})
def TypeDetailView(request,pk):
    page = request.GET.get('page',1)
    type =Type.objects.get(pk=pk)

    dresslist= type.dress_set.all()
    paginator = Paginator(dresslist,8)
    dress_list = paginator.page(page)

    return render(request, 'catalog/type_detail.html', {'type':type,'dress_list': dress_list})
@user_passes_test(lambda u: u.is_superuser)
def TypeDetailOwnerView(request,pk):
    page = request.GET.get('page',1)
    type =Type.objects.get(pk=pk)

    dresslist= type.dress_set.all()
    paginator = Paginator(dresslist,8)
    dress_list = paginator.page(page)

    return render(request, 'catalog/type_detailowner.html', {'type':type,'dress_list': dress_list})
@login_required
def LoanedDressesByUserListView(request):
    """
    Generic class-based view listing books on loan to current user.
    """



    Booked=booking.objects.filter(user=request.user)
    return render(request, 'catalog/dressinstance_list_borrowed_user.html', context={'book_list':Booked})

@login_required
def mycart(request):
    """
    Generic class-based view listing books on loan to current user.
    """
    total=request.session.get('total',0)
    cart=request.session.get('cart',{})
    displist={}

    for dressid in cart:
        dress=get_object_or_404(Dress, pk = dressid)
        displist[dress]=cart[dressid]

    return render(request, 'catalog/mycart.html', context={'disp_list':displist,'total':total})

@login_required
def myprofile(request):
    """
    Generic class-based view listing books on loan to current user.
    """
    user= request.user

    return render(request, 'catalog/myprofile.html', context={'user':user})


def book_a_dress(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    dress=get_object_or_404(Dress, pk = pk)
    allbooking=booking.objects.all()

    b=1

    for gl in allbooking:

        if gl.user == request.user and gl.dress==dress:
            b=0


    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = BookDressForm(request.POST)
        if form.is_valid():

        # Create a form instance and populate it with data from the request (binding):


        # Check if the form is valid:

            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            m1 = booking(id=pk+str(request.user.id),user=request.user,dress=dress,bookdate=datetime.date.today(),price=form.cleaned_data['price'],daysno=form.cleaned_data['daysno'],reqdate=form.cleaned_data['reqdate'])
            m1.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-booked') )

    # If this is a GET (or any other method) create the default form.
    else:

        form = BookDressForm()
    return render(request, 'catalog/book_a_dress.html', { 'form':form,'dress':dress,'prebook':b})
def userinfochange(request):
    """
    View function for renewing a specific BookInstance by librarian
    """
    user=request.user
    m1=UserDetail.objects.get(user=user)
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UserinfoChangeForm(request.POST,user=user)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            user.username=form.cleaned_data['username']
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            user.email=form.cleaned_data['email']
            user.save()

            m1.location = form.cleaned_data['location']
            m1.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-profile') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_number = 3
        form = UserinfoChangeForm(initial={'username': user.username,'first_name': user.first_name,'last_name': user.last_name,'email': user.email,'location': m1.location,},user=user)

    return render(request, 'catalog/change_user_info.html', {'form': form})


def buy_a_dress(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    total=request.session.get('total',0)
    cart=request.session.get('cart',{})
    dress=get_object_or_404(Dress, pk = pk)



        # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = BuyDressForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            cart[dress.id]=form.cleaned_data['Buyno']
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            total=total+dress.price*cart[dress.id]
            request.session['cart']=cart
            request.session['total']=total


            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-cart') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_number = 1
        form = BuyDressForm(initial={'Buyno': proposed_number})

    return render(request, 'catalog/buy_a_dress.html', {'form': form, 'dress':dress})
def completeorder(request):
    cart=request.session.get("cart",{})
    m1=Order(user=request.user,orderdate=datetime.date.today(),active=True)
    m1.save()
    for dressid in cart:
        currentdress=get_object_or_404(Dress,pk=dressid)
        m2=OrderDetail(dress=currentdress,orderno=cart[dressid],orderuser=m1)
        m2.save()
    del request.session['cart']
    del request.session['total']
    return HttpResponseRedirect(reverse('my-ordered') )

def confirmorder(request):


    return render(request,'catalog/orderconfirm.html',)
@login_required
def myordered(request):


    myorderdress=Order.objects.filter(user=request.user)

    return render(request,'catalog/myordered.html',{'myorder_list':myorderdress})





@user_passes_test(lambda u: u.is_superuser)
def ownerview(request):
    """
    View function for home page of site.
    """


    return render(
        request,
        'indexowner.html'

    )
def DressListViewowner(request):
    page = request.GET.get('page', 1)


    if "search" in request.GET:

        dresslist= Dress.objects.filter(Q(name__icontains=request.GET["search"])|Q(type__name__icontains=request.GET["search"]))
        paginator = Paginator(dresslist,8)
        try:
            dress_list = paginator.page(page)
        except PageNotAnInteger:
            dress_list = paginator.page(1)
        except EmptyPage:
            dress_list = paginator.page(paginator.num_pages)
        return render(request, 'catalog/dress_list_owner.html', {'dress_list': dress_list,'searchvalue':request.GET["search"]})

    else:

        dresslist= Dress.objects.all()
        paginator = Paginator(dresslist,8)

        try:
            dress_list = paginator.page(page)
        except PageNotAnInteger:
            dress_list = paginator.page(1)
        except EmptyPage:
            dress_list = paginator.page(paginator.num_pages)
        return render(request, 'catalog/dress_list_owner.html', {'dress_list': dress_list})
def TypeListViewowner(request):
    page = request.GET.get('page',1)
    if "search" in request.GET:

        typelist= Type.objects.filter(name__icontains=request.GET["search"])
        paginator = Paginator(typelist,8)
        try:
            type_list = paginator.page(page)
        except PageNotAnInteger:
            type_list = paginator.page(1)
        except EmptyPage:
            type_list = paginator.page(paginator.num_pages)

    else:
        typelist= Type.objects.all()
        paginator = Paginator(typelist,8)
        try:
            type_list = paginator.page(page)
        except PageNotAnInteger:
            type_list = paginator.page(1)
        except EmptyPage:
            type_list = paginator.page(paginator.num_pages)

    return render(request, 'catalog/type_list_owner.html', {'type_list': type_list})
def UsersListViewowner(request):
    page = request.GET.get('page',1)
    if "search" in request.GET:

        userlist= User.objects.filter(name__icontains=request.GET["search"])
        paginator = Paginator(userlist,8)
        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            user_list = paginator.page(1)
        except EmptyPage:
            user_list = paginator.page(paginator.num_pages)

    else:
        userlist= User.objects.all()
        paginator = Paginator(userlist,8)
        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            user_list = paginator.page(1)
        except EmptyPage:
            user_list = paginator.page(paginator.num_pages)

    return render(request, 'catalog/user_list_owner.html', {'user_list': user_list})

def deleteobject(request,pk,obj):
    if obj == 'dress':
        delobj=get_object_or_404(Dress,pk=pk)
    if obj == 'type':
        delobj=get_object_or_404(Type,pk=pk)
    if obj == 'transaction':
        delobj=get_object_or_404(transaction,pk=pk)
    delobj.delete()

    return HttpResponseRedirect(reverse('index') )


def DressAdd(request):






    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddDressForm(request.POST,request.FILES)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            m1 = Dress(user=request.user,name=form.cleaned_data['name'],price=form.cleaned_data['price'],type=form.cleaned_data['type'],detail=form.cleaned_data['detail'],dress_pic=request.FILES['dress_pic'],rentday=form.cleaned_data['rentday'],date=datetime.date.today())
            if "dress_pic2" in request.FILES:
                m1.dress_pic2=request.FILES["dress_pic2"]
            m1.save()
            print (m1.search_index)
            t = Thread(target = new_thread(m1.id))

            t.daemon = True
            t.start()
            print ("GObabygo")
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

    # If this is a GET (or any other method) create the default form.
    else:

        form = AddDressForm(initial={'name': "",'detail':""})

    return render(request, 'catalog/add_a_dress.html', {'form': form})
def addtransaction(request,pk):
    bid=get_object_or_404(booking,pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddTransactionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            m1 = transaction(renter=bid.user,dress=bid.dress,price=form.cleaned_data['price'],daysno=form.cleaned_data['daysno'],reqdate=form.cleaned_data['reqdate'],transactiondate=datetime.date.today())
            m1.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

    # If this is a GET (or any other method) create the default form.
    else:

        form = AddTransactionForm()

    return render(request, 'catalog/add_transaction.html', {'form': form})
def final(request,pk):
    transact=get_object_or_404(transaction,pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddFinalForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            m1 = rentinfo(transaction=transact,fine=form.cleaned_data['fine'],insuranceclaimstatus=form.cleaned_data['insuranceclaimstatus'])
            m1.save()
            transact.completion=True
            transact.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

    # If this is a GET (or any other method) create the default form.
    else:

        form = AddFinalForm()

    return render(request, 'catalog/add_final.html', {'form': form})
def TypeAdd(request):






    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddTypeForm(request.POST,request.FILES)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            m1 = Type(name=form.cleaned_data['name'],detail=form.cleaned_data['detail'],type_pic=request.FILES['type_pic'],)
            m1.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

    # If this is a GET (or any other method) create the default form.
    else:

        form = AddTypeForm(initial={'name': "",'detail':""})

    return render(request, 'catalog/add_a_type.html', {'form': form})
def DressEdit(request,pk):

    m1=get_object_or_404(Dress,pk=pk)



        # If this is a POST request then process the Form data
    if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
        form = AddDressForm(request.POST,request.FILES)

            # Check if the form is valid:
        if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            m1.name = form.cleaned_data['name']
            m1.price=form.cleaned_data['price']
            m1.type=form.cleaned_data['type']
            m1.detail=form.cleaned_data['detail']
            m1.dress_pic=request.FILES['dress_pic']
            m1.save()


                # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

        # If this is a GET (or any other method) create the default form.
    else:

        form = AddDressForm(initial={'name': m1.name,'detail':m1.detail,'price':m1.price,'type':m1.type,'dress_pic':m1.dress_pic})

    return render(request, 'catalog/add_a_dress.html', {'form': form})
def TypeEdit(request,pk):

    m1=get_object_or_404(Type,pk=pk)



        # If this is a POST request then process the Form data
    if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
        form = AddDressForm(request.POST,request.FILES)

            # Check if the form is valid:
        if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            m1.name = form.cleaned_data['name']
            m1.price=form.cleaned_data['price']
            m1.type=form.cleaned_data['type']
            m1.detail=form.cleaned_data['detail']
            m1.dress_pic=request.FILES['dress_pic']
            m1.save()


                # redirect to a new URL:
            return HttpResponseRedirect(reverse('index') )

        # If this is a GET (or any other method) create the default form.
    else:

        form = AddDressForm(initial={'name': m1.name,'detail':m1.detail,'price':m1.price,'type':m1.type,'dress_pic':m1.dress_pic})

    return render(request, 'catalog/add_a_dress.html', {'form': form})
class UserCreate(CreateView):
    model = User
    template_name='catalog/user_form.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('users')



class UserUpdate(UpdateView):
    model = User
    fields = ['first_name','last_name','username','password','is_superuser']
    template_name='catalog/user_form.html'
    success_url = reverse_lazy('users')


class UserDelete(DeleteView):
    model = User
    template_name='catalog/user_confirm_delete.html'
    success_url = reverse_lazy('users')
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
            toemail = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[toemail])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        m1=UserDetail(user=user)
        m1.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
def showbid(request,pk):
    """
    View function for home page of site.
    """
    bids=booking.objects.filter(Q(dress__user=request.user)&Q(dress_id=pk))
    return render(
        request,
        'catalog/showbid.html',{'bids':bids}

    )
def givebid(request,pk):
    """
    View function for home page of site.
    """
    if request.method=="POST":
        if "involve" in request.POST:
            return HttpResponseRedirect(reverse('addtransaction',args=(pk,)) )


        else:
            print ("noinvolve")
            return HttpResponseRedirect(reverse('index') )
    else:

        return render(
            request,
            'catalog/type_transaction.html',

    )
