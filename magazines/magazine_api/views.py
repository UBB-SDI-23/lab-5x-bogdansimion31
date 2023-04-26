import datetime

from django.db.models import Avg, Case, ExpressionWrapper, F, fields, When
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Magazine, Author, Publisher, Buyer, BuyerSubscription, PublisherStatsDTO, Purchase, AuthorStatsDTO
from .serializer import MagazineSerializer, AuthorSerializer, PublisherSerializer, BuyerSerializer, \
    BuyerSubscriptionSerializer, PublisherStatsDTOSerializer, AuthorStatsDTOSerializer


# Create your views here.
# responsible for logic to create or return data
# magazines/list


@api_view(['GET'])
def magazines_list(request):
    magazines = Magazine.objects.all()  # complex data
    serializer = MagazineSerializer(magazines, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def magazine_create(request):
    serializer = MagazineSerializer(data=request.data)
    if serializer.is_valid():
        magazine = serializer.save()

        buyer_ids = request.data.get('buyers', [])
        purchases = []
        for buyer_id in buyer_ids:
            buyer = get_object_or_404(Buyer, id=buyer_id)
            purchase = Purchase(magazine=magazine, buyer=buyer, price=magazine.price)
            purchases.append(purchase)

        Purchase.objects.bulk_create(purchases)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def magazine_detail(request, pk):
    try:
        magazine = Magazine.objects.get(pk=pk)
    except:
        return Response({'error': 'Magazine does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MagazineSerializer(magazine)
        data = serializer.data

        # Get the author and publisher objects and add them to the response
        if magazine.author:
            author_serializer = AuthorSerializer(magazine.author)
            data['author'] = author_serializer.data
        if magazine.publisher:
            publisher_serializer = PublisherSerializer(magazine.publisher)
            data['publisher'] = publisher_serializer.data

        buyers = magazine.buyers.all()
        buyer_serializer = BuyerSerializer(buyers, many=True)
        data['buyers'] = buyer_serializer.data

        return Response(data)

    if request.method == 'PUT':
        serializer = MagazineSerializer(magazine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        magazine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def magazines_with_pages_above(request, min_pages):
    magazines = Magazine.objects.filter(
        number_of_pages__gte=min_pages)  # filter by number_of_pages greater than or equal to min_pages
    serializer = MagazineSerializer(magazines, many=True)
    return Response(serializer.data)


# Author views
@api_view(['GET'])
def authors_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def author_create(request):
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except:
        return Response({'error': 'Author does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        data = serializer.data

        magazines = Magazine.objects.filter(author=author)
        magazines_serializer = MagazineSerializer(magazines, many=True)
        data['magazines'] = magazines_serializer.data

        return Response(data)

    if request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Publisher views
@api_view(['GET'])
def publishers_list(request):
    publishers = Publisher.objects.all()
    serializer = PublisherSerializer(publishers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def publisher_create(request):
    serializer = PublisherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def publisher_detail(request, pk):
    try:
        publisher = Publisher.objects.get(pk=pk)
    except:
        return Response({'error': 'Publisher does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PublisherSerializer(publisher)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PublisherSerializer(publisher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        publisher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def buyers_list(request):
    buyers = Buyer.objects.all()
    serializer = BuyerSerializer(buyers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def buyer_create(request):
    serializer = BuyerSerializer(data=request.data)
    if serializer.is_valid():
        buyer = serializer.save()

        magazine_ids = request.data.get('magazines', [])
        purchases = []
        for magazine_id in magazine_ids:
            magazine = get_object_or_404(Magazine, id=magazine_id)
            purchase = Purchase(buyer=buyer, magazine=magazine, price=magazine.price)
            purchases.append(purchase)

        Purchase.objects.bulk_create(purchases)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


from rest_framework import status


@api_view(['GET', 'PUT', 'DELETE'])
def buyer_detail(request, pk):
    try:
        buyer = Buyer.objects.get(pk=pk)
    except Buyer.DoesNotExist:
        return Response({'error': 'Buyer does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BuyerSerializer(buyer)
        data = serializer.data
        magazines = Magazine.objects.filter(purchase__buyer=buyer).distinct()
        magazine_serializer = MagazineSerializer(magazines, many=True)
        data['magazines'] = magazine_serializer.data
        return Response(data)

    elif request.method == 'PUT':
        serializer = BuyerSerializer(buyer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        buyer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# BuyerSubscription views
@api_view(['GET'])
def subscriptions_list(request):
    subscriptions = BuyerSubscription.objects.all()
    serializer = BuyerSubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def subscription_create(request):
    serializer = BuyerSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def subscription_detail(request, pk):
    try:
        subscription = BuyerSubscription.objects.get(pk=pk)
    except:
        return Response({'error': 'Subscription does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BuyerSubscriptionSerializer(subscription)
        data = serializer.data

        buyer_serializer = BuyerSerializer(subscription.buyer)
        data['buyer'] = buyer_serializer.data

        return Response(data)

    if request.method == 'PUT':
        serializer = BuyerSubscriptionSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def publisher_stats(request):
    # Calculate the average number of pages for magazines published by each publisher
    publisher_page_stats = (
        Publisher.objects.annotate(average_number_of_pages=Avg('magazine__number_of_pages'))
        .values('name', 'average_number_of_pages')
        .order_by('average_number_of_pages')
    )

    # Create a list of DTO instances
    publisher_stats = [
        PublisherStatsDTO(publisher_name=stat['name'], average_number_of_pages=stat['average_number_of_pages'])
        for stat in publisher_page_stats
    ]

    # Serialize the DTO instances
    serializer = PublisherStatsDTOSerializer(publisher_stats, many=True)

    # Return the serialized data as a JSON response
    return Response(serializer.data)

@api_view(['GET'])
def author_stats(request):
    # Calculate the average number of pages for magazines written by each author
    author_page_stats = (
        Author.objects.annotate(average_number_of_pages=Avg('magazine__number_of_pages'))
        .exclude(average_number_of_pages__isnull=True)
        .values('first_name', 'average_number_of_pages')
        .order_by('average_number_of_pages')
    )

    # Create a list of DTO instances
    author_stats = [
        AuthorStatsDTO(author_first_name=stat['first_name'], average_number_of_pages=stat['average_number_of_pages'])
        for stat in author_page_stats
    ]

    # Serialize the DTO instances
    serializer = AuthorStatsDTOSerializer(author_stats, many=True)

    # Return the serialized data as a JSON response
    return Response(serializer.data)

# @api_view(['POST'])
# def add_buyer_to_magazine(request, id):
#     try:
#         magazine = Magazine.objects.get(pk=id)
#         buyer_id = request.data.get('buyer_id')
#         buyer = Buyer.objects.get(pk=buyer_id)
#         magazine.buyers.add(buyer)
#         magazine.save()
#         return Response({'success': True, 'message': 'Buyer added successfully to the magazine.'},
#                         status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['DELETE'])
# def remove_buyer_from_magazine(request, id, buyer_id):
#     try:
#         magazine = Magazine.objects.get(pk=id)
#         buyer = Buyer.objects.get(pk=buyer_id)
#         magazine.buyers.remove(buyer)
#         magazine.save()
#         return Response({'success': True, 'message': 'Buyer removed successfully from the magazine.'},
#                         status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def magazine_add_buyer(request, id):
    magazine = get_object_or_404(Magazine, id=id)
    buyer_id = request.data.get('buyer_id')
    buyer = get_object_or_404(Buyer, id=buyer_id)

    magazine.buyers.add(buyer)
    magazine.save()

    purchase = Purchase(magazine=magazine, buyer=buyer, price=magazine.price)
    purchase.save()

    return Response({'success': True, 'message': 'Buyer added successfully to the magazine.'},
                    status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def magazine_update_buyers(request, id):
    magazine = get_object_or_404(Magazine, id=id)
    buyer_ids = request.data.get('buyer_ids')

    # Clear all the existing buyers
    magazine.buyers.clear()

    # Delete all the purchases with the specified magazine ID and buyer ID
    for buyer_id in buyer_ids:
        buyer = get_object_or_404(Buyer, id=buyer_id)
        Purchase.objects.filter(magazine=magazine, buyer=buyer).delete()

        # Add the buyer to the magazine
        magazine.buyers.add(buyer)

        # Create a new purchase with the updated buyer and magazine
        purchase = Purchase(magazine=magazine, buyer=buyer, price=magazine.price)
        purchase.save()

    return Response({'success': True, 'message': 'Buyers updated successfully for the magazine.'},
                    status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
def magazine_update_or_delete_buyer(request, id, buyer_id):
    magazine = get_object_or_404(Magazine, id=id)
    buyer = get_object_or_404(Buyer, id=buyer_id)

    if request.method == 'PUT':
        new_price = request.data.get('price')

        if new_price:
            purchase = get_object_or_404(Purchase, magazine=magazine, buyer=buyer)
            purchase.price = new_price
            purchase.save()
            return Response({'success': True, 'message': 'Purchase updated successfully.'},
                            status=status.HTTP_200_OK)

        return Response({'success': False, 'message': 'Missing price information.'},
                        status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        purchase = get_object_or_404(Purchase, magazine=magazine, buyer=buyer)
        purchase.delete()
        magazine.buyers.remove(buyer)
        magazine.save()
        return Response({'success': True, 'message': 'Buyer removed from the magazine.'},
                        status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def buyer_add_magazine(request, id):
    buyer = get_object_or_404(Buyer, id=id)
    magazine_id = request.data.get('magazine_id')

    if magazine_id:
        magazine = get_object_or_404(Magazine, id=magazine_id)
        purchase = Purchase(buyer=buyer, magazine=magazine, price=magazine.price)
        purchase.save()
        return Response({'success': True, 'message': 'Magazine added to the buyer.'},
                        status=status.HTTP_201_CREATED)

    return Response({'success': False, 'message': 'Missing magazine_id information.'},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def buyer_update_or_delete_magazine(request, id, magazine_id):
    buyer = get_object_or_404(Buyer, id=id)
    magazine = get_object_or_404(Magazine, id=magazine_id)

    if request.method == 'PUT':
        new_price = request.data.get('price')

        if new_price:
            purchase = get_object_or_404(Purchase, magazine=magazine, buyer=buyer)
            purchase.price = new_price
            purchase.save()
            return Response({'success': True, 'message': 'Purchase updated successfully.'},
                            status=status.HTTP_200_OK)

        return Response({'success': False, 'message': 'Missing price information.'},
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        purchase = Purchase.objects.filter(magazine=magazine, buyer=buyer).first()
        if purchase:
            purchase.delete()
            return Response({'success': True, 'message': 'Magazine removed from the buyer.'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'success': False, 'message': 'No matching purchase found.'},
                            status=status.HTTP_404_NOT_FOUND)
