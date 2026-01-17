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
import DropList from '@/components/dropList'
import TagInput from '@/components/tagInput'

import { copy } from '@/helpers'
import useCollection from '@/hooks/useCollection'
import useRequest from '@/hooks/useRequest'
import useQueryParams from '@/hooks/useQueryParams'
import useToggle from '@/hooks/useToggle'
import { useForm } from '@/hooks/useForm'
import useFilter from '@/hooks/useFilter'

const stats = [
    {
        mainLabel: 'Total Keywords',
        mainValue: '114',
        subLabel: '',
        subValue: '',
        isActive: true
    },
    {
        mainLabel: 'Keywords with Warnings',
        mainValue: '19',
        subLabel: '',
        subValue: '',
        isActive: true
    },
    {
        mainLabel: 'Keywords Failed Compliance',
        mainValue: '7',
        subLabel: '',
        subValue: '',
        isActive: true
    },
    {
        mainLabel: 'Inactive Keywords',
        mainValue: '14',
        subLabel: '',
        subValue: '',
        isActive: true
    },
]

const quickFilter = [
    {
        label: 'Active Keywords',
        key: 'ACTIVE',
        isActive: true
    },
    {
        label: 'Inactive Keywords',
        key: 'INACTIVE',
        isActive: false
    },
]

const initialFilterData = {
    f_status: {
        operator: 'equals',
        value: '',
        type: 'checkbox'
    }
}

const initialKeywordData = {
    title: '',
    keywords: [],
}

const keywordsColumns = [
    {
      "id": 1,
      "title": "Privacy Policy Alignment",
      "keywords": [
        "privacy policy",
        "compliance",
        "data protection laws",
        "adheres to",
        "UK GDPR",
        "compliant"
      ]
    },
    {
      "id": 2,
      "title": "Contact Information",
      "keywords": [
        "contact information",
        "DPO",
        "data protection officer",
        "contact point"
      ]
    },
    {
      "id": 3,
      "title": "Cookies and Tracking",
      "keywords": [
        "cookies",
        "tracking technologies",
        "consent for cookies",
        "ePrivacy",
        "mechanisms"
      ]
    },
    {
      "id": 4,
      "title": "Data Collection Practices",
      "keywords": [
        "data collection",
        "personal data",
        "data collected",
        "methods used",
        "collecting data"
      ]
    },
    {
      "id": 5,
      "title": "Purposes of Data Processing",
      "keywords": [
        "purposes of data processing",
        "uses of data",
        "legal basis for processing",
        "data use",
        "why data is collected"
      ]
    },
    {
      "id": 6,
      "title": "Third Party Opt-in",
      "keywords": [
        "third party opt-in",
        "data sharing",
        "user consent",
        "consent agreements",
        "Third Party Opt-in 1",
        "third party opt-in",
        "data sharing",
        "user consent",
        "consent agreements",
        "Third Party Opt-in 1"
      ]
    }
  ]

export default function Keywords() {
    const { request } = useRequest()
    const [queryParams, setQueryParam] = useQueryParams()
    const [activeRowID, setActiveRowID] = useState(null)
    const [showDeactivateButton, toggleDeactivateButton] = useToggle()
    const [activeKeywordIndex, setActiveKeywordIndex] = useState(null)
    const [expandedRows, setExpandedRows] = useState({})
    const [showAddKeywordModal, setShowAddKeywordModal] = useState({})
    const [keywordsCollection, updateKeywordsCollection] = useCollection('admin/keywords', null, keywordsColumns)

    const columns = [
        {
            name: 'Title',
            id: 'title',
            visible: true,
            sortable: 'backend',
            render: row => <div className='keyword-title'>{row?.title || '--'}</div>,
        },
        {
            name: 'Keyword',
            id: 'keywords',
            visible: true,
            sortable: 'backend',
            render: row => {
                const isExpanded = expandedRows[row.id] || false
                const displayKeywords = isExpanded ? row.keywords : row.keywords.slice(0, 5)
                const remainingCount = row.keywords.length - 5

                return (
                    <div className='keyword-list'>
                        {displayKeywords.map((keyword, index) => (
                            <div key={index} className={`keyword-list-item-keyword ${activeRowID === row.id && activeKeywordIndex === index ? 'active' : ''}`}>
                                <div className='keyword-text'>{keyword}</div>

                                <div 
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        if (activeRowID === row.id && activeKeywordIndex === index) {
                                            console.log('Closing menu');
                                            setActiveRowID(null);
                                            setActiveKeywordIndex(null);
                                        } else {
                                            console.log('Opening menu for row:', row.id, 'index:', index);
                                            setActiveRowID(row.id);
                                            setActiveKeywordIndex(index);
                                        }
                                    }}
                                    className='keyword-actions'
                                >
                                    <img src='more-icon.svg' />
                                </div>

                                {activeRowID === row.id && activeKeywordIndex === index && (
                                    <div className='keyword-action-menu' onClick={(e) => e.stopPropagation()}>
                                        <button 
                                            className='deactivate-action-button'
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setActiveRowID(null);
                                                setActiveKeywordIndex(null);
                                                console.log('Deactivate clicked for keyword:', keyword);
                                            }}
                                        >
                                            Deactivate Keyword
                                        </button>
                                    </div>
                                )}
                            </div>
                        ))}

                        <div className='link-like-button-wrapper'>
                            <div 
                                className='keyword-add-icon'
                                onClick={(e) => {
                                    e.stopPropagation();
                                    setShowAddKeywordModal(prev => ({
                                        ...prev,
                                        [row.id]: !prev[row.id]
                                    }));
                                }}
                            >
                                <img src='plus-circle.svg' />
                            </div>
                            {showAddKeywordModal[row.id] && (
                                <div onClick={(e) => e.stopPropagation()}>
                                    <DropList
                                        title='Add New Keywords'
                                        name='tag-input-drop-list'
                                    >
                                        <TagInput
                                            label='Keywords'
                                            toggleWordsModal={() => {
                                                setShowAddKeywordModal(prev => ({
                                                    ...prev,
                                                    [row.id]: false
                                                }));
                                            }}
                                            addOffensiveWord={(tags) => handleAddKeywordFromTable(row.id, tags)}
                                        />
                                    </DropList>
                                </div>
                            )}
                        </div>
                        {row.keywords.length > 5 && (
                            <button 
                                className='link-like-button'
                                onClick={(e) => {
                                    e.stopPropagation();
                                    setExpandedRows(prev => ({
                                        ...prev,
                                        [row.id]: !prev[row.id]
                                    }));
                                }}
                            >
                                {isExpanded ? 'View less' : `View ${remainingCount} more`}
                            </button>
                        )}
                    </div>
                )
            }
        }
    ]

    const [showRightSidePanel, toggleRightSidePanel] = useToggle()
    const [showDeleteModal, toggleDeleteModal] = useToggle()
    const [showKeywordsModal, toggleKeywordsModal] = useToggle()
    const [showFilterDropList, toggleFilterDropList] = useToggle()

    const [clickedKeywordIndex, setClickedKeywordIndex] = useState()
    const [keywordIndex, setKeywordIndex] = useState(null)
    const [keywordDetails, setKeywordDetails] = useState()
    const [viewMode, setViewMode] = useState()

    const [deleteModalTitle, setDeleteModalTitle] = useState()
    const [deleteModalDescription, setDeleteModalDescription] = useState()
    const [deleteBtn, setDeleteBtn] = useState()
    const [keywordToDelete, setKeywordToDelete] = useState()
    const [deactivateKeywordIndex, setDeactivateKeywordIndex] = useState(null)

    const [message, setMessage] = useState([])

    const [
        addKeywordData,
        setAddKeywordData,
        onAddKeywordDataInputChange,
        addKeywordDataErrors,
        setAddKeywordDataErrorsMap,
        addKeywordDataErrorMessage,
        setAddKeywordDataErrorMessage,
    ] = useForm(copy(initialKeywordData))

    const [
        updateKeywordData,
        setUpdateKeywordData,
        onUpdateKeywordDataInputChange,
        updateKeywordDataErrors,
        setUpdateKeywordDataErrorsMap,
        updateKeywordDataErrorMessage,
        setUpdateKeywordDataErrorMessage,
    ] = useForm(copy(initialKeywordData))

    const [
        currentFilterData,
        filterEnabled,
        getFilterSearchParams,
        onFilterInputChange,
        applyFilter,
        clearFilter,
        setFilterData 
    ] = useFilter(initialFilterData, updateKeywordsCollection)

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
        let requestData = copy(addKeywordData)
        // Convert keywords array to the format expected by API
        if (Array.isArray(requestData.keywords)) {
            requestData.keywords = requestData.keywords.join(',')
        }
        try {
            await request.post('keywords', requestData)
            updateKeywordsCollection({ reload: true })
            setAddKeywordData(copy(initialKeywordData))
            toggleRightSidePanel()
            showMessage('success', 'Keyword created successfully.')
        } catch (err) {
            showMessage('error', 'Failed to create keyword.')
        }
    }

    const handleUpdate = async e => {
        e.preventDefault()
        let requestData = copy(updateKeywordData)
        // Convert keywords array to the format expected by API
        if (Array.isArray(requestData.keywords)) {
            requestData.keywords = requestData.keywords.join(',')
        }
        try {
            await request.patch(`keywords/${keywordsCollection.items[clickedKeywordIndex].id}`, requestData)
            updateKeywordsCollection({ reload: true })
            setUpdateKeywordData(copy(initialKeywordData))
            toggleRightSidePanel()
            showMessage('success', 'Keyword updated successfully!')
        } catch (err) {
            showMessage('error', 'Failed to update keyword')
        }
    }

    const handleDelete = async (e, id) => {
        e.preventDefault()
        try {
            await request.delete(`keywords/${id}`)
            updateKeywordsCollection({ reload: true })
            toggleDeleteModal()
            showMessage('success', 'Keyword deleted successfully')
        } catch (err) {
            showMessage('error', 'Failed to delete keyword')
        }
    }

    const handleAddKeyword = async (newKeywords) => {
        if (!keywordDetails || !newKeywords || newKeywords.length === 0) {
            return
        }

        try {
            // Get existing keywords and combine with new ones
            const existingKeywords = keywordDetails.keywords || []
            const allKeywords = [...existingKeywords, ...newKeywords]
            
            // Prepare request data
            const requestData = {
                title: keywordDetails.title,
                keywords: Array.isArray(allKeywords) ? allKeywords.join(',') : allKeywords
            }

            // Update via API
            await request.patch(`keywords/${keywordDetails.id}`, requestData)
            
            // Reload collection and update local state
            updateKeywordsCollection({ reload: true })
            
            // Update keywordDetails with new keywords
            setKeywordDetails(prev => ({
                ...prev,
                keywords: allKeywords
            }))
            
            // Close modal and show success message
            toggleKeywordsModal()
            showMessage('success', 'Keywords added successfully!')
        } catch (err) {
            showMessage('error', 'Failed to add keywords')
        }
    }

    const handleAddKeywordFromTable = async (rowId, newKeywords) => {
        if (!newKeywords || newKeywords.length === 0) {
            return
        }

        try {
            const row = keywordsCollection.items.find(item => item.id === rowId)
            if (!row) return

            // Get existing keywords and combine with new ones
            const existingKeywords = row.keywords || []
            const allKeywords = [...existingKeywords, ...newKeywords]
            
            // Prepare request data
            const requestData = {
                title: row.title,
                keywords: Array.isArray(allKeywords) ? allKeywords.join(',') : allKeywords
            }

            // Update via API
            await request.patch(`keywords/${rowId}`, requestData)
            
            // Reload collection
            updateKeywordsCollection({ reload: true })
            
            // Close modal and show success message
            setShowAddKeywordModal(prev => ({
                ...prev,
                [rowId]: false
            }))
            showMessage('success', 'Keywords added successfully!')
        } catch (err) {
            showMessage('error', 'Failed to add keywords')
        }
    }

    const onRowClick = (e, index) => {
        e.stopPropagation()
        setKeywordIndex(index)
        setKeywordDetails(keywordsCollection.items[index])
        setViewMode('view')
        toggleRightSidePanel()
    }

    function handleNextButton() {
        const newIndex = keywordIndex + 1
        setKeywordIndex(newIndex)
        setKeywordDetails(keywordsCollection?.items[newIndex])
    }

    function handlePrevButton() {
        const newIndex = keywordIndex - 1
        setKeywordIndex(newIndex)
        setKeywordDetails(keywordsCollection?.items[newIndex])
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
                                title='Keywords'
                                onSearch={handleSearch}
                                toggleFilterDropList={toggleFilterDropList}
                                showFilterDropList={showFilterDropList}
                                onFilterInputChange={onFilterInputChange}
                                onAddClick={true}
                                onExportClick={null}
                                showActionButtons
                                buttonText='Add Title'
                                quickFilter={quickFilter}
                                currentFilterData={currentFilterData}
                                collection={keywordsCollection}
                                applyFilter={applyFilter}
                                toggleRightSidePanel={toggleRightSidePanel}
                                setViewMode={setViewMode}
                            />
                            <div className='table-container'>
                                <Table
                                    className='category-table'
                                    items={keywordsCollection.items}
                                    columns={columns}
                                    controlColumns={[]}
                                    loaded={keywordsCollection.loaded}
                                    searchParams={keywordsCollection.searchParams}
                                    collection={keywordsCollection}
                                    onRowClick={onRowClick}
                                    updateCollection={updateKeywordsCollection}
                                    selectedIndex={keywordIndex}
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
                        setKeywordIndex(null)
                    }}
                >
                    <RightSidePanel
                        viewMode={viewMode}
                        title={
                            viewMode === 'view'
                                ? 'Keyword Information'
                                : viewMode === 'edit'
                                    ? 'Edit Keyword'
                                    : viewMode === 'add'
                                        ? 'Add Title'
                                        : ''
                        }
                        details={keywordDetails}
                        setDetails={setKeywordDetails}
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
                                ? 'Export Keywords'
                                : viewMode === 'edit' || viewMode === 'add'
                                    ? 'Cancel'
                                    : ''
                        }
                        buttonTextTwo={
                            viewMode === 'view'
                                ? ''
                                : viewMode === 'edit'
                                    ? 'Save'
                                    : viewMode === 'add'
                                        ? 'Save'
                                        : ''
                        }
                        toggleRightSidePanel={toggleRightSidePanel}
                        buttonIconLeft='/arrow-left.svg'
                        buttonIconRight='/arrow-right.svg'
                        setIndex={setKeywordIndex}
                        index={keywordIndex}
                        collection={keywordsCollection}
                        updateData={
                            viewMode === 'edit'
                                ? updateKeywordData
                                : viewMode === 'add'
                                    ? addKeywordData
                                    : ''
                        }
                        updateOnChange={
                            viewMode === 'edit'
                                ? onUpdateKeywordDataInputChange
                                : viewMode === 'add'
                                    ? onAddKeywordDataInputChange
                                    : ''
                        }
                        handleUpdate={handleUpdate}
                        onAddDataInputChange={onAddKeywordDataInputChange}
                        addData={addKeywordData}
                        setUpdateData={
                            viewMode === 'edit'
                                ? setUpdateKeywordData
                                : viewMode === 'add'
                                    ? setAddKeywordData
                                    : ''
                        }
                        page='keywords'
                        collection={keywordsCollection.items}
                        setKeywordIndex={setDeactivateKeywordIndex}
                        keywordIndex={deactivateKeywordIndex}
                        showDeactivateButton={showDeactivateButton}
                        toggleDeactivateButton={toggleDeactivateButton}
                        showKeywordsModal={showKeywordsModal}
                        toggleKeywordsModal={toggleKeywordsModal}
                        handleAddKeyword={handleAddKeyword}
                    />
                </div>
            )}

            {showDeleteModal && (
                <Modal title={deleteModalTitle} toggleModal={toggleDeleteModal}>
                    <DeleteModal
                        toggleDeleteModal={toggleDeleteModal}
                        handleDelete={handleDelete}
                        buyerByCompanyId={keywordToDelete}
                        text={deleteModalDescription}
                        deleteBtn={deleteBtn}
                    />
                </Modal>
            )}
        </div>
    )
}

