"""Static responses for dashboard endpoints."""

REVENUE_TREND_DATA = [
    {'date': '2024-07-01', 'revenue': 48250.45},
    {'date': '2024-07-02', 'revenue': 48510.12},
    {'date': '2024-07-03', 'revenue': 48775.83},
    {'date': '2024-07-04', 'revenue': 49040.55},
    {'date': '2024-07-05', 'revenue': 49305.26},
    {'date': '2024-07-06', 'revenue': 49570.98},
    {'date': '2024-07-07', 'revenue': 49835.69},
    {'date': '2024-07-08', 'revenue': 50100.41},
    {'date': '2024-07-09', 'revenue': 50365.12},
    {'date': '2024-07-10', 'revenue': 50630.84},
    {'date': '2024-07-11', 'revenue': 50895.55},
    {'date': '2024-07-12', 'revenue': 51160.27},
    {'date': '2024-07-13', 'revenue': 51424.98},
    {'date': '2024-07-14', 'revenue': 51689.7},
    {'date': '2024-07-15', 'revenue': 51954.41},
    {'date': '2024-07-16', 'revenue': 52219.13},
    {'date': '2024-07-17', 'revenue': 52483.84},
    {'date': '2024-07-18', 'revenue': 52748.56},
    {'date': '2024-07-19', 'revenue': 53013.27},
    {'date': '2024-07-20', 'revenue': 53277.99},
    {'date': '2024-07-21', 'revenue': 53542.7},
    {'date': '2024-07-22', 'revenue': 53807.42},
    {'date': '2024-07-23', 'revenue': 54072.13},
    {'date': '2024-07-24', 'revenue': 54336.85},
    {'date': '2024-07-25', 'revenue': 54601.56},
    {'date': '2024-07-26', 'revenue': 54866.28},
    {'date': '2024-07-27', 'revenue': 55130.99},
    {'date': '2024-07-28', 'revenue': 55395.71},
    {'date': '2024-07-29', 'revenue': 55660.42},
    {'date': '2024-07-30', 'revenue': 55925.14},
    {'date': '2024-07-31', 'revenue': 56189.85},
    {'date': '2024-08-01', 'revenue': 56454.57},
    {'date': '2024-08-02', 'revenue': 56719.28},
    {'date': '2024-08-03', 'revenue': 56983.99},
    {'date': '2024-08-04', 'revenue': 57248.71},
    {'date': '2024-08-05', 'revenue': 57513.42},
    {'date': '2024-08-06', 'revenue': 57778.14},
    {'date': '2024-08-07', 'revenue': 58042.85},
    {'date': '2024-08-08', 'revenue': 58307.57},
    {'date': '2024-08-09', 'revenue': 58572.28},
    {'date': '2024-08-10', 'revenue': 58836.99},
    {'date': '2024-08-11', 'revenue': 59101.71},
    {'date': '2024-08-12', 'revenue': 59366.42},
    {'date': '2024-08-13', 'revenue': 59631.14},
    {'date': '2024-08-14', 'revenue': 59895.85},
    {'date': '2024-08-15', 'revenue': 60160.57},
    {'date': '2024-08-16', 'revenue': 60425.28},
    {'date': '2024-08-17', 'revenue': 60689.99},
    {'date': '2024-08-18', 'revenue': 60954.71},
    {'date': '2024-08-19', 'revenue': 61219.42},
]

REVENUE_TREND_RESPONSE = {
    'data': REVENUE_TREND_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(REVENUE_TREND_DATA),
        'returned_items': len(REVENUE_TREND_DATA),
        'total_items': len(REVENUE_TREND_DATA),
    },
}


REVENUE_TYPE_DATA = [
    {'revenue_type': 'TDS', 'amount': 186250.75},
    {'revenue_type': 'DD Portal', 'amount': 74210.5},
    {'revenue_type': 'Ad Portal', 'amount': 91340.0},
]

REVENUE_TYPE_RESPONSE = {
    'data': REVENUE_TYPE_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(REVENUE_TYPE_DATA),
        'returned_items': len(REVENUE_TYPE_DATA),
        'total_items': len(REVENUE_TYPE_DATA),
    },
}


TOP_DISPUTE_REASONS_DATA = [
    {'reason': 'Duplicate Record', 'count': 128},
    {'reason': 'GDPR/CCPA Violation', 'count': 94},
    {'reason': 'Non-Delivery of Leads', 'count': 156},
    {'reason': 'TPS/MPS Violation', 'count': 72},
    {'reason': 'Wrong Demographic', 'count': 88},
]

TOP_DISPUTE_REASONS_RESPONSE = {
    'data': TOP_DISPUTE_REASONS_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(TOP_DISPUTE_REASONS_DATA),
        'returned_items': len(TOP_DISPUTE_REASONS_DATA),
        'total_items': len(TOP_DISPUTE_REASONS_DATA),
    },
}


TOP_CATEGORIES_BY_PURCHASE_DATA = [
    {'category': 'Energy & Utilities', 'count': 142},
    {'category': 'Advertising Data', 'count': 118},
    {'category': 'Financial & Insurance', 'count': 176},
    {'category': 'Home Improvements', 'count': 101},
    {'category': 'Residential Data', 'count': 89},
]

TOP_CATEGORIES_BY_PURCHASE_RESPONSE = {
    'data': TOP_CATEGORIES_BY_PURCHASE_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(TOP_CATEGORIES_BY_PURCHASE_DATA),
        'returned_items': len(TOP_CATEGORIES_BY_PURCHASE_DATA),
        'total_items': len(TOP_CATEGORIES_BY_PURCHASE_DATA),
    },
}


RETURNING_VS_NEW_USERS_DATA = {
    'total_users': 1824,
    'new_users': 432,
    'returning_users': 1392,
}

RETURNING_VS_NEW_USERS_RESPONSE = {
    'data': RETURNING_VS_NEW_USERS_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': 1,
        'returned_items': 1,
        'total_items': 1,
    },
}


VISITOR_STATUS_DATA = {
    'buyers': {
        'total': 1280,
        'statuses': [
            {'status': 'active', 'count': 845},
            {'status': 'pending', 'count': 312},
            {'status': 'rejected', 'count': 123},
        ],
    },
    'sellers': {
        'total': 540,
        'statuses': [
            {'status': 'active', 'count': 402},
            {'status': 'pending', 'count': 96},
            {'status': 'rejected', 'count': 42},
        ],
    },
    'buyer_and_seller_verification': [
        {'status': 'verified', 'count': 972},
        {'status': 'unverified', 'count': 348},
    ],
}

VISITOR_STATUS_RESPONSE = {
    'data': VISITOR_STATUS_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': 1,
        'returned_items': 1,
        'total_items': 1,
    },
}


DISPUTE_INSIGHTS_DATA = {
    'status': [
        {'status': 'active', 'count': 62},
        {'status': 'solved', 'count': 138},
        {'status': 'closed', 'count': 44},
    ],
    'reasons': [
        {'reason': 'payment', 'count': 71},
        {'reason': 'gdpr fine', 'count': 39},
        {'reason': 'wrong product', 'count': 84},
    ],
    'gdpr_fines': [
        {'status': 'gdpr fined', 'count': 28},
        {'status': 'not fined', 'count': 216},
    ],
}

DISPUTE_INSIGHTS_RESPONSE = {
    'data': DISPUTE_INSIGHTS_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': 1,
        'returned_items': 1,
        'total_items': 1,
    },
}


COMPLIANCE_BREAKDOWN_DATA = {
    'reasons': [
        {'reason': 'Verified', 'count': 684},
        {'reason': 'Non-Compliant', 'count': 172},
        {'reason': 'Rejected', 'count': 96},
    ],
    'total_records': 952,
}


COMPLIANCE_BREAKDOWN_RESPONSE = {
    'data': COMPLIANCE_BREAKDOWN_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': 1,
        'returned_items': 1,
        'total_items': 1,
    },
}


COMPLIANCE_ISSUE_TYPES_DATA = [
    {
        'date': '2024-07-01',
        'issues': [
            {'reason': 'invalid_address', 'count': 18},
            {'reason': 'missing_dob', 'count': 11},
            {'reason': 'auth_failure', 'count': 7},
        ],
    },
    {
        'date': '2024-07-02',
        'issues': [
            {'reason': 'invalid_address', 'count': 15},
            {'reason': 'missing_dob', 'count': 9},
            {'reason': 'auth_failure', 'count': 10},
        ],
    },
    {
        'date': '2024-07-03',
        'issues': [
            {'reason': 'invalid_address', 'count': 21},
            {'reason': 'missing_dob', 'count': 8},
            {'reason': 'auth_failure', 'count': 9},
        ],
    },
    {
        'date': '2024-07-04',
        'issues': [
            {'reason': 'invalid_address', 'count': 16},
            {'reason': 'missing_dob', 'count': 12},
            {'reason': 'auth_failure', 'count': 6},
        ],
    },
    {
        'date': '2024-07-05',
        'issues': [
            {'reason': 'invalid_address', 'count': 19},
            {'reason': 'missing_dob', 'count': 10},
            {'reason': 'auth_failure', 'count': 11},
        ],
    },
]


COMPLIANCE_ISSUE_TYPES_RESPONSE = {
    'data': COMPLIANCE_ISSUE_TYPES_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(COMPLIANCE_ISSUE_TYPES_DATA),
        'returned_items': len(COMPLIANCE_ISSUE_TYPES_DATA),
        'total_items': len(COMPLIANCE_ISSUE_TYPES_DATA),
    },
}


API_CHECK_TREND_DATA = [
    {'date': '2024-07-01', 'api_checks': 245},
    {'date': '2024-07-02', 'api_checks': 268},
    {'date': '2024-07-03', 'api_checks': 259},
    {'date': '2024-07-04', 'api_checks': 276},
    {'date': '2024-07-05', 'api_checks': 283},
    {'date': '2024-07-06', 'api_checks': 295},
    {'date': '2024-07-07', 'api_checks': 302},
]


API_CHECK_TREND_RESPONSE = {
    'data': API_CHECK_TREND_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(API_CHECK_TREND_DATA),
        'returned_items': len(API_CHECK_TREND_DATA),
        'total_items': len(API_CHECK_TREND_DATA),
    },
}


TOP_API_ERROR_TYPES_DATA = [
    {'error_type': 'invalid_address', 'count': 57},
    {'error_type': 'missing_dob', 'count': 43},
    {'error_type': 'timeout', 'count': 39},
    {'error_type': 'auth_failure', 'count': 34},
    {'error_type': 'invalid_document', 'count': 28},
]


TOP_API_ERROR_TYPES_RESPONSE = {
    'data': TOP_API_ERROR_TYPES_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(TOP_API_ERROR_TYPES_DATA),
        'returned_items': len(TOP_API_ERROR_TYPES_DATA),
        'total_items': len(TOP_API_ERROR_TYPES_DATA),
    },
}


LEAD_DELIVERY_TREND_DATA = [
    {
        'date': '2024-07-01',
        'delivered': 420,
        'accepted': 398,
        'rejected': 22,
    },
    {
        'date': '2024-07-02',
        'delivered': 435,
        'accepted': 410,
        'rejected': 25,
    },
    {
        'date': '2024-07-03',
        'delivered': 448,
        'accepted': 421,
        'rejected': 27,
    },
    {
        'date': '2024-07-04',
        'delivered': 462,
        'accepted': 436,
        'rejected': 26,
    },
    {
        'date': '2024-07-05',
        'delivered': 475,
        'accepted': 447,
        'rejected': 28,
    },
    {
        'date': '2024-07-06',
        'delivered': 489,
        'accepted': 458,
        'rejected': 31,
    },
    {
        'date': '2024-07-07',
        'delivered': 504,
        'accepted': 472,
        'rejected': 32,
    },
    {
        'date': '2024-07-08',
        'delivered': 518,
        'accepted': 485,
        'rejected': 33,
    },
    {
        'date': '2024-07-09',
        'delivered': 533,
        'accepted': 497,
        'rejected': 36,
    },
    {
        'date': '2024-07-10',
        'delivered': 548,
        'accepted': 509,
        'rejected': 39,
    },
]

LEAD_DELIVERY_TREND_RESPONSE = {
    'data': LEAD_DELIVERY_TREND_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(LEAD_DELIVERY_TREND_DATA),
        'returned_items': len(LEAD_DELIVERY_TREND_DATA),
        'total_items': len(LEAD_DELIVERY_TREND_DATA),
    },
}


TOP_BUYERS_BY_SPEND_DATA = [
    {
        'buyer_id': 1,
        'buyer_name': 'Acme Growth Labs',
        'total_spend': 98540.25,
        'purchased_products': 38,
        'disputed_products': 3,
    },
    {
        'buyer_id': 2,
        'buyer_name': 'Globex Demand Partners',
        'total_spend': 87215.0,
        'purchased_products': 32,
        'disputed_products': 5,
    },
    {
        'buyer_id': 3,
        'buyer_name': 'Quantum Leads Ltd.',
        'total_spend': 75680.75,
        'purchased_products': 27,
        'disputed_products': 2,
    },
    {
        'buyer_id': 4,
        'buyer_name': 'Sakura Data Partners',
        'total_spend': 68420.1,
        'purchased_products': 25,
        'disputed_products': 4,
    },
    {
        'buyer_id': 5,
        'buyer_name': 'Volta Acquisition Group',
        'total_spend': 61155.33,
        'purchased_products': 21,
        'disputed_products': 1,
    },
]

TOP_BUYERS_BY_SPEND_RESPONSE = {
    'data': TOP_BUYERS_BY_SPEND_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(TOP_BUYERS_BY_SPEND_DATA),
        'returned_items': len(TOP_BUYERS_BY_SPEND_DATA),
        'total_items': len(TOP_BUYERS_BY_SPEND_DATA),
    },
}


TOP_SELLERS_BY_REVENUE_DATA = [
    {
        'seller_id': 101,
        'seller_name': 'Atlas Data Exchange',
        'total_revenue': 112450.0,
        'listed_products': 54,
        'disputed_products': 4,
    },
    {
        'seller_id': 102,
        'seller_name': 'Northwind Signal Corp',
        'total_revenue': 98560.5,
        'listed_products': 47,
        'disputed_products': 6,
    },
    {
        'seller_id': 103,
        'seller_name': 'Emerald Marketplaces',
        'total_revenue': 90835.75,
        'listed_products': 39,
        'disputed_products': 3,
    },
    {
        'seller_id': 104,
        'seller_name': 'Zenith Lead Partners',
        'total_revenue': 84210.9,
        'listed_products': 36,
        'disputed_products': 5,
    },
    {
        'seller_id': 105,
        'seller_name': 'Beacon Outreach Labs',
        'total_revenue': 76890.25,
        'listed_products': 31,
        'disputed_products': 2,
    },
]

TOP_SELLERS_BY_REVENUE_RESPONSE = {
    'data': TOP_SELLERS_BY_REVENUE_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(TOP_SELLERS_BY_REVENUE_DATA),
        'returned_items': len(TOP_SELLERS_BY_REVENUE_DATA),
        'total_items': len(TOP_SELLERS_BY_REVENUE_DATA),
    },
}


VISITOR_ACTIVITY_TREND_DATA = [
    {
        'date': '2024-07-01',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 2},
            {'hour': '01:00', 'activity': 1},
            {'hour': '02:00', 'activity': 1},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 2},
            {'hour': '05:00', 'activity': 2},
            {'hour': '06:00', 'activity': 3},
            {'hour': '07:00', 'activity': 3},
            {'hour': '08:00', 'activity': 4},
            {'hour': '09:00', 'activity': 5},
            {'hour': '10:00', 'activity': 5},
            {'hour': '11:00', 'activity': 4},
            {'hour': '12:00', 'activity': 4},
            {'hour': '13:00', 'activity': 3},
            {'hour': '14:00', 'activity': 4},
            {'hour': '15:00', 'activity': 5},
            {'hour': '16:00', 'activity': 5},
            {'hour': '17:00', 'activity': 4},
            {'hour': '18:00', 'activity': 3},
            {'hour': '19:00', 'activity': 3},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 2},
            {'hour': '23:00', 'activity': 1},
        ],
    },
    {
        'date': '2024-07-02',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 1},
            {'hour': '01:00', 'activity': 1},
            {'hour': '02:00', 'activity': 1},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 2},
            {'hour': '05:00', 'activity': 2},
            {'hour': '06:00', 'activity': 2},
            {'hour': '07:00', 'activity': 3},
            {'hour': '08:00', 'activity': 3},
            {'hour': '09:00', 'activity': 4},
            {'hour': '10:00', 'activity': 5},
            {'hour': '11:00', 'activity': 5},
            {'hour': '12:00', 'activity': 5},
            {'hour': '13:00', 'activity': 4},
            {'hour': '14:00', 'activity': 4},
            {'hour': '15:00', 'activity': 4},
            {'hour': '16:00', 'activity': 5},
            {'hour': '17:00', 'activity': 5},
            {'hour': '18:00', 'activity': 4},
            {'hour': '19:00', 'activity': 4},
            {'hour': '20:00', 'activity': 3},
            {'hour': '21:00', 'activity': 3},
            {'hour': '22:00', 'activity': 2},
            {'hour': '23:00', 'activity': 2},
        ],
    },
    {
        'date': '2024-07-03',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 1},
            {'hour': '01:00', 'activity': 1},
            {'hour': '02:00', 'activity': 1},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 1},
            {'hour': '05:00', 'activity': 2},
            {'hour': '06:00', 'activity': 2},
            {'hour': '07:00', 'activity': 3},
            {'hour': '08:00', 'activity': 3},
            {'hour': '09:00', 'activity': 4},
            {'hour': '10:00', 'activity': 4},
            {'hour': '11:00', 'activity': 4},
            {'hour': '12:00', 'activity': 5},
            {'hour': '13:00', 'activity': 5},
            {'hour': '14:00', 'activity': 4},
            {'hour': '15:00', 'activity': 4},
            {'hour': '16:00', 'activity': 4},
            {'hour': '17:00', 'activity': 3},
            {'hour': '18:00', 'activity': 3},
            {'hour': '19:00', 'activity': 3},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 2},
            {'hour': '23:00', 'activity': 1},
        ],
    },
    {
        'date': '2024-07-04',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 2},
            {'hour': '01:00', 'activity': 2},
            {'hour': '02:00', 'activity': 2},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 1},
            {'hour': '05:00', 'activity': 2},
            {'hour': '06:00', 'activity': 3},
            {'hour': '07:00', 'activity': 3},
            {'hour': '08:00', 'activity': 4},
            {'hour': '09:00', 'activity': 5},
            {'hour': '10:00', 'activity': 5},
            {'hour': '11:00', 'activity': 5},
            {'hour': '12:00', 'activity': 4},
            {'hour': '13:00', 'activity': 4},
            {'hour': '14:00', 'activity': 4},
            {'hour': '15:00', 'activity': 5},
            {'hour': '16:00', 'activity': 5},
            {'hour': '17:00', 'activity': 4},
            {'hour': '18:00', 'activity': 4},
            {'hour': '19:00', 'activity': 3},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 2},
            {'hour': '23:00', 'activity': 1},
        ],
    },
    {
        'date': '2024-07-05',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 2},
            {'hour': '01:00', 'activity': 2},
            {'hour': '02:00', 'activity': 2},
            {'hour': '03:00', 'activity': 2},
            {'hour': '04:00', 'activity': 2},
            {'hour': '05:00', 'activity': 3},
            {'hour': '06:00', 'activity': 3},
            {'hour': '07:00', 'activity': 4},
            {'hour': '08:00', 'activity': 4},
            {'hour': '09:00', 'activity': 5},
            {'hour': '10:00', 'activity': 5},
            {'hour': '11:00', 'activity': 5},
            {'hour': '12:00', 'activity': 5},
            {'hour': '13:00', 'activity': 4},
            {'hour': '14:00', 'activity': 4},
            {'hour': '15:00', 'activity': 4},
            {'hour': '16:00', 'activity': 4},
            {'hour': '17:00', 'activity': 3},
            {'hour': '18:00', 'activity': 3},
            {'hour': '19:00', 'activity': 3},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 2},
            {'hour': '23:00', 'activity': 1},
        ],
    },
]

VISITOR_ACTIVITY_TREND_RESPONSE = {
    'data': VISITOR_ACTIVITY_TREND_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(VISITOR_ACTIVITY_TREND_DATA),
        'returned_items': len(VISITOR_ACTIVITY_TREND_DATA),
        'total_items': len(VISITOR_ACTIVITY_TREND_DATA),
    },
}


USER_ACTIVITY_TREND_DATA = [
    {
        'date': '2024-07-01',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 1},
            {'hour': '01:00', 'activity': 1},
            {'hour': '02:00', 'activity': 1},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 1},
            {'hour': '05:00', 'activity': 2},
            {'hour': '06:00', 'activity': 2},
            {'hour': '07:00', 'activity': 3},
            {'hour': '08:00', 'activity': 3},
            {'hour': '09:00', 'activity': 4},
            {'hour': '10:00', 'activity': 5},
            {'hour': '11:00', 'activity': 5},
            {'hour': '12:00', 'activity': 4},
            {'hour': '13:00', 'activity': 4},
            {'hour': '14:00', 'activity': 4},
            {'hour': '15:00', 'activity': 4},
            {'hour': '16:00', 'activity': 3},
            {'hour': '17:00', 'activity': 3},
            {'hour': '18:00', 'activity': 3},
            {'hour': '19:00', 'activity': 2},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 1},
            {'hour': '23:00', 'activity': 1},
        ],
    },
    {
        'date': '2024-07-02',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 1},
            {'hour': '01:00', 'activity': 1},
            {'hour': '02:00', 'activity': 1},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 1},
            {'hour': '05:00', 'activity': 1},
            {'hour': '06:00', 'activity': 2},
            {'hour': '07:00', 'activity': 2},
            {'hour': '08:00', 'activity': 3},
            {'hour': '09:00', 'activity': 4},
            {'hour': '10:00', 'activity': 4},
            {'hour': '11:00', 'activity': 5},
            {'hour': '12:00', 'activity': 5},
            {'hour': '13:00', 'activity': 4},
            {'hour': '14:00', 'activity': 4},
            {'hour': '15:00', 'activity': 3},
            {'hour': '16:00', 'activity': 3},
            {'hour': '17:00', 'activity': 3},
            {'hour': '18:00', 'activity': 2},
            {'hour': '19:00', 'activity': 2},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 1},
            {'hour': '23:00', 'activity': 1},
        ],
    },
    {
        'date': '2024-07-03',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 1},
            {'hour': '01:00', 'activity': 1},
            {'hour': '02:00', 'activity': 1},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 1},
            {'hour': '05:00', 'activity': 2},
            {'hour': '06:00', 'activity': 2},
            {'hour': '07:00', 'activity': 2},
            {'hour': '08:00', 'activity': 3},
            {'hour': '09:00', 'activity': 3},
            {'hour': '10:00', 'activity': 4},
            {'hour': '11:00', 'activity': 4},
            {'hour': '12:00', 'activity': 4},
            {'hour': '13:00', 'activity': 4},
            {'hour': '14:00', 'activity': 3},
            {'hour': '15:00', 'activity': 3},
            {'hour': '16:00', 'activity': 3},
            {'hour': '17:00', 'activity': 3},
            {'hour': '18:00', 'activity': 2},
            {'hour': '19:00', 'activity': 2},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 1},
            {'hour': '23:00', 'activity': 1},
        ],
    },
    {
        'date': '2024-07-04',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 1},
            {'hour': '01:00', 'activity': 1},
            {'hour': '02:00', 'activity': 1},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 1},
            {'hour': '05:00', 'activity': 2},
            {'hour': '06:00', 'activity': 2},
            {'hour': '07:00', 'activity': 3},
            {'hour': '08:00', 'activity': 3},
            {'hour': '09:00', 'activity': 4},
            {'hour': '10:00', 'activity': 4},
            {'hour': '11:00', 'activity': 4},
            {'hour': '12:00', 'activity': 4},
            {'hour': '13:00', 'activity': 4},
            {'hour': '14:00', 'activity': 3},
            {'hour': '15:00', 'activity': 3},
            {'hour': '16:00', 'activity': 3},
            {'hour': '17:00', 'activity': 3},
            {'hour': '18:00', 'activity': 2},
            {'hour': '19:00', 'activity': 2},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 1},
            {'hour': '23:00', 'activity': 1},
        ],
    },
    {
        'date': '2024-07-05',
        'hourly_activity': [
            {'hour': '00:00', 'activity': 1},
            {'hour': '01:00', 'activity': 1},
            {'hour': '02:00', 'activity': 1},
            {'hour': '03:00', 'activity': 1},
            {'hour': '04:00', 'activity': 1},
            {'hour': '05:00', 'activity': 2},
            {'hour': '06:00', 'activity': 2},
            {'hour': '07:00', 'activity': 3},
            {'hour': '08:00', 'activity': 3},
            {'hour': '09:00', 'activity': 4},
            {'hour': '10:00', 'activity': 4},
            {'hour': '11:00', 'activity': 4},
            {'hour': '12:00', 'activity': 4},
            {'hour': '13:00', 'activity': 4},
            {'hour': '14:00', 'activity': 3},
            {'hour': '15:00', 'activity': 3},
            {'hour': '16:00', 'activity': 3},
            {'hour': '17:00', 'activity': 2},
            {'hour': '18:00', 'activity': 2},
            {'hour': '19:00', 'activity': 2},
            {'hour': '20:00', 'activity': 2},
            {'hour': '21:00', 'activity': 2},
            {'hour': '22:00', 'activity': 1},
            {'hour': '23:00', 'activity': 1},
        ],
    },
]

USER_ACTIVITY_TREND_RESPONSE = {
    'data': USER_ACTIVITY_TREND_DATA,
    'message': None,
    'pagination': {
        'page': 1,
        'page_size': len(USER_ACTIVITY_TREND_DATA),
        'returned_items': len(USER_ACTIVITY_TREND_DATA),
        'total_items': len(USER_ACTIVITY_TREND_DATA),
    },
}
