import { useRef, useState } from 'react'

import { DateField, SelectField } from './form';

import { getEventValue, useForm } from '@/hooks/useForm'

import SliderButton from './sliderButton';
import DropDown from './dropDown';
import DropList from './dropList';
import { getOptions, replaceUnderScoreWithSpace } from '@/helpers';

interface FilterDropListProps {
    quickFilter?: any
    toggleFilterDropList?: any
    showFilterDropList?: any
    isDateDropList?: any
    isDateInput?: any
    collection?: any
    currentFilterData?: any
    sliderFilter?: any
    updateCollection?: any
    updateData?: any
    name?: any
}

const initialFromAndToDate = {
    from_date: '',
    to_date: '',
    status: ''
}

export default function FilterDropList(props: FilterDropListProps) {
    // Set the from and to date 
    const [
        inputDateForm,
        setInputDateForm,
        onInputDateChange,
        onInputDateError,
        setInputDateError
    ] = useForm(initialFromAndToDate)

    return <DropList
        name={props.name}
        title='Filters'
        showDropList={props.showFilterDropList}
        toggleDropList={props.toggleFilterDropList}
    > 
    <div className='quick-filter-section'>
        <div className='filter-heading-wrapper'>
            <div className='heading-label'>
                Quick Filter
            </div>
            <button className='clear-btn'>Clear</button>
        </div>
        <div className='quick-filter-items'>
            {props.quickFilter.map((item, index) => 
                <div className='quick-filter'>
                    <label className='quick-filter-label'>
                        {item.label}
                        <SliderButton 
                            index={index}
                            itemKey={item.key}
                            currentFilterData={props.currentFilterData}
                            onClick={props.sliderFilter}
                            updateCollection={props.updateCollection}
                        />
                    </label>
                </div>
            )}
        </div>
        <div className='filter-heading-wrapper'>
            <div className='heading-label'>
                Signed up
            </div>
            <button className='clear-btn'>Clear</button>
        </div>
        <div className='signed-up-filter-items'>
            <div className='date-input-wrapper'>
                {props.isDateDropList &&
                    <div class="date-range">
                        <div className='date-drop-list-wrapper'>
                            <button className='drop-list-btn'>
                                Last Week
                                <img src='/down-icon.svg' />
                            </button>
                        </div>
                    </div>
                }
                {props.isDateInput &&
                    <div className="date-range">
                        <div className='date-rangeInput-wrapper'>
                            <DateField
                                placeholder='From Date'
                                name='from_date'
                                value={inputDateForm.from_date}
                                className='from-date-input-btn'
                                onChange={onInputDateChange}
                                // error={props.error[`${props.name}.payment_date`]}
                                // viewMode={props.viewMode}
                                viewMode='edit'
                                component='filter'

                            />
                            <DateField
                                placeholder='To Date'
                                name='to_date'
                                value={inputDateForm.to_date}
                                className='to-date-input-btn'
                                onChange={onInputDateChange}
                                // error={props.error[`${props.name}.payment_date`]}
                                viewMode='edit'
                                component='filter'
                            />
                        </div>
                    </div>
                } 
            </div>
        </div>
        <div className='filter-heading-wrapper'>
            <div className='heading-label'>
                Status
            </div>
            <button className='clear-btn'>Clear</button>
        </div>
        <div className='drop-down-wrapper'>
            <SelectField
                placeholder='All Status'
                name='status'
                value={inputDateForm.status}
                onChange={onInputDateChange}
                className='input-wrapper'
                options={props.collection.loaded
                    ? getOptions([...new Set(props.collection.items.map(item => replaceUnderScoreWithSpace(item?.company_details?.approval_status)))]
                        .map(status => ({ status })), 'status', 'status')
                    : []
                }
            />
        </div>
        <div className='action-button-wrapper'>
            <button className='without-bg-btn'>
                Reset
            </button>
            <button className='with-bg-btn'>
                Apply
            </button>
        </div>
    </div>

    </DropList>
}

