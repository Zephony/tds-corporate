from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Text, Numeric, Integer, DateTime, ForeignKey
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Order(CommonColumnsMixin, BaseModel):
    __tablename__ = 'orders'
    
    _info = {
        'description': 'Orders table tracking buyer purchases and transactions',
        'type': 'transactional',
    }

    title: Mapped[str] = mc(String(500), nullable=False, info={
        'name': 'title',
        'display_name': 'Order Title',
        'description': 'Descriptive title for the order',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 500,
    })
    
    description: Mapped[str|None] = mc(Text, info={
        'name': 'description',
        'display_name': 'Description',
        'description': 'Detailed description of the order',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    
    # Order timing
    order_date: Mapped[datetime] = mc(DateTime(timezone=True), default=lambda: datetime.now(), nullable=False, info={
        'name': 'order_date',
        'display_name': 'Order Date',
        'description': 'Date and time when the order was placed',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    completion_date: Mapped[datetime|None] = mc(DateTime(timezone=True), info={
        'name': 'completion_date',
        'display_name': 'Completion Date',
        'description': 'Date and time when the order was completed',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    # Product and quantity details
    id_product: Mapped[int] = mc(
        ForeignKey('products.id', name='fk_orders_products'),
        nullable=False,
        info={
        'name': 'id_product',
        'display_name': 'Product',
        'description': 'FK to Product being purchased',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    
    quantity_ordered: Mapped[int] = mc(Integer, default=1, nullable=False, info={
        'name': 'quantity_ordered',
        'display_name': 'Quantity Ordered',
        'description': 'Number of units or records ordered',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 1,
    })
    
    # Pricing details
    unit_price: Mapped[float] = mc(Numeric(10, 2), nullable=False, info={
        'name': 'unit_price',
        'display_name': 'Unit Price',
        'description': 'Price per unit at the time of order',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    total_amount: Mapped[float] = mc(Numeric(10, 2), nullable=False, info={
        'name': 'total_amount',
        'display_name': 'Total Amount',
        'description': 'Total order amount (quantity × unit_price)',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    discount_amount: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'discount_amount',
        'display_name': 'Discount Amount',
        'description': 'Any discount applied to the order',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': False,
        'min_value': 0,
    })
    
    final_amount: Mapped[float] = mc(Numeric(10, 2), nullable=False, info={
        'name': 'final_amount',
        'display_name': 'Final Amount',
        'description': 'Final amount after discounts',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    # Enhanced status tracking
    status: Mapped[str] = mc(String(20), default='PENDING', info={
        'name': 'status',
        'display_name': 'Order Status',
        'description': 'Current status of the order',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'COMPLETED', 'label': 'Completed'},
                {'value': 'DISPUTED', 'label': 'Disputed'},
                {'value': 'REFUNDED', 'label': 'Refunded'},
                {'value': 'CANCELLED', 'label': 'Cancelled'}
            ]
        },
    })
    
    payment_status: Mapped[str] = mc(String(20), default='PENDING', info={
        'name': 'payment_status',
        'display_name': 'Payment Status',
        'description': 'Status of payment for this order',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'PAID', 'label': 'Paid'},
                {'value': 'FAILED', 'label': 'Failed'},
                {'value': 'REFUNDED', 'label': 'Refunded'}
            ]
        },
    })
    
    delivery_status: Mapped[str] = mc(String(20), default='PENDING', info={
        'name': 'delivery_status',
        'display_name': 'Delivery Status',
        'description': 'Status of data/product delivery',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'DELIVERED', 'label': 'Delivered'},
                {'value': 'FAILED', 'label': 'Failed'},
                {'value': 'CANCELLED', 'label': 'Cancelled'}
            ]
        },
    })
    
    # Buyer and fulfilment relationships
    id_buyer: Mapped[int] = mc(
        ForeignKey('buyers.id', name='fk_orders_buyers'),
        nullable=False,
        info={
            'name': 'id_buyer',
            'display_name': 'Buyer',
            'description': 'FK to Buyer who placed the order',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    id_company: Mapped[int] = mc(
        ForeignKey('companies.id', name='fk_orders_companies'),
        nullable=False,
        info={
            'name': 'id_company',
            'display_name': 'Company',
            'description': 'FK to Company fulfilling the order',
            'display_type': 'foreign_key',
            'is_visible': True,
            'is_editable': True,
            'is_required': True,
            'is_searchable': True,
            'is_sortable': True,
            'is_filterable': True,
        },
    )

    updateable_fields = [
        'title',
        'description',
        'order_date',
        'completion_date',
        'id_product',
        'quantity_ordered',
        'unit_price',
        'total_amount',
        'discount_amount',
        'final_amount',
        'status',
        'payment_status',
        'delivery_status',
        'id_buyer',
        'id_company',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'title',
        'description',
        'order_date',
        'completion_date',
        'id_product',
        'quantity_ordered',
        'unit_price',
        'total_amount',
        'discount_amount',
        'final_amount',
        'status',
        'payment_status',
        'delivery_status',
        'id_buyer',
        'id_company',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'order_date',
        'completion_date',
        'quantity_ordered',
        'unit_price',
        'total_amount',
        'final_amount',
        'status',
        'payment_status',
        'delivery_status',
    ]

    searchable_fields = [
        'title',
        'description',
    ]

    filterable_fields = [
        'id',
        'order_date',
        'completion_date',
        'id_product',
        'status',
        'payment_status',
        'delivery_status',
        'id_buyer',
        'id_company',
    ]
