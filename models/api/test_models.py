from django.test import TestCase, Client
from api.models import User, Author, Book, Review, Listing

class AuthorTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_author(self):
        response = self.client.post(
            '/api/v1/author/create', 
            { 
                'first_name': 'J.K.', 
                'last_name': 'Rowling', 
                'age': 52
            }
        )
        author = Author.objects.get(pk = int(response.json()['result']['pk']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(author.first_name, 'J.K.')
        self.assertEqual(author.last_name, 'Rowling')
        self.assertEqual(author.age, 52)

    def test_read_author(self):
        author = Author.objects.create(first_name = 'Stephen', last_name = 'King', age = 50)
        response = self.client.get('/api/v1/author/' + str(author.pk))
        json = response.json()['result']['fields']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['first_name'], 'Stephen')
        self.assertEqual(json['last_name'], 'King')
        self.assertEqual(json['age'], 50)

    def test_update_author(self):
        author = Author.objects.create(first_name = 'Mark', last_name = 'Twain', age = 50)
        response = self.client.post(
            '/api/v1/author/' + str(author.pk), 
            {
                'first_name': 'Jennifer', 
                'last_name': 'Fang', 
                'age': 19
            }
        )
        author = Author.objects.get(pk = author.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(author.first_name, 'Jennifer')
        self.assertEqual(author.last_name, 'Fang')
        self.assertEqual(author.age, 19)

    def test_delete_author(self):
        author = Author.objects.create(first_name = 'Ernest', last_name = 'Hemmingway', age = 50)
        response = self.client.get('/api/v1/author/delete/' + str(author.pk))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(pk=author.pk)

    def test_fails_invalid(self):
        response = self.client.get('/api/v1/author')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        pass
 




class BookTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_book(self):
        author = Author.objects.create(first_name = 'Ernest', last_name = 'Hemmingway', age = 50)
        response = self.client.post(
            '/api/v1/book/create', 
            {
                'title': 'Harry Potter', 
                'year_published': 1997, 
                'rating': 5.0,
                'author': author.pk,
            }
        )        
        book = Book.objects.get(pk = int(response.json()['result']['pk']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book.title, 'Harry Potter')
        self.assertEqual(book.year_published, 1997)
        self.assertEqual(book.rating, 5.0)
        self.assertEqual(book.author, author)

    def test_read_book(self):
        author = Author.objects.create(first_name = 'Ernest', last_name = 'Hemmingway', age = 50)
        book = Book.objects.create(title = 'Old Man and the Sea', year_published = 1952, rating = 5.0, author = author)
        response = self.client.get('/api/v1/book/' + str(book.pk))
        json = response.json()['result']['fields']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['title'], 'Old Man and the Sea')
        self.assertEqual(json['year_published'], 1952)
        self.assertEqual(json['rating'], 5.0)
        self.assertEqual(json['author'], author.pk)

    def test_update_book(self):
        author = Author.objects.create(first_name = 'Ernest', last_name = 'Hemmingway', age = 50)
        author2 = Author.objects.create(first_name = 'J.K.', last_name = 'Rowling', age = 55)
        book = Book.objects.create(title = 'Harry Potter', year_published = 2000, rating = 5.0, author = author)
        response = self.client.post(
            '/api/v1/book/' + str(book.pk), 
            {
                'title': 'Harry Potter 2', 
                'year_published': 2002, 
                'rating': 3.0,
                'author': author2.pk,
            }
        )
        book = Book.objects.get(pk = book.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book.title, 'Harry Potter 2')
        self.assertEqual(book.year_published, 2002)
        self.assertEqual(book.rating, 3.0)
        self.assertEqual(book.author, author2)

    def test_delete_book(self):
        author2 = Author.objects.create(first_name = 'J.K.', last_name = 'Rowling', age = 55)
        book = Book.objects.create(title = 'Harry Potter 3', year_published = 2005, rating = 4.0, author = author2)
        response = self.client.get('/api/v1/book/delete/' + str(book.pk))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=book.pk)

    def test_fails_invalid(self):
        response = self.client.get('/api/v1/book')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        pass






class ReviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username = 'jennifer', 
            password = 'fang', 
            first_name = 'Jennifer', 
            last_name = 'Fang')
        self.author = Author.objects.create(
            first_name = 'Ernest', 
            last_name = 'Hemmingway', 
            age = 50)
        self.book = Book.objects.create(
            title = 'Old Man and the Sea', 
            year_published = 1952, 
            rating = 5.0, 
            author = self.author)

    def test_create_review(self):
        response = self.client.post(
            '/api/v1/review/create', 
            {
                'reviewer': self.user.pk, 
                'book': self.book.pk,
                'rating': 5.0, 
                'content': 'I liked this book',
            }
        )        
        review = Review.objects.get(pk = int(response.json()['result']['pk']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.reviewer, self.user)
        self.assertEqual(review.book, self.book)
        self.assertEqual(review.rating, 5.0)
        self.assertEqual(review.content, 'I liked this book')

    def test_read_review(self):
        review = Review.objects.create(
            reviewer = self.user, 
            book = self.book, 
            rating = 4.0, 
            content = 'This book was great!')
        response = self.client.get('/api/v1/review/' + str(review.pk))
        json = response.json()['result']['fields']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['reviewer'], self.user.pk)
        self.assertEqual(json['book'], self.book.pk)
        self.assertEqual(json['rating'], 4.0)
        self.assertEqual(json['content'], 'This book was great!')

    def test_update_review(self):
        user2 = User.objects.create(username = 'b', password = 'l', first_name = 'brandon', last_name = 'liu')
        book2 = Book.objects.create(title = 'Harry Potter', year_published = 2000, rating = 5.0, author = self.author)
        review = Review.objects.create(reviewer =self.user, book = self.book, rating = 3.0, content = 'This book was okay.')
        response = self.client.post(
            '/api/v1/review/' + str(review.pk), 
            {
                'reviewer': user2.pk, 
                'book': book2.pk,
                'rating': 5.0, 
                'content': 'I loved this book!',
            }
        )
        review = Review.objects.get(pk = review.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.reviewer, user2)
        self.assertEqual(review.book, book2)
        self.assertEqual(review.rating, 5.0)
        self.assertEqual(review.content, 'I loved this book!')

    def test_delete_review(self):
        review = Review.objects.create(reviewer = self.user, book = self.book, rating = 3.5, content = 'This book was okay.')
        response = self.client.get('/api/v1/review/delete/' + str(review.pk))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(pk=review.pk)

    def test_fails_invalid(self):
        response = self.client.get('/api/v1/review')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        pass








# class ListingTestCase(TestCase):
#     def setUp(self):
#         pass

#     def test_create_listing(self):
#         author = Author.objects.create(first_name = 'Ernest', last_name = 'Hemmingway', age = 50)
#         book = Book.objects.create(title = 'Old Man and the Sea', year_published = 1952, rating = 5.0, author = author)
#         response = self.client.post(
#             '/api/v1/listing/create', 
#             {
#                 'lister': 'Jennifer Fang', 
#                 'book': book.pk,
#                 'price': 12.50, 
#             }
#         )        
#         listing = Listing.objects.get(pk = int(response.json()['result']['pk']))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(listing.lister, 'Jennifer Fang')
#         self.assertEqual(listing.book, book)
#         self.assertEqual(listing.price, 12.50)

#     def test_read_listing(self):
#         author = Author.objects.create(first_name = 'Ernest', last_name = 'Hemmingway', age = 50)
#         book = Book.objects.create(title = 'Old Man and the Sea', year_published = 1952, rating = 5.0, author = author)
#         listing = Listing.objects.create(lister = 'Jennifer Fang', book = book, 
#             price =  140.00)
#         response = self.client.get('/api/v1/listing/' + str(listing.pk))
#         json = response.json()['result']['fields']
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(json['lister'], 'Jennifer Fang')
#         self.assertEqual(json['book'], book.pk)
#         self.assertEqual(json['price'], 140.00)

#     def test_update_listing(self):
#         author = Author.objects.create(first_name = 'Ernest', last_name = 'Hemmingway', age = 50)
#         author2 = Author.objects.create(first_name = 'J.K.', last_name = 'Rowling', age = 55)
#         book = Book.objects.create(title = 'Old Man and the Sea', year_published = 1952, rating = 5.0, author = author)
#         book2 = Book.objects.create(title = 'Harry Potter', year_published = 2000, rating = 5.0, author = author2)
#         listing = Listing.objects.create(lister = 'Brandon Liu', book = book2, 
#             price = 3.00)
#         response = self.client.post(
#             '/api/v1/listing/' + str(listing.pk), 
#             {
#                 'lister': 'Jennifer Fang', 
#                 'book': book.pk,
#                 'price': 15.00, 
#             }
#         )
#         listing = Listing.objects.get(pk = listing.pk)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(listing.lister, 'Jennifer Fang')
#         self.assertEqual(listing.book, book)
#         self.assertEqual(listing.price, 15.00)

#     def test_delete_listing(self):
#         author2 = Author.objects.create(first_name = 'J.K.', last_name = 'Rowling', age = 55)
#         book2 = Book.objects.create(title = 'Harry Potter', year_published = 2000, rating = 5.0, author = author2)
#         listing = Listing.objects.create(lister = 'Eric Xie', book = book2, 
#             rating = 3.5, content = 'This book was okay.')
#         response = self.client.get('/api/v1/listing/delete/' + str(listing.pk))
#         self.assertEqual(response.status_code, 200)
#         with self.assertRaises(Listing.DoesNotExist):
#             Listing.objects.get(pk=listing.pk)

#     def test_fails_invalid(self):
#         response = self.client.get('/api/v1/listing')
#         self.assertEqual(response.status_code, 404)

#     def tearDown(self):
#         pass


