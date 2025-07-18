from django.urls import path

from .views import *



urlpatterns = [
    path('user-add/',SignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('',IndexView.as_view(),name='index'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('users/',UserListView.as_view(),name='users'),
    path('user-edit/<int:pk>/',UserEditView.as_view(),name='user-edit'),
    path('user-delete/<int:pk>/',UserDeleteView.as_view(),name='user-delete'),
    path('blog-post/',BlogPublishView.as_view(),name='blog-post'),
    path('blog-draft/',BlogDraftView.as_view(),name='drafts'),
    path('blog-list/',BlogListView.as_view(),name='blog-list'),
    path('blog-edit/<int:pk>/',BlogEditView.as_view(),name='blog-edit'),
    path('blog-delete/<int:pk>/',BlogDeleteView.as_view(),name='blog-delete'),
    path('draft-delete/',BlogDraftDeleteView.as_view(),name='draft-delete'),
    path('builders/',PropertyBuilderListView.as_view(),name='builders'),
    path('builder-add/',PropertyBuilderAddView.as_view(),name='builder-add'),
    path('builder-edit/<int:pk>/',PropertyBuilderEditView.as_view(),name='builder-edit'),
    path('builder-delete/<int:pk>/',PropertyBuilderDeleteView.as_view(),name='builder-delete'),
    path('builder/toggle-status/<int:pk>/',ToggleBuilderStatusView.as_view(),name='builder-toggle-status'),
    path('community-list/',PropertyCommunityListView.as_view(),name='community-list'),
    path('community-add/',PropertyCommunityAddView.as_view(),name='community-add'),
    path('toggle-blog/<int:pk>/',ToggleBlogStatusView.as_view(),name='toggle-blog'),
    path('blog/<int:blog_id>/save-to-draft/', save_to_draft, name='save-to-draft'),
    path('publish-blog/<int:blog_id>/',publish_blog,name='publish-blog'),
    path('community-list/',PropertyCommunityListView.as_view(),name='community-list'),
    path('community-toggle/<int:pk>/',ToggleCommunityView.as_view(),name='community-toggle'),
    path('community-edit/<int:pk>/',PropertyCommunityEditView.as_view(),name='community-edit'),
    path('community-delete/<int:pk>/',PropertyCommunityDeleteView.as_view(),name='community-delete'),
    path('blog-images/',BlogImageGalleryView.as_view(),name='blog-images'),
    path('blog-images/delete/<int:pk>/',BlogImageGalleryDeleteView.as_view(),name='delete-blogimg'),
    path('builder-logo/',BuilderGalleryView.as_view(),name='builder-logo'),
    path('builder-logo/delete/<int:pk>/',BuilderGalleryDeleteView.as_view(),name='delete-builder'),
    path('toggle-staffs/<int:pk>/',ToggleUserView.as_view(),name='toggle-staffs'),
   
     


     # PROPERTY SECTION
     path('add/', AddPropertyView.as_view(), name='add_property'),
    path('edit/<int:pk>/', EditPropertyView.as_view(), name='property-edit'),
    path('list/', PropertyListView.as_view(), name='property-list'),
    path('delete/<int:pk>/', PropertyDeleteView.as_view(), name='property-delete'),
    path('drafts/', DraftPropertyListView.as_view(), name='property-draft'),
    path('<int:pk>/publish/', PublishPropertyView.as_view(), name='property-publish'),
    path('<int:pk>/draft/', MoveToDraftView.as_view(), name='property-move-to-draft'),  # ✅ FIXED
    path('<int:pk>/toggle-status/', TogglePropertyStatusView.as_view(), name='property-toggle-status'),
    path('amenities/', AmenityListView.as_view(), name='amenities-list'),
    path('amenities/add/', AddAmenityView.as_view(), name='amenities-add'),
     path('amenities/<int:pk>/edit/', EditAmenityView.as_view(), name='amenity-edit'),
    path('amenities/<int:pk>/delete/', DeleteAmenityView.as_view(), name='amenity-delete'),
    path('amenities/<int:pk>/toggle-status/', ToggleAmenityStatusView.as_view(), name='amenity-toggle-status'),
    
    
    path('property-types/', PropertyTypeListView.as_view(), name='property-type-list'),
    path('property-types/add/', AddPropertyTypeView.as_view(), name='property-type-add'),
    path('property-types/<int:pk>/edit/', EditPropertyTypeView.as_view(), name='property-type-edit'),
    path('property-types/<int:pk>/delete/', DeletePropertyTypeView.as_view(), name='property-type-delete'),
    path('property-types/<int:pk>/toggle-status/', TogglePropertyTypeStatusView.as_view(), name='property-type-toggle-status'),
    path('information/', InformationListView.as_view(), name='information-list'),
    path('information/add/', InformationCreateView.as_view(), name='information-add'),
    path('information/edit/<int:pk>/', InformationUpdateView.as_view(), name='information-edit'),
    path('information/delete/<int:pk>/', InformationDeleteView.as_view(), name='information-delete'),
    path('property-images/',PropertyImageGalleryView.as_view(),name='property-images'),
    path('property-images/delete/<int:pk>/',PropertyImageGalleryDeleteView.as_view(),name='delete-property-images')
    

]





