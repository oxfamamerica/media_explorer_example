from django.db import models
from media_explorer.fields import MediaField, RichTextField

class Blog(models.Model):
    """
    Example Blog model
    """

    title = models.CharField(max_length=150)

    #If you do not provide a type then media can be image/video/gallery
    lead_media = MediaField()

    #Providing a type will restrict the element to this type
    video = MediaField(type="video")

    #Entry is changed from TextField to RichTextField
    #You will see a CKEditor WYSIWYG with DME plugin
    #NOTE: You cannot use more than one RichText field in a model
    entry = RichTextField()
