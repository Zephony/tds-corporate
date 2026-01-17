'use client'
import { replaceUnderScoreWithSpace ,getOptions, shortenText, copy} from '@/helpers'
import Link from 'next/link'

import { AnyNsRecord } from 'dns'
import ExpandCollapseSection from './collapseExpand'
import KeyValue from './keyValue'
import Tabs from './tabs'
import { Input, SelectField, DateField } from './form'
import ImageUpload from './imageUploadBox'
import ReviewPanelContent from './reviewPanelContent'
import BlogPanelContent from './blogPanelContent'
import ProductEditView from './productEditView'
import Checklist from './checklist'
import KeywordsInput from './keywordsInput'
import EmailAddView from './emailAddView'
import SmsAddView from './smsAddView'
import Table from './table'
import DropList from './dropList'
import TagInput from './tagInput'

// Hardcoded product policy compliance data
const productPolicyComplianceData = [
    {
        label: "Privacy Policy Alignment",
        status: "error",
        keyWord: [],
        action: () => console.log("Add keywords for Privacy Policy Alignment"),
    },
    {
        label: "Third Party Opt-in",
        status: "error",
        keyWord: [],
        action: () => console.log("Add keywords for Third Party Opt-in"),
    },
    {
        label: "Data Collection Practices",
        status: "success",
        keyWord: ["user data", "cookies", "tracking"],
    },
    {
        label: "Purposes of Data Processing",
        status: "success",
        keyWord: ["marketing", "analytics", "personalization"],
    },
    {
        label: "Data Sharing and Disclosure",
        status: "success",
        keyWord: ["third-party", "consent"],
    },
    {
        label: "User Rights and Controls",
        status: "success",
        keyWord: ["opt-out", "access", "deletion"],
    },
    {
        label: "Data Security Measures",
        status: "error",
        keyWord: [],
        action: () => console.log("Add keywords for Data Security Measures"),
    },
    {
        label: "Data Retention",
        status: "success",
        keyWord: ["90 days", "policy retention", "data lifecycle"],
    },
]

interface RightSidePanelProps {
    viewMode?: any
    title?: string
    details?: any
    tabs?: any
    setTabs?: any
    activeTab?: any
    setActiveTab?: any
    label?: any
    profileImg?: any
    stats?: any
    keyValueDataList?: any
    paperTrailDataList?: any
    complianceDetailsList?: any
    consentDetailsList?: any
    labelTwo?: any
    labelValueData?: any
    buttonNameOne?: string
    buttonNameTwo?: string
    buttonTextOne?: string
    buttonTextTwo?: string
    toggleRightSidePanel?: string
    buttonIconLeft?: string
    buttonIconRight?: string
    totalDisputes?: any
    disputesKeyValue?: any
    onSearch?: any,
    toggleTeamModal?: any,
    setTeamDetails?: any,
    setIndex?: any,
    index?: any
    collection?: any
    setDetails?: any
    usersByCompanyId?: any
    purchasesKeyValue?: any
    totalPurchase?: any
    updateCollectionOne?: any
    updateCollectionTwo?: any
    updateData?: any
    updateOnChange?: any
    handleUpdate?: any
    onAddDataInputChange?: any
    addData?: any
    setUpdateData?: any
    viewDetailsBtn?: any
    summaryView?: any
    toggleFileSummary?: any
    showFileSummary?: any
    records?: any
    performaceKeyValue?: any
    showDropDown?: any
    toggleDropDown?: any
    selectedDocument?: any
    setSelectedDocument?: any
    uploadedFile?: any
    setUploadedFile?: any
    onChange?: any
    onClick?: any
    fileInputRef?: any
    keyValueDataListTwo?: any
    keyValueDataListThree?: any
    handleDragOver?: any
    handleDrop?: any
    handleDropFile?: any
    page?: any
    offensiveWordsColumn?: any
    setOffensiveWordsColumn?: any
    showWordsModal?: any
    toggleWordsModal?: any
    buttonOneFunction?: any
    buttonTwoFunction?: any
    deleteModalDescription?: any
    deleteModalTitle?: any
    deleteId?: any
    toggleDeleteModal?: any
    setDeleteBtn?: any
    addOffensiveWord?: any
    collectionTwo ?:any
    coloumn ?: any
    type?: any
    setType?: any
    setColumn?: any     
    onEditIconClick?: any
    rolesCollection?: any
    showKeywordsModal?: any
    toggleKeywordsModal?: any
    handleAddKeyword?: any
    keywordsTableColumns?: any
    setKeywordsTableColumns?: any
    isEditable?: any
    setIsEditable?: any
    editIndex?: any
    setEditIndex?: any
    keywordIndex?: any
    setKeywordIndex?: any
    showDeactivateButton?: any
    toggleDeactivateButton?: any
    activityLogColumns?: any
    activityLogSummaryDataList?: any
    activityLogDateForm?: any
    onActivityLogDateChange?: any
}

export default function RightSidePanel(props: RightSidePanelProps) {   
    console.log(props.collection.items, 'collection')
    return <div 
        className='right-side-panel' 
        onClick={(e) => 
            e.stopPropagation()
        }
    >
        {/* Top section of right side panel */}
        <div className='right-panel-top-row'>
            <div className='right-panel-heading-row'>
                <div className='right-panel-heading'>
                    {props.title}
                </div>
                <button
                    className='right-panel-close-icon'
                    onClick={() => {
                        props.toggleRightSidePanel()
                        props.setIndex(null)
                    }}
                >
                    <img src='close-icon.svg'/>
                </button>
            </div>

            {/* Tabs component */}
            {props.tabs && props.viewMode !== 'add' && Object.keys(props.tabs?.[props?.viewMode] || {}).length > 0 &&  <>
                <Tabs
                    tabs={props.tabs?.[props?.viewMode]}
                    setTabs={props.setTabs}
                    activeTab={props.activeTab}
                    setActiveTab={props.setActiveTab}
                />
                <hr className='light-line'/>
            </>}
        </div>

        {/* Right side panel children Components */}
        <div className='right-panel-children-container'>

            {/* basic_details tab active */}
            {props.activeTab === 'basic_details' && (props.page === 'buyer' || props.page === 'seller') && (
                props.viewMode === 'view'
                    ? <div>
                        <BasicDetailTop
                            label={props.label}
                            profileImg= {props.profileImg}
                            stats={null}
                            mainLabel={props.details?.company_details?.name}
                            subLabel={props.details?.company_details?.ico_number}
                            status={props?.details?.company_details?.approval_status}  
                        />

                        {/* Key Value Data List for Right Side Panel */}
                        {props.keyValueDataList && props.keyValueDataList.length > 0 && (
                            <div className='key-value-section'>
                                {props.keyValueDataList.map((item, index) => (
                                    <KeyValue
                                        key={index}
                                        displayKey={item.displayKey}
                                        value={item.value}
                                        subValue={item.subValue}
                                        name={item.name}
                                    />
                                ))}
                            </div>
                        )}
                        
                        <BasicDetailsBottom
                            label={props.labelTwo}
                            labelValueData={props.labelValueData}
                            toggleTeamDetails={props.toggleTeamModal}
                            setTeamDetails={props.setTeamDetails}
                            usersByCompanyId={props.usersByCompanyId}
                            viewDetailsBtn={props.viewDetailsBtn}
                        />
                        {props.page === 'product' && <hr className='light-line' />}
                    </div>
                    : <div>
                        <BasicDetailEdit
                            updateData={props.updateData}
                            updateOnChange={props.updateOnChange}
                            buyerDetails={props.details}
                            collection={props.collection}
                        />
                    </div>
            )}

            {/* disputes tab is active */}
            {props.activeTab === 'disputes' && (
                props.totalDisputes.length !== 0
                    ? <div>
                        <SummaryHeader
                            label='Total Disputes'
                            count={props.details.total_disputes}
                            search={props.onSearch}
                            updateCollection={props.updateCollectionOne}
                        />
                        <div className='expand-collapse-items'>
                            {props.totalDisputes.map(item => <>
                                <ExpandCollapseSection
                                    item={item}
                                    disputesKeyValue={props.disputesKeyValue}
                                    mainLabelText={item.title}
                                    subTextLabel={item.dispute_reason}
                                    status={item.status}
                                />
                                <hr className='light-line'/>
                            </>)} 
                        </div>
                    </div>
                    : <>
                        <div className='empty-disputes'>
                            <label className='empty-text'>
                                This buyer has not raised any disputes
                            </label>
                        </div>
                    </>
                )
            }

            {/* purchases tab is active */}
            {props.activeTab === 'purchases' &&
                <div>
                    <SummaryHeader
                        label='Total Purchases'
                        count={props.details.total_purchases}
                        search={props.onSearch}
                        updateCollection={props.updateCollectionTwo}
                    />
                    <div className='expand-collapse-items '>
                        {props.totalPurchase?.map(item => <>
                            <ExpandCollapseSection
                                mainLabelText={item.title}
                                subTextLabel={item.description}
                                status={item.status}
                                summaryView={props.summaryView}
                                item={item}
                                disputesKeyValue={props.purchasesKeyValue}
                            />
                            <hr className='light-line' />
                        </>)}
                    </div>
                </div>
            }


            {(props.page === 'buyer' || props.page === 'seller') &&
                props.activeTab === 'user' && props.viewMode === 'edit'
                    ? <div>
                        <UsercDetailEdit 
                            updateData={props.updateData}  
                            updateOnChange={props.updateOnChange}
                            addData={props.addData}
                            viewMode={props.viewMode}
                            deleteModalDescription={props.deleteModalDescription}
                            deleteModalTitle={props.deleteModalTitle}
                            toggleDeleteModal={props.toggleDeleteModal}
                            setDeleteBtn={props.setDeleteBtn}

                        />
                    </div>
                    : props.viewMode === 'add' && (props.page === 'buyer' || props.page === 'seller')
                        ? <div>
                            <UsercDetailEdit
                                updateData={props.updateData}
                                updateOnChange={props.updateOnChange}
                                addData={props.addData}
                                viewMode={props.viewMode}
                            />
                        </div>
                        : null
            }

            {props.activeTab === 'listing' && (
                props.viewMode === 'view'
                    ? <div>
                        {/* disputes tab is active */}
                        <SummaryHeader
                            label='Total Listing'
                            count={props.details.total_listings}
                            search={props.onSearch}
                            updateCollection={props.updateCollectionOne}
                        />
                        <div className='expand-collapse-items'>
                            {props.totalDisputes.map(item => <>
                                <ExpandCollapseSection
                                    item={item}
                                    mainLabelText={item.company_details.name}
                                    subTextLabel={item.company_details.registration_number}
                                    disputesKeyValue={props.disputesKeyValue}
                                    status={item.user_status}
                                    summaryView={props.summaryView}
                                    showFileSummary={props.showFileSummary}
                                    toggleFileSummary={props.toggleFileSummary}
                                    records={props.records}

                                />
                                <hr className='light-line' />
                            </>)}
                        </div>
                    </div>
                    : ''
            )}

            {props.activeTab === 'performance' && (
                props.viewMode === 'view'
                    ? <div className='performance-wrapper'>
                        {/* performance tab is active */}
                        <div className='key-value-section'>
                            {props.performaceKeyValue.map(item =>
                                <KeyValue
                                    displayKey={item.displayKey}
                                    value={item.value}
                                />
                            )}
                        </div>
        
                    </div>
                    : ''
            )}


            {/* Category Page Right side Panel components */}
            {props.page === 'category' &&
                <CategoryEdit
                    details={props.details}
                    updateData={props.updateData}
                    updateOnChange={props.updateOnChange}
                    collection={props.collection}
                    selectedDocument={props.selectedDocument}
                    setSelectedDocument={props.setSelectedDocument}
                    uploadedFile={props.uploadedFile}
                    setUploadedFile={props.setUploadedFile}
                    onChange={props.onChange}
                    onClick={props.onClick}
                    fileInputRef={props.fileInputRef}
                    handleDragOver={props.handleDragOver}
                    handleDrop={props.handleDrop}
                    handleDropFile={props.handleDropFile}
                    viewMode={props.viewMode}
                    page={props.page}
                />
            }
            {props.page === 'sub-category' &&
                <CategoryEdit
                    details={props.details}
                    updateData={props.updateData}
                    updateOnChange={props.updateOnChange}
                    collection={props.collection}
                    selectedDocument={props.selectedDocument}
                    setSelectedDocument={props.setSelectedDocument}
                    uploadedFile={props.uploadedFile}
                    setUploadedFile={props.setUploadedFile}
                    onChange={props.onChange}
                    onClick={props.onClick}
                    fileInputRef={props.fileInputRef}
                    handleDragOver={props.handleDragOver}
                    handleDrop={props.handleDrop}
                    handleDropFile={props.handleDropFile}
                    viewMode={props.viewMode}
                    page={props.page}
                />
            }


            {props.page === 'selection' &&
                <CategoryEdit
                    details={props.details}
                    updateData={props.updateData}
                    updateOnChange={props.updateOnChange}
                    collection={props.collection}
                    selectedDocument={props.selectedDocument}
                    setSelectedDocument={props.setSelectedDocument}
                    uploadedFile={props.uploadedFile}
                    setUploadedFile={props.setUploadedFile}
                    onChange={props.onChange}
                    onClick={props.onClick}
                    fileInputRef={props.fileInputRef}
                    handleDragOver={props.handleDragOver}
                    handleDrop={props.handleDrop}
                    handleDropFile={props.handleDropFile}
                    viewMode={props.viewMode}
                    page={props.page}
                />
            }

            {props.page === 'header' &&
                <CategoryEdit
                    details={props.details}
                    updateData={props.updateData}
                    updateOnChange={props.updateOnChange}
                    collection={props.collection}
                    selectedDocument={props.selectedDocument}
                    setSelectedDocument={props.setSelectedDocument}
                    uploadedFile={props.uploadedFile}
                    setUploadedFile={props.setUploadedFile}
                    onChange={props.onChange}
                    onClick={props.onClick}
                    fileInputRef={props.fileInputRef}
                    handleDragOver={props.handleDragOver}
                    handleDrop={props.handleDrop}
                    handleDropFile={props.handleDropFile}
                    viewMode={props.viewMode}
                    page={props.page}
                />
            }

            {/* Data Type Page Right side Panel components */}
            {props.page === 'data-type' && (
                props.viewMode === 'view'
                    ? <div>
                        <div className='key-value-section'>
                            <KeyValue
                                displayKey='Data Type ID'
                                value={props.details?.reference_id || `DT${String(props.details?.id).padStart(3, '0')}`}
                            />
                            <KeyValue
                                displayKey='Data Type Name'
                                value={props.details?.name || '--'}
                            />
                            <KeyValue
                                displayKey='Description'
                                value={props.details?.description || '--'}
                            />
                            <KeyValue
                                displayKey='Status'
                                value={props.details?.status === 'active' ? 'Active' : replaceUnderScoreWithSpace(props.details?.status) || '--'}
                            />
                        </div>
                    </div>
                    : <div>
                        <div className='edit-wrapper'>
                            <div className='edit-section'>
                                <Input
                                    label='Data Type Name'
                                    name='name'
                                    value={props?.updateData['name'] || ''}
                                    onChange={props.updateOnChange}
                                    className='input-wrapper'
                                    placeholder='Ex: Consumer, Business'
                                />
                            </div>
                            <div className='edit-section'>
                                <Input
                                    label='Description'
                                    name='description'
                                    value={props?.updateData['description'] || ''}
                                    onChange={props.updateOnChange}
                                    className='input-wrapper'
                                    type='textarea'
                                    placeholder='Enter description'
                                />
                            </div>
                            <div className='edit-section'>
                                <SelectField
                                    label='Status'
                                    name='status'
                                    value={props?.updateData['status'] || 'active'}
                                    onChange={props.updateOnChange}
                                    className='input-wrapper'
                                    options={[
                                        { name: 'Active', value: 'active' },
                                        { name: 'Inactive', value: 'inactive' },
                                    ]}
                                />
                            </div>
                        </div>
                    </div>
            )}

            {/* Tags Page Right side Panel components */}
            {props.page === 'tags' && (
                props.viewMode === 'view'
                    ? <div className='key-value-section'>
                        <KeyValue displayKey='Global Type' value={props.details?.global_type || '--'} />
                        <KeyValue displayKey='Template' value={props.details?.template || '--'} />
                        <KeyValue displayKey='Product Name' value={props.details?.product_name || '--'} />
                        <KeyValue displayKey='Field' value={props.details?.field || '--'} />
                        <KeyValue displayKey='Description' value={props.details?.description || '--'} />
                        <KeyValue displayKey='Global Calculation' value={props.details?.global_calculation || '--'} />
                    </div>
                    : <div className='edit-wrapper'>
                        <div className='edit-section'>
                            <Input
                                label='Global Type'
                                name='global_type'
                                value={props?.updateData['global_type'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='company'
                            />
                        </div>
                        <div className='edit-section'>
                            <Input
                                label='Template'
                                name='template'
                                value={props?.updateData['template'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='email'
                            />
                        </div>
                        <div className='edit-section'>
                            <Input
                                label='Product Name'
                                name='product_name'
                                value={props?.updateData['product_name'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='Seller ID'
                            />
                        </div>
                        <div className='edit-section'>
                            <Input
                                label='Field'
                                name='field'
                                value={props?.updateData['field'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='seller_id'
                            />
                        </div>
                        <div className='edit-section'>
                            <Input
                                label='Description'
                                name='description'
                                value={props?.updateData['description'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                type='textarea'
                                placeholder='Company Seller ID Tag'
                            />
                        </div>
                        <div className='edit-section'>
                            <Input
                                label='Global Calculation'
                                name='global_calculation'
                                value={props?.updateData['global_calculation'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='$seller_id'
                            />
                        </div>
                    </div>
            )}

            {/* Keywords Page Right side Panel components */}
            {props.page === 'keywords' && (
                props.viewMode === 'view'
                    ? <div className='review-panel-content-wrapper'>
                        <div className='key-value-section'>
                            <KeyValue 
                                displayKey='Title' 
                                value={props.details?.title || '--'} 
                            />
                        </div>
                        <div className='keywords-view-wrapper'>
                            <div className='review-panel-header'>
                                <div className='key-value-label'>Active Keywords</div>
                                <div className='link-like-button-wrapper'>
                                    <button onClick={props.toggleKeywordsModal} className='link-like-button'>
                                        Add Keyword
                                    </button>
                                    {props.showKeywordsModal &&
                                        <DropList
                                            title='Add New Keywords'
                                            name='tag-input-drop-list'
                                        >
                                            <TagInput
                                                label='Keywords'
                                                toggleWordsModal={props.toggleKeywordsModal}
                                                addOffensiveWord={props.handleAddKeyword}
                                            />
                                        </DropList>
                                    }
                                </div>
                            </div>
                            <div className='offensive-words-table'>
                                {props.details?.keywords && props.details.keywords.length > 0 ? (
                                    props.details.keywords.map((keyword, index) => (
                                        <div key={index} className='keyword-wrapper'>
                                            <div className='keyword-text-wrapper'>
                                                <div className='keyword-text'>{keyword}</div>
                                                <div className='keyword-actions'>
                                                    <div 
                                                        onClick={() => {
                                                            props.setKeywordIndex?.(index)
                                                            props.toggleDeactivateButton?.()
                                                        }} 
                                                        className='dot-wrapper'
                                                    >
                                                        <img src='/more-icon.svg' />
                                                    </div>
                                                </div>
                                                {props.keywordIndex === index && props.showDeactivateButton && (
                                                    <button 
                                                        onClick={() => {
                                                            props.setKeywordIndex?.(null)
                                                            props.toggleDeactivateButton?.()
                                                        }} 
                                                        className='deactivate-action-button'
                                                    >
                                                        Deactivate Keyword
                                                    </button>
                                                )}
                                            </div>
                                            <hr className='light-line' />
                                        </div>
                                    ))
                                ) : (
                                    <div className='no-keywords'>No keywords available</div>
                                )}
                            </div>
                        </div>
                    </div>
                    : props.viewMode === 'add' && <div className='edit-wrapper'>
                        <div className='edit-section'>
                            <Input
                                label='Title Name'
                                name='title'
                                value={props?.updateData['title'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='Ex: Privacy Policy Alignment'
                            />
                        </div>
                        <div className='edit-section'>
                            <KeywordsInput
                                label='Keywords'
                                name='keywords'
                                keywords={props?.updateData['keywords'] || []}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                            />
                        </div>
                    </div>
            )}

            {props.page === 'review' && 
                <ReviewPanelContent
                    labelValueData={props.labelValueData}
                    page={props.page}
                    details={props.details}
                    updateData={props.updateData}
                    updateOnChange={props.updateOnChange}
                    collection={props.collection}
                    viewMode={props.viewMode}
                    search={props.onSearch}
                    label='Offensive Words'
                    offensiveWordsColumn={props.offensiveWordsColumn}
                    setOffensiveWordsColumn={props.setOffensiveWordsColumn}
                    updateCollection={props.updateCollectionOne}
                    toggleWordsModal={props.toggleWordsModal}
                    showWordsModal={props.showWordsModal}
                    addOffensiveWord={props.addOffensiveWord}
                    isEditable={props.isEditable}
                    setIsEditable={props.setIsEditable}
                    editIndex={props.editIndex}
                    setEditIndex={props.setEditIndex}
                    updateCollectionTwo={props.updateCollectionTwo}
                    collectionTwo={props.collectionTwo}
                    column={props.coloumn}
                    onEditIconClick={props.onEditIconClick}
                    setColumn={props.setColumn}

                />    
            }
            {props.page === 'blog' && 
                <BlogPanelContent
                    labelValueData={props.labelValueData}
                    page={props.page}
                    details={props.details}
                    updateData={props.updateData}
                    updateOnChange={props.updateOnChange}
                    collection={props.collectionTwo}
                    viewMode={props.viewMode}
                    search={props.onSearch}
                    label='Category List'
                    offensiveWordsColumn={props.offensiveWordsColumn}
                    setOffensiveWordsColumn={props.setOffensiveWordsColumn}
                    updateCollection={props.updateCollectionTwo}
                    toggleWordsModal={props.toggleWordsModal}
                    showWordsModal={props.showWordsModal}
                    addOffensiveWord={props.addOffensiveWord}
                    isEditable={props.isEditable}
                    setIsEditable={props.setIsEditable}
                    editIndex={props.editIndex}
                    setEditIndex={props.setEditIndex}
                />
            }

            {/* User Page Right side Panel components */}
            {props.page === 'user' && (
                props.viewMode === 'view'
                    ? <>
                        {/* Basic Details Tab */}
                        {props.activeTab === 'basic_details' && (
                            <div>
                                <BasicDetailTop
                                    label={null}
                                    profileImg={props.details?.profile_image || '/admin-dp.svg'}
                                    mainLabel={props.details?.name}
                                    subLabel={props.details?.role_details?.name || props.details?.role}
                                    status={props.details?.status}
                                />
                                <hr className='light-line'/>
                                <div className='key-value-section'>
                                    <KeyValue
                                        displayKey='Employee ID'
                                        value={props.details?.employee_id || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Email'
                                        value={props.details?.email || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Phone Number'
                                        value={props.details?.phone || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Address'
                                        value={props.details?.address || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Joined on'
                                        value={props.details?.joined_on || '--'}
                                    />
                                    <KeyValue
                                        displayKey='NI Number'
                                        value={props.details?.ni_number || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Gender'
                                        value={props.details?.gender || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Date of Birth'
                                        value={props.details?.date_of_birth || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Nationality'
                                        value={props.details?.nationality || '--'}
                                    />
                                </div>
                            </div>
                        )}

                        {/* Activity Log Tab */}
                        {props.activeTab === 'activity_log' && (
                            <div>
                                <div className='activity-log-header'>
                                    <div className='activity-log-title'>Activity Logs</div>
                                    <div className='activity-log-date-range'>
                                        <div className='date-rangeInput-wrapper'>
                                            <DateField 
                                                placeholder='From Date'
                                                name='from_date'
                                                value={props.activityLogDateForm?.from_date || ''}
                                                className='from-date-input-btn'
                                                onChange={props.onActivityLogDateChange}
                                                viewMode='edit'
                                            />
                                            <DateField
                                                placeholder='To Date'
                                                name='to_date'
                                                value={props.activityLogDateForm?.to_date || ''}
                                                className='to-date-input-btn'
                                                onChange={props.onActivityLogDateChange}
                                                viewMode='edit'
                                            />
                                        </div>
                                    </div>
                                </div>
                                {props.details?.activity_logs && props.details.activity_logs.length > 0 ? (
                                    <>
                                        <div className='activity-log-table-wrapper'>
                                            <Table
                                                className='activity-log-table'
                                                items={props.details.activity_logs}
                                                columns={props.activityLogColumns || []}
                                                controlColumns={[]}
                                                loaded={true}
                                                searchParams={new URLSearchParams()}
                                                collection={{ items: props.details.activity_logs }}
                                                updateCollection={() => {}}
                                            />
                                        </div>
                                        {props.activityLogSummaryDataList && props.activityLogSummaryDataList.length > 0 && (
                                            <div className='activity-log-summary'>
                                                <div className='key-value-section'>
                                                    {props.activityLogSummaryDataList.map((item, index) => (
                                                        <KeyValue
                                                            key={index}
                                                            displayKey={item.displayKey}
                                                            value={item.value}
                                                            subValue={item.subValue}
                                                            name={item.name}
                                                        />
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </>
                                ) : (
                                    <div className='empty-activity-log'>
                                        <label className='empty-text'>No activity logs available</label>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Payroll Tab */}
                        {props.activeTab === 'payroll' && (
                            <div>
                                <div className='section-title'>Payroll & Legal Details</div>
                                <div className='key-value-section'>
                                    <KeyValue
                                        displayKey='Salary/Pay Rate'
                                        value={props.details?.payroll?.salary_pay_rate || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Bank Name'
                                        value={props.details?.payroll?.bank_name || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Account Number'
                                        value={props.details?.payroll?.account_number || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Probation Period'
                                        value={props.details?.payroll?.probation_period || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Working Hours'
                                        value={props.details?.payroll?.working_hours || '--'}
                                    />
                                    <KeyValue
                                        displayKey='Holiday Entitlement'
                                        value={props.details?.payroll?.holiday_entitlement || '--'}
                                    />
                                </div>
                            </div>
                        )}
                    </>
                    : <div className='edit-wrapper'>
                        <div className='edit-section'>
                            <Input
                                label='Name'
                                name='name'
                                value={props?.updateData['name'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='Enter name'
                            />
                        </div>
                        <div className='edit-section'>
                            <Input
                                label='Email'
                                name='email'
                                value={props?.updateData['email'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                type='email'
                                placeholder='Enter email'
                            />
                        </div>
                        <div className='edit-section'>
                            <SelectField
                                label='Role'
                                name='id_role'
                                value={props?.updateData['id_role'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                options={props.rolesCollection?.items?.map(role => ({
                                    name: role.name,
                                    value: role.id
                                })) || []}
                            />
                        </div>
                    </div>
            )}

            {/* Role Page Right side Panel components */}
            {props.page === 'role' && (
                props.viewMode === 'view'
                    ? <div className='key-value-section'>
                        <KeyValue
                            displayKey='Role Name'
                            value={props.details?.name || '--'}
                        />
                    <KeyValue
                        displayKey='Permission'
                        value={props.details?.permission || '--'}
                    />
                    </div>
                    : <div className='edit-wrapper'>
                        <div className='edit-section'>
                            <Input
                                label='Role Name'
                                name='name'
                                value={props?.updateData['name'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='Enter role name'
                            />
                        </div>
                        <div className='edit-section'>
                            <Input
                                label='Permission'
                                name='permission'
                                value={props?.updateData['permission'] || ''}
                                onChange={props.updateOnChange}
                                className='input-wrapper'
                                placeholder='Enter permission'
                            />
                        </div>
                    </div>
            )}

            {/* Email Template Page Right side Panel components */}
            {props.page === 'email-template' && (
                props.viewMode === 'view'
                    ? <div className='key-value-section'>
                        {props.keyValueDataList && props.keyValueDataList.map((item, index) => (
                            <KeyValue
                                key={index}
                                displayKey={item.displayKey}
                                value={item.value}
                                subValue={item.subValue}
                                name={item.name}
                            />
                        ))}
                    </div>
                    : <EmailAddView
                        updateData={props.updateData}
                        updateOnChange={props.updateOnChange}
                        viewMode={props.viewMode}
                    />
            )}

            {/* SMS Template Page Right side Panel components */}
            {props.page === 'sms-template' && (
                props.viewMode === 'view'
                    ? <div className='key-value-section'>
                        {props.keyValueDataList && props.keyValueDataList.map((item, index) => (
                            <KeyValue
                                key={index}
                                displayKey={item.displayKey}
                                value={item.value}
                                subValue={item.subValue}
                                name={item.name}
                            />
                        ))}
                    </div>
                    : <SmsAddView
                        updateData={props.updateData}
                        updateOnChange={props.updateOnChange}
                        viewMode={props.viewMode}
                    />
            )}

            {/* Product Page - View Mode */}
            {props.page === 'product' && props.viewMode === 'view' && (
                <>
                    {/* Basic Details Tab */}
                    {props.activeTab === 'basic_details' && (
                        <div>
                            <BasicDetailTop
                                label={props.label}
                                profileImg={props.profileImg}
                                mainLabel={props.details?.name}
                                subLabel={props.details?.data_type}
                                stats={props.stats}
                            />
                            <div className='key-value-section'>
                                {props.keyValueDataList.map((item, index) =>
                                    <KeyValue
                                        key={index}
                                        displayKey={item.displayKey}
                                        value={item.value}
                                        subValue={item.subValue}
                                    />
                                )}
                            </div>
                            <hr className='light-line' />
                            <div className='key-value-section'>
                                <div className='section-title'>Product  Duration & Usage Limit</div>
                                {props.keyValueDataListTwo && props.keyValueDataListTwo.length > 0 && (
                                    <div className='key-value-section'>
                                        {props.keyValueDataListTwo.map((item, index) => (
                                            <KeyValue
                                                key={index}
                                                displayKey={item.displayKey}
                                                value={item.value}
                                                subValue={item.subValue}
                                                name={item.name}
                                            />
                                        ))}
                                    </div>
                                )}
                            </div>
                            {props.details?.product_type === 'DATA_BUNDLE' && 
                                <>
                                    <hr className='light-line' />
                                    <div className='key-value-section'>
                                        <div className='section-title'>Data Validations</div>
                                        {props.keyValueDataListThree && props.keyValueDataListThree.length > 0 && (
                                            <div className='key-value-section'>
                                                {props.keyValueDataListThree.map((item, index) => (
                                                    <KeyValue
                                                        key={index}
                                                        displayKey={item.displayKey}
                                                        value={item.value}
                                                        subValue={item.subValue}
                                                        name={item.name}
                                                    />
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </>
                            }
                        </div>
                    )}

                    {/* Paper Trail Tab */}
                    {props.activeTab === 'paper_trail' && (
                        <>
                            {/* Compliance Details Section */}
                            <div className='paper-trail-section'>
                                <div className='section-title'>Compliance Details</div>
                                <div className='key-value-section'>
                                    {props.complianceDetailsList && props.complianceDetailsList.map((item, index) => (
                                        <div key={index} className='key-values-wrapper'>
                                            <div className='key-value-label'>
                                                {item.displayKey}
                                            </div>
                                            <div className='key-value-value'>
                                                {item.isLink ? (
                                                    <Link 
                                                        href={item.value} 
                                                        target='_blank' 
                                                        className='link-like-button'
                                                        onClick={(e) => e.stopPropagation()}
                                                    >
                                                        {item.value}
                                                    </Link>
                                                ) : (
                                                    <span>{item.value}</span>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                            
                            {props.details?.product_type === 'DATA_BUNDLE' && 
                                <>
                                    <hr className='light-line' />
                                    {/* Consent Details Section */}
                                    <div className='paper-trail-section'>
                                        <div className='section-title'>Consent Details</div>
                                        <div className='key-value-section'>
                                            {props.consentDetailsList && props.consentDetailsList.map((item, index) => (
                                                <div key={index} className='key-values-wrapper'>
                                                    <div className='key-value-label'>
                                                        {item.displayKey}
                                                    </div>
                                                    <div className='key-value-value'>
                                                        {item.isLink ? (
                                                            <Link 
                                                                href={item.value} 
                                                                target='_blank' 
                                                                className='link-like-button'
                                                                onClick={(e) => e.stopPropagation()}
                                                            >
                                                                {item.value}
                                                            </Link>
                                                        ) : (
                                                            <span>{item.value}</span>
                                                        )}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </>
                            }
                            <hr className='light-line' />
                            
                            {/* Validation Checks Section */}
                            <div className='paper-trail-section'>
                                <div className='section-title'>Validation Checks</div>
                                <div className='key-value-section'>
                                    {props.paperTrailDataList && props.paperTrailDataList.map((item, index) => {
                                        const isPassed = item.status === 'PASSED'
                                        const isYes = item.status === 'YES'
                                        const showCheckmark = isPassed || isYes
                                        return (
                                            <div key={index} className='key-values-wrapper'>
                                                <div className='key-value-label'>
                                                    {item.displayKey}
                                                </div>
                                                <div className='key-value-value validation-status'>
                                                    <span>{item.value}</span>
                                                    {showCheckmark && (
                                                        <img 
                                                            className='validation-check-icon' 
                                                            src='/green-check.svg' 
                                                            alt='check'
                                                        />
                                                    )}
                                                </div>
                                            </div>
                                        )
                                    })}
                                </div>
                            </div>
                            {props.details?.product_type === 'DATA_BUNDLE' && 
                                <>
                                    <hr className='light-line' />
                                    
                                    {/* Licensing Details Section */}
                                    <div className='paper-trail-section'>
                                        <div className='section-title'>Licensing Details</div>
                                        <div className='licensing-table-wrapper'>
                                            {props.collection?.items && props.collection.items.length > 0 ? (
                                                <table className='licensing-table'>
                                                    <thead>
                                                        <tr>
                                                            <th>TPS Check</th>
                                                            <th>Company</th>
                                                            <th>Licensed</th>
                                                            <th>Licensed on</th>
                                                            <th>Expired on</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {props.collection.items.map((item, index) => {
                                                            const formatDate = (dateString) => {
                                                                if (!dateString) return '--'
                                                                const date = new Date(dateString)
                                                                if (Number.isNaN(date.getTime())) return '--'
                                                                return date.toLocaleDateString('en-GB', {
                                                                    day: 'numeric',
                                                                    month: 'short',
                                                                    year: 'numeric',
                                                                })
                                                            }

                                                            return (
                                                                <tr key={index}>
                                                                    <td>{replaceUnderScoreWithSpace(item?.tps_check_status || item?.status) || 'Passed'}</td>
                                                                    <td>{shortenText(item?.name)|| '--'}</td>
                                                                    <td>{item?.license_period_months || '--'}</td>
                                                                    <td>{formatDate(item?.licensed_on || item?.license_date || item?.start_date || item?.created_at)}</td>
                                                                    <td>{formatDate(item?.expired_on || item?.expiry_date || item?.end_date)}</td>
                                                                </tr>
                                                            )
                                                        })}
                                                    </tbody>
                                                </table>
                                            ) : (
                                                <div className='no-data-message'>
                                                    No licensing details available
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </>
                            }
                        </>
                    )}

                    {/* Source Tab - Checklist Component */}
                    {props.activeTab === 'source' && (
                        <Checklist
                            title='Policy Compliance'
                            subtitle='Uploaded Date'
                            text='Last Updated'
                            subtitleText='Date Info'
                            items={productPolicyComplianceData}
                            showKeywordsModal={props.showKeywordsModal}
                            toggleKeywordsModal={props.toggleKeywordsModal}
                            handleAddKeyword={props.handleAddKeyword}
                        />
                    )}
                </>
            )}

            {/* Product Page - Edit Mode */}
            {props.page === 'product' && props.viewMode === 'edit' && <>
                {/* Basic Details Tab */}
                <BasicDetailTop
                    label={props.label}
                    profileImg={props.profileImg}
                    mainLabel={props.details?.name}
                    subLabel={props.details?.data_type}
                    stats={null}
                />

                <SelectField
                    label='Status'
                    name='status'
                    value={props.details?.status}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    options={props.collection.loaded
                        ? getOptions([...new Set(props.collection.items.map(item => item?.status))]
                            .map(status => ({ status })), 'status', 'status')
                        : []
                    }
                />

                {props.details?.status === 'REJECTED' && 
                    <SelectField 
                        label='Rejection Reason'
                        name='rejection_reason'
                        value={props.details?.rejection_reason}
                        onChange={props.updateOnChange}
                        className='input-wrapper'
                        options={props.collection.loaded
                            ? getOptions([...new Set(props.collection.items.map(item => item?.rejection_reason))]
                                .map(rejection_reason => ({ rejection_reason })), 'rejection_reason', 'rejection_reason')
                            : []
                        }
                    />
                }

                <Checklist
                    title='Source Details'
                    subtitle='Source URL'
                    text='Source URL'
                    subtitleText='Date Info'
                    items={productPolicyComplianceData}
                    showKeywordsModal={props.showKeywordsModal}
                    toggleKeywordsModal={props.toggleKeywordsModal}
                    handleAddKeyword={props.handleAddKeyword}
                />
            </>}
        </div>
        <hr className='light-line' />

        {/* Right panel bottom section */}
        {props.buttonNameOne && <RightSidePanelBottomSection
            buttonNameOne={props.buttonNameOne}
            buttonNameTwo={props.buttonNameTwo}
            buttonTextOne={props.buttonTextOne}
            buttonTextTwo={props.buttonTextTwo}
            buttonIconLeft={props.buttonIconLeft}
            buttonIconRight={props.buttonIconRight}
            setIndex={props.setIndex}
            index={props.index}
            collection={props.collection}
            setDetails={props.setDetails}
            viewMode={props.viewMode}
            handleUpdate={props.handleUpdate}
            toggleRightSidePanel={props.toggleRightSidePanel}
            setUpdateData={props.setUpdateData}
            page={props.page}
            activeTab={props.activeTab}
            buttonOneFunction={props.buttonOneFunction}
            buttonTwoFunction={props.buttonTwoFunction}
        />}
    </div>
}

interface BasicDetailTopProps {
    label?: any
    profileImg?: any
    stats?: any
    mainLabel?: any
    subLabel?: any
    status?: any
}

function BasicDetailTop(props: BasicDetailTopProps) {
    return <div className='basic-details-wrapper'>
        {props.label && 
            <div className='basic-details-top-section'>
                {props.label}
            </div>
        }
        <div className='basic-details-middle-section'>
            <div className='basic-details-middle-top'>
                <div className='basic-details-middle-left'>
                    {props.profileImg && 
                        <div className='profile-image-wrapper'>
                            <img 
                                className='company-icon' 
                                src={props.profileImg} 
                            />
                        </div>
                    }
                    <div className='basic-details-middle-text'>
                        <div className='basic-details-middle-main-label-wrapper'>
                            <div className='basic-details-middle-main-label'>
                                {props.mainLabel}
                            </div>
                            <div className='status-icon-wrapper'>
                                {props.status === 'APPROVED' 
                                    ? <img className='status-icon' src='/green-check.svg'/> 
                                    : ''
                                }
                            </div>
                        </div>
                        <div className='basic-details-middle-sub-label'>
                            {props.subLabel}
                        </div>
                    </div>
                </div>
                <div className='basic-details-middle-right'>
                    <div className='basic-details-status'>
                        <div 
                            className={
                                `status-right-${
                                    props.status === 'APPROVED' || props.status === 'Active'
                                        ? 'green'
                                        : props.status === 'PENDING_APPROVAL' 
                                            ? 'grey'
                                            : props.status === 'NOT_VERIFIED'
                                                ? 'red'
                                                : ''
                                }`
                            }
                        >
                            {replaceUnderScoreWithSpace(props.status)}
                        </div>
                    </div>
                </div>
            </div>
            {props.stats && 
                <div className='basic-details-middle-bottom'>
                    <div className='bar-wrapper'>
                        <img src='/chart.svg'/>
                        <div className='bar-value'>
                            {props.stats.bar}
                        </div>
                    </div>
                    <div className='likes-wrapper'>
                        <img src='/heart.svg'/>
                        <div className='likes-value'>
                            {props.stats.likes}
                        </div>
                    </div>
                    <div className='rating-wrapper'>
                        <img src='/star.svg'/>
                        <div className='rating-value'>
                            {props.stats.rating}
                        </div>
                    </div>
                </div>
            }
        </div>
    </div>
}

interface BasicDetailsBottomProps {
    label?: any
    labelValueData?: any
    toggleTeamDetails?: any
    setTeamDetails?: any
    usersByCompanyId?: any
    viewDetailsBtn?: any
}

function BasicDetailsBottom(props: BasicDetailsBottomProps) {
    
    return <div className='basic-details-bottom-section'>
        <div className='basic-details-bottom-top-section'>
            <div className='basic-details-bottom-top-label'>
                {props.label}
            </div>
            {props.viewDetailsBtn &&
                <button 
                    onClick={props.toggleTeamDetails} 
                    className='link-like-button'
                >
                    View Details
                </button>
            }
        </div>
        <div className='key-value-section'>
            {props.usersByCompanyId.map(item => <KeyValue
                displayKey={item.name || item.displayKey}
                value={item.email || item.value}
                name={
                    item.property === 'phone' || item.property === 'position' 
                        ? '' 
                        : 'strong'
                }
            />)}
        </div>
    </div>
}

interface RightSidePanelBottomSectionProps {
    buttonNameOne?: string
    buttonNameTwo?: string
    buttonTextOne?: string
    buttonTextTwo?: string
    buttonIconLeft?: string
    buttonIconRight?: string
    setIndex?: any,
    index?: any,
    collection?: any
    setDetails?: any
    viewMode?: any
    handleUpdate?: any
    toggleRightSidePanel?: any
    setUpdateData?: any
    page?: any
    activeTab?: any
    buttonOneFunction?: any
    buttonTwoFunction?: any
}

function RightSidePanelBottomSection(props: RightSidePanelBottomSectionProps) {

    console.log(props.viewMode, 'viewmode')

    const length = props.collection?.items?.length || 0 

    return <div className={`panel-bottom-section-wrapper ${props.activeTab === 'user' ? 'add-view' : ''}`}>
        {/* Export Keywords button for keywords page in view mode */}
        {props.viewMode === 'view' && props.page === 'keywords' && props.activeTab !== 'user' &&
            <button 
                onClick={(e) =>  {
                    e.stopPropagation()
                    props.buttonOneFunction?.(e)
                }}
                className='with-bg-btn'
            >
                <div className='button-text'>
                    {props.buttonTextOne}
                </div>
            </button>
        }
        {/* Previous/First button for other pages */}
        {(props.viewMode === 'edit' || props.viewMode === 'add' || (props.viewMode === 'view' && props.page !== 'keywords')) && props.activeTab !== 'user' &&
            <button 
                disabled={props.index === 0}
                onClick={(e) =>  {
                    e.stopPropagation()
                    props.buttonOneFunction?.(e)
                }}
                className={`${props.buttonNameOne} ${props.index === 0 ? 'disable' : ''}`}
            >
                {props.buttonIconLeft && props.viewMode !== 'edit' && props.viewMode !== 'add' &&
                    <img className='arrow-left-icon' src={props.buttonIconLeft} />
                }
                <div className='button-text'>
                    {props.buttonTextOne}
                </div>
            </button>
        }
        {/* Second button (Next/Save) - hidden for keywords page in view mode only */}
        {(props.page !== 'keywords' || props.viewMode === 'edit' || props.viewMode === 'add') && props.activeTab !== 'user' &&
            <button 
                disabled={props.page === 'keywords' ? false : length - 1 === props.index}
                onClick={(e) => {
                    e.stopPropagation()
                    props.buttonTwoFunction?.(e)
                }}
                className={`
                    ${ props.viewMode === 'edit' || props.viewMode === 'add'
                        ? 'with-bg-btn' 
                        : props.buttonNameOne
                    } 
                    ${props.page !== 'keywords' && length - 1 === props.index 
                        ? 'disable' 
                        : ''
                    }
                `}
            >
                <div className='button-text'>
                    {props.buttonTextTwo}
                </div>
                {props.buttonIconRight && props.viewMode !== 'edit' && props.viewMode !== 'add' &&
                    <img className='arrow-right-icon' src={props.buttonIconRight} />
                }            
            </button>
        }
    </div>
}

interface SummaryHeaderProps {
    label?: any
    count?: any
    search?: any
    updateCollection?: any
}

function SummaryHeader(props: SummaryHeaderProps) {
    return <div className='summary-header-wrapper'>
        <div className='summary-header-left'>
            <div className='main-label'>{props.label}</div>
            <div className='total-count'>{props.count}</div>
        </div>
        <div className='summary-header-right'>
            {props.search && <input
                id='search-input'
                type='text'
                className='search-input'
                placeholder='Search'
                onChange={e => props.search(e.target.value, props.updateCollection)}
            />}
        </div>
    </div>
}

interface BasicDetailEditProps {
    updateData?: any
    updateOnChange?: any
    buyerDetails?: any
    collection?: any

}

function BasicDetailEdit(props: BasicDetailEditProps) {
    const list = props.collection?.items.map(item => item?.company_details?.approval_status)
    const uniqueList = [...new Set(list)]
    console.log(props.updateData['country'], 'place')
    return <div className='edit-wrapper'>
        <div className="edit-section">
            <Input
                label='First Name'
                name='first_name'
                value={props?.updateData['first_name']}
                onChange={props.updateOnChange}
                className='input-wrapper'

            />
            <Input
                label='Last Name'
                name='last_name'
                value={props?.updateData['last_name']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Email'
                name='email'
                value={props?.updateData['email']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Phone'
                name='phone'
                value={props?.updateData['phone']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Company Name'
                name='name'
                value={props?.updateData['company_name']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Company Registration No'
                name='company_reg_no'
                value={props?.updateData['company_registration_no']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Address'
                name='address'
                value={props?.updateData['address']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label=' '
                name='place'
                value={props?.updateData['place']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
            <SelectField
                label=''
                name='city'
                placeholder={[props?.updateData['city']]}
                options={[
                    { name: 'London', value: 'london' },
                    { name: 'Manchester', value: 'manchester' },
                    { name: 'Birmingham', value: 'birmingham' },
                    { name: 'Edinburgh', value: 'edinburgh' },
                    { name: 'Glasgow', value: 'glasgow' },
                    { name: 'Cardiff', value: 'cardiff' },
                    { name: 'Belfast', value: 'belfast' },
                    { name: 'Cambridge', value: 'cambridge' },
                    { name: 'Oxford', value: 'oxford' },
                    { name: 'Liverpool', value: 'liverpool' }
                ]}
                value={props?.updateData['city']}
                onChange={props.updateOnChange}
                className='input-wrapper'
                viewMode='edit'
            />
        </div>
        <div className="edit-section">
            <Input
                label=''
                name='pincode'
                value={props?.updateData['pincode']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
            <SelectField
                label=''
                name='country'
                placeholder={[props?.updateData['country']]}
                options={[
                    { name: 'United Kingdom', value: 'united_kingdom' },
                    { name: 'United States', value: 'united_states' },
                    { name: 'Canada', value: 'canada' },
                    { name: 'Australia', value: 'australia' },
                    { name: 'France', value: 'france' },
                    { name: 'Germany', value: 'germany' },
                    { name: 'Japan', value: 'japan' },
                    { name: 'India', value: 'india' },
                    { name: 'United Arab Emirates', value: 'united_arab_emirates' },
                    { name: 'Saudi Arabia', value: 'saudi_arabia' },
                    { name: 'Egypt', value: 'egypt' },
                    { name: 'South Africa', value: 'south_africa' }
                ]}
                value={props?.updateData['country']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Company website'
                name='name'
                value={props?.updateData['company_website']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Business Category'
                name='name'
                value={props?.updateData['business_category']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />  
        </div>
        <div className="edit-section">
            <Input
                label='Company Phone'
                name='company_phone'
                value={props?.updateData['company_phone']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Company Postion'
                name='name'
                value={props?.updateData['company_position']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='ICNO No'
                name='name'
                value={props?.updateData['icno_no']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
        <SelectField
                label='Status'
                name='status'
                placeholder={props?.updateData['status']}
                value={props?.updateData['status']}
                onChange={props.updateOnChange}
                className='input-wrapper'
                options={props.collection.loaded
                    ? getOptions([...new Set(props.collection.items.map(item => replaceUnderScoreWithSpace(item?.company_details?.approval_status)))]
                        .map(status =>  ({status})), 'status', 'status')
                    : []
                }
            />
        </div>

    </div>
}

interface UserDetailEditProps {
    updateData?: any
    updateOnChange?: any
    addData?: any
    viewMode?: any
    deleteModalDescription?: any
    deleteModalTitle?: any
    toggleDeleteModal?: any
    setDeleteBtn?: any
}

function UsercDetailEdit(props: UserDetailEditProps) {
    console.log(props.updateData, props.viewMode,  'updateData')
    return <div className='edit-wrapper'>
        <div className="edit-section">
            <Input
                label='First Name'
                name='name'
                value={props?.updateData['name']}
                onChange={props.updateOnChange}
                className='input-wrapper'

            />
            <Input
                label='Last Name'
                name='name'
                value={props?.updateData['name']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        <div className="edit-section">
            <Input
                label='Email'
                name='email'
                value={props?.updateData['email']}
                onChange={props.updateOnChange}
                className='input-wrapper'
            />
        </div>
        {props.viewMode !== 'add' && <>
            <div className="edit-section">
                <Input
                    label='Company Postion'
                    name='name'
                    value={props?.updateData['company_position']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                />
            </div>
            
            <div className='button-wrapper'>
                <button
                onClick={() => {
                    props.deleteModalDescription('Are you sure, want to remove this user')
                    props.deleteModalTitle('Remove User')
                    props.setDeleteBtn('Remove')
                    props.toggleDeleteModal()

                }}
                className='status-no-bg red-no-bg'>
                    Remove User
                </button>
            </div>
        </>}
    </div>
}

interface CategoryEditProps {
    details?: any
    updateData?: any
    updateOnChange?: any
    buyerDetails?: any
    collection?: any
    selectedDocument?: any
    setSelectedDocument?: any 
    uploadedFile?: any
    setUploadedFile?: any
    onChange?: any
    onClick?: any
    fileInputRef?: any 
    handleDragOver?: any
    handleDrop?: any
    handleDropFile?: any
    viewMode?: any
    page?: any
}

function CategoryEdit (props: CategoryEditProps) {
    console.log(props.page, 'page')
    return <div className='edit-wrapper'>
        {(
            props.page === 'category' ||
            props.page === 'sub-category' ||
            props.page === 'selection' ) &&
            <div className="edit-section">
                <SelectField
                    label='Data Type'
                    name='data_type'
                    value={props?.updateData['data_type']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    options={props.collection.loaded
                        ? getOptions([...new Set(props.collection.items.map(item => item?.data_type_details?.name))]
                            .map(name => ({ name })), 'name', 'name')
                        : []
                    }
                />
            </div>
        }

        {props.page === 'header' && <>
            <div className='edit-section'>
                <SelectField
                    label='Select Category'
                    name='status'
                    value={props?.updateData['status']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    options={props.collection.loaded
                        ? getOptions([...new Set(props.collection.items.map(item => item?.status))]
                            .map(status => ({ status })), 'status', 'status')
                        : []
                    }
                />
            </div>

            <div className="edit-section">
                <Input
                    label='Header Name'
                    name='category_name'
                    value={props?.updateData['category_name']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: First name'
                />
            </div>
            <div className="edit-section">
                <Input
                    label='Description'
                    name='category_name'
                    type='textarea'
                    value={props?.updateData['category_name']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Description'
                />
            </div>
        </>}


        {props.page === 'category' && 
            <div className="edit-section">
                <Input
                    label='Category Name'
                    name='category_name'
                    value={props?.updateData['category_name']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: residental data'
                />
            </div>
        }

        {props.page === 'sub-category' && <>
            <div className="edit-section">
                <SelectField
                    label='Select Category'
                    name='category_name'
                    value={props?.updateData['category_name']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    options={props.collection.loaded
                        ? getOptions([...new Set(props.collection.items.map(item => item?.category_details.name))]
                            .map(name => ({ name })), 'name', 'name')
                        : []
                    }
                />
            </div>
            <div className="edit-section">
                <Input
                    label='Sub Category Name'
                    name='sub_category_name'
                    value={props?.updateData['sub_category_name']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: residental data'
                />
            </div>
        </>}

        {props.page === 'selection' && <>
            <div className="edit-section">
                <SelectField
                    label='Select Category'
                    name='category_name'
                    value={props?.updateData['category_name']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    options={props.collection.loaded
                        ? getOptions([...new Set(props.collection.items.map(item => item.category_details.name,))]
                            .map(name => ({ name })), 'name', 'name')
                        : []
                    }
                />
            </div>
            <div className="edit-section">
                <SelectField
                    label='Select Sub Category'
                    name='sub_category_name'
                    value={props?.updateData['sub_category_name']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    options={props.collection.loaded
                        ? getOptions([...new Set(props.collection.items.map(item => item?.sub_category_details.name))]
                            .map(name => ({ name })), 'name', 'name')
                        : []
                    }
                />
            </div>
            <div className="edit-section">
                <Input
                    label='Selection Name'
                    name='selections'
                    value={props?.updateData['selections']}
                    onChange={props.updateOnChange}
                    className='input-wrapper'
                    placeholder='Ex: residental data'
                />
            </div>
        </>}
        
        {(
            props.page === 'category' || 
            props.page === 'sub-category' || 
            props.page === 'selection') &&
            <div className='edit-section'>
                <ImageUpload
                    selectedDocument={props.selectedDocument}
                    setSelectedDocument={props.setSelectedDocument}
                    uploadedFile={props.uploadedFile}
                    setUploadedFile={props.setUploadedFile}
                    onChange={props.onChange}
                    onClick={props.onClick}
                    fileInputRef={props.fileInputRef}
                    handleDragOver={props.handleDragOver}
                    handleDrop={props.handleDrop}
                    handleDropFile={props.handleDropFile}
                    details={props.details}
                />
            </div>
        }
    </div>
}