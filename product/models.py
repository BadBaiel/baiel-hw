from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100)

    @property
    def products_count(self):
        return self.product_set.count()

    def products_list(self):
        return [product.title for product in self.product_set.all()]

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    price = models.FloatField()
    rating = models.FloatField()
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag, blank=True)

    @property
    def category_name(self):
        try:
            return self.category_id.name
        except:
            return "Нет категорий"

    @property
    def mid_review(self):
        try:
            stars_list = [review.stars for review in self.review.all()]
            return round(sum(stars_list) / len(stars_list), 2)
        except ZeroDivisionError:
            return 0



    def __str__(self):
        return self.title

class Review(models.Model):
    CHOICES = ((i, "*" * i) for i in range(1, 6))
    text = models.TextField()
    stars = models.IntegerField(choices=CHOICES, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='review')




    def __str__(self):
        return self.text

    @property
    def product_title(self):
        return self.product.title
