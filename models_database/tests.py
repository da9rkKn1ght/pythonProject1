from django.urls import reverse
from models_database.models import Category
from django.test import TestCase
from models_database import factories, models
from PIL import Image
import tempfile



class ModelsTestCase(TestCase):

    def setUp(self):
        self.product = factories.ProductFactory()

        self.image_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        image = Image.new('RGB', (1, 1), color=(255, 255, 255))
        image.save(self.image_file, 'PNG')
        self.image_file.seek(0)

        self.image_path = self.image_file.name

        self.category = models.Category.objects.create(category_name='Test_Category')



    def test_get_product_list(self):
        url = reverse('products_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), models.Product.objects.count())


    def test_get_product_detail(self):
        url = reverse('product_detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        product = response.context.get('product')

        self.assertIsNotNone(product, "Product should be present in the response context")
        self.assertEqual(product.pk, self.product.pk)
        self.assertEqual(product.product_name, self.product.product_name)
        self.assertEqual(product.price, self.product.price)
        self.assertEqual(product.description, self.product.description)
        self.assertEqual(product.quantity, self.product.quantity)

    def test_update_product(self):
        url = reverse('product_update', kwargs={'pk': self.product.pk})
        old_description = self.product.description
        old_product_name = self.product.product_name
        old_price = self.product.price
        response = self.client.post(url, {
            'product_name': 'new_product_name',
            'price': old_price,
            'description': 'new_description'
        })


        self.product.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(self.product.description, old_description)
        self.assertNotEqual(self.product.product_name, old_product_name)


    def test_delete_product(self):
        url = reverse('product_delete', kwargs={'pk': self.product.pk})
        old_product_count = models.Product.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 302)
        self.assertGreater(old_product_count, models.Product.objects.count())


    def test_create_product(self):

        url = reverse('product_create')
        old_product_count = models.Product.objects.count()

        with open(self.image_path, 'rb') as img:
            data = {
                'product_name': 'New_Product',
                'description': 'New Description',
                'price': 500,
                'quantity': 20,
                'category': self.category.id,  # Используем id категории
                'image': img  # Передаем файл изображения
            }

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 302)
            self.assertNotEqual(models.Product.objects.count(), old_product_count)

            try:
                new_product = models.Product.objects.get(product_name='New_Product')
            except models.Product.DoesNotExist:
                self.fail('Product was not created in the database')

            self.assertEqual(new_product.description, 'New Description')
            self.assertEqual(new_product.price, 500)
            self.assertEqual(new_product.quantity, 20)
            self.assertEqual(new_product.category.id, self.category.id)


    def tearDown(self):
        # Удаляем временный файл
        self.image_file.close()
