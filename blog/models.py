from django.db import models
from django.core.urlresolvers import reverse
from media_explorer.fields import MediaField, RichTextField

class Blog(models.Model):
    """
    Example Blog model
    """

    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=150)

    #If you do not provide a type then media can be image/video/gallery
    lead_media = MediaField()

    #Providing a type will restrict the element to this type
    video = MediaField(type="video")

    #You will see a CKEditor WYSIWYG with DME plugin
    #NOTE: You cannot use more than one RichText field in a model
    entry = RichTextField()

    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('blog.views.post', args=[self.slug])

