from django.shortcuts import render,redirect
from django.views.generic import View
from realestate_app.models import CustomUser,Blog,Builder,Community,BlogGallery,BuilderLogos,PropertyImage,PropertyGallery
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.

class SignupView(View):
    def get(self, request, *args, **kwargs):
       
        return render(request, 'signup.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phonenumber', '').strip()
        password = request.POST.get('password', '')
        cpassword = request.POST.get('cpassword', '')
        role = request.POST.get('role', '').strip()
        is_active = request.POST.get('is_active') == "True"

        # Validate required fields
        if not username:
            messages.error(request, "Username is required.")
            return redirect('signup')

        if not email:
            messages.error(request, "Email is required.")
            return redirect('signup')

        if not phone or not phone.isdigit():
            messages.error(request, "Please enter a valid phone number.")
            return redirect('signup')
        phone = int(phone)

        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Create user
        CustomUser.objects.create(
            username=username,
            email=email,
            phonenumber=phone,
            password=make_password(password),
            role=role,
            is_active=is_active
        )

        messages.success(request, "User created successfully.")
        return redirect('signup')
  
class LoginView(View):
  def get(self,request,*args,**kwargs):
    return render(request,'sign-in.html')
  
  def post(self,request,*args,**kwargs):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user_obj = authenticate(username=username,password=password)
    if user_obj:
      login(request,user_obj)
    return redirect('index')
  
class LogoutView(View):
  def get(self,request,*args,**kwargs):
    logout(request)
    return redirect('login')
  
class IndexView(View):
  def get(self,request,*args,**kwargs):
    if not request.user.is_authenticated:
      return redirect('login')
    return render(request,'index.html')
  
class UserListView(View):
  def get(self,request,*args,**kwargs):
    if not request.user.is_authenticated:
      return redirect('login')
    staffs = CustomUser.objects.filter(is_superuser=False)

    
    return render(request,'users.html',{'staffs':staffs})
  
class UserEditView(View):
    def get(self, request, *args, **kwargs):
        staff_id = kwargs.get('pk')
        staff_obj = CustomUser.objects.filter(is_superuser=False).get(id=staff_id)
        return render(request, 'signup.html', {'staff': staff_obj})
  
    def post(self, request, *args, **kwargs):
        staff_id = kwargs.get('pk')
        staff_user = CustomUser.objects.get(id=staff_id)
        reset_mode = request.GET.get('reset') == 'password'

        if reset_mode:
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            if password == cpassword:
                staff_user.password = make_password(password)
                staff_user.save(update_fields=['password'])
            return redirect('users')

        username = request.POST.get('username')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active')

        staff_user.username = username
        staff_user.email = email
        staff_user.phonenumber = phonenumber
        staff_user.role = role
        staff_user.is_active = is_active == 'True'
        staff_user.save()

        # ✅ Update group assignment
        staff_user.groups.clear()
        group = Group.objects.filter(name__iexact=f"{role.capitalize()}Staff").first()
        if group:
            staff_user.groups.add(group)

        return redirect('users')
  
class UserDeleteView(View):
  def get(self,request,*args,**kwargs):
    staff_id = kwargs.get('pk')    
    CustomUser.objects.get(id=staff_id).delete()
    return redirect('users')

class BlogPublishView(PermissionRequiredMixin, View):
    permission_required = 'realestate_app.add_blog'  # or 'realestate_app.change_blog' if editing
    raise_exception = True  # This makes Django return 403 instead of redirecting to login

    def get(self, request, *args, **kwargs):
        return render(request, 'blog-post.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        description = request.POST.get('description')
        img = request.FILES.get('img')
        action = request.POST.get('action')

        # Handling booleans and integers safely
        is_active_raw = request.POST.get('is_active', '').strip().lower()
        is_active = is_active_raw == 'true'
        add_to_homepage = 'add_to_homepage' in request.POST

        try:
            reorder = int(request.POST.get('reorder', 0))
        except ValueError:
            reorder = 0

        # Create Blog instance
        blog = Blog(title=title, description=description, img=img)

        if action == 'publish':
            blog.status = 'publish'
            blog.is_active = is_active
            blog.add_to_homepage = add_to_homepage
            blog.reorder = reorder
        elif action == 'draft':
            blog.status = 'draft'
            blog.is_active = False
            blog.add_to_homepage = False
            blog.reorder = 0

        blog.save()

        # Create gallery entries for all blogs - not sure if you want this on every post save
        blogs = Blog.objects.all()
        for blog_item in blogs:
            BlogGallery.objects.create(blog=blog_item, image=blog_item.img)

        return redirect('blog-list')

      


# class BlogListView(View):
#   def get(self,request,*args,**kwargs):
#     blogs =Blog.objects.all()
#     return render(request,'blog-list.html',{'blogs':blogs}) 
  
class BlogEditView(PermissionRequiredMixin, View):
    permission_required = 'realestate_app.change_blog'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get('pk')
        blog_obj = Blog.objects.get(id=blog_id)
        return render(request, 'blog-post.html', {'blog': blog_obj})

    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get('pk')
        blog_obj = Blog.objects.get(id=blog_id)

        title = request.POST.get('title')
        description = request.POST.get('description')
        img = request.FILES.get('img')

        is_active_raw = request.POST.get('is_active', '').strip().lower()
        is_active = is_active_raw == 'true'

        add_to_homepage = 'add_to_homepage' in request.POST

        try:
            reorder = int(request.POST.get('reorder', 0))
        except ValueError:
            reorder = 0

        action = request.POST.get('action')
        status = 'draft'
        if action == 'publish':
            status = 'publish'
        elif action == 'draft':
            is_active = False
            add_to_homepage = False
            reorder = 0

        blog_obj.title = title
        blog_obj.description = description
        blog_obj.is_active = is_active
        blog_obj.add_to_homepage = add_to_homepage
        blog_obj.reorder = reorder
        blog_obj.status = status

        if img:
            blog_obj.img = img

        blog_obj.save()

        return redirect('drafts' if status == 'draft' else 'blog-list')


   

   
class BlogListView(View):
   def get(self,request,*args,**kwargs):
      blogs = Blog.objects.filter(status='publish')
      return render(request,'blog-list.html',{'blogs':blogs})
   
class BlogDeleteView(View):
   def get(self,request,*args,**kwargs):
      blogs_id = kwargs.get('pk')
      Blog.objects.get(id=blogs_id).delete()
      return redirect('blog-list')
   
class BlogDraftView(View):
   def get(self,request,*args,**kwargs):
     blogs = Blog.objects.filter(status='draft')
     print("🔥 BlogDraftView called")
     print(blogs)
     return render(request,'blog-drafts.html',{'blogs':blogs})
   
class BlogDraftDeleteView(View):
   def get(self,request,*args,**kwargs):
      blog_id = kwargs.get('pk')
      Blog.objects.get(id=blog_id).delete()
      return render('drafts')
   
class PropertyBuilderListView(View):
   def get(self,request,*args,**kwargs):
      builders = Builder.objects.all()
      return render(request,'Builders.html',{'builders':builders})
   
class PropertyBuilderAddView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'builder-add.html')

    def post(self, request, *args, **kwargs):
        names = request.POST.getlist('name[]')
        statuses = request.POST.getlist('status[]')
        logos = request.FILES.getlist('img[]')

        for i in range(len(names)):
            name = names[i]
            status = statuses[i] == 'True'  # Convert to boolean
            logo = logos[i] if i < len(logos) else None  # Avoid index error if no file uploaded

            Builder.objects.create(
                name=name,
                status=status,
                logo=logo
            )
        
        builders=Builder.objects.all()
        for builder in builders:
           BuilderLogos.objects.create(builder=builder,image=builder.logo)
          
        return redirect('builders')

   
class PropertyBuilderEditView(View):
   def get(self,request,*args,**kwargs):
      builder_id = kwargs.get('pk')
      builder_obj =  Builder.objects.get(id=builder_id)
      print(builder_obj.logo)
      return render(request,'builder-add.html',{'builder_obj':builder_obj})
   
   def post(self,request,*args,**kwargs):
        builder_id = kwargs.get('pk')
        builder_obj = Builder.objects.get(id=builder_id)

        name = request.POST.get('name')
        img = request.FILES.get('img')
        status = request.POST.get('status')
        addToHomepage = 'addToHomepage' in request.POST

        try:
            displayOrder = int(request.POST.get('displayOrder', 0))
        except ValueError:
            displayOrder = 0

        builder_obj.name = name

        if img:
          builder_obj.logo = img

        builder_obj.status = status
        builder_obj.add_to_homepage = addToHomepage
        builder_obj.reorder = displayOrder

        builder_obj.save()
        return redirect('builders')
   
class PropertyBuilderDeleteView(View):
   def get(self,request,*args,**kwargs):
      builder_id = kwargs.get('pk')
      Builder.objects.get(id=builder_id).delete()
      return redirect('builders')
   
class ToggleBuilderStatusView(View):
   def post(self,request,*args,**kwargs):
      builder_id = kwargs.get('pk')
      builder_obj = Builder.objects.get(id=builder_id)
      builder_obj.status = not builder_obj.status
      builder_obj.save()
      return JsonResponse({'status':builder_obj.status})
   
class ToggleBlogStatusView(View):
   def post(self,request,*args,**kwargs):
      blog_id = kwargs.get('pk')
      blog_obj = Blog.objects.get(id=blog_id)
      blog_obj.is_active = not blog_obj.is_active 
      blog_obj.save()
      return JsonResponse({'status':blog_obj.is_active})
   
class PropertyCommunityListView(View):
   def get(self,request,*args,**kwargs):
      return render(render,'community.html')
   
class PropertyCommunityAddView(View):
   def get(self,request,*args,**kwargs):
      return render(request,'community-add.html')
   
   def post(self,request,*args,**kwargs):
      name = request.POST.getlist('name[]')
      status = request.POST.getlist('status[]') # the list data contain name and string name are must to be different
      for i in range(len(name)):  # eg statuses and status , status is a list and statuses is a string 
          names = name[i] 
          statuses = status[i] == 'True' 
          Community.objects.create(name=names,status=statuses)
      return redirect('community-list')
   
class PropertyCommunityListView(View):
   def get(self,request,*args,**kwargs):
      community_list = Community.objects.all()
      return render(request,'community.html',{'community_list':community_list})
   

def save_to_draft(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    blog.status = 'draft'
    blog.save()
    return redirect('blog-list')

def publish_blog(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        blog.status = 'publish'
        blog.save()
        return redirect('drafts') 
         
class ToggleCommunityView(View):
   def post(self,request,*args,**kwargs):
      community_id = kwargs.get('pk')
      community_obj = Community.objects.get(id=community_id)
      community_obj.status = not community_obj.status

      community_obj.save()
      return JsonResponse({'status':community_obj.status})
   
class ToggleUserView(View):
   def post(self,request,*args,**kwargs):
      staff_id = kwargs.get('pk')
      staff_obj = CustomUser.objects.get(id=staff_id)
      staff_obj.is_active = not staff_obj.is_active
      return JsonResponse({'status':staff_obj.is_active})
   
class PropertyCommunityEditView(View):
   def get(self,request,*args,**kwargs):
      community_id = kwargs.get('pk')
      community_obj = Community.objects.get(id=community_id)
      return render(request,'community-add.html',{'community_obj':community_obj})
   
   def post(self,request,*args,**kwargs):
      community_id = kwargs.get('pk')
      community_obj = Community.objects.get(id=community_id)

      name = request.POST.get('name')
      status = request.POST.get('status')

      community_obj.name = name
      community_obj.status = status

      community_obj.save()
      return redirect('community-list')
   
class PropertyCommunityDeleteView(View):
   def get(self,request,*args,**kwargs):
      community_id = kwargs.get('pk')
      Community.objects.get(id=community_id).delete()
      return redirect('community-list')
  
class BlogImageGalleryView(View):
   def get(self,request,*args,**kwargs):
      blog_gallery = BlogGallery.objects.all()
      return render(request,'blog-images.html',{'blog_gallery':blog_gallery})
  

class BlogImageGalleryDeleteView(View):
   def get(self,request,*args,**kwargs):
      blog_img_id = kwargs.get('pk')
      blog_gallery =BlogGallery.objects.get(id=blog_img_id)
      # Check: if this image is also set as Blog main image
      if blog_gallery.blog.img.name == blog_gallery.image.name:
            blog_gallery.blog.img.delete(save=False)  # Delete the image file
            blog_gallery.blog.img = None              # Remove from model
            blog_gallery.blog.save()

      blog_gallery.delete()
      return redirect('blog-images')
   
class BuilderGalleryView(View):
   def get(self,request,*args,**kwargs):
      builder_gallery = BuilderLogos.objects.all()
      return render(render,'builders-logogallery.html',{'builder_img':builder_gallery})
   
class BuilderGalleryDeleteView(View):
   def get(self,request,*args,**kwargs):
      builder_id = kwargs.get('pk')
      builder_obj = BuilderLogos.objects.get(id=builder_id)
      if builder_obj.builder.logo.name == builder_obj.image.name:
            builder_obj.builder.logo.delete(save=False)  # Delete the image file
            builder_obj.builder.logo = None              # Remove from model
            builder_obj.builder.save()

      builder_obj.delete()
      return redirect('builder-logo')

      
   # PROPERTY SECTION
   

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Property, PropertyImage, Amenity, PropertyType
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class AddPropertyView(View):
    def get(self, request):
        property_type_id = request.GET.get('property_type')
        builders  = Builder.objects.all()
        communities = Community.objects.all()
        infos = Information.objects.all()
       
        
        amenities = Amenity.objects.all()
        property_types = PropertyType.objects.filter(status='Active')
        return render(request, 'add_property.html', {
            'property': None,
            'amenities': amenities,
            'property_types': property_types,
            'selected_property_type': property_type_id,
            'builders' :builders,
            'communities':communities,
            'infos':infos
        })

    def post(self, request):
        action = request.POST.get('action')

        builder_id = request.POST.get('builder')
        builder = Builder.objects.get(id=builder_id)

        community_id = request.POST.get('community')
        community = Community.objects.get(id=community_id)

        info_id = request.POST.get('property_info')
        info_obj = Information.objects.get(id=info_id)


        
        status = 'draft' if action == 'draft' else request.POST.get('status') or 'active'
        add_to_homepage = request.POST.get('addToHomepage') == 'Add To Home Page'

        # ✅ FIXED: Use property_type_id instead of assigning FK instance
        property_type_raw = request.POST.get('property_type')
        try:
            property_type_id = int(property_type_raw) if property_type_raw else None
        except ValueError:
            property_type_id = None

        property_obj = Property.objects.create(
            property_name=request.POST.get('property_name'),
            property_address=request.POST.get('property_address'),
            property_description=request.POST.get('property_description'),
            property_type_id=property_type_id,  # ✅ THIS IS THE CORRECT FIELD TO SET
            price=request.POST.get('price') or 0,
            bedrooms=request.POST.get('bedrooms') or 0,
            bathrooms=request.POST.get('bathrooms') or 0,
            min_sqft=request.POST.get('min_sqft') or 0,
            max_sqft=request.POST.get('max_sqft') or 0,
            location=request.POST.get('location'),
            status=status,
            addToHomepage=add_to_homepage,
            displayOrder=request.POST.get('displayOrder') or None,
            builder = builder,
            community=community,
            information = info_obj

        )

        property_obj.amenities = request.POST.getlist('amenities[]')

        if 'floorplanPDF' in request.FILES:
            property_obj.floorplanPDF = request.FILES['floorplanPDF']
        if 'brochurePDF' in request.FILES:
            property_obj.brochurePDF = request.FILES['brochurePDF']

        property_obj.save()

        images = request.FILES.getlist('propertyImages[]')
        for image in images:
            PropertyImage.objects.create(property=property_obj, image=image)
        
        prop_imgs = PropertyImage.objects.all()
        for p_img in prop_imgs:
           PropertyGallery.objects.create(propertyimage=p_img,img=p_img.image)

        return redirect('property-draft' if action == 'draft' else 'property-list')


class EditPropertyView(View):
    def get(self, request, pk):
        amenities = Amenity.objects.all()
        property_obj = get_object_or_404(Property, pk=pk)
        property_types = PropertyType.objects.filter(status='Active')
        
        return render(request, 'add_property.html', {
            'property': property_obj,
            'amenities': amenities,
            'property_types': property_types,
            'selected_property_type': property_obj.property_type_id,
        })

    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        was_draft = property_obj.status == 'draft'

        # ✅ Fix: Ensure property_type is converted to int or None
        property_type_id_raw = request.POST.get('property_type')
        try:
            property_type_id = int(property_type_id_raw) if property_type_id_raw else None
        except ValueError:
            property_type_id = None

        property_obj.property_name = request.POST.get('property_name')
        property_obj.property_address = request.POST.get('property_address')
        property_obj.property_description = request.POST.get('property_description')
        property_obj.property_type_id = property_type_id
        property_obj.price = request.POST.get('price') or 0
        property_obj.bedrooms = request.POST.get('bedrooms') or 0
        property_obj.bathrooms = request.POST.get('bathrooms') or 0
        property_obj.min_sqft = request.POST.get('min_sqft') or 0
        property_obj.max_sqft = request.POST.get('max_sqft') or 0
        property_obj.location = request.POST.get('location')
        property_obj.addToHomepage = request.POST.get('addToHomepage') == 'Add To Home Page'
        property_obj.displayOrder = request.POST.get('displayOrder') or None
        property_obj.amenities = request.POST.getlist('amenities[]')

        if 'floorplanPDF' in request.FILES:
            property_obj.floorplanPDF = request.FILES['floorplanPDF']
        if 'brochurePDF' in request.FILES:
            property_obj.brochurePDF = request.FILES['brochurePDF']

        new_status = request.POST.get('status')
        if new_status:
            property_obj.status = new_status

        property_obj.save()

        images = request.FILES.getlist('propertyImages[]')
        for image in images:
            PropertyImage.objects.create(property=property_obj, image=image)

        return redirect('property-draft' if was_draft else 'property-list')




class PropertyListView(View):
    def get(self, request):
        properties = Property.objects.exclude(status='draft').prefetch_related('images').order_by('-id')
        return render(request, 'property-list.html', {'properties': properties})


class DraftPropertyListView(View):
    def get(self, request):
        properties = Property.objects.filter(status='draft').prefetch_related('images').order_by('-id')
        return render(request, 'property-draft.html', {'properties': properties})


class PropertyDeleteView(DeleteView):
    model = Property
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('property-list')


class PublishPropertyView(View):
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        property_obj.status = 'active'
        property_obj.save()
        return redirect('property-draft')


class MoveToDraftView(View):
    def post(self, request, pk):
        property_obj = get_object_or_404(Property, pk=pk)
        property_obj.status = 'draft'
        property_obj.save()
        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class TogglePropertyStatusView(View):
    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
            property_obj.status = 'inactive' if property_obj.status == 'active' else 'active'
            property_obj.save()
            return JsonResponse({'success': True, 'new_status': property_obj.status})
        except Property.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Property not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class AmenityListView(View):
    def get(self, request):
        amenities = Amenity.objects.all()
        return render(request, 'amenities.html', {'amenities': amenities})


class AddAmenityView(View):
    def get(self, request):
        return render(request, 'amenities-add.html')

    def post(self, request):
        names = request.POST.getlist('amenity_name[]')
        statuses = request.POST.getlist('status[]')

        for name, status in zip(names, statuses):
            if name.strip():
                Amenity.objects.create(name=name.strip(), status=status)
        return redirect('amenities-list')


class DeleteAmenityView(View):
    def post(self, request, pk):
        amenity = get_object_or_404(Amenity, pk=pk)
        amenity.delete()
        return redirect('amenities-list')


class EditAmenityView(View):
    def get(self, request, pk):
        amenity = get_object_or_404(Amenity, pk=pk)
        return render(request, 'amenities-add.html', {
            'amenity': amenity,
            'form_mode': 'Edit',
            'is_edit': True,
        })

    def post(self, request, pk):
        amenity = get_object_or_404(Amenity, pk=pk)
        name = request.POST.getlist('amenity_name[]')
        status = request.POST.getlist('status[]')
        if name and status:
            amenity.name = name[0].strip()
            amenity.status = status[0].strip()
            amenity.save()
        return redirect('amenities-list')


@method_decorator(csrf_exempt, name='dispatch')
class ToggleAmenityStatusView(View):
    def post(self, request, pk):
        amenity = Amenity.objects.get(pk=pk)
        amenity.status = 'Inactive' if amenity.status == 'Active' else 'Active'
        amenity.save()
        return JsonResponse({'success': True, 'new_status': amenity.status})


class PropertyTypeListView(View):
    def get(self, request):
        property_types = PropertyType.objects.all()
        return render(request, 'property-type.html', {'property_types': property_types})


class AddPropertyTypeView(View):
    def get(self, request):
        return render(request, 'propertytype-add.html')

    def post(self, request):
        names = request.POST.getlist('property_type_name[]')
        statuses = request.POST.getlist('status[]')

        if names:
            for name, status in zip(names, statuses):
                name = name.strip()
                if name:
                    PropertyType.objects.create(name=name, status=status or 'Active')
        else:
            name = request.POST.get('name', '').strip()
            status = request.POST.get('status', 'Active')
            if name:
                PropertyType.objects.create(name=name, status=status)

        return redirect('property-type-list')


class EditPropertyTypeView(View):
    def get(self, request, pk):
        pt = get_object_or_404(PropertyType, pk=pk)
        return render(request, 'propertytype-add.html', {
            'propertytype': pt,
            'form_mode': 'Edit',
            'is_edit': True
        })

    def post(self, request, pk):
        pt = get_object_or_404(PropertyType, pk=pk)
        pt.name = request.POST.get('name').strip()
        pt.status = request.POST.get('status', 'Active')
        pt.save()
        return redirect('property-type-list')


class DeletePropertyTypeView(View):
    def post(self, request, pk):
        pt = get_object_or_404(PropertyType, pk=pk)
        pt.delete()
        return redirect('property-type-list')


@method_decorator(csrf_exempt, name='dispatch')
class TogglePropertyTypeStatusView(View):
    def post(self, request, pk):
        pt = get_object_or_404(PropertyType, pk=pk)
        pt.status = 'Inactive' if pt.status == 'Active' else 'Active'
        pt.save()
        return JsonResponse({'success': True, 'new_status': pt.status})



#INFORMATION SECTION 

      
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Information


class InformationListView(ListView):
    model = Information
    template_name = 'information.html'
    context_object_name = 'information_list'


class InformationCreateView(View):
    template_name = 'information-add.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get('name')
        status = request.POST.get('status')

        if not name or not status:
            messages.error(request, "All fields are required.")
            return render(request, self.template_name)

        Information.objects.create(
            name=name.strip(),
            status=status.strip()
        )
        messages.success(request, "Information added successfully.")
        return redirect('information-list')


class InformationUpdateView(View):
    template_name = 'information-add.html'

    def get(self, request, pk):
        info = get_object_or_404(Information, pk=pk)
        return render(request, self.template_name, {'info': info})

    def post(self, request, pk):
        info = get_object_or_404(Information, pk=pk)
        name = request.POST.get('name')
        status = request.POST.get('status')

        if not name or not status:
            messages.error(request, "All fields are required.")
            return render(request, self.template_name, {'info': info})

        info.name = name.strip()
        info.status = status.strip()
        info.save()

        messages.success(request, "Information updated successfully.")
        return redirect('information-list')
    


class InformationDeleteView(View):
    def post(self, request, pk):
        info = get_object_or_404(Information, pk=pk)
        info.delete()
        messages.success(request, "Information deleted successfully.")
        return redirect('information-list')
    

class PropertyImageGalleryView(View):
   def get(self,request,*args,**kwargs):
      property_imgs = PropertyGallery.objects.all()
      return render(request,'property-images.html',{'property_imgs':property_imgs})

      

class PropertyImageGalleryDeleteView(View):
   def get(self,request,*args,**kwargs):
      propgall_id = kwargs.get('pk')
      propgall_obj = PropertyGallery.objects.get(id=propgall_id)
      if propgall_obj.propertyimage.image.name == propgall_obj.img.name:
            propgall_obj.propertyimage.image.delete(save=False)  # Delete the image file
            propgall_obj.propertyimage.image = None              # Remove from model
            propgall_obj.propertyimage.save()

      propgall_obj.delete()
      return redirect('builder-logo')

      
   

    



 

    

    
 







         



   








    