from sqlalchemy.orm import Mapped, mapped_column as mc
from sqlalchemy import String, Boolean, Integer, DateTime, Numeric
from datetime import datetime

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class Company(CommonColumnsMixin, BaseModel):
    __tablename__ = 'companies'

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Company Name',
        'description': 'The official registered name of the company',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })
    registration_number: Mapped[str] = mc(String(100), nullable=False, info={
        'name': 'registration_number',
        'display_name': 'Registration Number',
        'description': 'Company registration number (e.g., syn12523746)',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 100,
    })
    ico_number: Mapped[str|None] = mc(String(50), info={
        'name': 'ico_number',
        'display_name': 'ICO Number',
        'description': 'Information Commissioner Office registration number',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 50,
    })
    ico_verification_status: Mapped[str] = mc(String(20), default='NOT_SUBMITTED', info={
        'name': 'ico_verification_status',
        'display_name': 'ICO Verification Status',
        'description': 'Status of ICO number verification',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'VERIFIED', 'label': 'Verified'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'FAILED', 'label': 'Failed'},
                {'value': 'NOT_SUBMITTED', 'label': 'Not Submitted'}
            ]
        },
    })
    ico_verified_date: Mapped[datetime|None] = mc(DateTime(timezone=True), info={
        'name': 'ico_verified_date',
        'display_name': 'ICO Verified Date',
        'description': 'Date when ICO number was verified',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    vat_number: Mapped[str|None] = mc(String(50), info={
        'name': 'vat_number',
        'display_name': 'VAT Number',
        'description': 'Value Added Tax registration number',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 50,
    })
    vat_verification_status: Mapped[str] = mc(String(20), default='NOT_SUBMITTED', info={
        'name': 'vat_verification_status',
        'display_name': 'VAT Verification Status',
        'description': 'Status of VAT number verification',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'VERIFIED', 'label': 'Verified'},
                {'value': 'PENDING', 'label': 'Pending'},
                {'value': 'FAILED', 'label': 'Failed'},
                {'value': 'NOT_SUBMITTED', 'label': 'Not Submitted'}
            ]
        },
    })
    vat_verified_date: Mapped[datetime|None] = mc(DateTime(timezone=True), info={
        'name': 'vat_verified_date',
        'display_name': 'VAT Verified Date',
        'description': 'Date when VAT number was verified',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    status: Mapped[str] = mc(String(20), default='ACTIVE', info={
        'name': 'status',
        'display_name': 'Company Status',
        'description': 'Operational status of the company',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'ACTIVE', 'label': 'Active'},
                {'value': 'INACTIVE', 'label': 'Inactive'}
            ]
        },
    })
    phone: Mapped[str|None] = mc(String(50), info={
        'name': 'phone',
        'display_name': 'Phone Number',
        'description': 'Company contact phone number',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': False,
        'is_filterable': False,
        'max_length': 50,
    })
    gdpr_fines: Mapped[bool] = mc(Boolean, default=False, info={
        'name': 'gdpr_fines',
        'display_name': 'GDPR Fines',
        'description': 'Whether the company has received GDPR fines',
        'display_type': 'boolean',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    follower_count: Mapped[int] = mc(Integer, default=0, info={
        'name': 'follower_count',
        'display_name': 'Follower Count',
        'description': 'Number of followers for this company',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    approval_status: Mapped[str] = mc(String(20), default='PENDING_APPROVAL', info={
        'name': 'approval_status',
        'display_name': 'Approval Status',
        'description': 'Company approval status for platform access',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'display_settings': {
            'options': [
                {'value': 'APPROVED', 'label': 'Approved'},
                {'value': 'REJECTED', 'label': 'Rejected'},
                {'value': 'NOT_VERIFIED', 'label': 'Not Verified'},
                {'value': 'PENDING_APPROVAL', 'label': 'Pending Approval'}
            ]
        },
    })
    
    # Buyer-specific financial tracking fields
    total_spent: Mapped[float|None] = mc(Numeric(12, 2), default=0.0, info={
        'name': 'total_spent',
        'display_name': 'Total Spent',
        'description': 'Total amount spent by this company on purchases',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': False,  # Calculated field
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    total_purchases: Mapped[int|None] = mc(Integer, default=0, info={
        'name': 'total_purchases',
        'display_name': 'Total Purchases',
        'description': 'Total number of purchases made by this company',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': False,  # Calculated field
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    average_purchase_amount: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'average_purchase_amount',
        'display_name': 'Average Purchase Amount',
        'description': 'Average amount per purchase for this company',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': False,  # Calculated field
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    # GDPR fine details
    gdpr_fine_amount: Mapped[float|None] = mc(Numeric(10, 2), info={
        'name': 'gdpr_fine_amount',
        'display_name': 'GDPR Fine Amount',
        'description': 'Amount of GDPR fine if applicable',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })
    
    gdpr_fine_date: Mapped[datetime|None] = mc(DateTime(timezone=True), info={
        'name': 'gdpr_fine_date',
        'display_name': 'GDPR Fine Date',
        'description': 'Date when GDPR fine was imposed',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })
    signed_up_date: Mapped[datetime] = mc(DateTime(timezone=True), default=lambda: datetime.now(), nullable=False, info={
        'name': 'signed_up_date',
        'display_name': 'Signed Up Date',
        'description': 'Date when the company registered on the platform',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })
    id_address: Mapped[int] = mc(nullable=False, info={
        'name': 'id_address',
        'display_name': 'Address',
        'description': 'FK to Address for company location',
        'display_type': 'foreign_key',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'name',
        'registration_number',
        'ico_number',
        'ico_verification_status',
        'ico_verified_date',
        'vat_number',
        'vat_verification_status',
        'vat_verified_date',
        'status',
        'phone',
        'gdpr_fines',
        'follower_count',
        'approval_status',
        'signed_up_date',
        'gdpr_fine_amount',
        'gdpr_fine_date',
        'id_address',
    ]

    readable_fields = [
        'id',
        'created_at',
        'name',
        'registration_number',
        'ico_number',
        'ico_verification_status',
        'ico_verified_date',
        'vat_number',
        'vat_verification_status',
        'vat_verified_date',
        'status',
        'phone',
        'gdpr_fines',
        'follower_count',
        'approval_status',
        'signed_up_date',
        'total_spent',
        'total_purchases',
        'average_purchase_amount',
        'gdpr_fine_amount',
        'gdpr_fine_date',
        'id_address',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'name',
        'registration_number',
        'ico_verification_status',
        'vat_verification_status',
        'status',
        'follower_count',
        'approval_status',
        'signed_up_date',
    ]

    searchable_fields = [
        'name',
        'registration_number',
        'ico_number',
        'vat_number',
        'phone',
    ]

    filterable_fields = [
        'id',
        'name',
        'registration_number',
        'ico_verification_status',
        'vat_verification_status',
        'status',
        'gdpr_fines',
        'follower_count',
        'approval_status',
        'total_spent',
        'total_purchases',
        'average_purchase_amount',
        'id_address',
    ]
