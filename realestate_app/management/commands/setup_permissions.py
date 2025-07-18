from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from realestate_app.models import CustomUser, Property, Blog

class Command(BaseCommand):
    help = 'Set up Blog and Property roles with model permissions'

    def handle(self, *args, **kwargs):
        # Step 1: Create groups
        blog_group, _ = Group.objects.get_or_create(name="BlogStaff")
        property_group, _ = Group.objects.get_or_create(name="PropertyStaff")

        # Step 2: Get content types
        blog_ct = ContentType.objects.get_for_model(Blog)
        property_ct = ContentType.objects.get_for_model(Property)

        # Step 3: Assign permissions to each group
        blog_permissions = Permission.objects.filter(content_type=blog_ct)
        property_permissions = Permission.objects.filter(content_type=property_ct)

        blog_group.permissions.set(blog_permissions)
        property_group.permissions.set(property_permissions)

        # ✅ Step 4: Assign users to groups
        for user in CustomUser.objects.filter(role='blog'):
            user.groups.clear()
            user.groups.add(blog_group)

        for user in CustomUser.objects.filter(role='property'):
            user.groups.clear()
            user.groups.add(property_group)

        self.stdout.write(self.style.SUCCESS("✅ Blog and Property roles set up with permissions."))
