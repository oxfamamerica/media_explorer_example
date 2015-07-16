from django.db import models
from django.core.urlresolvers import reverse
#from ckeditor.fields import RichTextField


class Blog(models.Model):
    LEAD_MEDIA_CHOICES = (('none','No lead'),('image','Image'),('video','Video'),('gallery','Gallery'))

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    #content = RichTextField()
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    lead_media_type = models.CharField(null=True,blank=True,max_length=25,choices=LEAD_MEDIA_CHOICES,default="none")
    lead_media_id = models.IntegerField(blank=True,null=True)
    lead_media_caption = models.CharField(blank=True,null=True,max_length=255)
    lead_media_credit = models.CharField(blank=True,null=True,max_length=255)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('blog.views.post', args=[self.slug])


