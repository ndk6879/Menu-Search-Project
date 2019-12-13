from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 15)
    ingredient = models.CharField(max_length = 100, null=True, blank=True)
    link = models.CharField(max_length = 200, null=True, blank=True )

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    def forwards(self, orm):
        # Rename 'name' field to 'full_name'
        db.rename_column('Menu', 'ingredient', 'ingredient1')
