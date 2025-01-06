from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from pathlib import Path


class Account(models.Model):
    name = models.CharField(max_length=64)
    icon = models.ImageField(
        upload_to="account_icons/",
        blank=True,
        width_field="width",
        height_field="height",
    )
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.icon and isinstance(self.icon, UploadedFile):
            print(self.icon)
            img = Image.open(self.icon)

            img.thumbnail((512, 512), Image.Resampling.LANCZOS)

            new_img = Image.new("RGB", (512, 512), (255, 255, 255))

            new_img.paste(img, ((512 - img.size[0]) // 2, (512 - img.size[1]) // 2))

            output = BytesIO()
            new_img.save(output, format="ICO")
            output.seek(0)
            self.icon.save(
                "backed/" + Path(self.icon.name).stem + ".ico",
                ContentFile(output.read()),
                save=False,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
