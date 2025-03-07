from django.shortcuts import render,redirect
from.models import*

from django.conf import settings
from django.core.mail import send_mail
import random
import razorpay

# Create your views here.
def index(request):
    if 'email' in request.session:
        uid = User.objects.get(email=request.session['email'])
        lid = User.objects.get(email=request.session['email'])
        pid = Add_product.objects.filter()
        lid = Add_to_cart.objects.filter(user_id=uid).count
        ctid = Add_to_cart.objects.filter(user_id=uid)
        con={
            'lid' : lid,
            'pid' : pid,
            'lid' : lid,
            'ctid' : ctid
        }
        return render(request,'index.html',con)
    else:
        return render(request,'login.html')
    
      
def login(request):
        if 'email' in request.session:
            lid = User.objects.get(email=request.session['email'])
            pid = Add_product.objects.all()
            con = {
                'lid' : lid,
                'pid' : pid
            }
            return render(request,'index.html',con)
        else:
            try:
                if request.POST:
                    email = request.POST['email']
                    password = request.POST['password']
                    lid = User.objects.get(email=email,)
                    pid = Add_product.objects.all()

                    if lid.password == password:
                        request.session['email'] = lid.email

                        con={
                            'lid' : lid,
                            'pid' : pid
                        }

                        return render(request,"index.html",con)
                    else:
                        con={
                        'eid' : "Invalid Password.."
                        }
                        return render(request,"login.html",con)
                else:
                        return render(request,"login.html")
            except:
                con = {
                     'eid': "Invalid Email.."
                 }
                return render(request,"login.html",con)

def logout(request):
    if 'email' in request.session:
        del request.session['email']

        return render(request,'login.html')
    else:
        return render(request,'login.html')
    
def forget_password(request):
    if request.POST:
        email=request.POST['email']
        otp = random.randint(1111,9999)

        try:
            uid= User.objects.get(email=email)
            uid.otp=otp
            uid.save()

            send_mail("forget password","your OTP is"+str(otp),'gohiljayb10@gmail.com',[email])
            con = {
                'email' : email
            }
            return render(request,'confirm_password.html',con)
        except:
            con = {
                'eid' : "Invalid Email.."
            }
            return render(request,'forget_password.html',con)
    else:
        return render(request,'forget_password.html')
    
def confirm_password(request):
    if request.POST:
        email = request.POST['email']
        otp = request.POST['otp']
        new_password = request.POST['new_password']
        c_password = request.POST['c_password']

        lid = User.objects.get(email=email)

        if str(lid.otp) == otp:
            if new_password == c_password:
                lid.password = new_password
                lid.save()

                con = {
                    'email' : email,
                    'lid' : lid
                }
                return render(request,'login.html',con)
            else:
                con = {
                    'email' : email,
                    'oid' : "Invalid Confirm password.."
                    }
                return render(request,"confirm_password.html",con)
        else:
                con = {
                    'email' : email,
                    'oid' : "Invalid OTP.."
                }
                return render(request,"confirm_password.html",con)
    else:
        return render(request,"confirm_password.html")
    
def about(request):
    uid=User.objects.get(email=request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count
    ctid = Add_to_cart.objects.filter(user_id=uid)
    con = {
        'lid' : lid,
        'ctid' : ctid
    }
    return render(request,'about.html',con)
   
def cart(request):
    uid=User.objects.get(email=request.session['email'])
    cid = Add_to_cart.objects.filter(user_id=uid)
    lid = Add_to_cart.objects.filter(user_id=uid).count
    ctid = Add_to_cart.objects.filter()
    con = {
        'cid' : cid,
        'lid' : lid,
        'ctid' : ctid
    }
    return render(request,'cart.html',con)

def plus(request,id):
    pid = Add_to_cart.objects.get(id=id)
    if pid :
        pid.qty = pid.qty + 1
        pid.total_price = pid.qty* pid.price
        pid.save()
        
        return redirect('cart')
    else:
        return render(request,'cart.html')
    
def minus(request,id):
    mid = Add_to_cart.objects.get(id=id)

    if mid.qty == 1:
        mid.delete()
        return redirect('cart')
    else:
        if mid:
            mid.qty=mid.qty - 1
            mid.total_price = mid.qty*mid.price
            mid.save()

            return redirect('cart')
        else:
            return render(request,'cart.html')
        
def remove(request,id):
    did = Add_to_cart.objects.get(id=id).delete()

    return redirect('cart')

def checkout(request):
    uid=User.objects.get(email=request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count
    ctid = Add_to_cart.objects.all()
    prod = Add_to_cart.objects.filter(user_id=uid)

    l1 = []
    sub_total = 0
    total = 1

    for i in prod:
        z = i.price * i.qty
        l1.append(z)
        a = sum(l1)
    sub_total = sub_total + a 
    total = sub_total + 50

    amount = total*100 
    client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
    response = client.order.create({
                                   'amount':amount,
                                   'currency':'INR',
                                   'payment_capture':1
    })

    con = {
        'lid' : lid,
        'ctid' : ctid,
        'response' : response,
        'prod' : prod,
        'sub_total' : sub_total,
        'total' : total,
    }

    for i in prod:
        Order.objects.create(user_id=i.user_id,
                             product_id=i.product_id,
                             name = i.name,
                             price = i.price,
                             qty = i.qty,
                             total_price = i.total_price,
                             pic = i.pic)
    return render(request,"checkout.html",con)


def order(request):
    uid=User.objects.get(email=request.session['email'])
    did = Add_to_cart.objects.all().delete()
    oid=Order.objects.filter(user_id=uid)
    aid=Address.objects.filter(user_id=uid)
    con={
        'oid':oid,
        'aid':aid

    }
    return render(request,'order.html',con)

def error(request):
    return render(request,'error.html')

def contact(request):
    uid=User.objects.get(email=request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count
    ctid = Add_to_cart.objects.filter(user_id=uid)
    if request.POST:
        
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        cid= Contact.objects.create(name=name,
                                   email = email,
                                   subject = subject,
                                   message = message)
        con = {
               'cid':"successfully add data........"
        }
        return render(request,"contact.html",con)
    else:
        con = {
            'lid' : lid,
            'ctid' : ctid
        }
        return render(request,"contact.html",con)

def gallery(request):
    uid = User.objects.get(email=request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count
    ctid = Add_to_cart.objects.filter(user_id=uid)
    con = {
            'lid' : lid,
            'ctid' : ctid
        }
    return render(request,"gallery.html",con)

def my_account(request):
    return render(request,"my_account.html")

def shop_detail(request,id):
    uid = User.objects.get(email=request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count
    ctid = Add_to_cart.objects.filter(user_id=uid)
    vid = Add_product.objects.get(id=id)

    con = {
        'vid' : vid,
        'lid' : lid,
        'ctid' : ctid
    }
    return render(request,"shop_detail.html",con)

def shop(request):
    uid = User.objects.get(email=request.session['email'])
    pid = Add_product.objects.all()
    cid = Category.objects.all()
    lid = Add_to_cart.objects.filter(user_id=uid).count
    ctid = Add_to_cart.objects.filter(user_id=uid)

    con = {
        'pid' : pid,
        'cid' : cid,
        'lid' : lid,
        'ctid' : ctid
    }
    return render(request,"shop.html",con)

def category(request,id):
    pid = Add_product.objects.filter(category_id=id)
    cid = Category.objects.all()

    con = {
        'pid' : pid,
        'cid' : cid
    }
    return render(request,"shop.html",con)

def add_to_cart(request,id):
    if 'email' in request.session:
        uid = User.objects.get(email=request.session['email'])
        pid = Add_product.objects.get(id=id)
        pcid = Add_to_cart.objects.filter(user_id=uid,product_id=pid).exists()

        if pcid:
            pcid = Add_to_cart.objects.get(product_id=id)

            pcid.qty = pcid.qty + 1
            pcid.total_price = pcid.qty * pcid.price
            pcid.save()
            return redirect('cart')
        else:

            pid = Add_product.objects.get(id=id)

            acid = Add_to_cart.objects.create(user_id = uid,
                                            product_id= pid,
                                            name = pid.name,
                                            pic = pid.pic,
                                            price = pid.price,
                                            qty = pid.qty,
                                            total_price = pid.qty * pid.price
                                            )
            return redirect('cart')
    else:
        return render(request,"shop.html")  

def add_to_wishlist(request,id):
        uid = User.objects.get(email=request.session['email'])
        pid = Add_product.objects.get(id=id)

        wid = Add_to_wishlist.objects.create(user_id=uid,
                                             product_id=pid,
                                             name= pid.name,
                                             price=pid.price,
                                             pic=pid.pic)
        return redirect('wishlist')

def wishlist(request):
    uid = User.objects.get(email=request.session['email'])
    lid = Add_to_cart.objects.filter(user_id=uid).count()
    cart_id = Add_to_cart.objects.filter(user_id=uid)
    wid = Add_to_wishlist.objects.all()

    con = {
        'lid' : lid,
        'cart_id' : cart_id,
        'wid' : wid 
    }
    return render(request,"wishlist.html",con)

def wishlist_remove(request,id):

    wid = Add_to_wishlist.objects.get(id=id).delete()
    return redirect('wishlist')

def register(request):
     if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        uid= User.objects.create(name=name,
                                 email=email,
                                 password=password)
        con = {
               'uid':"successfully add data........"
        }
        return render(request,"register.html",con)
     else:
        return render(request,"register.html")
     
def search(request):
    product_name = request.GET['product_name']

    if product_name:
        pid = Add_product.objects.filter(name__contains=product_name)

        con = {
            'pid' : pid
        }
        return render(request,'shop.html',con)
    else:
        return render(request,'index.html')
    
def billing_address(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        aid = Address.objects.filter(user_id=uid).exists()
        cid = Address.objects.get(user_id=uid)

        if aid:
            l1 = []
            pid = Add_to_cart.objects.filter(user_id=uid)
            for i in pid:
                l1.append(f"name = {i.name} price= {i.price} qty= {i.qty} total_price={i.total_price}")

            cid.list= l1
            cid.save()
            return redirect('checkout')
    except:
        if request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_name = request.POST['user_name']
            email= request.POST['email']
            address= request.POST['address']
            address_2= request.POST['address_2']
            country= request.POST['country']
            state= request.POST['state']
            pincode= request.POST['pincode']
            
            bid = Address.objects.create(user_id=uid,
                                         first_name=first_name,
                                        last_name=last_name,
                                        user_name=user_name,
                                        email=email,
                                        address=address,
                                        address_2=address_2,
                                        country=country,
                                        state=state,
                                        pincode=pincode)
        
            l1 = []
        
            aid = Add_to_cart.objects.filter(user_id=uid)
            
            for i in aid:
                l1.append(f"name = {i.name}  price = {i.price}  qty = {i.qty} total_price = {i.total_price} ")

                bid.list = l1
                bid.save()

            return redirect("checkout")
        else:
            return render(request,"billing_address.html")
            
def change_address(request):
    uid = User.objects.get(email=request.session['email'])
    did = Address.objects.get(user_id=uid).delete()

    return redirect('billing_address')

def my_address(request):
    uid = User.objects.get(email=request.session['email'])

    aid=Address.objects.filter(user_id=uid)
    con={
        'aid':aid
        }

    return render(request,'my_address.html',con)

def gallery(request):
    cid = Add_product.objects.all()
    gid = Add_product.objects.all()

    con={
        'cid' : cid,
        'gid' : gid
    }
    return render(request,'gallery.html',con)

def category_gallery(request):
    cid = Add_product.objects.all()
    gid = Add_product.objects.all()

    con={
        'cid' : cid,
        'gid' : gid
    }
    return render(request,'gallery.html',con)
