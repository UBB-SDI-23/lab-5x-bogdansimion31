from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

from .views import (
    magazines_list,
    magazine_create,
    magazine_detail,
    authors_list,
    author_create,
    author_detail,
    publishers_list,
    publisher_create,
    publisher_detail,
    magazines_with_pages_above,
    buyers_list,
    buyer_create,
    buyer_detail,
    subscriptions_list,
    subscription_create,
    subscription_detail,
    publisher_stats,
    magazine_add_buyer,
    magazine_update_or_delete_buyer,
    buyer_add_magazine,
    buyer_update_or_delete_magazine,
    magazine_update_buyers, author_stats,
    magazine_update_buyers, author_stats, magazines_pagination, authors_pagination, buyers_pagination,
     publishers_pagination
)
schema_view = swagger_get_schema_view(
    openapi.Info(
        title="MAGAZINES API",
        default_version="1.0.0",
        description="API documentation"
    ),
    public=True,
)

urlpatterns = [
    path('magazines/list/', magazines_list),
    path('magazines/', magazine_create),
    path('magazines/<int:pk>/', magazine_detail),
    path('authors/list/', authors_list),
    path('authors/', author_create),
    path('authors/<int:pk>/', author_detail),
    path('publishers/list/', publishers_list),
    path('publishers/', publisher_create),
    path('publishers/<int:pk>/', publisher_detail),
    path('magazines/above/<int:min_pages>/', magazines_with_pages_above, name='magazines_with_pages_above'),
    path('buyers/list/', buyers_list),
    path('buyers/', buyer_create),
    path('buyers/<int:pk>/', buyer_detail),
    path('subscriptions/list/', subscriptions_list),
    path('subscriptions/', subscription_create),
    path('subscriptions/<int:pk>/', subscription_detail),
    path('publisher_stats/', publisher_stats, name='publisher_stats'),
    path('author_stats/', author_stats, name='author_stats'),
    path('magazines/<int:id>/buyers/', magazine_add_buyer, name='magazine-add-buyer'),
    path('magazines/<int:id>/buyers/<int:buyer_id>/', magazine_update_or_delete_buyer, name='magazine-update-or-delete-buyer'),
    path('buyers/<int:id>/magazines/', buyer_add_magazine, name='buyer-add-magazine'),
    path('buyers/<int:id>/magazines/<int:magazine_id>/', buyer_update_or_delete_magazine, name='buyer-update-or-delete-magazine'),
    path('magazines/<int:id>/buyers/update', magazine_update_buyers),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('magazines/<int:id>/buyers/<int:buyer_id>/', magazine_update_or_delete_buyer, name='magazine-update-or-delete-buyer'),
    path('buyers/<int:id>/magazines/<int:magazine_id>/', buyer_update_or_delete_magazine, name='buyer-update-or-delete-magazine'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('magazines/pagination/', magazines_pagination, name='magazines_pagination'),
    path('authors/pagination/', authors_pagination, name='magazines_pagination'),
    path('publishers/pagination/', publishers_pagination, name='magazines_pagination'),
    path('buyers/pagination/', buyers_pagination, name='magazines_pagination'),

]