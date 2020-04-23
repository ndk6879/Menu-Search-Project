from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 15)
    Essential_Ingredient = models.CharField(max_length = 100, blank=True, default ='')
    Nonessential_Ingredient = models.CharField(max_length = 100, blank=True,default ='')
    link = models.CharField(max_length = 200, blank=True, default ='')
    tip = models.TextField(blank=True, default ='')

    class Meta:
        verbose_name_plural = 'Menu' #admin에서 Menus를 Menu로 바꿔줌
    # 
    # def publish(self):
    #     self.published_at = timezone.now()
    #     self.save()

    def __str__(self): #admin에서 저장하면 object으로 출력안되고 입력햇던 값으로 나옴.
        return self.name
