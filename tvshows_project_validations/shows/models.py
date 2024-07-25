
from django.db import models
from datetime import datetime

class showmanager(models.Manager):
    def validate_show_data(self,postData, exclude_id= None):
        errors = {}
        title= postData.get('title')
        network = postData.get('network')
        release_date = postData.get('release_date')
        description = postData.get('description')

        #validate_title
        if not title or len(title) < 2 :
            errors['title'] = "Title should be at least 2 characters long"
        elif self.filter(title=title).exclude(id=exclude_id).exists():
            errors['title'] = "Title already exists."

         # Validate network
        if not network or len(network) < 3:
            errors['network'] = "Network should be at least 3 characters long."

          # Validate release date
        if not release_date:
            errors['release_date'] = "Release date is required."
        else:
            try:
                release_date_obj = datetime.strptime(release_date, '%Y-%m-%d')
                if release_date_obj >= datetime.now():
                    errors['release_date'] = "Release date should be in the past."
            except ValueError:
                errors['release_date'] = "Invalid date format."

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)