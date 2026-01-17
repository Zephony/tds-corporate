'use client'

import {useRef, useState, useEffect} from 'react'
import { DateField } from './form'
import { useForm } from '@/hooks/useForm'
import DropList from './dropList'
import useToggle from '@/hooks/useToggle'

interface StatsProps {
    title?: string
    statValues?: any
    isDateDropList?: any
    isDateInput?: any
}

const initialFromAndToDate = {
    from_date:'',
    to_date:''
}

export default function Stats(props: StatsProps) {
    // Set the from and to date 
    const [
        inputDateForm, 
        setInputDateForm, 
        onInputDateChange, 
        onInputDateError,
        setInputDateError
    ] = useForm(initialFromAndToDate)

    const [showManageStats, toggleManageStats] = useToggle()

    const inputRefFrom = useRef()
    const inputRefTo = useRef()

    const [fromDate, setFromDate] = useState()
    const [toDate, setToDate] = useState()

    const onFromClick = () => {
        inputRefFrom.current?.showPicker();
    }

    const onToClick = () => {
        inputRefTo.current?.showPicker();
    }

    useEffect(() => {
        // console.log('Updated date form:', inputDateForm);
        // Do something after it updates
    }, [inputDateForm]); 

    const activeStateValues= props.statValues.filter(item => item.isActive === true)

    return <div className='stats-container'>
        <div className='stats-top-row'>
            <div className='stats-title'>Stats</div>
            <div className='stats-right'>
                <div className='manage-cards-and-droplist'>
                    <button className='manage-cards' onClick={toggleManageStats}>
                        Manage stats
                    </button>
                    {showManageStats && <ManageStatsDropList
                        mainStats={props.statValues}
                        toggleManageStats={toggleManageStats}
                        showManageStats={showManageStats}
                        name='link'
                    />}
                </div>

                <div className='date-input-wrapper'>
                    {props.isDateDropList && 
                        <div class="date-range">
                            <div className='date-droplist-wrapper'>
                                <button className='droplist-btn'>
                                    Last Week
                                    <img src='/down-icon.svg'/>
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

                                />
                                <DateField
                                    placeholder='To Date'
                                    name='to_date'
                                    value={inputDateForm.to_date}
                                    className='to-date-input-btn'
                                    onChange={onInputDateChange}
                                // error={props.error[`${props.name}.payment_date`]}
                                    viewMode='edit'
                                />
                            </div> 
                        </div>
                    } 
                    {/* {props.isDateInput &&
                        <div className="date-range">
                            <div className='date-drop-input-wrapper'>
                                <button 
                                    className='drop-input-btn' 
                                    onClick={() => onFromClick()}
                                >
                                    <label className='from'>
                                        {fromDate ? fromDate : 'From Date'}
                                    </label>
                                    <img src='/calender.svg' />
                                    <input 
                                        onChange={(e) => 
                                            setFromDate(e.target.value)
                                        } 
                                        ref={inputRefFrom} 
                                        className='hidden-input-from' 
                                        type='date' 
                                    />
                                </button>
                                <button 
                                    className='drop-input-btn' 
                                    onClick={() => onToClick()}
                                >
                                    <label className='to'>
                                        {toDate ? toDate : 'To Date'}
                                    </label>
                                    <img src='/calender.svg' />
                                    <input 
                                        onChange={(e) => 
                                            setToDate(e.target.value)
                                        } 
                                        ref={inputRefTo} 
                                        className='hidden-input-to' 
                                        type='date' 
                                    />
                                </button>
                            </div>
                        </div>
                    } */}
                </div>
            </div>
        </div>
        <div className='stats-cards-wrapper'>
            {activeStateValues.map((item, index) =>
                <StatsCard
                    key={index}
                    index={index}
                    mainLabel={item.mainLabel}
                    mainValue={item.mainValue}
                    subLabel={item.subLabel}
                    subValue={item.subValue}
                />
            )}
        </div>
    </div>    
}

function StatsCard(props) {
    return <div 
        key={props.index}
        className='stats-card'
    >
        <div className='stats-card-left'>
            <div className='main-label'>
                {props.mainLabel}
            </div>
            <div className='main-value'>
                {props.mainValue}
            </div>
        </div>
        <div className='stats-card-right'>
            <div className='sub-label'>
                {props.subLabel}
            </div>
            <div className='sub-value'>
                {props.subValue}
            </div>
        </div>
    </div>
}

function ManageStatsDropList(props) {
    const activeStats = props.mainStats.filter(item => item.isActive === true)
    const inActiveStats = props.mainStats.filter(item => item.isActive === false)

    return <DropList 
        title='Manage Stats'
        showDropList={props.showManageStats}
        toggleDropList={props.toggleManageStats}
        name={props.name}
    >
        <div className='manage-drop-list'>
            <div className='active-stats'>
                <div className='active-title'>Active</div>
                {activeStats.map(item => 
                    <div className='stat-active-list'>
                        <img src='/drag-icon.svg' className='drag-icon'/>
                        <div className={`stat-name ${item.isActive ? 'active' : ''}`}>
                            {item.mainLabel}
                        </div>
                    </div>
                )}
            </div>
            <div className='inactive-stats'>
                <div className='active-title'>Other</div>
                {inActiveStats.map(item =>
                    <div className='stat-active-list'>
                        <img src='/drag-icon.svg' className='drag-icon' />
                        <div className='stat-name'>
                            {item.mainLabel}
                        </div>
                    </div>
                )}
            </div>
        </div>
    </DropList>
}