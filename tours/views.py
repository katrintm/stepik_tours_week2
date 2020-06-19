import random

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from tours import data


class MainView(View):
    def get(self, request, *args, **kwargs):
        tour_ids = random.sample(range(1, 16), 6)
        tours = {tour_id: data.tours[tour_id] for tour_id in tour_ids}
        return render(
            request, 'tours/index.html', context={
                'title': data.title,
                'subtitle': data.subtitle,
                'description': data.description,
                'tours': tours,
                'departures': data.departures
            }
        )


class DepartureView(View):
    def get(self, request, departure, *args, **kwargs):
        if departure not in data.departures:
            return HttpResponseNotFound('Из этого города мы пока не летаем!')
        else:
            tour_ids = [i for i in range(1, len(data.tours) + 1)]
            tours = {tour_id: data.tours[tour_id] for tour_id in tour_ids
                     if data.tours[tour_id]['departure'] == departure}

            count_tours = len(tours)

            min_nights = tours[list(tours.keys())[0]]['nights']
            max_nights = tours[list(tours.keys())[0]]['nights']
            min_price = tours[list(tours.keys())[0]]['price']
            max_price = tours[list(tours.keys())[0]]['price']

            for tour in tours:
                min_nights = min(min_nights, tours[tour]['nights'])
                max_nights = max(max_nights, tours[tour]['nights'])
                min_price = min(min_price, tours[tour]['price'])
                max_price = max(max_price, tours[tour]['price'])

            return render(
                request, 'tours/departure.html', context={
                    'title': data.title,
                    'departures': data.departures,
                    'departure': data.departures[departure],
                    'tours': tours,
                    'count_tours': count_tours,
                    'min_nights': min_nights,
                    'max_nights': max_nights,
                    'min_price': min_price,
                    'max_price': max_price
                }
            )


class TourView(View):
    def get(self, request, id, *args, **kwargs):
        if id not in data.tours:
            return HttpResponseNotFound('В этот город мы пока не летаем!')
        else:
            return render(
                request, 'tours/tour.html', context={
                    'tour_title': data.tours[id]['title'],
                    'tour_stars': data.tours[id]['stars'],
                    'tour_country': data.tours[id]['country'],
                    'tour_departure': data.departures[data.tours[id]['departure']],
                    'tour_nights': data.tours[id]['nights'],
                    'tour_picture': data.tours[id]['picture'],
                    'tour_description': data.tours[id]['description'],
                    'tour_price': data.tours[id]['price'],
                    'title': data.title,
                    'departures': data.departures,
                }
            )


def custom_handler404(request, exception):
    return HttpResponseNotFound('Пока такой страницы не существует!')
