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

import { formatDateTime, getCollectionSearchParamsFromPage, replaceUnderScoreWithSpace } from '@/helpers'
import { copy, shortenText } from '@/helpers'
import useRequest from '@/hooks/useRequest'
import Stats from '@/components/stats'

import '@/css/pages/billing.css'
import Tabs from '@/components/tabs'
import { Checkbox } from '@/components/form'

const stats = [
    {
        mainLabel: 'Data Sales',
        mainValue: '£1,236,890',
        subLabel: 'Orders',
        subValue: '3,211',
        isActive: true
    },
    {
        mainLabel: 'Lead Sales',
        mainValue: '£1,741,635',
        subLabel: 'Orders',
        subValue: '1,840',
        isActive: true
    },
    {
        mainLabel: 'KYC Sales',
        mainValue: '£218,400',
        subLabel: 'Checks',
        subValue: '218,400',
        isActive: true
    },
    {
        mainLabel: 'Ad Sales',
        mainValue: '£846,350',
        subLabel: 'Campaigns',
        subValue: '346',
        isActive: true
    },
]

export default function Billing() {

    const { request } = useRequest()

    const [url, setUrl] = useState('admin/transactions')

    const [transactionC, updateTransactionC] = useCollection(url, getCollectionSearchParamsFromPage())

    // Pass values to the main table
    const [tdsColumns, setTdsColumns] = useState([
        {
            name: '',
            id: 's_no',
            visible: true,
            // sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => {
                const isSelected = row._selected || false;
                return <div className='checkbox'>
                    <div className='checkbox' onClick={(e) => e.stopPropagation()}>
                        <Checkbox
                            checked={isSelected}
                            onChange={(e) => {
                                e.stopPropagation();
                                const checked = e.target.checked;
                                
                                if (updateCollection) {
                                    updateCollection(old => {
                                        const newItems = old.items.map((item, idx) => {
                                            if (idx === index) {
                                                return { ...item, _selected: checked };
                                            }
                                            return item;
                                        });
                                        return { ...old, items: newItems };
                                    });
                                }
                                
                                // Clear selectedIndex when unchecking to remove grey background
                                if (!checked) {
                                    if (transactionIndex === index) {
                                        setTransactionIndex(null);
                                    }
                                }
                            }}
                        />
                    </div>
                </div>
            }
        },
        {
            name: 'Transaction On',
            id: 'transaction_date',
            visible: true,
            sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => <div className='s-no'>
                <div className='transaction-date'>
                    {shortenText(formatDateTime(row.transaction_date))}
                </div>
            </div>
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
                {shortenText(row.product_details.name)}
            </div>
        },
        {
            name: 'Buyer',
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
                {shortenText(replaceUnderScoreWithSpace(row?.status))}
            </div>
        },
        {
            name: 'Action',
            id: 'action',
            visible: true,
            sortable: 'backend',
            render: row => <button
                className='link-like-button'
            >
               <img src='/download-icon.svg' />
               <span>Download Invoice</span>
            </button>
        },

    ])


    // Pass values to the main table
    const [ddColumns, setDdColumns] = useState([
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

    // Pass values to the main table
    const [addColumns, setAddColumns] = useState([
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

        // Right side panel tab label and key
    const [tabs, setTabs] = useState({
        'view': {
            'tds': {
                label: 'TDS'
            },
            'dd_portal': {
                label: 'DD Portal'
            },
            'add_portal': {
                label: 'Ad Portal'
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
            value: transactionDetails?.id_transaction || 'N/A'
        },
        {
            property: 'product',
            displayKey: 'Product',
            value: transactionDetails?.product_details?.name || 'N/A'
        },
        {
            property: 'buyer',
            displayKey: 'Buyer',
            value: (
                <Link href='/buyers' className='link-like-button'>
                    {transactionDetails?.buyer_details?.name || 'N/A'}
                    {transactionDetails?.buyer_details?.company_name && ` - ${transactionDetails.buyer_details.company_name}`}
                </Link>
            )
        },
        {
            property: 'seller',
            displayKey: 'Seller',
            value: (
                <Link href='/seller' className='link-like-button'>
                    {transactionDetails?.seller_details?.company_name || transactionDetails?.seller_details?.name || 'N/A'}
                    {transactionDetails?.seller_details?.name && transactionDetails?.seller_details?.company_name && ` - ${transactionDetails.seller_details.name}`}
                </Link>
            )
        },
        {
            property: 'sale_price',
            displayKey: 'Sale Price',
            value: transactionDetails?.sale_price 
                ? `£${transactionDetails.sale_price}${transactionDetails?.sale_price_vat ? ` + VAT (£${transactionDetails.sale_price_vat})` : ''}`
                : 'N/A'
        },
        {
            property: 'tds_fee',
            displayKey: 'TDS Fee',
            value: transactionDetails?.tds_fee 
                ? `£${transactionDetails.tds_fee}${transactionDetails?.tds_fee_vat ? ` + VAT (£${transactionDetails.tds_fee_vat})` : ''}`
                : 'N/A'
        },
        {
            property: 'paypal_fee',
            displayKey: 'Paypal Fee',
            value: transactionDetails?.paypal_fee ? `£${transactionDetails.paypal_fee}` : 'N/A'
        },
        {
            property: 'net_payable',
            displayKey: 'Net Payable',
            value: transactionDetails?.net_payable ? `£${transactionDetails.net_payable}` : 'N/A'
        },
        {
            property: 'remaining_vat',
            displayKey: 'Remaining VAT',
            value: transactionDetails?.remaining_vat ? `£${transactionDetails.remaining_vat}` : 'N/A'
        },
        {
            property: 'total_payable',
            displayKey: 'Total Payable',
            value: transactionDetails?.total_payable ? `£${transactionDetails.total_payable}` : 'N/A'
        },
        {
            property: 'payable_date',
            displayKey: 'Payable Date',
            value: transactionDetails?.payable_date 
                ? formatDateTime(transactionDetails.payable_date) 
                : 'N/A'
        },
        {
            property: 'status',
            displayKey: 'Status',
            value: (
                <div
                    className={`status-main ${transactionDetails?.status === 'ACTIVE' || transactionDetails?.status === 'COMPLETED'
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
                    {transactionDetails?.status === 'PENDING' ? 'Pending' : 
                     transactionDetails?.status === 'COMPLETED' ? 'Completed' :
                     transactionDetails?.status || 'N/A'}
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

    const [activeTab, setActiveTab] = useState('tds')

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
                    title='Billing'
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
                            // toggleFilterModal={toggleFilterModal}
                            onAddClick={true}
                            onExportClick={null}
                            // moreOptionVisible
                            buttonText='View Offensive Words'
                            toggleRightSidePanel={toggleRightSidePanel}
                            setViewMode={setViewMode}
                        />
                        <div className='table-container'>
                            <Table
                                className='category-table'
                                items={transactionC.items}
                                columns={activeTab === 'tds' ? tdsColumns : activeTab === 'dd_portal' ? ddColumns : addColumns}
                                controlColumns={[]}
                                loaded={transactionC.loaded}
                                searchParams={transactionC.searchParams}
                                collection={transactionC}
                                onRowClick={onRowClick}
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