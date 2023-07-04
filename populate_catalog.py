import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locallibrary.settings')

import django
django.setup()

from catalog.models import Book, BookInstance, Genre, Author
from django.contrib.auth.models import User

def populate():

    genres = [
        {'name': 'Horror'},
        {'name': 'Thriller'},
        {'name': 'Science Fiction'},
        {'name': 'Historical'}
    ]

    authors = [
        {
            'first_name': 'Stephen',
            'last_name': 'King',
            'date_of_birth': '1947-09-21',
            'date_of_death': ''
        },
        {
            'first_name': 'Isaac',
            'last_name': 'Asimov',
            'date_of_birth': '1920-01-02',
            'date_of_death': '1992-05-06'
        }
    ]

    books = [
        {
            'title': 'The Shining',
            'summary': 'The Shining centers on the life of Jack Torrance, a struggling writer and recovering alcoholic who accepts a position as the off-season caretaker of the historic Overlook Hotel in the Colorado Rockies.',
            'author': {'first_name': authors[0]['first_name'], 'last_name': authors[0]['last_name']},
            'isbn': '9780345806789',
            'genre': [genres[0]['name'], genres[1]['name']],
        },
        {
            'title': 'Cementerio de Animales',
            'summary': 'El Dr. Louis Creed descubre un cementerio extraño en un bosque cercano a su nueva casa. Cuando el gato de la familia muere atropellado, Louis lo entierra en ese inquietante cementerio y, lo que ocurre después, le aterra tanto como le fascina.',
            'author': {'first_name':authors[0]['first_name'], 'last_name':authors[0]['last_name']},
            'isbn': '9780450057694',
            'genre': genres[0]['name'],
        },
        {
            'title': 'I Robot',
            'summary': 'I Robot is a fixup novel of science fiction short stories or essays by American writer Isaac Asimov. The stories originally appeared in the American magazines Super Science Stories and Astounding Science Fiction.',
            'author': {'first_name':authors[1]['first_name'], 'last_name':authors[1]['last_name']},
            'isbn': '9780194242363',
            'genre': [genres[2]['name']],
        },
        {
            'title': 'Viaje Alucinante',
            'summary': 'En plena Guerra Fría un científico soviético, especialista en la miniaturización de objetos, deserta a los Estados Unidos. En la fuga es ayudado por un agente de la CIA, que no puede evitar un intento de asesinato en su contra, quedando el tránsfuga en estado de coma.',
            'author': {'first_name':authors[1]['first_name'], 'last_name':authors[1]['last_name']},
            'isbn': '9780553275728',
            'genre': [genres[2]['name']],
        }
    ]

    book_instances = [
        {
        'book': books[0]['title'],
        'imprint': 'It was restored three years ago.',
        'due_back': '',
        'status': 'a'
        },
        {
        'book': books[0]['title'],
        'imprint': 'New purchase.',
        'due_back': '',
        'status': 'a'
        },
        {
        'book': books[1]['title'],
        'imprint': 'Nueva edición comprada hace dos años.',
        'due_back': '',
        'status': 'a'
        },
        {
        'book': books[2]['title'],
        'imprint': 'It comes from the main library.',
        'due_back': '',
        'status': 'a'
        },
        {
        'book': books[3]['title'],
        'imprint': 'It is a non-remunerated donation.',
        'due_back': '',
        'status': 'r'
        }
    ]


    for gen in genres:
        genr = Genre(name=gen['name'])
        genr.save()

    for aut in authors:
        if not aut['date_of_death']:
            dod = None
        else:
            dod = aut['date_of_death']
        auth = Author(first_name=aut['first_name'], last_name=aut['last_name'], date_of_birth=aut['date_of_birth'], date_of_death=dod)
        auth.save()

    for bo in books:
        t    = bo['title']
        s    = bo['summary']
        isb  = bo['isbn']
        g    = bo['genre']
        a_fn = bo['author']['first_name']
        a_ln = bo['author']['last_name']

        aut  = Author.objects.filter(first_name__contains=a_fn, last_name__contains=a_ln).first()
        new_book = Book(title=t, isbn=isb, summary=s, author=aut)
        new_book.save() # A first save is convenient to avoid Foreign Key problems with the N-M relation
        for ge in g:
            gen = Genre.objects.filter(name__contains=ge).first()
            new_book.genre.add(gen)
        new_book.save()

    for bi in book_instances:
        bok  = Book.objects.filter(title__contains=bi['book']).first()
        if not bi['due_back']:
            db = None
        else:
            db = bi['due_back']
        new_book_instance = BookInstance(book=bok, imprint=bi['imprint'], due_back=db, status=bi['status'])
        new_book_instance.save()

def super_user():
        user = User.objects.create_user(username='admin',
                                first_name='John',
                                is_staff=True,
                                is_superuser=True,
                                last_name='Wick',
                                email='john@mail.com',
                                password='admin2023')
        user.save()

def clean():
    Book.objects.all().delete()
    BookInstance.objects.all().delete()
    Genre.objects.all().delete()
    Author.objects.all().delete()
    User.objects.all().delete()


if __name__ == '__main__':
    print("Starting catalog population script...")
    clean()
    populate()
    super_user()
    print("Done!")