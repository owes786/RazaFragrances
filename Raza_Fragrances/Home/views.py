from django.shortcuts import render,HttpResponseRedirect, redirect
from django.views import View
from .models import Product, Review ,OrderDetails, Customer_Details, Cart , Wishlist, Buy_now_model
from .forms import signupForm, loginForm, NewAddress ,ChangePassword, User_Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.db.models import Q
from django.http import JsonResponse
import razorpay
from django.conf import settings


# This Functin show Products on Home Page.
class HomeProductView(View):
    def get(self, request):
        Attar = Product.objects.order_by('?').filter(Category = 'Attar').filter(Stock = 'in stock')
        Perfume = Product.objects.order_by('?').filter(Category = "Perfume").filter(Stock = 'in stock')
        Deodent = Product.objects.order_by('?').filter(Category = 'Deodent').filter(Stock = 'in stock')
        Fragrances = Product.objects.all()
        if request.user.is_authenticated:
            Cart_len = len(Cart.objects.filter(user = request.user))
            return render(request, '1.Home.html' ,{'Attar':Attar, 'Perfume':Perfume, 'Deodent':Deodent, 'HomeActive':'active', 'Cart_len':Cart_len, 'Products':Fragrances})
        return render(request, '1.Home.html' ,{'Attar':Attar, 'Perfume':Perfume, 'Deodent':Deodent, 'Products': Fragrances, 'HomeActive':'active'})


# This Function render Search.html  
def Search(request):
    return render(request, "19.Search.html")


# This Function for SEarch
def Search_results(request):
    if request.POST:
        res = None
        Fragrance = request.POST.get('Fragrance')
        product_obj = Product.objects.filter(Title__icontains = Fragrance)
        if len(product_obj) > 0 and len(Fragrance) > 0:
            data = []
            for pos in product_obj:
                item = {
                    'pk': pos.pk,
                    'Title': pos.Title,
                    'image': str(pos.Product_Image.url),
                }
                data.append(item)
            res = data
        else:
            res = "<p class='text-center text-muted'>No Fragrance found..</p>"
        return JsonResponse({'data':res})
    return JsonResponse({})


# This Function Show Fragrance page
class FragranceView(View):
    def get(self, request,data=None):
        if data == None:
            product_obj = Product.objects.order_by('?').all()
        elif data == 'Attar' or data == 'Perfume' or data == 'Deodent':
            product_obj = Product.objects.filter(Category = data).order_by('?')
        else:
            product_obj = Product.objects.order_by('?').all()

        if request.user.is_authenticated:
            Cart_len = len(Cart.objects.filter(user = request.user))
            return render(request, '12.Fragrance.html', {'Product':product_obj ,'FragranceActive':'active' ,'Cart_len':Cart_len})
        
        return render(request, '12.Fragrance.html', {'Product':product_obj ,'FragranceActive':'active'})


# This function show Product Details.
class Product_DetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        product_obj = Product.objects.order_by('?').all()
         # This is determine is product in wishlist or not
        Already_in_Wishlist = False
        if request.user.is_authenticated:
            Already_in_Wishlist = Wishlist.objects.filter(Q(user = request.user) & Q(Product = product)).exists()
            
        # This is determine is product in Cart or not
        Already_in_Cart = False
        if request.user.is_authenticated:
            Already_in_Cart = Cart.objects.filter(Q(user = request.user) & Q(Product = product)).exists()

        # This is for Show Reviews.
        review_obj = Review.objects.filter(Product = product)
        Reviews_len = len(Review.objects.filter(Product = pk))

        is_Purchased = False
        Prod = Product.objects.get(pk = pk)
        if request.user.is_authenticated:
            is_Purchased = OrderDetails.objects.filter(Q(user = request.user) & Q(Product = Prod)).exists()


        if request.user.is_authenticated:
            Cart_len = len(Cart.objects.filter(user = request.user))
            return render(request,'4.Product Detail.html',{'product':product, "AllProduct":product_obj, 'Already_in_Wishlist':Already_in_Wishlist, 'Already_in_Cart':Already_in_Cart, 'Reviews_len':Reviews_len , 'is_Purchased':is_Purchased, 'review_obj':review_obj ,'Cart_len':Cart_len})

        return render(request,'4.Product Detail.html',{'product':product, "AllProduct":product_obj, 'review_obj':review_obj})


# This Function for Buy now.
def Buy_now(request):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        Product_id = request.GET.get('Prod_id')
        Product_obj = Product.objects.get(pk = Product_id)
        Already_in_Buy_Now_Table = Buy_now_model.objects.filter(user = request.user)
        Already_in_Buy_Now_Table.delete()
        Buy_now_model(user = request.user, Product = Product_obj).save()
        return redirect('checkout')
    else:
        messages.warning(request, "Please Login or Create new Account for Shopping.")
        return HttpResponseRedirect('/Login/')
    

# This Function Show Checkout Page for Buy now.
def Buy_now_Checkout(request):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        Cust_address = Customer_Details.objects.filter(user = request.user)
        Buy_Now_Product = Buy_now_model.objects.filter(user = request.user)

        for p in Buy_Now_Product:
            Total_amount = p.Product.Selling_Price

        try:                
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_ID))

            data = { "amount": Total_amount * 100 ,"currency": "INR", "payment_capture" : 1 }
            payment = client.order.create(data=data)
            print(payment)

            order_id = payment['id']
            
        except:
            return redirect('/Connection-lost/')
        
        return render(request, '27.Buy now checkout.html', {'Product':Buy_Now_Product ,'Cust_address':Cust_address, 'Cart_len':Cart_len, 'Total_amount': Total_amount ,'order_id':order_id})
    else:
        return HttpResponseRedirect('/Login/')
    

# Payment done function for Buy Now.
def Buy_Now_Payment_done(request):
    if request.user.is_authenticated:
        Customer_address_id = request.GET.get('custid')
        try:
            Customer_address_obj = Customer_Details.objects.get(pk = Customer_address_id)
        except:
            messages.warning(request, "Please select your shipping address before checkout !")
            return redirect('/checkout/')
        Buy_now_obj = Buy_now_model.objects.filter(user = request.user)

        rzporder_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        signature = request.GET.get('signature')

        if rzporder_id is not None:
            Prepaid_Status = True
        else:
            Prepaid_Status = False

        for item in Buy_now_obj:
            Prod_id = Product.objects.get(pk=item.Product.id)            
            OrderDetails(user=request.user, Product = Prod_id ,Razorpay_Order_id = rzporder_id, Razorpay_Payment_id = payment_id, Razorpay_signature = signature , Prepaid = Prepaid_Status, Name=Customer_address_obj.Name, Mobile_Number=Customer_address_obj.Mobile_Number,Pincode=Customer_address_obj.Pincode, City=Customer_address_obj.City, Address=Customer_address_obj.Address, State=Customer_address_obj.State, Landmark=Customer_address_obj.Landmark , Title=item.Product.Title, Mrp=item.Product.Mrp, Selling_Price=item.Product.Selling_Price, Product_Image=item.Product.Product_Image, Quantity=item.quantity, Total_Amount=item.quantity*item.Product.Selling_Price).save()
            item.delete()
            return redirect('/My-Orders/')
    else:
        return HttpResponseRedirect('/Login/')


# This Function Render Cart.html
def Add_To_Cart(request):
    if request.user.is_authenticated:
        Product_id = request.GET.get('Product_id')
        Product_obj = Product.objects.get(pk = Product_id)
        Cart(user = request.user, Product = Product_obj).save()
        return redirect('/Cart/')
    else:
        messages.warning(request, "Please Login or Create new Account for Shopping.")
        return HttpResponseRedirect('/Login/')


# This Function Show Cart items
def Show_Cart(request):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        cart = Cart.objects.filter(user = request.user)
        amount = 0.0
        Total_amount = 0.0
        Cart_Product = [p for p in Cart.objects.all() if p.user == request.user]
        items = len(Cart_Product)
        if Cart_Product:
            for prod in Cart_Product:
                tempamount = (prod.quantity * prod.Product.Selling_Price)
                amount += tempamount
                Total_amount = amount
            
            return render(request, '11.Cart.html', {'Cart_item':cart,'items':items ,'amount':amount ,'Total_amount':Total_amount ,'Cart_len':Cart_len})
        else:
            return render(request, '5.Empty Cart.html')
        
    else:
        return HttpResponseRedirect('/Login/')


# This Function Increase Cart item Quantity
def increase_quantity(request):
    if request.method == "GET":
        Prod_id = request.GET['Product_id']
        Cart_obj = Cart.objects.get(Q(user = request.user) & Q(Product = Prod_id))
        if Cart_obj.quantity < 5:
            Cart_obj.quantity += 1 
            Cart_obj.save()
        amount = 0.0
        Total_amount = 0.0
        Cart_Product = [p for p in Cart.objects.all() if p.user == request.user]
        if Cart_Product:
            for prod in Cart_Product:
                tempamount = (prod.quantity * prod.Product.Selling_Price)
                amount += tempamount
                Total_amount = amount
        
        data ={
            'quantity': Cart_obj.quantity,
            'amount': amount,
            'total_amount': Total_amount
        }
        return JsonResponse(data)

    return redirect('/Cart/')


# This Function Decrease Cart item Quantity
def decrease_quantity(request):
    if request.method == "GET":
        Prod_id = request.GET['Product_id']
        Cart_obj = Cart.objects.get(Q(user = request.user) & Q(Product = Prod_id))
        if Cart_obj.quantity > 1:
            Cart_obj.quantity -= 1 
            Cart_obj.save()
        amount = 0.0
        Total_amount = 0.0
        Cart_Product = [p for p in Cart.objects.all() if p.user == request.user]
        if Cart_Product:
            for prod in Cart_Product:
                tempamount = (prod.quantity * prod.Product.Selling_Price)
                amount += tempamount
                Total_amount = amount
        
        data ={
            'quantity': Cart_obj.quantity,
            'amount': amount,
            'total_amount': Total_amount
        }
        return JsonResponse(data)

    return redirect('/Cart/')


# This Function Show Checkout Page for Add to Cart.
def Checkout(request):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        Cust_address = Customer_Details.objects.filter(user = request.user)
        amount = 0.0
        Total_amount = 0.0
        Cart_Product = [p for p in Cart.objects.all() if p.user == request.user]
        if Cart_Product:
            for prod in Cart_Product:
                tempamount = (prod.quantity * prod.Product.Selling_Price)
                amount += tempamount
                Total_amount = amount
                Razorpay_Total_amount = amount * 100

        try:                
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_ID))

            data = { "amount": Razorpay_Total_amount ,"currency": "INR", "payment_capture" : 1 }
            payment = client.order.create(data=data)
            print(payment)

            order_id = payment['id']
            
        except:
            return redirect('/Connection-lost/')

    return render(request, '20.Checkout.html', {'Total_amount':Total_amount, 'Cust_address':Cust_address, 'Cart_len':Cart_len, 'Cart_Product':Cart_Product,'Razorpay_Total_amount':Razorpay_Total_amount, 'order_id': order_id})


# Payment done function for Add to Cart.
def Payment_done(request):
    if request.user.is_authenticated:
        Customer_address_id = request.GET.get('custid')
        try:
            Customer_address_obj = Customer_Details.objects.get(pk = Customer_address_id)
        except:
            messages.warning(request, "Please select your shipping address before checkout !")
            return redirect('/Checkout/')
        
        Cart_obj = Cart.objects.filter(user = request.user)

        # Razorpay response order id, payment id, Signature    
        rzporder_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        signature = request.GET.get('signature')

        if rzporder_id:
            Prepaid_Status = True
        else:
            Prepaid_Status = False

        for item in Cart_obj:
            Prod_id = Product.objects.get(pk=item.Product.id)
            OrderDetails(user=request.user, Razorpay_Order_id = rzporder_id, Razorpay_Payment_id = payment_id, Razorpay_signature = signature , Prepaid = Prepaid_Status, Product=Prod_id, Name=Customer_address_obj.Name, Mobile_Number=Customer_address_obj.Mobile_Number,Pincode=Customer_address_obj.Pincode, City=Customer_address_obj.City, Address=Customer_address_obj.Address, State=Customer_address_obj.State, Landmark=Customer_address_obj.Landmark , Title=item.Product.Title, Mrp=item.Product.Mrp, Selling_Price=item.Product.Selling_Price, Product_Image=item.Product.Product_Image, Quantity=item.quantity, Total_Amount=item.quantity*item.Product.Selling_Price).save()
            item.delete()
            
        return redirect('/My-Orders/')
    else:
        return HttpResponseRedirect('/Login/')


# for connection lost
def connection_lost(request):
    Cart_len = len(Cart.objects.filter(user = request.user))
    return render(request, "26.no internet connction.html", {'Cart_len':Cart_len})


# Order cancelled
def Order_not_placed(request):
    Cart_len = len(Cart.objects.filter(user = request.user))
    return render(request, '28. Order not placed.html', {'Cart_len':Cart_len})


# This Function show Review Textarea
def review(request,pk):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        is_Purchased = False
        Prod = Product.objects.get(pk = pk)
        is_Purchased = OrderDetails.objects.filter(Q(user = request.user) & Q(Product = Prod)).exists()
        if is_Purchased:
            if request.method == 'POST':
                Prod_id = Product.objects.get(pk = pk)
                review = request.POST['review']
                try:
                    img = request.FILES['image']
                except:
                    messages.warning(request, "Please choose an image for review!!")
                    return redirect('/My-Orders/')
                reg = Review(user=request.user, Product=Prod_id, Review_Description=review, image=img)
                reg.save()
                messages.success(request, "Review Posted")
                return redirect('/My-Reviews/')
            
            return render(request,'15.Review.html',{'Cart_len':Cart_len})
        else:
            return redirect('/Login/')
    else:
        return HttpResponseRedirect('/Login/')


# This Function Shows Reviews to user how has posted.
def ShowMyReviews(request):
    if request.user.is_authenticated:
        Review_obj = Review.objects.filter(user = request.user)
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '16.My Reviews.html', {'Review_obj':Review_obj ,'ButtonActive':'btn btn-dark text-light' ,'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')


# This Function Delete user Reviews.
def DeleteMyReviews(request,pk):
    if request.user.is_authenticated:
        Review_id = Review.objects.get(pk = pk)
        Review_id.delete()
        return redirect('/My-Reviews/')
    else:
        return HttpResponseRedirect('/Login/')


# This Function Update user Reviews.
def UpdateMyReviews(request,pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            Review_id = Review.objects.get(pk = pk)
            fm = Review_Form(request.POST, instance=Review_id)
            fm.save()
            return redirect('/My-Reviews/')
        else:
            Review_id = Review.objects.get(pk = pk)
            fm = Review_Form(instance=Review_id)
    
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '17.Update My Review.html', {'form':fm ,'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')
    

# This Function show All Reviews of a product
def ShowAllReviews(request,pk):
    Product_obj = Product.objects.get(pk = pk)
    Reviews_obj = Review.objects.filter(Product = pk)
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '18.All Reviews.html', {'product':Product_obj,'reviews':Reviews_obj ,'Cart_len':Cart_len})
    else:
        return render(request, '18.All Reviews.html', {'product':Product_obj,'reviews':Reviews_obj})


# This Function Add product To Wishlist.
def Move_To_Wishlist(request,pk):
    if request.user.is_authenticated:
        wishlist_item = Product.objects.get(pk = pk)
        Wishlist(user = request.user, Product = wishlist_item).save()
        return redirect('/Wishlist/')
    else:
        return HttpResponseRedirect('/Login/')
    

# This Function Show Wishlist Items.
def Show_Wishlist(request):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        Wishlist_items = Wishlist.objects.filter(user = request.user)
        return render(request, '14.Wishlist.html', {'Wishlist_items':Wishlist_items, "WishlistActive":'btn btn-dark text-light' ,'Cart_len':Cart_len })
    else:
        return HttpResponseRedirect('/Login/')


# This Function remove Wishlist item.
def Remove_Wishlist_Item(request,pk):
    if request.user.is_authenticated:
        item = Wishlist.objects.filter(pk=pk)
        item.delete()
        return redirect('/Wishlist/')
    else:
        return HttpResponseRedirect('/Login/')


# This Function Show Cart items
def RemoveCartItem(request, pk):
    Cartitem = Cart.objects.get(pk = pk)
    Cartitem.delete()
    return HttpResponseRedirect('/Cart/')
    

# This Function show Empty Cart.
def EmptyCart(request):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request,'5.Empty Cart.html', {'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')


# This Function show profile page.
def Profile(request):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        if request.method == "POST":
            fm = User_Profile(request.POST, instance = request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request, "Profile Updated Successfully!!")
        else:
            fm = User_Profile(instance = request.user)
        return render(request, '006.Profile.html', {'form':fm ,'ProfileActive':"btn-dark" ,'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')



# This Function show User All Addresses.
def My_Address(request):
    if  request.user.is_authenticated:
        UserAddressData = Customer_Details.objects.filter(user = request.user)
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '6.profile.html', {'UserAddressData':UserAddressData ,'ButtonActive':'btn-dark' ,'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')


#This Function delete Existing Address
def DeleteAddress(request,pk):
    address = Customer_Details.objects.get(pk=pk)
    address.delete()
    return redirect('/My-address/')


#  This Function Edit Existing Address.
def Edit_address(request,pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            address_id = Customer_Details.objects.get(pk=pk)
            fm = NewAddress(request.POST, instance=address_id)
            if fm.is_valid():
                fm.save()
                messages.success(request, "Address updated successfully!")
                return redirect('/My-address/')
        else:
            address_id = Customer_Details.objects.get(pk=pk)
            fm = NewAddress(instance=address_id)
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '21.Edit address.html', {'form':fm ,'Cart_len':Cart_len})

    else:
        return HttpResponseRedirect('/Login/')


# This Function show User Profile.
def MyNewAddress(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = NewAddress(request.POST)
            if fm.is_valid():
                user = request.user
                uname = fm.cleaned_data['Name']
                mnumber = fm.cleaned_data['Mobile_Number']
                pincode = fm.cleaned_data['Pincode']
                city = fm.cleaned_data['City']
                address = fm.cleaned_data['Address']
                state = fm.cleaned_data['State']
                landmark = fm.cleaned_data['Landmark']

                MyNewAddress = Customer_Details(user = user, Name = uname, Mobile_Number = mnumber, Pincode = pincode, City = city, Address = address, State = state, Landmark = landmark)
                MyNewAddress.save()
                messages.success(request, 'Address added successfully!')
                return redirect('/My-address/')
        else:
            fm = NewAddress()
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '7.Add New Address.html', {'form':fm, 'ButtonActive':'btn-dark' ,'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')
    

#This Function show About us page.
def AboutUs(request):
    if request.user.is_authenticated:
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '10.About us.html', {'AboutUsActive':'active' ,'Cart_len':Cart_len})
    else:
        return render(request, '10.About us.html', {'AboutUsActive':'active'})


# This Function for Change Password.
def PasswordChange(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = ChangePassword(user = request.user , data = request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, "Password Changed Successfully.")
                update_session_auth_hash(request, user = request.user)
                return HttpResponseRedirect('/Profile/')
        else:
            fm = ChangePassword(user = request.user)
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '9.Change Password.html', {'form':fm ,'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')


# This Function for My Orders.
def ShowMyOrders(request):
    if request.user.is_authenticated:
        MyOrder_obj = OrderDetails.objects.filter(user = request.user)
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, '8.My Orders.html', {'MyOrder':MyOrder_obj ,'ButtonActive':'btn-dark text-white' ,'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')
    

# This Function Show Order Details
def MyOrderDetails(request,pk):
    if request.user.is_authenticated:
        Product_obj = OrderDetails.objects.get(pk=pk)
        if Product_obj.Prepaid == True:
            Determine = 'Prepaid'
        else:
            Determine = 'Cash on delevery'
        Cart_len = len(Cart.objects.filter(user = request.user))
        return render(request, "13.Order Details.html", {'ProductDetails':Product_obj , 'Determine':Determine ,'Cart_len':Cart_len})
    else:
        return HttpResponseRedirect('/Login/')
    

# This Function Render Terms and Condition page.
def Terms_Condition(request):
    Cart_len = len(Cart.objects.filter(user = request.user))
    return render(request, '23.Terms & Conditions.html', {'Cart_len':Cart_len})


# This Function Render Privacy & Policy page.
def Privacy(request):
    Cart_len = len(Cart.objects.filter(user = request.user))
    return render(request, '24.Privacy.html', {'Cart_len':Cart_len})


# This Function Render Privacy & Policy page.
def Return_Refund(request):
    Cart_len = len(Cart.objects.filter(user = request.user))
    return render(request, '25.Return & Refund.html', {'Cart_len':Cart_len})
    


# This Function is for Create New Account.
def Signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = signupForm(request.POST)
            if fm.is_valid():
                messages.success(request,'Account Crated Successfully, now you can login with your Email and Password.')
                fm.save()
                return HttpResponseRedirect('/Login/')
        else:
            fm = signupForm()
        return render(request,'2.Signup.html', {'form':fm})
    else:
        return HttpResponseRedirect('/Login/')


# This Function is for Login with Existing Account.
def Login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = loginForm(request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(email = uname, password = upass)
                if user is not None:
                    login(request,user)
                    if  Customer_Details.objects.filter(Q(user = request.user)).exists():
                        return redirect('Home')
                    else:
                        return redirect('AddNewAddress')
        else:
            fm = loginForm()
        return render(request,'3.Login.html', {'form':fm})
    else:
        return HttpResponseRedirect('/Profile/')


# This Function Logout with Existing Account.
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/Login/')