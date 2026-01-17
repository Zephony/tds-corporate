'use client'
import { useState } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table/index'
import TablePageHeader from '@/components/tablePageHeader'
import RightSidePanel from '@/components/rightSidePanel'
import Modal from '@/components/modal'
import DeleteModal from '@/components/deleteModal'
import StatusText from '@/components/statusText'

import { getCollectionSearchParamsFromPage } from '@/helpers'
import { copy } from '@/helpers'
import { replaceUnderScoreWithSpace } from '@/helpers'

import useCollection from '@/hooks/useCollection'
import useQueryParams from '@/hooks/useQueryParams'
import useToggle from '@/hooks/useToggle'
import { useForm } from '@/hooks/useForm'
import useRequest from '@/hooks/useRequest'

// Form initial Data
const initialUpdateDataTypeData = {
    name: '',
    description: '',
    status: 'active',
}

// Form initial Data
const initialAddDataTypeData = {
    name: '',
    description: '',
    status: 'active',
}

export default function DataType() {
    const { request } = useRequest()

    // Set query params
    const [queryParams, setQueryParam] = useQueryParams()

    // Stores DataTypes data
    const [dataTypeC, updateDataTypeC] = useCollection('admin/data-types', null, null)

    // Pass values to the main table
    const [columns] = useState([
        {
            name: 'S No',
            id: 's_no',
            visible: true,
            sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => (
                <div className='s-no'>{index + 1}</div>
            )
        },
        {
            name: 'Data Type ID',
            id: 'id',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='data-type-id'>
                    {row?.reference_id || `DT${String(row?.id).padStart(3, '0')}`}
                </div>
            )
        },
        {
            name: 'Data Type Name',
            id: 'name',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='data-type-name'>{row?.name}</div>
            )
        },
        {
            name: 'Status',
            id: 'status',
            visible: true,
            sortable: 'backend',
            render: row => (
                <div className='status-main'>
                    <div className={`status-${row?.status === 'active' ? 'active' : 'inactive'}`}>
                        {row?.status === 'active' ? 'Active' : replaceUnderScoreWithSpace(row?.status)}
                    </div>
                </div>
            )
        },
    ])

    // Toggle states
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDeleteModal, toggleDeleteModal] = useToggle()

    // Store clicked data type index
    const [clickedDataTypeIndex, setClickedDataTypeIndex] = useState()
    const [dataTypeIndex, setDataTypeIndex] = useState()
    const [dataTypeDetails, setDataTypeDetails] = useState()

    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    // Delete modal states
    const [deleteModalTitle, setDeleteModalTitle] = useState()
    const [deleteModalDescription, setDeleteModalDescription] = useState()
    const [deleteBtn, setDeleteBtn] = useState()
    const [dataTypeToDelete, setDataTypeToDelete] = useState()

    // Message state
    const [message, setMessage] = useState([])

    // Form states
    const [
        addDataTypeData,
        setAddDataTypeData,
        onAddDataTypeDataInputChange,
        addDataTypeDataErrors,
        setAddDataTypeDataErrorsMap,
        addDataTypeDataErrorMessage,
        setAddDataTypeDataErrorMessage,
    ] = useForm(copy(initialAddDataTypeData))

    const [
        updateDataTypeData,
        setUpdateDataTypeData,
        onUpdateDataTypeDataInputChange,
        updateDataTypeDataErrors,
        setUpdateDataTypeDataErrorsMap,
        updateDataTypeDataErrorMessage,
        setUpdateDataTypeDataErrorMessage,
    ] = useForm(copy(initialUpdateDataTypeData))

    // Search functionality
    const handleSearch = (qString, updateCollection) => {
        setQueryParam('q', qString)
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            searchParams.set('q', qString)
            return { searchParams }
        })
    }

    // Display the request status
    const showMessage = (status, text) => {
        const id = Date.now()
        setMessage((prev) => [...prev, { id, status, text }])
        setTimeout(() => {
            setMessage((prev) => prev.filter(item => item.id !== id))
        }, 5000)
    }

    // Add functionality
    const handleAdd = async (e) => {
        e.preventDefault()

        let requestData = copy(addDataTypeData)

        try {
            await request.post('data-types', requestData)
            updateDataTypeC({ reload: true })
            setAddDataTypeData(copy(initialAddDataTypeData))
            toggleRightSidePanel()
            showMessage('success', 'Data type created successfully.')
        } catch (err) {
            showMessage('error', 'Failed to create data type.')
        }
    }

    // Update functionality
    const handleUpdate = async (e) => {
        e.preventDefault()

        let requestData = copy(updateDataTypeData)

        try {
            await request.patch(`data-types/${dataTypeC.items[clickedDataTypeIndex].id}`, requestData)
            updateDataTypeC({ reload: true })
            setUpdateDataTypeData(copy(initialUpdateDataTypeData))
            toggleRightSidePanel()
            showMessage('success', 'Data type updated successfully!')
        } catch (err) {
            showMessage('error', 'Failed to update data type')
        }
    }

    // Delete functionality
    const handleDelete = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`data-types/${id}`)
            updateDataTypeC({ reload: true })
            toggleDeleteModal()
            showMessage('success', 'Data type deleted successfully')
        } catch (err) {
            showMessage('error', 'Failed to delete data type')
        }
    }

    // On table row click get the row index and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()
        // toggleRightSidePanel()
        setDataTypeIndex(index)
        setDataTypeDetails(dataTypeC.items[index])
        setViewMode('view')
    }

    // Next button functionality inside the right side panel
    function handleNextButton() {
        const newIndex = dataTypeIndex + 1
        setDataTypeIndex(newIndex)
        setDataTypeDetails(dataTypeC?.items[newIndex])
    }

    // Previous button functionality inside the right side panel
    function handlePrevButton() {
        const newIndex = dataTypeIndex - 1
        setDataTypeIndex(newIndex)
        setDataTypeDetails(dataTypeC?.items[newIndex])
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
                                title='Data Type'
                                onSearch={handleSearch}
                                onAddClick={true}
                                onExportClick={null}
                                updateCollection={updateDataTypeC}
                                buttonText='Add'
                                toggleRightSidePanel={toggleRightSidePanel}
                                setViewMode={setViewMode}
                            />
                            <div className='table-container'>
                                <Table
                                    className='category-table'
                                    items={dataTypeC.items}
                                    columns={columns}
                                    controlColumns={[]}
                                    loaded={dataTypeC.loaded}
                                    searchParams={dataTypeC.searchParams}
                                    collection={dataTypeC}
                                    // onRowClick={onRowClick}
                                    updateCollection={updateDataTypeC}
                                    selectedIndex={dataTypeIndex}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </>

            {/* Right Side Panel */}
            {showRightSidePanel && (
                <div
                    className='overlay'
                    onClick={() => {
                        toggleRightSidePanel()
                        setDataTypeIndex(null)
                    }}
                >
                    <RightSidePanel
                        viewMode={viewMode}
                        title={
                            viewMode === 'view'
                                ? 'Data Type Information'
                                : viewMode === 'edit'
                                    ? 'Edit Data Type'
                                    : viewMode === 'add'
                                        ? 'Add Data Type'
                                        : ''
                        }
                        details={dataTypeDetails}
                        setDetails={setDataTypeDetails}
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
                                ? 'Previous Data Type'
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? 'Cancel'
                                    : ''
                        }
                        buttonTextTwo={
                            viewMode === 'view'
                                ? 'Next Data Type'
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Save'
                                        : ''
                        }
                        toggleRightSidePanel={toggleRightSidePanel}
                        buttonIconLeft='/arrow-left.svg'
                        buttonIconRight='/arrow-right.svg'
                        setIndex={setDataTypeIndex}
                        index={dataTypeIndex}
                        collection={dataTypeC}
                        updateData={
                            viewMode === 'edit'
                                ? updateDataTypeData
                                : viewMode === 'add'
                                    ? addDataTypeData
                                    : ''
                        }
                        updateOnChange={
                            viewMode === 'edit'
                                ? onUpdateDataTypeDataInputChange
                                : viewMode === 'add'
                                    ? onAddDataTypeDataInputChange
                                    : ''
                        }
                        handleUpdate={handleUpdate}
                        onAddDataInputChange={onAddDataTypeDataInputChange}
                        addData={addDataTypeData}
                        setUpdateData={
                            viewMode === 'edit'
                                ? setUpdateDataTypeData
                                : viewMode === 'add'
                                    ? setAddDataTypeData
                                    : ''
                        }
                        page='data-type'
                    />
                </div>
            )}

            {/* Delete Modal */}
            {showDeleteModal && (
                <Modal
                    title={deleteModalTitle}
                    toggleModal={toggleDeleteModal}
                >
                    <DeleteModal
                        toggleDeleteModal={toggleDeleteModal}
                        handleDelete={handleDelete}
                        buyerByCompanyId={dataTypeToDelete}
                        text={deleteModalDescription}
                        deleteBtn={deleteBtn}
                    />
                </Modal>
            )}
        </div>
    )
}

