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
import useFilter from '@/hooks/useFilter'
import { useForm } from '@/hooks/useForm'

import { formatDateTime, getCollectionSearchParamsFromPage, replaceUnderScoreWithSpace } from '@/helpers'
import { copy, shortenText } from '@/helpers'
import useRequest from '@/hooks/useRequest'
import Stats from '@/components/stats'

import '@/css/pages/billing.css'
import Tabs from '@/components/tabs'

const quickFilter = [
    {
        label: 'Pending buyers',
        key: 'PENDING',
        isActive: true
    },
    {
        label: 'Rejected/Blocked buyers',
        key: 'INACTIVE',
        isActive: false
    },
    {
        label: 'Dispute raised buyers',
        key: 'NOT_VERIFIED',
        isActive: false
    },
    {
        label: 'Newly signed-up buyers',
        key: 'ACTIVE',
        isActive: true
    },
]

const initialFilterData = {
    f_user_status: {
        operator: 'equals',
        value: '',
        type: 'checkbox'
    }
}

const stats = [
    {
        mainLabel: 'Active Buyers',
        mainValue: '267',
        subLabel: 'Pending',
        subValue: '14',
        isActive: true
    },
    {
        mainLabel: 'Total Orders',
        mainValue: '792',
        subLabel: 'Data / Live Lead',
        subValue: '445 / 347',
        isActive: true
    },
    {
        mainLabel: 'Total Disputes',
        mainValue: '159',
        subLabel: 'Refunds / Chargebacks',
        subValue: '42 / 7',
        isActive: true
    },
    {
        mainLabel: 'Avg. Leads Purchased per Order',
        mainValue: '1,220',
        isActive: true
    },
]

export default function ReportBuyer() {

    const { request } = useRequest()

    const [url, setUrl] = useState('admin/transactions')

    const [transactionC, updateTransactionC] = useCollection(url, getCollectionSearchParamsFromPage())

    // Pass Filter params to the url
    const [
        currentFilterData,
        filterEnabled,
        getFilterSearchParams,
        onFilterInputChange,
        applyFilter,
        clearFilter,
        setFilterData
    ] = useFilter(initialFilterData, updateTransactionC)

    // Pass values to the main table
    const [topBuyersColumns, setTopBuyersColumns] = useState([
        {
            name: 'Signed up on',
            id: 'transaction_date',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>
                <div className='signed-up'>
                    {shortenText(formatDateTime(row.transaction_date))}
                </div>
            </div>
        },
        {
            name: 'Buyer ID',
            id: 'id_transaction',
            visible: true,
            sortable: 'backend',
            render: row => <div className='transaction-id'>{row.id_transaction}</div>
        },
        {
            name: 'User Name',
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
            name: 'Leads Orders',  
            id: 'product_details',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {shortenText(row.product_details.name)}
            </div>
        },
        {
            name: 'Product Orders',
            id: 'buyer_details',
            visible: true,
            sortable: 'backend',
            render: row => <div className='buyer-details'>
                <div className='name'>
                    {shortenText(row?.buyer_details?.name)}
                </div>
                <div className='company'>
                    {shortenText(row?.product_details.data_source_name)}
                </div>
            </div>
        },
        {
            name: 'Total Spent',
            id: 'sale_price',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                €{row.sale_price}
            </div>
        },
    ])


    // Pass values to the main table
    const [disputesColumns, setDisputesColumns] = useState([
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

    // Pass values to the main table - Purchase Activity
    const [purchaseActivityColumns, setPurchaseActivityColumns] = useState([
        {
            name: 'Activity Date',
            id: 'transaction_date',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>{formatDateTime(row.transaction_date)}</div>
        },
        {
            name: 'Activity ID',
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
                {row.product_details?.name}
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
                    {row?.product_details?.data_source_name}
                </div>
            </div>
        },
        {
            name: 'Purchase Amount',
            id: 'sale_price',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                €{row.sale_price}
            </div>
        },
        {
            name: 'Activity Status',
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
                {row?.status || 'N/A'}
            </div>
        },
    ])

    // Pass values to the main table - Review Activity
    const [reviewActivityColumns, setReviewActivityColumns] = useState([
        {
            name: 'Review Date',
            id: 'transaction_date',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>
                {formatDateTime(row.transaction_date)}
            </div>
        },
        {
            name: 'Review ID',
            id: 'id_transaction',
            visible: true,
            sortable: 'backend',
            render: row => <div className='transaction-id'>{row.id_transaction}</div>
        },
        {
            name: 'Buyer Name',
            id: 'buyer_details',
            visible: true,
            sortable: 'backend',
            render: row => <div className='buyer-details'>
                <div className='name'>
                    {row?.buyer_details?.name}
                </div>
            </div>
        },
        {
            name: 'Product',
            id: 'product_details',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.product_details?.name}
            </div>
        },
        {
            name: 'Rating',
            id: 'rating',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.rating || 'N/A'}
            </div>
        },
        {
            name: 'Review Status',
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
                {row?.status || 'N/A'}
            </div>
        },
    ])

    // Pass values to the main table - Purchase Breakdown
    const [purchaseBreakdownColumns, setPurchaseBreakdownColumns] = useState([
        {
            name: 'Purchase Date',
            id: 'transaction_date',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>
                {formatDateTime(row.transaction_date)}
            </div>
        },
        {
            name: 'Purchase ID',
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
            name: 'Product Name',
            id: 'product_details',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.product_details?.name}
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
                    {row?.product_details?.data_source_name}
                </div>
            </div>
        },
        {
            name: 'Amount',
            id: 'sale_price',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                €{row.sale_price}
            </div>
        },
        {
            name: 'Quantity',
            id: 'quantity',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.quantity || 'N/A'}
            </div>
        },
    ])

    const [queryParams, setQueryParam] = useQueryParams()

    const [showFilterModal, toggleFilterModal] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDropDown, toggleDropDown] = useToggle()
    const [showFilterDropList, toggleFilterDropList] = useToggle()
    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [transactionIndex, setTransactionIndex] = useState()

    // Store the clicked buyer from table row click
    const [transactionDetails, setTransactionDetail] = useState()

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

        // Right side panel tab label and key
    const [tabs, setTabs] = useState({
        'view': {
            'top_buyers': {
                label: 'Top Buyers'
            },
            'disputes': {
                label: 'Disputes'
            },
            'purchase_activity': {
                label: 'Purchase Activity'
            },
            'review_activity': {
                label: 'Review Activity'
            },
            'purchase_breakdown': {
                label: 'Purchase Breakdown'
            },
        },
        'edit': {
            // No tabs for edit mode
        }
    })

    const reviewDetailsKeyValue = [
        {
            property: 'transaction_id',
            displayKey: 'Transaction ID',
            value: (<div href='' className='link-text'>
                {transactionDetails?.product_details?.name}
            </div>)
        },
        {
            property: 'product',
            displayKey: 'Product',
            value: (<Link href='/buyers' className='link-text'>
                {transactionDetails?.buyer_details?.name}
            </Link>)
        },
        {
            property: 'buyer',
            displayKey: 'Buyer',
            value: (<Link href='/seller' className='link-text'>
                {transactionDetails?.seller_details?.name}
            </Link> )
            
        },
        {
            property: 'seller',
            displayKey: 'Seller',
            value: `€${transactionDetails?.sale_price}`
        },
        {
            property: 'sale_price',
            displayKey: 'Sale Price',
            value: `€${transactionDetails?.tds_fee}`
        },
        {
            property: 'TDS Fee',
            displayKey: 'tds_fee',
            value: `€${transactionDetails?.net_payable}`
        },
        {
            property: 'paypal_fee',
            displayKey: 'Paypal Fee',
            value: `€${transactionDetails?.remaining_vat}`
        },
        {
            property: 'net_payable',
            displayKey: 'Net Payable',
            value: `€${transactionDetails?.total_payable}`
        },
        {
            property: 'remaining_vat',
            displayKey: 'Remaining VAT',
            value: formatDateTime(transactionDetails?.payable_date)
        },
        {
            property: 'total_payable',
            displayKey: 'Total Payable',
            value: formatDateTime(transactionDetails?.payable_date)
        },  
        {
            property: 'payable_date',
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

    const handleSearch = (qString, updateCollection) => {
        setQueryParam('q', qString)
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }

    // Filter functionality
    const handleFilter = (key, value, updateCollection, checked) => {
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            if (checked) {
                searchParams.set(key, value)
            } else {
                searchParams.delete(key)
            }

            return { searchParams }
        })
    }


    // On table row click get the row index 
    // and return that particular item
    // const onRowClick = (e, index) => {
    //     e.stopPropagation()

    //     toggleRightSidePanel()
    //     setTransactionIndex(index)
    //     setTransactionDetail(transactionC.items[index])
    //     setViewMode('view')
    // }

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

    const [activeTab, setActiveTab] = useState('top_buyers')

    // Clicked Transaction Index
    const [clickedTransactionIndex, setClickedTransactionIndex] = useState()

    console.log(activeTab, 'activeTab')
    return <div className='page-container'>
        <>
            <div className='left-container'>
                <Menubar
                />
            </div>
            <div className='main-content'>
                <Header
                    title='Report'
                />
                <div className='main-content-body'>
                    <Stats
                        title='Stats'
                        statValues={stats}
                        isDateDropList={false}
                        isDateInput={true}
                    />
                    <div className='table-wrapper'>
                        <div className='table-tabs'>
                            <Tabs
                                tabs={tabs['view']}
                                setTabs={setTabs}
                                activeTab={activeTab}
                                setActiveTab={setActiveTab}
                            />
                            <hr className='light-line'/>
                        </div>
                        <TablePageHeader
                            title={tabs['view'][activeTab].label}
                            onSearch={handleSearch}
                            toggleFilterDropList={toggleFilterDropList}
                            showFilterDropList={showFilterDropList}
                            onFilterInputChange={onFilterInputChange}
                            onAddClick={true}
                            onExportClick={null}
                            showActionButtons
                            buttonText='Export Users'
                            quickFilter={quickFilter}
                            currentFilterData={initialFilterData}
                            collection={transactionC}
                            applyFilter={applyFilter}
                            sliderFilter={handleFilter}
                            updateData={null}
                            updateCollection={updateTransactionC}
                        />
                        <div className='table-container'>
                            <Table
                                className='category-table'
                                items={transactionC.items}
                                columns={
                                    activeTab === 'top_buyers' ? topBuyersColumns :
                                    activeTab === 'disputes' ? disputesColumns :
                                    activeTab === 'purchase_activity' ? purchaseActivityColumns :
                                    activeTab === 'review_activity' ? reviewActivityColumns :
                                    activeTab === 'purchase_breakdown' ? purchaseBreakdownColumns :
                                    topBuyersColumns
                                }
                                controlColumns={[]}
                                loaded={transactionC.loaded}
                                searchParams={transactionC.searchParams}
                                collection={transactionC}
                                // onRowClick={onRowClick}
                                selectedIndex={transactionIndex}
                                updateCollection={updateTransactionC}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </>
        {/* Right Side Panel */}
        {showRightSidePanel &&
            <div
                className='overlay'
                onClick={() => {
                    toggleRightSidePanel()
                    setTransactionIndex(null)
                }}
            >
                <RightSidePanel
                    viewMode={viewMode}
                    title={
                        viewMode === 'add'
                            ? 'Offensive Words'
                            : viewMode === 'edit'
                                ? 'Edit Review'
                                : 'Transaction Details'
                    }
                    details={transactionDetails}
                    setDetails={setTransactionDetail}
                    labelValueData={reviewDetailsKeyValue}
                    buttonNameOne='without-bg-btn'
                    buttonNameTwo='with-bg-btn'
                    buttonTextOne={viewMode === 'view'
                        ? 'Previous Transaction'
                        : ''
                    }
                    buttonTextTwo={
                        viewMode === 'view'
                            ? 'Next Transaction'
                            : ''
                    }
                    buttonOneFunction={viewMode === 'view'
                        ? handlePrevButton
                        : ''
                    }
                    buttonTwoFunction={viewMode === 'view'
                        ? handleNextButton
                        : ''
                    }
                    toggleRightSidePanel={toggleRightSidePanel}
                    buttonIconLeft='/arrow-left.svg'
                    buttonIconRight='/arrow-right.svg'
                    onSearch={handleSearch}
                    setIndex={setTransactionIndex}
                    index={transactionIndex}
                    collection={transactionC}
                    viewDetailsBtn={true}
                    summaryView={false}
                    showDropDown={showDropDown}
                    toggleDropDown={toggleDropDown}
                    page='review'

                />
            </div>
        }

    </div>
}