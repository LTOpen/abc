from django.db import models
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files.base import ContentFile
from easy_thumbnails.fields import ThumbnailerImageField
from pathlib import Path


class Account(models.Model):
    name = models.CharField(max_length=64)
    icon = ThumbnailerImageField(upload_to="account_icons/", blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     is_new = self.pk is None
    #     if self.icon and is_new:
    #         img = Image.open(self.icon).convert("RGBA")

    #         # Create a thumbnail of the image
    #         img.resize((512, 512), Image.Resampling.LANCZOS)

    #         # Create a circular mask
    #         mask = Image.new("L", (512, 512), 0)
    #         draw = ImageDraw.Draw(mask)
    #         draw.ellipse((0, 0, 512, 512), fill=255)
    #         print(img.size)
    #         # Apply the circular mask to the image
    #         circular_img = Image.new("RGBA", (512, 512))
    #         print(circular_img.size)
    #         circular_img.paste(
    #             img, ((512 - img.size[0]) // 2, (512 - img.size[1]) // 2), mask=mask
    #         )

    #         # Save the circular image as ICO
    #         output = BytesIO()
    #         circular_img.save(output, format="PNG")
    #         output.seek(0)
    #         self.icon.save(
    #             "backed/" + Path(self.icon.name).stem + ".png",
    #             ContentFile(output.read()),
    #             save=False,
    #         )
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name
