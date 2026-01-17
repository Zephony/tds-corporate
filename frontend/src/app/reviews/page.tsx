'use client'
import { useState, useRef, useEffect } from 'react'

import Header from '@/components/header'
import Menubar from '@/components/menuBar'
import Table from '@/components/table/index'
import TablePageHeader from '@/components/tablePageHeader'
import RightSidePanel from '@/components/rightSidePanel'

import useCollection from '@/hooks/useCollection'
import useQueryParams from '@/hooks/useQueryParams'
import useToggle from '@/hooks/useToggle'
import { useForm } from '@/hooks/useForm'

import { formatDateTime, getCollectionSearchParamsFromPage, shortenText } from '@/helpers'
import { copy } from '@/helpers'
import useRequest from '@/hooks/useRequest'

import '@/css/pages/review.css'
import StatusText from '@/components/statusText'
import Modal from '@/components/modal'
import DeleteModal from '@/components/deleteModal'
import { Input } from '@/components/form'

// Form initial Data
const initialUpdateReviewData = {
    status: '',
    word: ''
}

// Form initial Data
const initialAddReviewData = {
    status: '',
    word: ''
}

export default function Reviews() {

    const { request } = useRequest()

    const [reviewC, updateReviewC] = useCollection('admin/reviews', getCollectionSearchParamsFromPage())
    const [showDeleteModal,  toggleDeleteModal] = useToggle()
    const [showMoreOption, toggleMoreOption] = useToggle()


    // Create the form for editng the buyer Data
    const [
        updateReviewData,
        setUpdateReviewData,
        onUpdateReviewDataInputChange,
        updateReviewDataErrors,
        setUpdateReviewDataErrorsMap,
        updateReviewDataErrorMessage,
        setUpdateReviewDataErrorMessage,
    ] = useForm(copy(initialUpdateReviewData))

    console.log(updateReviewData, 'updateReviewData main')
    
    // Use ref to store current state for render functions
    const updateReviewDataRef = useRef(updateReviewData)
    updateReviewDataRef.current = updateReviewData

    // Pass values to the main table
    const [columns, setColumns] = useState([
        {
            name: 'Added on',
            id: 'review_date',
            visible: true,
            sortable: 'backend',
            render: row => <div className='s-no'>{formatDateTime(row.review_date)}</div>
        },
        {
            name: 'Review',
            id: 'review_text',
            visible: true,
            sortable: 'backend',
            render: row => <div className='data-type'>{row.review_text}</div>
        },
        {
            name: 'Reported Count',
            id: 'reported_count',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-name-and-img'>
                <div className='name'>
                    {row.reported_count}
                </div>
            </div>
        },
        {
            name: 'Recommended',
            id: 'is_recommended',
            visible: true,
            sortable: 'backend',
            render: row => <div className='category-id'>
                {row.is_recommended ? 'Yes' : 'No'}
            </div>
        },
        {
            name: 'Rating',
            id: 'accuracy_rating',
            visible: true,
            sortable: 'backend',
            render: row => <div className='rating'>

                {row.overall_rating &&
                    <img className='star-icon' src='/star.svg' />
                }
                <div>{row.overall_rating ? row.overall_rating : 'N/A'}</div>
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
                            :row?.status === 'FLAGGED'
                                ? 'red'
                                : ''
                    }`}
            >
                {row?.status}
            </div>
        },
        {
            name: 'Action',
            id: 'action',
            visible: true,
            // sortable: 'backend',
            render: (row, customData, collection, updateCollection, index) => <div className='action'>
                <div className='action-button'>
                    <button
                        onClick={(e) => {
                            e.stopPropagation()
                            setViewMode('edit')
                            setReviewDetails(row)
                            setEditIndex(null)
                            setUpdateReviewData({
                                status: row.status,
                            })
                            toggleRightSidePanel()
                        }}
                        className='edit-icon-wrapper'
                    >
                        <img
                            className='edit-icon'
                            src='/edit-icon.svg'
                        />
                    </button>
                    <button 
                        onClick={(e) => {
                            e.stopPropagation()
                            setDeleteModalDescription('Are you sure, want to delete this Review')
                            setDeleteModalTitle('Delete Review')
                            setDeleteBtn('Delete')
                            toggleDeleteModal()
                            setReviewId(row.id)
                        }}
                    
                        className='delete-icon-wrapper'
                    >
                        <img
                            className='delete-icon'
                            src='/delete-icon.svg'
                        />
                    </button>
                </div>

            </div>
        },
    ])

    const [isEditable, setIsEditable] = useState(false)

    const [editIndex, setEditIndex] = useState()

    const [offensiveC, updateOffensiveC] = useCollection('admin/offensive-words', getCollectionSearchParamsFromPage() )

    const [offensiveWordsColumn, setOffensiveWordsColumn] = useState([
        {
            name: 'Added on',
            id: 'added_date',
            visible: true,
            sortable: 'backend',
            render: row => <div title={formatDateTime(row.added_date)} className='panel-review-date'>{shortenText(formatDateTime(row.added_date))}</div>
        },
        {
            name: 'Words',
            id: 'word',
            visible: true,
            sortable: 'backend',
            render: (row, customData, collection, updateCollection, index, isEditing) => <>
                { isEditing 
                    ? <div className="edit-section">
                        {console.log('Inside render - updateReviewDataRef.current:', updateReviewDataRef.current)}
                        <Input
                            label=''
                            name='word'
                            value={updateReviewDataRef.current['word'] || ''}
                            onChange={onUpdateReviewDataInputChange}
                            className='table-edit'
                        />
                    </div>
                    : <div className='panel-offensive-words'>
                        {row.word}
                    </div>
                }
            </> 
        }, 
        {
            name: '',
            id: 'action',
            visible: true,
            // sortable: 'backend',
            render: (row, customData, collection, updateCollection, index, isEditing) => <div className='action'>
                { isEditing
                    ? <div className='edit-action'>
                        <div onClick={() => setEditIndex(null)} className='save'>
                            <img src='/green-check.svg'/>
                        </div>
                        <div onClick={() => setEditIndex(null)} className='cancel'>
                            <img src='/edit-cancel.svg'/>
                        </div>
                    </div>
                    : <div className='action-button'>
                        <button
                            onClick={(e) => {
                                e.stopPropagation()
                                
                                setEditIndex(row.id)
                                // setViewMode('edit')
                                // setReviewDetail(row)
                                setUpdateReviewData({
                                    word: row.word,
                                })
                            }}
                            className='panel-edit-icon-wrapper'
                        >
                            <img
                                className='edit-icon'
                                src='/edit-icon.svg'
                            />
                        </button>
                        <button 
                            onClick={(e) => {
                                e.stopPropagation()
                                setDeleteModalDescription('Are you sure, want to delete this Review')
                                setDeleteModalTitle('Delete Review')
                                setDeleteBtn('Delete')
                                toggleDeleteModal()
                                setReviewId(row.id)
                            }}
                            className='panel-delete-icon-wrapper'
                        >
                            <img
                                className='delete-icon'
                                src='/delete-icon.svg'
                            />
                        </button>
                    </div>
                }
            </div>
        },
        
    ])

    const [queryParams, setQueryParam] = useQueryParams()

    const [showFilterModal, toggleFilterModal] = useToggle()
    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDropDown, toggleDropDown] = useToggle()
    const [showWordsModal, toggleWordsModal] = useToggle()

    // Stores the row clicked index also update the 
    // index when clicked on next and previous button in the right panel
    const [reviewIndex, setReviewIndex] = useState()

    const [selectedDocument, setSelectedDocument] = useState([])
    const [uploadedFile, setUploadedFile] = useState()

    // Store the clicked buyer from table row click
    const [reviewDetails, setReviewDetails] = useState()

    const [
        addReviewData,
        setAddReviewData,
        onAddReviewDataInputChange,
        addReviewDataErrors,
        setAddReviewDataErrorsMap,
        addReviewDataErrorMessage,
        setAddReviewDataErrorMessage,
    ] = useForm(copy(initialAddReviewData))


    // Store the state of right side panel (view mode or edit mode)
    const [viewMode, setViewMode] = useState()

    // Delete Button text
    const [deleteBtn, setDeleteBtn] = useState()

    const [message, setMessage] = useState([])

    // sets delete modal title
    const [deleteModalTitle, setDeleteModalTitle] = useState()

    // sets delete modal description
    const [deleteModalDescription, setDeleteModalDescription] = useState()

    const reviewDetailsKeyValue = [
        {
            property: 'product_id',
            displayKey: 'Product Id',
            value: reviewDetails?.id_product
        },
        {
            property: 'id_order',
            displayKey: 'Order Id',
            value: reviewDetails?.id_order
        },
        {
            property: 'id_buyer',
            displayKey: 'Buyer Id',
            value: reviewDetails?.order_details?.id_buyer
        },
        {
            property: 'is_recommended',
            displayKey: 'Recommended',
            value: reviewDetails?.is_recommended ? 'Yes' : 'No'
        },
        {
            property: 'reported_count',
            displayKey: 'Report Count',
            value: reviewDetails?.reported_count
        },
        {
            property: 'accuracy_rating',
            displayKey: 'Accuracy',
            value: (<div className='accuracy-rating'>
                <img className='star-icon' src='/star.svg' />
                {reviewDetails?.accuracy_rating}
            </div>)
        },
        {
            property: 'receptivity_rating',
            displayKey: 'Receptivity',
            value: ( <div className='receptivity-rating'>
                <img className='star-icon' src='/star.svg' />
                {reviewDetails?.receptivity_rating}
            </div>
            )
        },
        {
            property: 'contact_rate_rating',
            displayKey: 'Contact Rate',
            value: (<div className='contact-rating'>
                <img className='star-icon' src='/star.svg' />
                {reviewDetails?.contact_rate_rating}
            </div>)
        },
        {
            property: 'overall_rating',
            displayKey: 'Rating',
            value: ( <div className='rating'>
                <img className='star-icon' src='/star.svg' />
                {reviewDetails?.overall_rating}
            </div>)
        },
        {
            property: 'review_text',
            displayKey: 'Review',
            value: reviewDetails?.review_text
        },
        {
            property: 'status',
            displayKey: 'Status',
            value: (
                <div
                    className={`status-main ${reviewDetails?.status === 'ACTIVE'
                        ? 'green'
                        : reviewDetails?.status === 'PENDING'
                            ? 'yellow'
                            : reviewDetails?.status === 'HIDDEN'
                                ? 'grey'
                                : reviewDetails?.status === 'FLAGGED'
                                    ? 'red'
                                    : ''
                        }`}
                >
                    {reviewDetails?.status}
                </div>
            )
        },
    ]

    const editPageKeyValue = [
        {
            property: 'accuracy_rating',
            displayKey: 'Accuracy',
            value: (<div className='accuracy-rating'>
                <img className='star-icon' src='/star.svg' />
                {reviewDetails?.accuracy_rating}
            </div>)
        },
        {
            property: 'receptivity_rating',
            displayKey: 'Receptivity',
            value: (<div className='receptivity-rating'>
                <img className='star-icon' src='/star.svg' />
                {reviewDetails?.receptivity_rating}
            </div>
            )
        },
        {
            property: 'contact_rate_rating',
            displayKey: 'Contact Rate',
            value: (<div className='contact-rating'>
                <img className='star-icon' src='/star.svg' />
                {reviewDetails?.contact_rate_rating}
            </div>)
        },
        {
            property: 'overall_rating',
            displayKey: 'Rating',
            value: (<div className='rating'>
                <img className='star-icon' src='/star.svg' />
                {reviewDetails?.overall_rating}
            </div>)
        },
        {
            property: 'review_text',
            displayKey: 'Review',
            value: reviewDetails?.review_text
        },
    ]

    const handleAdd = async (e) => {
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(addReviewData)
        // requestData.id_role = Number(requestData.id_role)

        try {
            await request.post('buyers', requestData)
            updateReviewC({ reload: true })
            setAddReviewData(copy(initialAddReviewData))
        } catch (err) {
            console.error('Failed to add user:', err)
            alert('Failed to add user')
        }
    }

    const handleSearch = qString => {
        setQueryParam('q', qString)

        updateReviewC(old => {
            console.log('old', old)
            let searchParams = new URLSearchParams(old.searchParams)
            console.log('SeatchParams', searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }

    const handleOfffensiveWordsSearch = qString => {
        setQueryParam('q', qString)

        updateOffensiveC(old => {
            console.log('old', old)
            let searchParams = new URLSearchParams(old.searchParams)
            console.log('SeatchParams', searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }

    // Update functionality
    const handleUpdate = async (e) => {
        console.log('handle update triggerd')
        e.preventDefault()

        // Normalize id_role
        let requestData = copy(updateReviewData)
        // requestData.id_role = Number(requestData.id_role)

        // requestData = removeEmptyKeys(requestData, [null, ''])
        try {
            await request.patch(`review/${reviewC.items[reviewIndex].id}`, requestData)
            updateReviewC({ reload: true })
            setUpdateReviewData(copy(initialUpdateReviewData))
            showMessagee('success', 'Review updated successfully!' )
        } catch (err) {
            console.error('Failed to update user:', err)
            showMessagee('error', 'Failed to update Review')
        }
    }

    const addOffensiveWord = async() => {
        let requestData = copy(updateReviewData)

        try {
            await request.post(`review/${reviewC.items[reviewIndex].id}`, requestData)
            updateReviewC({ reload: true })
            setUpdateReviewData(copy(initialUpdateReviewData))
            showMessagee('success', 'Offensive word added successfully!')
        }
        catch(err) {
            console.error('Failed to update user:', err)
            showMessagee('error', 'Failed to add Offensive word')
        }
    }

    // Store buyers by company ID
    const [reviewId, setReviewId] = useState()

    // Delete functionality
    const handleDelete = async (e, id) => {
        e.preventDefault()

        try {
            await request.delete(`reviewa/${id}`)
            updateReviewC({ reload: true })
            showMessagee('success', 'Buyer Deleted Successfully')
        } catch (err) {
            console.error('Failed to add user:', err)
            showMessagee('error', 'Failed to delete buyer')
        }
    }

    // On table row click get the row index 
    // and return that particular item
    const onRowClick = (e, index) => {
        e.stopPropagation()
        toggleRightSidePanel()
        setReviewIndex(index)
        setReviewDetails(reviewC.items[index])
        setViewMode('view')
    }


    function handleNextButton() {
        const newIndex = reviewIndex + 1
        setReviewIndex(newIndex)
        setReviewDetails(reviewC?.items[newIndex])

    }

    function handlePrevButton() {
        const newIndex = reviewIndex - 1
        setReviewIndex(newIndex)
        setReviewDetails(reviewC?.items[newIndex])
    }

    // Display the request status
    const showMessagee = (status: string, text: string) => {
        const id = Date.now()
        setMessage((prev) => [...prev, { id, status, text }])
        setTimeout(() => {
            setMessage((prev) => prev.filter(item => item.id !== id))
        }, 5000)
    }

    console.log(updateReviewData['words'], 'isEditable')

    return <div className='page-container'>
        
        <StatusText
            text={message}
        />
        
        <>
            <div className='left-container'>
                <Menubar
                />
            </div>
            <div className='main-content'>
                <Header
                    title='Reviews'
                />
                <div className='main-content-body'>
                    <div className='table-wrapper'>
                        <TablePageHeader
                            title='Reviews List'
                            onSearch={handleSearch}
                            // toggleFilterModal={toggleFilterModal}
                            onAddClick={true}
                            onExportClick={null}
                            // moreOptionVisible
                            showActionButtons
                            // blogButtonVisible
                            buttonText='View Offensive Words'
                            toggleRightSidePanel={toggleRightSidePanel}
                            setViewMode={setViewMode}
                            updateCollection={updateReviewC}
                            showMoreOption={showMoreOption}
                            toggleMoreOption={toggleMoreOption}
                        />
                        <div className='table-container'>
                            <Table
                                className='category-table'
                                items={reviewC.items}
                                columns={columns}
                                controlColumns={[]}
                                loaded={reviewC.loaded}
                                searchParams={reviewC.searchParams}
                                collection={reviewC}
                                onRowClick={onRowClick}
                                selectedIndex={reviewIndex}
                                updateCollection={updateReviewC}
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
                    setReviewIndex(null)
                }}
            >
                <RightSidePanel
                    viewMode={viewMode}
                    title={viewMode === 'view'
                        ? 'Review Information'
                        : viewMode === 'edit'
                            ? 'Edit Review'
                            : viewMode === 'add'
                                ? 'Offensive Words'
                                : ''
                    }
                    details={reviewDetails}
                    setDetails={setReviewDetails}
                    offensiveWordsColumn={offensiveWordsColumn}
                    setOffensiveWordsColumn={setOffensiveWordsColumn}
                    labelValueData={viewMode === 'view' 
                        ? reviewDetailsKeyValue
                        : viewMode === 'edit'
                            ? editPageKeyValue
                            : ''}
                    buttonNameOne='without-bg-btn'
                    buttonNameTwo='with-bg-btn'
                    buttonTextOne={viewMode === 'view'
                        ? 'Previous Review'
                        : viewMode === 'edit' || viewMode === 'add'
                            ? 'Cancel'
                            : ''
                    }
                    buttonTextTwo={
                        viewMode === 'view'
                            ? 'Next Review'
                            : viewMode === 'edit' || viewMode === 'add'
                                ? 'Save'
                                :  ''
                    }
                    buttonOneFunction={viewMode === 'view'
                        ? handlePrevButton
                        : viewMode === 'edit' || viewMode === 'add'
                            ? toggleRightSidePanel
                            : viewMode === 'add'
                                ? ''
                                : ''

                    }
                    buttonTwoFunction={viewMode === 'view'
                        ? handleNextButton
                        : viewMode === 'edit' 
                            ? handleUpdate
                            : viewMode === 'add'
                                ? handleAdd
                                : ''
                    }
                    toggleRightSidePanel={toggleRightSidePanel}
                    buttonIconLeft='/arrow-left.svg'
                    buttonIconRight='/arrow-right.svg'
                    onSearch={handleOfffensiveWordsSearch}
                    setIndex={setReviewIndex}
                    index={reviewIndex}
                    collection={reviewC}
                    updateCollectionOne={updateReviewC}
                    updateData={updateReviewData}
                    updateOnChange={
                        viewMode === 'edit'
                            ? onUpdateReviewDataInputChange
                            : viewMode === 'add'
                                ? onAddReviewDataInputChange
                                : ''
                    }
                    onAddDataInputChange={onAddReviewDataInputChange}
                    addData={addReviewData}
                    setUpdateData={viewMode === 'edit'
                        ? setUpdateReviewData
                        : viewMode === 'add'
                            ? setAddReviewData
                            : ''
                    }
                    viewDetailsBtn={true}
                    summaryView={false}
                    showDropDown={showDropDown}
                    toggleDropDown={toggleDropDown}
                    selectedDocument={selectedDocument}
                    setSelectedDocument={setSelectedDocument}
                    uploadedFile={uploadedFile}
                    setUploadedFile={setUploadedFile}
                    toggleWordsModal={toggleWordsModal}
                    showWordsModal={showWordsModal}
                    page='review'
                    isEditable={isEditable}
                    setIsEditable={setIsEditable}
                    editIndex={editIndex}
                    setEditIndex={setEditIndex}
                    addOffensiveWord={addOffensiveWord}
                    updateCollectionTwo={updateOffensiveC}
                    collectionTwo={offensiveC}
                    coloumn={offensiveWordsColumn}
                    setColumn={setOffensiveWordsColumn}
                    
                />
            </div>
        }
        {
            showDeleteModal && <Modal
                title={deleteModalTitle}
                toggleModal={toggleDeleteModal}
            >
                <DeleteModal
                    toggleDeleteModal={toggleDeleteModal}
                    handleDelete={handleDelete}
                    buyerByCompanyId={reviewId}
                    text={deleteModalDescription}
                    deleteBtn={deleteBtn}
                />
            </Modal>
        }
    </div>
}