from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(verbose_name='Имя пользователя', max_length=255)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name='Пользователь',
        verbose_name_plural='Пользователи',
        ordering=['username']

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    address = models.CharField(verbose_name='Адрес', max_length=255)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        'User',
        verbose_name='Имя пользователя',
        related_name='userprofile',
        on_delete=models.CASCADE,
        primary_key=True
    )

    class Meta:
        verbose_name='Профиль пользователя',
        verbose_name_plural='Профили пользователей',
        ordering=['address']

    def __str__(self):
        return f'{self.address}, {self.phone_number}'


class Category(models.Model):
    category_name = models.CharField(verbose_name='Категории товаров', max_length=255)
    description = models.CharField(verbose_name='Описание', max_length=255, default='Описание категории продуктов')

    class Meta:
        verbose_name='Категория',
        verbose_name_plural='Категории',
        ordering=['category_name']

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(verbose_name='Название продукта', max_length=100)
    description = models.CharField(verbose_name='Описание продукта', max_length=255, default='Описание продукта')
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(
        'Category',
        verbose_name='Категории товаров',
        related_name='product',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name='Название продукта',
        verbose_name_plural='Названия продуктов',
        ordering=['product_name']

    def __str__(self):
        return f'{self.product_name}, цена: {self.price}'

    def check_quantity(self):
        return self.quantity > 0


class Order(models.Model):
    total_price = models.PositiveIntegerField(verbose_name='Общая стоимость заказа', null=True, blank=True)
    status = models.CharField(verbose_name='Статус заказа', max_length=50, choices=[('Pending', 'В ожидании'),
                                                                                    ('Shipped', 'Отправлен'),
                                                                                    ('Delivered', 'Доставлен')])
    created_at = models.DateField(verbose_name='Время создания заказа', auto_now_add=True)
    updated_at = models.DateField(verbose_name='Время последнего изменения статуса', auto_now=True)
    user = models.ForeignKey(
        'User',
        verbose_name='Пользователь',
        related_name='order',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name='Общая стоимость',
        verbose_name_plural='Общие стоимости',
        ordering=['-total_price']

    def __str__(self):
        return f'Статус заказа: {self.status}, общая стоимость: {self.total_price}'

    def get_discount(self):
        self.total_price -= self.total_price * 0.15
        return f'Общая стоимость с учетом скидки: {self.total_price}'


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    order = models.ForeignKey(
        'Order',
        verbose_name='Заказ',
        related_name='orderitem',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        'Product',
        verbose_name='Название продукта',
        related_name='orderitem',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name='Количество',
        verbose_name_plural='Количество',
        ordering=['quantity', 'price']

    def __str__(self):
        return f'{self.quantity}'

    def get_total_price(self):
        return f'Товар: {self.product}\nКоличество: {self.quantity}\nОбщая цена: {self.quantity * self.price}'
