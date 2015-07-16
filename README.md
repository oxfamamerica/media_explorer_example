**Table of Contents**

- [Introduction](#introduction)
- [Installation](#installation)
- [Adding lead media to your blog/page etc. - Example 1](#adding-lead-media-example-1)
    - [The Model](#the-model)
    - [The Widget](#the-widget)
    - [The Form](#the-form)
    - [The Admin](#the-admin)
    - [The Widget Template, JS and CSS](#the-widget-template-js-and-css)
    - [The Frontend Template](#the-frontend-template)
- [Adding inline media via the WYSIWYG - Example 2](#adding-inline-media-via-the-wysiwyg-example-2)
    - [The Model](#the-model-1)
    - [The Widget](#the-widget-1)
    - [The Form](#the-form-1)
    - [The Admin](#the-admin-1)
    - [The Frontend Template](#the-frontend-template-1)
    
#Introduction

This application uses the Django Media Explorer to insert images, videos and slideshows into your content. 

Example 1 will show you how to setup your application so that you can insert a lead image, video or slideshow into your content (The term 'lead' means it's the first thing shown on the page).  After you add the lead media your content may look like this [screenshot](http://static.oxfamamerica.org.s3.amazonaws.com/github/dme_lead.jpg) which shows the lead slideshow in the red circle.

Example 2 will show you how to setup your application so that you can insert a lead image, video or slideshow into your content via the WYSIWYG.  After you add the media into your content the result may look like this [screenshot](http://static.oxfamamerica.org.s3.amazonaws.com/github/dme_lead_inline.jpg) which shows the lead video in the red circle and the inline image shown in a green circle.

#Installation
Install the Django Media Explorer by following instructions here: https://github.com/oxfamamerica/django-media-explorer

Download and install this Django project and add the Django Media Explorer settings to this project.

Add this to the bottom of your INSTALLED_APPS settings

```
    'blog',
    'media_explorer_example',
```

Add these to your urls.py

```
    url(r'^$', 'blog.views.index'),
    url(r'^(?P<slug>[\w\-]+)/$', 'blog.views.post'),   
```

#Adding lead media (EXAMPLE 1)

For this example we want to show a lead image, lead video or a lead media slideshow on our existing blog.

##The Model

We will assume that you have a model called **Blog** that looks like this:

```
from django.db import models
from django.core.urlresolvers import reverse

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __unicode__(self):
        return u'%s' % self.title
        
    def get_absolute_url(self):
        return reverse('blog.views.post', args=[self.slug])


```

The model above should look like this [screenshot](http://static.oxfamamerica.org.s3.amazonaws.com/github/dme_admin1.jpg).

After you follow the instructions below (add the extra model fields, add the widget, add the form, update the admin code, add the widget template, js and css) your model should now look like this [screenshot](http://static.oxfamamerica.org.s3.amazonaws.com/github/dme_admin2.jpg). Clicking the 'Select' button will open the Django Media Explorer so you can add a lead media and clicking the 'Remove' button will remove the lead media.

Add these fields to your model.

```
    LEAD_MEDIA_CHOICES = (('none','No lead'),('image','Image'),('video','Video'),('gallery','Gallery'))

    lead_media_type = models.CharField(null=True,blank=True,max_length=25,choices=LEAD_MEDIA_CHOICES,default="none")
    lead_media_id = models.IntegerField(blank=True,null=True)
    lead_media_caption = models.CharField(blank=True,null=True,max_length=255)
    lead_media_credit = models.CharField(blank=True,null=True,max_length=255)

```

Now your final model should look like:

```
from django.db import models
from django.core.urlresolvers import reverse

class Blog(models.Model):
    LEAD_MEDIA_CHOICES = (('none','No lead'),('image','Image'),('video','Video'),('gallery','Gallery'))

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
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


```

##The Widget

Add this to your app's widget classes. For instance if your app is called "blog" then copy the code below to the path **blog/widgets.py**

NOTE: Remove **http://code.jquery.com/jquery-1.11.2.min.js** if you are already using jQuery in your admin page.

```
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

class MELeadMediaWidget(forms.Widget):
    template_name = 'admin/lead_media_field.html'

    class Media:
        js = (
            'http://code.jquery.com/jquery-1.11.2.min.js',
            'js/media_explorer/media_explorer.js',
            'js/lead_media_field_admin.js',
        )
        css = {
            'all': (
                'css/hide_media_fields.css',
            )
        }

    def render(self, name, value, attrs=None):
        context = { }
        return mark_safe(render_to_string(self.template_name, context))

```

##The Form

Add this to your app's form class. For instance if your app is called "blog" then copy the code below to the path **blog/forms.py**

```
from django import forms
from blog.models import Blog
from blog.widgets import MELeadMediaWidget

class BlogAdminForm(forms.ModelForm):
    lead_media_widget = forms.CharField(required=False,label="Lead Media",widget=MELeadMediaWidget())

    class Meta:
        model = Blog
        widgets = {
            'lead_media_type': forms.HiddenInput(),
            'lead_media_id': forms.HiddenInput(),
            'lead_media_caption': forms.HiddenInput(),
            'lead_media_credit': forms.HiddenInput(),
        }


```

##The Admin

Add this to your app's admin class. For instance if your app is called "blog" then copy the code below to the path **blog/admin.py**

```

from django.contrib import admin
from blog.models import Blog
from blog.forms import BlogAdminForm

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm


admin.site.register(Blog , BlogAdmin)

```


##The Widget Template, JS and CSS

The [Widget code](#the-widget) above references certain template, CSS and JS files. You will need to create all of them except **js/media_explorer/media_explorer.js** which comes with the Media Explorer.

Copy this template code into **blog/templates/admin/lead_media_field.html** 

```

<div>
    <table>
        <tr>
            <td>
                <div>
                    <div id="mediaInfoDiv" style="display:none"></div>
                    <div id='currentImageDiv' style='margin-bottom:5px'></div>
                    <input class='addImage' type='button' value='Select' onclick="meSelectOrRemoveMedia('select');">
                    <input class='removeImage' type='button' value='Remove' onclick="meSelectOrRemoveMedia('remove');";>
                </div>
                <div id="leadMediaImageDiv" style="display:none">
                    <input title="Enter caption" type="text" id="temp_caption" value="" placeholder="Enter caption" style="margin-top:10px;width:200px">
<br>
                    <input title="Enter credit" type="text" id="temp_credit" value="" placeholder="Enter credit" style="margin-top:10px;width:200px">
                </div>
            </td>
        </tr>
    </table>
</div>

```

Copy this JS code into **blog/static/js/lead_media_field_admin.js** 

```

function meSelectOrRemoveMedia(action)
{

    MediaExplorer.div_id='currentImageDiv';
    MediaExplorer.type_input_id='id_lead_media_type';
    MediaExplorer.file_input_id='id_lead_media_id';
    MediaExplorer.caption_input_ids = ["id_lead_media_caption","temp_caption"];
    MediaExplorer.credit_input_ids = ["id_lead_media_credit","temp_credit"];
    MediaExplorer.callback = 'meProcessLeadMedia';
    if ( action == "select" )
    {
        MediaExplorer.openWindow();
    }
    else if ( action == "remove" )
    {
        MediaExplorer.remove();
    }
}

function meProcessLeadMedia()
{

    $("#mediaInfoDiv").html("");
    $("#mediaInfoDiv").hide();
    $("#leadMediaImageDiv").hide();

    var id = $('input[name="lead_media_id"]').val();
    var type = $('input[name="lead_media_type"]').val();

    if ( id && type )
    {
        var url = "/api/media/elements/" + id;

        if ( type == "gallery" )
        {
            url = "/api/media/galleries/" + id;
        }
        else if ( type == "image" )
        {
            $("#leadMediaImageDiv").show();
        }

        $.ajax({
            url: url
        }).done(function(data) {
            var html = "";
            html = "<div>";
            html += "<b>Media name:</b> ";
            if ( type == "image" )
            {
                html += "<a target='_blank' href='" + data.image_url + "'>"
                html += data.name;
                html += "</a>";
            }
            else if ( type == "video" )
            {
                html += "<a target='_blank' href='" + data.video_url + "'>"
                html += data.name;
                html += "</a>";
            }
            else if ( type == "gallery" )
            {
                html += data.name;
            }
            html += "</div>";
            html += "<div>";
            html += "<b>Media type:</b> " + type;
            html += "</div>";
            $("#mediaInfoDiv").html(html);
            $("#mediaInfoDiv").show();

            var html2 = "<img style='max-width:150px' src='";
            html2 += data.thumbnail_image_url;
            html2 += "' >";
            $("#currentImageDiv").html(html2);

        });
    }
}

$(function() {

  if ( $('input[name="lead_media_id"]').length )
  {

    $( '#temp_caption' ).keyup( function() {
      $("#id_lead_media_caption").val($(this).val());
    }); 

    $( '#temp_credit' ).keyup( function() {
      $("#id_lead_media_credit").val($(this).val());
    }); 

    meProcessLeadMedia();

    $("#temp_caption").val($("#id_lead_media_caption").val());
    $("#temp_credit").val($("#id_lead_media_credit").val());

  }

});


```
As you can see in the **BlogAdminForm** code above, we are hiding these input fields, **lead_media_type**, **lead_media_id**, **lead_media_caption** and **lead_media_credit**.

Even though the fields are hidden the labels will still be visible in the admin. Copy the CSS code below into **blog/static/css/hide_media_fields.css** and you will be able to hide the entire field rows in the admin.


```

.field-lead_media_type{ display:none; }
.field-lead_media_id{ display:none; }
.field-lead_media_credit{ display:none; }
.field-lead_media_caption{ display:none; }

```

##The Frontend Template

After you have integrated the Media Explorer to your backend - you will now need to show the images, videos and gallery to your users.

In our example we added a lead media to the "blog" app. The template that shows the blog post will originally look like this:

```
{% extends 'base.html' %}

{% block title %}{{post.title}}{% endblock %}

{% block content %}
    <article>
        <header>
            <h1> {{post.title}} </h1>
            <p>
                Posted on
                <time datetime="{{post.created|date:"c"}}">
                {{post.created|date}}
                </time>
            </p>
        </header>
        <p class="description">
            {{post.description}}
        </p>
        {{post.content|safe}}
    </article>
{% endblock %}

```

Add the template code below to the template above to show the lead media.


```
{% load media_explorer_tags %}

{% if post.lead_media_type == "video" %}
    {% get_video post.lead_media_id %}
{% elif post.lead_media_type == "gallery" %}
    {% get_media_gallery post.lead_media_id %}
{% elif post.lead_media_type == "image" %}
    <figure>
        <img src="{% get_image_url_from_size post.lead_media_id post.lead_media_type "1220x763" "orig_c"|safe %}">
        {% if post.lead_media_caption or post.lead_media_credit %}
            <figcaption>
            {% if post.lead_media_caption %}
                {{post.lead_media_caption}}
            {% endif %}
            {% if post.lead_media_credit %}
                {{post.lead_media_credit}}
            {% endif %}
            </figcaption>
        {% endif %}
    </figure>
{% endif %}
```

The final template may look like this:

```
{% extends 'base.html' %}
{% load media_explorer_tags %}

{% block title %}{{post.title}}{% endblock %}

{% block content %}
    <article>
        <header>
            <h1> {{post.title}} </h1>
            <p>
                Posted on
                <time datetime="{{post.created|date:"c"}}">
                {{post.created|date}}
                </time>
            </p>
        </header>

        {% if post.lead_media_type == "video" %}
            {% get_video post.lead_media_id %}
        {% elif post.lead_media_type == "gallery" %}
            {% get_media_gallery post.lead_media_id %}
        {% elif post.lead_media_type == "image" %}
            <figure>
                <img src="{% get_image_url_from_size post.lead_media_id post.lead_media_type "1220x763" "orig_c"|safe %}">
                {% if post.lead_media_caption or post.lead_media_credit %}
                    <figcaption>
                    {% if post.lead_media_caption %}
                        {{post.lead_media_caption}}
                    {% endif %}
                    {% if post.lead_media_credit %}
                        {{post.lead_media_credit}}
                    {% endif %}
                    </figcaption>
                {% endif %}
            </figure>
        {% endif %}

        <p class="description">
            {{post.description}}
        </p>
        {{post.content|safe}}
    </article>
{% endblock %}

```


#Adding inline media via the WYSIWYG (Example 2)

For this example we want to select an image, video or slideshow and insert it directly into your content through the use of a WYSIWYG. The Django Media Explorer comes with [CKEditor](http://ckeditor.com/) already installed so you can use that as the WYSIWYG editor.

##The Model

We will assume that you have a model called **Blog** that looks like this:

```
from django.db import models
from django.core.urlresolvers import reverse

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __unicode__(self):
        return u'%s' % self.title
        
    def get_absolute_url(self):
        return reverse('blog.views.post', args=[self.slug])


```
The model above should look like this [screenshot](http://static.oxfamamerica.org.s3.amazonaws.com/github/dme_admin1.jpg).

After you follow the instructions below (add the widget, add the form and update the admin code) your model should now look like this [screenshot](http://static.oxfamamerica.org.s3.amazonaws.com/github/dme_admin3.jpg). Clicking the button in the round blue circle will open the Django Media Explorer so you can select media and post it inline into your WYSIWYG.

##The Widget

Add this to your app's widget classes. For instance if your app is called "blog" then copy the code below to the path **blog/widgets.py**

NOTE: Remove **http://code.jquery.com/jquery-1.11.2.min.js** if you are already using jQuery in your admin page.

```
from ckeditor.widgets import CKEditorWidget

class MECKEditorWidget(CKEditorWidget):

    class Media:
        js = (
            'http://code.jquery.com/jquery-1.11.2.min.js',
            'js/vendor/jQuery-Impromptu-6.1.0/jquery-impromptu.min.js',
            'js/media_explorer/media_explorer.js',
            'ckeditor/ckeditor/plugins/media_explorer/callback.js',
        )
        css = {
            'all': (
                'js/vendor/jQuery-Impromptu-6.1.0/jquery-impromptu.min.css',
            )
        }

```

##The Form

Add this to your app's form class. For instance if your app is called "blog" then copy the code below to the path **blog/forms.py**

```
from django import forms
from blog.models import Blog
from blog.widgets import MECKEditorWidget

class BlogAdminForm(forms.ModelForm):

    class Meta:
        model = Blog
        widgets = {
            'content': MECKEditorWidget,
        }


```

##The Admin

Add this to your app's admin class. For instance if your app is called "blog" then copy the code below to the path **blog/admin.py**

```

from django.contrib import admin
from blog.models import Blog
from blog.forms import BlogAdminForm

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm


admin.site.register(Blog , BlogAdmin)

```

##The Frontend Template

After you have integrated the Media Explorer to your backend - you will now need to show the images, videos and gallery to your users.

In our example we added a lead media to the "blog" app. The template that shows the blog post will originally look like this:

```
{% extends 'base.html' %}

{% block title %}{{post.title}}{% endblock %}

{% block content %}
    <article>
        <header>
            <h1> {{post.title}} </h1>
            <p>
                Posted on
                <time datetime="{{post.created|date:"c"}}">
                {{post.created|date}}
                </time>
            </p>
        </header>
        <p class="description">
            {{post.description}}
        </p>
        {{post.content|safe}}
    </article>
{% endblock %}

```

Replace this template code: 

```
        {{post.content|safe}}
```

With this one:

```
        {{ post.content|show_short_code|safe }}

```

After the replacement the final template code will look like this:

```

{% extends 'base.html' %}

{% block title %}{{post.title}}{% endblock %}

{% block content %}
    <article>
        <header>
            <h1> {{post.title}} </h1>
            <p>
                Posted on
                <time datetime="{{post.created|date:"c"}}">
                {{post.created|date}}
                </time>
            </p>
        </header>
        <p class="description">
            {{post.description}}
        </p>
        {{ post.content|show_short_code|safe }}
    </article>
{% endblock %}


```

