'use client'
import { useState } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table'
import TablePageHeader from '@/components/tablePageHeader'
import RightSidePanel from '@/components/rightSidePanel'
import Modal from '@/components/modal'
import DeleteModal from '@/components/deleteModal'
import StatusText from '@/components/statusText'

import { copy } from '@/helpers'
import useCollection from '@/hooks/useCollection'
import useRequest from '@/hooks/useRequest'
import useQueryParams from '@/hooks/useQueryParams'
import useToggle from '@/hooks/useToggle'
import { useForm } from '@/hooks/useForm'

const commissionColumns = [
    {
        "id": 1,
        "s_no": 1,
        "commission_rate": 20
    }
]

const initialCommissionData = {
    commission_rate: '',
}

export default function Commission() {
    const { request } = useRequest()
    const [queryParams, setQueryParam] = useQueryParams()
    const [commissionCollection, updateCommissionCollection] = useCollection('admin/commission', null, commissionColumns)

    const [columns, setColumns] = useState([
        {
            name: 'S No.',
            id: 's_no',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type-name'>{row?.s_no || '--'}</div>,
        },
        {
            name: 'Commission Rate',
            id: 'commission_rate',
            visible: true,
            sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => (
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div className='data-type-name'>{row?.commission_rate || '--'}</div>
                </div>
            ),
        },
             {
            name: '',
            id: 'action',
            visible: true,
            // sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => <div className='action'>
                <div className='action-button'>
                    <button
                        onClick={(e) => {
                            e.stopPropagation()
                            setViewMode('edit')
                            toggleRightSidePanel()
                            setClickedSellerIndex(index)
                            setActiveTab('basic_details')
                            setUpdateSellersData({
                                name: row.name,
                                email: row.email,
                                phone: row?.company_details?.phone,
                                company_name: row?.company_details?.name,
                                total_disputes: row.total_disputes,
                                status: row.status,
                                company_registration_no: row?.company_details?.registration_number,
                                address: '123 Rosewood Lane Bristol BS1 4XY United Kingdom',
                                place: 'Cambridge',
                                pincode: 'EC4N 6AF',
                                company_website: 'https://www.testcompany.co.uk',
                                business_category: 'Retail & E-commerce',
                                business_sub_category: 'Online Marketplace',
                                company_phone: row?.company_details?.phone,
                                company_position: 'CEO (Chief Executive Officer)',
                                icno_no: row?.company_details?.ico_number,
                                status: row?.status,
                                city: 'Cambridge',
                                country: 'United Kingdom',
                            })
                        }}
                        className='edit-icon-wrapper'
                    >
                        <img
                            className='edit-icon'
                            src='/edit-icon.svg'
                        />
                    </button>
                </div>
            </div>
        },
    ])

    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDeleteModal, toggleDeleteModal] = useToggle()

    const [clickedCommissionIndex, setClickedCommissionIndex] = useState()
    const [commissionIndex, setCommissionIndex] = useState()
    const [commissionDetails, setCommissionDetails] = useState()
    const [viewMode, setViewMode] = useState()

    const [deleteModalTitle, setDeleteModalTitle] = useState()
    const [deleteModalDescription, setDeleteModalDescription] = useState()
    const [deleteBtn, setDeleteBtn] = useState()
    const [commissionToDelete, setCommissionToDelete] = useState()

    const [message, setMessage] = useState([])

    const [
        addCommissionData,
        setAddCommissionData,
        onAddCommissionDataInputChange,
        addCommissionDataErrors,
        setAddCommissionDataErrorsMap,
        addCommissionDataErrorMessage,
        setAddCommissionDataErrorMessage,
    ] = useForm(copy(initialCommissionData))

    const [
        updateCommissionData,
        setUpdateCommissionData,
        onUpdateCommissionDataInputChange,
        updateCommissionDataErrors,
        setUpdateCommissionDataErrorsMap,
        updateCommissionDataErrorMessage,
        setUpdateCommissionDataErrorMessage,
    ] = useForm(copy(initialCommissionData))

    const handleSearch = (qString, updateCollection) => {
        setQueryParam('q', qString)
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            searchParams.set('q', qString)
            return { searchParams }
        })
    }

    const showMessage = (status, text) => {
        const id = Date.now()
        setMessage(prev => [...prev, { id, status, text }])
        setTimeout(() => {
            setMessage(prev => prev.filter(item => item.id !== id))
        }, 5000)
    }

    const handleUpdate = async e => {
        e.preventDefault()
        let requestData = copy(updateCommissionData)
        try {
            await request.patch(`commission/${commissionCollection.items[clickedCommissionIndex].id}`, requestData)
            updateCommissionCollection({ reload: true })
            setUpdateCommissionData(copy(initialCommissionData))
            toggleRightSidePanel()
            showMessage('success', 'Commission updated successfully!')
        } catch (err) {
            showMessage('error', 'Failed to update commission')
        }
    }

    function handleNextButton() {
        const newIndex = commissionIndex + 1
        setCommissionIndex(newIndex)
        setCommissionDetails(commissionCollection?.items[newIndex])
    }

    function handlePrevButton() {
        const newIndex = commissionIndex - 1
        setCommissionIndex(newIndex)
        setCommissionDetails(commissionCollection?.items[newIndex])
    }

    return (
        <div className='page-container'>
            <StatusText text={message} />
            <>
                <div className='left-container'>
                    <Menubar />
                </div>
                <div className='main-content'>
                    <Header title='Settings' />
                    <div className='main-content-body'>
                        <div className='table-wrapper'>
                            <TablePageHeader
                                title='Commission Percentage'
                                onSearch={handleSearch}
                                onAddClick={null}
                                onExportClick={null}
                                buttonText=''
                                toggleRightSidePanel={toggleRightSidePanel}
                                setViewMode={setViewMode}
                            />
                            <div className='table-container'>
                                <Table
                                    className='category-table'
                                    items={commissionCollection.items}
                                    columns={columns}
                                    controlColumns={[]}
                                    loaded={commissionCollection.loaded}
                                    searchParams={commissionCollection.searchParams}
                                    collection={commissionCollection}
                                    updateCollection={updateCommissionCollection}
                                    selectedIndex={commissionIndex}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </>

            {showRightSidePanel && (
                <div
                    className='overlay'
                    onClick={() => {
                        toggleRightSidePanel()
                        setCommissionIndex(null)
                    }}
                >
                    <RightSidePanel
                        viewMode={viewMode}
                        title={
                            viewMode === 'view'
                                ? 'Commission Information'
                                : viewMode === 'edit'
                                    ? 'Edit Commission'
                                    : viewMode === 'add'
                                        ? 'Add Commission'
                                        : ''
                        }
                        details={commissionDetails}
                        setDetails={setCommissionDetails}
                        buttonOneFunction={
                            viewMode === 'view'
                                ? handlePrevButton
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? toggleRightSidePanel
                                    : null
                        }
                        buttonTwoFunction={
                            viewMode === 'view'
                                ? handleNextButton
                                : viewMode === 'edit'
                                    ? handleUpdate
                                    : viewMode === 'add'
                                        ? null
                                        : null
                        }
                        buttonNameOne='without-bg-btn'
                        buttonNameTwo='with-bg-btn'
                        buttonTextOne={
                            viewMode === 'view'
                                ? 'Previous'
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? 'Cancel'
                                    : ''
                        }
                        buttonTextTwo={
                            viewMode === 'view'
                                ? 'Next'
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Save'
                                        : ''
                        }
                        toggleRightSidePanel={toggleRightSidePanel}
                        buttonIconLeft='/arrow-left.svg'
                        buttonIconRight='/arrow-right.svg'
                        setIndex={setCommissionIndex}
                        index={commissionIndex}
                        collection={commissionCollection}
                        updateData={
                            viewMode === 'edit'
                                ? updateCommissionData
                                : viewMode === 'add'
                                    ? addCommissionData
                                    : ''
                        }
                        updateOnChange={
                            viewMode === 'edit'
                                ? onUpdateCommissionDataInputChange
                                : viewMode === 'add'
                                    ? onAddCommissionDataInputChange
                                    : ''
                        }
                        handleUpdate={handleUpdate}
                        onAddDataInputChange={onAddCommissionDataInputChange}
                        addData={addCommissionData}
                        setUpdateData={
                            viewMode === 'edit'
                                ? setUpdateCommissionData
                                : viewMode === 'add'
                                    ? setAddCommissionData
                                    : ''
                        }
                        page='commission'
                    />
                </div>
            )}

            {showDeleteModal && (
                <Modal title={deleteModalTitle} toggleModal={toggleDeleteModal}>
                    <DeleteModal
                        toggleDeleteModal={toggleDeleteModal}
                        handleDelete={() => {}}
                        buyerByCompanyId={commissionToDelete}
                        text={deleteModalDescription}
                        deleteBtn={deleteBtn}
                    />
                </Modal>
            )}
        </div>
    )
}
