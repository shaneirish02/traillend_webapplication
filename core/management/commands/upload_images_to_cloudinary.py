import os
from django.core.management.base import BaseCommand
from cloudinary.uploader import upload
from django.conf import settings
from core.models import Item

class Command(BaseCommand):
    help = "Uploads local item images to Cloudinary and updates the database with Cloudinary URLs."

    def handle(self, *args, **kwargs):
        # Location where your local images are stored
        LOCAL_IMAGE_DIR = os.path.join(settings.BASE_DIR, "core", "static", "inventory", "items")

        self.stdout.write(self.style.WARNING("Starting Cloudinary upload process..."))

        items = Item.objects.all()

        for item in items:
            if not item.image:
                self.stdout.write(self.style.WARNING(f"Skipping '{item.name}': No image"))
                continue

            image_name = os.path.basename(item.image.name)

            # Check if already Cloudinary
            if str(item.image).startswith("http"):
                self.stdout.write(self.style.SUCCESS(f"Already on Cloudinary: {item.name}"))
                continue

            local_path = os.path.join(LOCAL_IMAGE_DIR, image_name)

            if not os.path.exists(local_path):
                self.stdout.write(self.style.ERROR(f"File not found for '{item.name}': {local_path}"))
                continue

            self.stdout.write(f"Uploading '{item.name}'...")

            # Upload the file
            result = upload(
                local_path,
                folder="items/",
                resource_type="image"
            )

            cloudinary_url = result["secure_url"]

            # Update the database
            item.image = cloudinary_url
            item.save()

            self.stdout.write(self.style.SUCCESS(f"Uploaded & updated: {item.name}"))

        self.stdout.write(self.style.SUCCESS("Done! All images have been processed."))
