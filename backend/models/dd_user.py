from datetime import datetime

from sqlalchemy import String, Integer, Numeric, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column as mc

from backend.models.base import BaseModel
from backend.models.mixins import CommonColumnsMixin


class DDUser(CommonColumnsMixin, BaseModel):
    __tablename__ = 'dd_users'

    name: Mapped[str] = mc(String(255), nullable=False, info={
        'name': 'name',
        'display_name': 'Name',
        'description': 'DD user full name',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })

    email: Mapped[str] = mc(String(255), nullable=False, unique=True, info={
        'name': 'email',
        'display_name': 'Email',
        'description': 'DD user primary email address',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })

    role: Mapped[str] = mc(String(50), nullable=False, info={
        'name': 'role',
        'display_name': 'Role',
        'description': 'Role assigned within the DD portal',
        'display_type': 'select',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    invited_by: Mapped[str | None] = mc(String(255), info={
        'name': 'invited_by',
        'display_name': 'Invited By',
        'description': 'Name or email of the inviter',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })

    total_checks: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'total_checks',
        'display_name': 'Total Checks',
        'description': 'Total verification checks performed',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    amount_spend: Mapped[float] = mc(Numeric(12, 2), default=0, nullable=False, info={
        'name': 'amount_spend',
        'display_name': 'Amount Spend',
        'description': 'Total spend for this DD user',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    status: Mapped[str] = mc(String(20), default='ACTIVE', info={
        'name': 'status',
        'display_name': 'Status',
        'description': 'Operational status of the DD user',
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
                {'value': 'INACTIVE', 'label': 'Inactive'},
                {'value': 'SUSPENDED', 'label': 'Suspended'},
            ]
        },
    })

    total_verifications: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'total_verifications',
        'display_name': 'Total Verifications',
        'description': 'Aggregate number of verifications completed',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    total_dd_verify: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'total_dd_verify',
        'display_name': 'Total DD Verify',
        'description': 'Number of due diligence verifications completed',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    total_kyc_verify: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'total_kyc_verify',
        'display_name': 'Total KYC Verify',
        'description': 'Number of KYC verifications completed',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    verified_leads: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'verified_leads',
        'display_name': 'Verified Leads',
        'description': 'Number of leads marked as verified',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    non_compliant_leads: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'non_compliant_leads',
        'display_name': 'Non-Compliant Leads',
        'description': 'Number of leads flagged as non-compliant',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    rejected_leads: Mapped[int] = mc(Integer, default=0, nullable=False, info={
        'name': 'rejected_leads',
        'display_name': 'Rejected Leads',
        'description': 'Number of leads rejected during verification',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    credits_remaining: Mapped[float] = mc(Numeric(12, 2), default=0, nullable=False, info={
        'name': 'credits_remaining',
        'display_name': 'Credits Remaining',
        'description': 'Credits remaining for verification checks',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': True,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
        'min_value': 0,
    })

    last_kyc_verify: Mapped[datetime | None] = mc(DateTime(timezone=True), info={
        'name': 'last_kyc_verify',
        'display_name': 'Last KYC Verify',
        'description': 'Timestamp of the most recent KYC verification',
        'display_type': 'datetime',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
    })

    lead_source_details: Mapped[dict | None] = mc(JSON, info={
        'name': 'lead_source_details',
        'display_name': 'Lead Source Details',
        'description': 'Structured data about lead source performance',
        'display_type': 'json_editor',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
    })

    top_lead_sources: Mapped[list | None] = mc(JSON, info={
        'name': 'top_lead_sources',
        'display_name': 'Top Lead Sources',
        'description': 'Array of top-performing lead sources',
        'display_type': 'json_editor',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': False,
        'is_filterable': False,
    })

    most_checked_source: Mapped[str | None] = mc(String(255), info={
        'name': 'most_checked_source',
        'display_name': 'Most Checked Source',
        'description': 'Source with highest number of checks',
        'display_type': 'text',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': True,
        'is_sortable': True,
        'is_filterable': True,
        'max_length': 255,
    })

    lowest_performing_score: Mapped[float | None] = mc(Numeric(5, 2), info={
        'name': 'lowest_performing_score',
        'display_name': 'Lowest Performing Score',
        'description': 'Lowest performance score across lead sources',
        'display_type': 'number',
        'is_visible': True,
        'is_editable': True,
        'is_required': False,
        'is_searchable': False,
        'is_sortable': True,
        'is_filterable': True,
    })

    updateable_fields = [
        'name',
        'email',
        'role',
        'invited_by',
        'total_checks',
        'amount_spend',
        'status',
        'total_verifications',
        'total_dd_verify',
        'total_kyc_verify',
        'verified_leads',
        'non_compliant_leads',
        'rejected_leads',
        'credits_remaining',
        'last_kyc_verify',
        'lead_source_details',
        'top_lead_sources',
        'most_checked_source',
        'lowest_performing_score',
    ]

    readable_fields = [
        'id',
        'created_at',
        'last_updated_at',
        'name',
        'email',
        'role',
        'invited_by',
        'total_checks',
        'amount_spend',
        'status',
        'total_verifications',
        'total_dd_verify',
        'total_kyc_verify',
        'verified_leads',
        'non_compliant_leads',
        'rejected_leads',
        'credits_remaining',
        'last_kyc_verify',
        'lead_source_details',
        'top_lead_sources',
        'most_checked_source',
        'lowest_performing_score',
    ]

    sortable_fields = [
        'id',
        'created_at',
        'name',
        'email',
        'role',
        'total_checks',
        'amount_spend',
        'status',
        'total_verifications',
        'total_dd_verify',
        'total_kyc_verify',
        'verified_leads',
        'non_compliant_leads',
        'rejected_leads',
        'credits_remaining',
        'last_kyc_verify',
        'most_checked_source',
        'lowest_performing_score',
    ]

    searchable_fields = [
        'name',
        'email',
        'role',
        'invited_by',
    ]

    filterable_fields = [
        'id',
        'name',
        'email',
        'role',
        'status',
        'total_checks',
        'total_verifications',
        'total_dd_verify',
        'total_kyc_verify',
        'verified_leads',
        'non_compliant_leads',
        'rejected_leads',
    ]
