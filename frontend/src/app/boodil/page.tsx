'use client'
import { useState, useRef } from 'react'
import Link from 'next/link'


import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table/index'
import TablePageHeader from '@/components/tablePageHeader'
import RightSidePanel from '@/components/rightSidePanel'

import useCollection from '@/hooks/useCollection'
import useQueryParams from '@/hooks/useQueryParams'
import useToggle from '@/hooks/useToggle'
import { useForm } from '@/hooks/useForm'

import { formatDateTime, getCollectionSearchParamsFromPage } from '@/helpers'
import { copy } from '@/helpers'
import useRequest from '@/hooks/useRequest'
import Stats from '@/components/stats'

import '@/css/pages/paypal.css'

const stats = [
    {
        mainLabel: 'Completed Payments',
        mainValue: '32',
        isActive: true
    },
    {
        mainLabel: 'Total Billed',
        mainValue: '€22,450',
        isActive: true

    },
    {
        mainLabel: 'Pending Invoices',
        mainValue: '6',
        isActive: true

    },
    {
        mainLabel: 'Disputed',
        mainValue: '3',
        isActive: true
    },
    {
        mainLabel: 'Other',
        mainValue: '$1,236,890',
        subLabel: 'Campaigns',
        subValue: '3,22',
        isActive: false
    },
    {
        mainLabel: 'Other',
        mainValue: '$1,236,890',
        subLabel: 'Campaigns',
        subValue: '3,22',
        isActive: false
    },
    {
        mainLabel: 'Other',
        mainValue: '$1,236,890',
        subLabel: 'Campaigns',
        subValue: '3,22',
        isActive: false
    },
    {
        mainLabel: 'Other',
        mainValue: '$1,236,890',
        subLabel: 'Campaigns',
        subValue: '3,22',
        isActive: false
    },
]

export default function Boodil() {

    const { request } = useRequest()

    const [transactionC, updateTransactionC] = useCollection('admin/transactions', getCollectionSearchParamsFromPage())

    // Pass values to the main table
    const [columns, setColumns] = useState([
        {
            name: 'Transaction On',
            id: 'transaction_date',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>{formatDateTime(row.transaction_date)}</div>
        },
        {
            name: 'Transaction ID',
            id: 'id_transaction',
            visible: true,
            sortable: 'backend',
            render: row => <div className='transaction-id'>{row.id_transaction}</div>
        },
        {
            name: 'Order ID',
            id: 'id_order',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-name-and-img'>
                <div className='name'>
                    {row.id_order}
                </div>
            </div>
        },
        {
            name: 'Product',
            id: 'product_details',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.product_details.name}
            </div>
        },
        {
            name: 'Buyer',
            id: 'buyer_details',
            visible: true,
            sortable: 'backend',
            render: row => <div className='buyer-details'>
                <div className='name'>
                    {row?.buyer_details?.name}
                </div>
                <div className='company'>
                    {row?.product_details.data_source_name}
                </div>
            </div>
        },
        {
            name: 'Price',
            id: 'sale_price',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                €{row.sale_price}
            </div>
        },
        {
            name: 'Status',
            id: 'status',
            visible: true,
            sortable: 'backend',
            render: row => <div
                className={`status-main ${row?.status === 'ACTIVE'
                    ? 'green'
                    : row?.status === 'PENDING'
                        ? 'yellow'
                        : row?.status === 'HIDDEN'
                            ? 'grey'
                            : row?.status === 'FLAGGED'
                                ? 'red'
                                : ''
                    }`}
            >
                {row?.status}
            </div>
        },

    ])

    const [queryParams, setQueryParam] = useQueryParams()

    const [showFilterModal, toggleFilterModal] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDropDown, toggleDropDown] = useToggle()

    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [transactionIndex, setTransactionIndex] = useState()

    // Store the clicked buyer from table row click
    const [transactionDetails, setTransactionDetail] = useState()

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()


    const reviewDetailsKeyValue = [
        {
            property: 'product',
            displayKey: 'Product',
            value: (<Link href='' className='link-text'>
                {transactionDetails?.product_details?.name}
            </Link>)
        },
        {
            property: 'id_order',
            displayKey: 'Buyer',
            value: (<Link href='/buyers' className='link-text'>
                {transactionDetails?.buyer_details?.name}
            </Link>)
        },
        {
            property: 'id_buyer',
            displayKey: 'Seller',
            value: (<Link href='/seller' className='link-text'>
                {transactionDetails?.seller_details?.name}
            </Link> )
            
        },
        {
            property: 'is_recommended',
            displayKey: 'Sale Price',
            value: `€${transactionDetails?.sale_price}`
        },
        {
            property: 'reported_count',
            displayKey: 'TDS Fee',
            value: `€${transactionDetails?.tds_fee}`
        },
        {
            property: 'accuracy_rating',
            displayKey: 'Net Payable',
            value: `€${transactionDetails?.net_payable}`
        },
        {
            property: 'receptivity_rating',
            displayKey: 'Remaining VAT',
            value: `€${transactionDetails?.remaining_vat}`
        },
        {
            property: 'contact_rate_rating',
            displayKey: 'Total Payable',
            value: `€${transactionDetails?.total_payable}`
        },
        {
            property: 'overall_rating',
            displayKey: 'Payable',
            value: formatDateTime(transactionDetails?.payable_date)
        },
        {
            property: 'status',
            displayKey: 'Status',
            value: (
                <div
                    className={`status-main ${transactionDetails?.status === 'ACTIVE'
                        ? 'green'
                        : transactionDetails?.status === 'PENDING'
                            ? 'yellow'
                            : transactionDetails?.status === 'HIDDEN'
                                ? 'grey'
                                : transactionDetails?.status === 'FLAGGED'
                                    ? 'red'
                                    : ''
                        }`}
                >
                    {transactionDetails?.status}
                </div>
            )
        },
    ]

    const handleSearch = qString => {
        setQueryParam('q', qString)

        updateTransactionC(old => {
            console.log('old', old)
            let searchParams = new URLSearchParams(old.searchParams)
            console.log('SeatchParams', searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }


    // On table row click get the row index 
    // and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()

        toggleRightSidePanel()
        setTransactionIndex(index)
        setTransactionDetail(transactionC.items[index])
        setViewMode('view')
    }

    function handleNextButton() {
        const newIndex = transactionIndex + 1
        setTransactionIndex(newIndex)
        setTransactionDetail(transactionC?.items[newIndex])

    }

    function handlePrevButton() {
        const newIndex = transactionIndex - 1
        setTransactionIndex(newIndex)
        setTransactionDetail(transactionC?.items[newIndex])
    }

    // Clicked Transaction Index
    const [clickedTransactionIndex, setClickedTransactionIndex] = useState()

    return <div className='page-container'>
        <>
            <div className='left-container'>
                <Menubar
                />
            </div>
            <div className='main-content'>
                <Header
                    title='Boodil'
                />
                <div className='main-content-body'>

                </div>
            </div>
        </>
    </div>
}