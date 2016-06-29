from constance import config
from os import path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from PIL import Image

from accounts.models import UserProfile
from events.models import Event


class Command(BaseCommand):
    help = 'Resize all images in fields small_image and big_image'

    def handle(self, *args, **options):
        """
        Run resize command
        :param args:
        :param options:
        :return:
        """

        for event in Event.objects.all().iterator():
            new_name = slugify(event.title)
            is_change = False
            if event.small_image:
                if event.small_image.width != Event.SMALL_IMAGE_WIDTH or \
                                event.small_image.height != Event.SMALL_IMAGE_HEIGHT:
                    resize_image(
                        event.small_image,
                        new_name,
                        Event.SMALL_IMAGE_WIDTH,
                        Event.SMALL_IMAGE_HEIGHT,
                    )
                    is_change = True

            if event.big_image:
                if event.big_image.width != Event.BIG_IMAGE_WIDTH or \
                                event.big_image.height != Event.BIG_IMAGE_HEIGHT:
                    resize_image(
                        event.big_image,
                        new_name,
                        Event.BIG_IMAGE_WIDTH,
                        Event.BIG_IMAGE_HEIGHT,
                    )
                    is_change = True

            if is_change:
                event.save()

def resize_image(image_field, new_name, width, height):
    """
    Calculate proportion and rescale
    :param image_field:
    :param new_name: new file name without extension
    :param width: maximal new width
    :param height: maximal new height
    """

    new_height = width * image_field.height / image_field.width
    if new_height > height:
        new_width = height * image_field.width / image_field.height
        new_height = height
    else:
        new_width = width
    size = (new_width, new_height)

    ext = image_field.name.split('.')[-1].lower()
    pref = image_field.name.split('/')[0]
    new_name = "{0}.{1}".format(new_name, ext)
    new_feld_path = path.join(pref, new_name)
    new_path = path.join(settings.MEDIA_ROOT, pref, new_name)

    image_field.open()
    org_image = Image.open(image_field)

    resized_image = org_image.resize(size)
    resized_image.save(new_path)
    image_field.name = new_feld_path
    image_field.close()
    # image_field.save(new_name, resized_image)

    print("NEWPATH: {}".format(new_path))
