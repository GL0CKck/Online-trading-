from django.db import models

class Bb(models.Model):
    title = models.CharField(max_length=50,verbose_name='Товар')
    content = models.TextField(null=True,blank=True,verbose_name='Описание')
    price = models.FloatField(null=True,blank=True,verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True,db_index=True,verbose_name='Опубликованно')
    rubric = models.ForeignKey('Rubric', null=True,on_delete=models.PROTECT,verbose_name='Рубрика')
    class Meta():
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-published']

    def __str__(self):
        return 'Продажа: ' + self.title


class Rubric(models.Model):
    name=models.CharField(max_length=50,verbose_name='Название')
    order=models.SmallIntegerField(default=0,db_index=True)

    class Meta():
        verbose_name='Рубрика'
        verbose_name_plural='Рубрики'
        ordering=['order','name']

    def __str__(self):
        return 'Рубрика: ' + self.name