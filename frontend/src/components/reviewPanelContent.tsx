'use client'

import { SelectField } from './form'

import { getOptions } from '@/helpers'

import Table from './table'
import { link } from 'fs'
import DropList from './dropList'
import TagInput from './tagInput'
import useToggle from '@/hooks/useToggle'
import KeyValue from './keyValue'

interface ReviewPanelContentProps {
    page?: any
    label?: any
    details?: any
    search?: any
    viewMode?: any
    collection?: any
    updateData?: any
    showWordsModal?: any
    updateOnChange?: any
    toggleWordsModal?: any
    addOffensiveWord?: any
    updateCollection?: any
    labelValueData?: any
    offensiveWordsColumn?: any
    setOffensiveWordsColumn?: any
    isEditable ?: any
    setIsEditable?: any
    editIndex?: any
    setEditIndex?: any
    updateCollectionTwo?: any
    collectionTwo?: any
    column?: any
    setColumn?: any
    onEditIconClick?: any
}

export default function ReviewPanelContent(props: ReviewPanelContentProps) {
    console.log(props.labelValueData, 'labelvaluedata')
    return <div className='review-panel-content-wrapper'>
        {props.viewMode === 'view' &&
            <div className='key-value-section'>
                {props.labelValueData.map(item => 
                    <div className='key-values-wrapper'>
                        <div className={'key-value-label'}>
                            {item.displayKey}
                        </div>
                        <div className={'key-value-value'}>
                            {item.value}
                        </div>
                    </div>
                )}
            </div>  
        }
        {props.viewMode === 'edit' && <div className='review-panel-edit-view'>
            <div className='key-value-section'>
                {props.labelValueData.map(item =>
                    <KeyValue
                        displayKey={item.displayKey}
                        value={item.value}
                    />
                )}
            </div>
            <div className='edit-wrapper'>
                <div className="edit-section">
                    <SelectField
                        label='Status'
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
            </div>
        </div>}
        {props.viewMode === 'add' && <div>
            <div className='review-panel-header'>
                {props.search && <input
                    id='search-input'
                    type='text'
                    className='search-input'
                    placeholder='Search'
                    onChange={e => props.search(e.target.value, props.updateCollection)}
                />}
                <div className='link-like-button-wrapper'>
                    <button onClick={props.toggleWordsModal} className='link-like-button'>
                        Add New Word
                    </button>
                    {props.showWordsModal &&
                        <DropList
                            title='Add New Words'
                            name='tag-input-drop-list'
                        >
                            <TagInput
                                label={props.label}
                                toggleWordsModal={props.toggleWordsModal}
                                addOffensiveWord={props.addOffensiveWord}
                            />
                        </DropList>
                    }
                </div>
            </div>
            <div className='offensive-words-table'>
                <Table
                    items={props.collectionTwo.items}
                    columns={props.offensiveWordsColumn}
                    controlColumns={[]}
                    loaded={props.collectionTwo.loaded}
                    searchParams={props.collectionTwo.searchParams}
                    collection={props.collectionTwo}
                    updateCollection={props.updateCollectionTwo}
                    isEditable={props.isEditable}
                    className='offensive-words-table'
                    onEditIconClick={props.onEditIconClick}
                    editIndex={props.editIndex}
                    setIsEditable={props.setIsEditable}
                />
            </div>
        </div>}
    </div>
}