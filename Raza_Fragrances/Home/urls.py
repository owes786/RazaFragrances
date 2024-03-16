from django.urls import path
from .import views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeDoneView, PasswordResetCompleteView

urlpatterns = [
    path('', views.HomeProductView.as_view(),name='Home'),
    path('Search/', views.Search,name="Search"),
    path('Search/Search-results/', views.Search_results,name='SearchResults'),
    path('Fragrance/', views.FragranceView.as_view(), name='Fragrance'),
    path('Fragrance/<slug:data>', views.FragranceView.as_view(), name='FragrancePage'),
    path('Product-details/<int:pk>/',views.Product_DetailView.as_view(),name='ProductDetail'),
    path('Add-to-Cart/', views.Add_To_Cart, name='Add-to-Cart'),
    path('Cart/', views.Show_Cart, name='Cart'),
    path('Buy-now/', views.Buy_now, name='BuyNow'),
    path('increase-quantity/', views.increase_quantity),
    path('decrease-quantity/', views.decrease_quantity),
    path('Checkout/', views.Checkout, name="Checkout"),
    path('checkout/', views.Buy_now_Checkout, name="checkout"),
    path('Payment/', views.Payment_done, name="Payment"),
    path('Buy-now-Payment/', views.Buy_Now_Payment_done, name="BuyNowPayment"),
    path('Order-not-placed/', views.Order_not_placed, name="OrderNotPlaced"),
    path('Connection-lost/', views.connection_lost, name="NointernetConnection"),
    path('Review/<int:pk>/', views.review, name='UserReview'),
    path('My-Reviews/', views.ShowMyReviews, name='MyReviews'),
    path('Delete-Review/<int:pk>/', views.DeleteMyReviews, name='DeleteMyReview'),
    path('Update-Review/<int:pk>/', views.UpdateMyReviews, name='UpdateMyReview'),
    path('All-Reviews/<int:pk>/', views.ShowAllReviews, name='AllReviews'),
    path('Move-to-wishlist/<int:pk>/', views.Move_To_Wishlist, name='MoveToWishlist'),
    path('Wishlist/', views.Show_Wishlist, name='MyWishlist'),
    path('Remove-wishlist-item/<int:pk>/', views.Remove_Wishlist_Item, name='RemoveWishlistItem'),
    path('Remove-cart-Item/<int:pk>/', views.RemoveCartItem, name='RemoveCartItem'),
    path('Empty-cart/', views.EmptyCart, name='EmptyCart'),
    path('Profile/', views.Profile, name='Profile'),
    path('My-address/', views.My_Address, name='MyAddress'),
    path('Add-new-address/', views.MyNewAddress, name='AddNewAddress'),
    path('Delete-address/<int:pk>/', views.DeleteAddress, name='DeleteAddress'),
    path('Edit-address/<int:pk>/', views.Edit_address, name='EditAddress'),
    path('My-Orders/', views.ShowMyOrders, name='MyOrders'),
    path('Order-Details/<int:pk>/', views.MyOrderDetails, name='OrderDetails'),
    path('About-us/', views.AboutUs, name='AboutUs'),
    path('Terms-and-conditions/', views.Terms_Condition, name='TermsAndConditions'),
    path('Privacy/', views.Privacy, name='Privacy'),
    path('Return-and-Refund/', views.Return_Refund, name='ReturnAndRefund'),
    path('Signup/', views.Signup, name='Signup'),
    path('Change-Password/', views.PasswordChange, name='ChangePassword'),
    path('Login/', views.Login, name='Login'),
    path('Logout/', views.Logout, name='Logout'),
]
