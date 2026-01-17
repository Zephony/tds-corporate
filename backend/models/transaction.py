from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Text, DateTime, Numeric, Date, ForeignKey

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Transaction(CommonColumnsMixin, BaseModel):
    __tablename__ = 'transactions'

    id_transaction: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'id_transaction',
        'display_name': 'Transaction ID',
        'description': 'External transaction ID from payment provider',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_order: Mapped[int] = mc(
        ForeignKey('orders.id', name='fk_transactions_orders'),
        nullable=False,
        info={
        'name': 'id_order',
        'display_name': 'Order ID',
        'description': 'Internal order reference',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    transaction_date: Mapped[DateTime] = mc(DateTime(timezone=True), nullable=False, info={
        'name': 'transaction_date',
        'display_name': 'Transaction Date',
        'description': 'When the transaction occurred',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    sale_price: Mapped[float] = mc(Numeric(10, 2), nullable=False, info={
        'name': 'sale_price',
        'display_name': 'Sale Price',
        'description': 'Base sale price before fees and VAT',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    vat_amount: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'vat_amount',
        'display_name': 'VAT Amount',
        'description': 'VAT amount',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    tds_fee: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'tds_fee',
        'display_name': 'TDS Fee',
        'description': 'TDS platform fee',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    payment_provider_fee: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'payment_provider_fee',
        'display_name': 'Payment Provider Fee',
        'description': 'Payment provider processing fee',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    net_payable: Mapped[float] = mc(Numeric(10, 2), nullable=False, info={
        'name': 'net_payable',
        'display_name': 'Net Payable',
        'description': 'Amount payable to seller after deductions',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    remaining_vat: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'remaining_vat',
        'display_name': 'Remaining VAT',
        'description': 'Remaining VAT amount',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    total_payable: Mapped[float] = mc(Numeric(10, 2), nullable=False, info={
        'name': 'total_payable',
        'display_name': 'Total Payable',
        'description': 'Total amount payable',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    payable_date: Mapped[Date|None] = mc(Date, info={
        'name': 'payable_date',
        'display_name': 'Payable Date',
        'description': 'When payment is due/scheduled',
        'display_type': 'date',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    status: Mapped[str] = mc(String(50), nullable=False, info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Transaction status',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    portal: Mapped[str] = mc(String(20), nullable=False, info={
        'name': 'portal',
        'display_name': 'Portal',
        'description': 'Source portal for the transaction',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'TDS', 'label': 'TDS'},
                {'value': 'DD_PORTAL', 'label': 'DD Portal'},
                {'value': 'AD_PORTAL', 'label': 'Ad Portal'},
            ]
        },
    })

    invoice_id: Mapped[str | None] = mc(String(50), info={
        'name': 'invoice_id',
        'display_name': 'Invoice ID',
        'description': 'Identifier for the associated invoice',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 50,
    })

    invoice_url: Mapped[str | None] = mc(Text, info={
        'name': 'invoice_url',
        'display_name': 'Invoice URL',
        'description': 'Download link for the invoice document',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
    })

    payment_provider: Mapped[str] = mc(String(100), nullable=False, info={
        'name': 'payment_provider',
        'display_name': 'Payment Provider',
        'description': 'Payment method used',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    notes: Mapped[str|None] = mc(Text, info={
        'name': 'notes',
        'display_name': 'Notes',
        'description': 'Additional transaction notes',
        'display_type': 'textarea',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
    })
    id_buyer: Mapped[int|None] = mc(
        ForeignKey('buyers.id', name='fk_transactions_buyers'),
        nullable=True,
        info={
        'name': 'id_buyer',
        'display_name': 'Buyer',
        'description': 'FK to buyer user',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_seller: Mapped[int|None] = mc(
        ForeignKey('sellers.id', name='fk_transactions_sellers'),
        nullable=True,
        info={
        'name': 'id_seller',
        'display_name': 'Seller',
        'description': 'FK to seller user',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_product: Mapped[int|None] = mc(
        ForeignKey('products.id', name='fk_transactions_products'),
        nullable=True,
        info={
        'name': 'id_product',
        'display_name': 'Product',
        'description': 'FK to product',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'id_transaction',
        'id_order',
        'transaction_date',
        'sale_price',
        'vat_amount',
        'tds_fee',
        'payment_provider_fee',
        'net_payable',
        'remaining_vat',
        'total_payable',
        'payable_date',
        'status',
        'portal',
        'invoice_id',
        'invoice_url',
        'payment_provider',
        'notes',
        'id_buyer',
        'id_seller',
        'id_product',
    ]

    readable_fields = [
        'id',
        'created_at',
        'id_transaction',
        'id_order',
        'transaction_date',
        'sale_price',
        'vat_amount',
        'tds_fee',
        'payment_provider_fee',
        'net_payable',
        'remaining_vat',
        'total_payable',
        'payable_date',
        'status',
        'portal',
        'invoice_id',
        'invoice_url',
        'payment_provider',
        'notes',
        'id_buyer',
        'id_seller',
        'id_product',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'id_transaction',
        'id_order',
        'transaction_date',
        'sale_price',
        'vat_amount',
        'tds_fee',
        'payment_provider_fee',
        'net_payable',
        'remaining_vat',
        'total_payable',
        'payable_date',
        'status',
        'portal',
        'invoice_id',
        'payment_provider',
    ]

    searchable_fields = [
        'id_transaction',
        'id_order',
        'status',
        'invoice_id',
        'payment_provider',
        'notes',
    ]

    filterable_fields = [
        'id',
        'transaction_date',
        'sale_price',
        'vat_amount',
        'tds_fee',
        'payment_provider_fee',
        'net_payable',
        'remaining_vat',
        'total_payable',
        'payable_date',
        'status',
        'portal',
        'invoice_id',
        'payment_provider',
        'id_buyer',
        'id_seller',
        'id_product',
    ]
