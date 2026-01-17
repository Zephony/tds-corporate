'use client'
import { useState } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Stats from '@/components/stats'
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

const stats = [
    {
        mainLabel: 'Total Tags',
        mainValue: '28',
        subLabel: '',
        subValue: '',
        isActive: true
    },
    {
        mainLabel: 'Tags used in Email',
        mainValue: '19',
        subLabel: '',
        subValue: '',
        isActive: true
    },
    {
        mainLabel: 'Tags used in SMS',
        mainValue: '11',
        subLabel: '',
        subValue: '',
        isActive: true
    },
    {
        mainLabel: 'Unused Tags',
        mainValue: '2',
        subLabel: '',
        subValue: '',
        isActive: true
    },
]

const tagsColumns = [
    {
      "id": 1,
      "global_type": "company",
      "template": "email",
      "product_name": "Seller ID",
      "field": "seller_id",
      "description": "Company Seller ID Tag",
      "global_calculation": "$seller_id"
    },
    {
      "id": 2,
      "global_type": "company",
      "template": "email",
      "product_name": "Buyer ID",
      "field": "buyer_id",
      "description": "Company Buyer ID Tag",
      "global_calculation": "$buyer_id"
    },
    {
      "id": 3,
      "global_type": "company",
      "template": "email",
      "product_name": "Sold Date",
      "field": "sold_date",
      "description": "Product Sold Date",
      "global_calculation": "$sold_date"
    },
    {
      "id": 4,
      "global_type": "company",
      "template": "email",
      "product_name": "Invoice ID",
      "field": "invoice_id",
      "description": "Invoice ID tag",
      "global_calculation": "$invoice_id"
    },
    {
      "id": 5,
      "global_type": "company",
      "template": "email",
      "product_name": "Product ID",
      "field": "product_id",
      "description": "Product ID Tag",
      "global_calculation": "$product_id"
    },
    {
      "id": 6,
      "global_type": "company",
      "template": "email",
      "product_name": "Product Name",
      "field": "product_name",
      "description": "Product Name Tag",
      "global_calculation": "$product_name"
    }
  ]

const initialTagData = {
    global_type: '',
    template: '',
    product_name: '',
    field: '',
    description: '',
    global_calculation: '',
}

export default function Tags() {
    const { request } = useRequest()
    const [queryParams, setQueryParam] = useQueryParams()
    const [tagsCollection, updateTagsCollection] = useCollection('admin/tags', null, tagsColumns)

    const [columns, setColumns] = useState([
        {
            name: 'Global Type',
            id: 'global_type',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type-name'>{row?.global_type || '--'}</div>,
        },
        {
            name: 'Template',
            id: 'template',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type-name'>{row?.template || '--'}</div>,
        },
        {
            name: 'Product Name',
            id: 'product_name',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type-name'>{row?.product_name || '--'}</div>,
        },
        {
            name: 'Field',
            id: 'field',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type-name'>{row?.field || '--'}</div>,
        },
        {
            name: 'Description',
            id: 'description',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type-name'>{row?.description || '--'}</div>,
        },
        {
            name: 'Global Calculation',
            id: 'global_calculation',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type-name'>{row?.global_calculation || '--'}</div>,
        },

    ])

    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDeleteModal, toggleDeleteModal] = useToggle()

    const [clickedTagIndex, setClickedTagIndex] = useState()
    const [tagIndex, setTagIndex] = useState()
    const [tagDetails, setTagDetails] = useState()
    const [viewMode, setViewMode] = useState()

    const [deleteModalTitle, setDeleteModalTitle] = useState()
    const [deleteModalDescription, setDeleteModalDescription] = useState()
    const [deleteBtn, setDeleteBtn] = useState()
    const [tagToDelete, setTagToDelete] = useState()

    const [message, setMessage] = useState([])

    const [
        addTagData,
        setAddTagData,
        onAddTagDataInputChange,
        addTagDataErrors,
        setAddTagDataErrorsMap,
        addTagDataErrorMessage,
        setAddTagDataErrorMessage,
    ] = useForm(copy(initialTagData))

    const [
        updateTagData,
        setUpdateTagData,
        onUpdateTagDataInputChange,
        updateTagDataErrors,
        setUpdateTagDataErrorsMap,
        updateTagDataErrorMessage,
        setUpdateTagDataErrorMessage,
    ] = useForm(copy(initialTagData))

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

    const handleAdd = async e => {
        e.preventDefault()
        let requestData = copy(addTagData)
        try {
            await request.post('tags', requestData)
            updateTagsCollection({ reload: true })
            setAddTagData(copy(initialTagData))
            toggleRightSidePanel()
            showMessage('success', 'Tag created successfully.')
        } catch (err) {
            showMessage('error', 'Failed to create tag.')
        }
    }

    const handleUpdate = async e => {
        e.preventDefault()
        let requestData = copy(updateTagData)
        try {
            await request.patch(`tags/${tagsCollection.items[clickedTagIndex].id}`, requestData)
            updateTagsCollection({ reload: true })
            setUpdateTagData(copy(initialTagData))
            toggleRightSidePanel()
            showMessage('success', 'Tag updated successfully!')
        } catch (err) {
            showMessage('error', 'Failed to update tag')
        }
    }

    const handleDelete = async (e, id) => {
        e.preventDefault()
        try {
            await request.delete(`tags/${id}`)
            updateTagsCollection({ reload: true })
            toggleDeleteModal()
            showMessage('success', 'Tag deleted successfully')
        } catch (err) {
            showMessage('error', 'Failed to delete tag')
        }
    }

    // const onRowClick = (e, index) => {
    //     e.stopPropagation()
    //     toggleRightSidePanel()
    //     setTagIndex(index)
    //     setTagDetails(tagsCollection.items[index])
    //     setViewMode('view')
    // }

    function handleNextButton() {
        const newIndex = tagIndex + 1
        setTagIndex(newIndex)
        setTagDetails(tagsCollection?.items[newIndex])
    }

    function handlePrevButton() {
        const newIndex = tagIndex - 1
        setTagIndex(newIndex)
        setTagDetails(tagsCollection?.items[newIndex])
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
                        <Stats title='Stats' statValues={stats} isDateInput />
                        <div className='table-wrapper'>
                            <TablePageHeader
                                title='Tags'
                                onSearch={handleSearch}
                                onAddClick={true}
                                onExportClick={null}
                                // updateCollection={updateTagsCollection}
                                buttonText='Add'
                                toggleRightSidePanel={toggleRightSidePanel}
                                setViewMode={setViewMode}
                            />
                            <div className='table-container'>
                                <Table
                                    className='category-table'
                                    items={tagsCollection.items}
                                    columns={columns}
                                    controlColumns={[]}
                                    loaded={tagsCollection.loaded}
                                    searchParams={tagsCollection.searchParams}
                                    collection={tagsCollection}
                                    // onRowClick={onRowClick}
                                    updateCollection={updateTagsCollection}
                                    selectedIndex={tagIndex}
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
                        setTagIndex(null)
                    }}
                >
                    <RightSidePanel
                        viewMode={viewMode}
                        title={
                            viewMode === 'view'
                                ? 'Tag Information'
                                : viewMode === 'edit'
                                    ? 'Edit Tag'
                                    : viewMode === 'add'
                                        ? 'Add Tag'
                                        : ''
                        }
                        details={tagDetails}
                        setDetails={setTagDetails}
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
                                        ? handleAdd
                                        : null
                        }
                        buttonNameOne='without-bg-btn'
                        buttonNameTwo='with-bg-btn'
                        buttonTextOne={
                            viewMode === 'view'
                                ? 'Previous Tag'
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? 'Cancel'
                                    : ''
                        }
                        buttonTextTwo={
                            viewMode === 'view'
                                ? 'Next Tag'
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Save'
                                        : ''
                        }
                        toggleRightSidePanel={toggleRightSidePanel}
                        buttonIconLeft='/arrow-left.svg'
                        buttonIconRight='/arrow-right.svg'
                        setIndex={setTagIndex}
                        index={tagIndex}
                        collection={tagsCollection}
                        updateData={
                            viewMode === 'edit'
                                ? updateTagData
                                : viewMode === 'add'
                                    ? addTagData
                                    : ''
                        }
                        updateOnChange={
                            viewMode === 'edit'
                                ? onUpdateTagDataInputChange
                                : viewMode === 'add'
                                    ? onAddTagDataInputChange
                                    : ''
                        }
                        handleUpdate={handleUpdate}
                        onAddDataInputChange={onAddTagDataInputChange}
                        addData={addTagData}
                        setUpdateData={
                            viewMode === 'edit'
                                ? setUpdateTagData
                                : viewMode === 'add'
                                    ? setAddTagData
                                    : ''
                        }
                        page='tags'
                    />
                </div>
            )}

            {showDeleteModal && (
                <Modal title={deleteModalTitle} toggleModal={toggleDeleteModal}>
                    <DeleteModal
                        toggleDeleteModal={toggleDeleteModal}
                        handleDelete={handleDelete}
                        buyerByCompanyId={tagToDelete}
                        text={deleteModalDescription}
                        deleteBtn={deleteBtn}
                    />
                </Modal>
            )}
        </div>
    )
}

