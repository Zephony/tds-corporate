'use client'

import { useState, useEffect } from 'react'

import Menubar from '@/components/menuBar';
import Header from '@/components/header';
import Tabs from '@/components/tabs';
import { Input, SelectField } from '@/components/form';
import Stats from '@/components/stats';

import useToggle from '@/hooks/useToggle';
import FilterDropList from '@/components/filterDropList';
import { formatDateTime } from '@/helpers';

import useCollection from '@/hooks/useCollection';
import useFilter from '@/hooks/useFilter';

import '@/css/pages/activity.css'

const stats = [
    {
        mainLabel: 'Total Activities',
        mainValue: '1,234',
        isActive: true
    },
    {
        mainLabel: 'Exceptions',
        mainValue: '47',
        isActive: true
    },
    {
        mainLabel: 'Commands',
        mainValue: '892',
        isActive: true
    },
    {
        mainLabel: 'Status Updates',
        mainValue: '295',
        isActive: true
    },
    {
        mainLabel: 'Other',
        mainValue: '123',
        subLabel: 'Metrics',
        subValue: '45',
        isActive: false
    },
]

const activityLog = [
    {
        Timestamp: "2025-08-28T20:45:22.405+02:00",
        SystemID: null,
        Type: "Exception",
        Message: "App started. Version: v1.5.3-dev"
    },
    {
        Timestamp: "2025-08-28T20:45:22.874+02:00",
        SystemID: null,
        Type: "Status",
        Message: "LOG: Network status 'online'"
    },
    {
        Timestamp: "2025-08-28T20:45:22.895+02:00",
        SystemID: null,
        Type: "Exception",
        Message: "APP: Entered screen 'Unpack'"
    },
    {
        Timestamp: "2025-08-28T20:45:22.896+02:00",
        SystemID: null,
        Type: "Exception",
        Message: "LOG: Find device on port: COM4. Try to connect"
    },
    {
        Timestamp: "2025-08-28T20:45:23.861+02:00",
        SystemID: null,
        Type: "Status",
        Message: "APP: Clicked Next button"
    },
    {
        Timestamp: "2025-08-28T20:45:23.865+02:00",
        SystemID: null,
        Type: "Exception",
        Message: "APP: Entered screen 'Connect'"
    },
    {
        Timestamp: "2025-08-28T20:45:23.920+02:00",
        SystemID: null,
        Type: "Status",
        Message: "LOG: MTU connected. 'OmniPro Club', number of gates to use '3'"
    },
    {
        Timestamp: "2025-08-28T20:45:23.921+02:00",
        SystemID: null,
        Type: "Command",
        Message: "WHOA response RSLT=WHOA,MSG,\"OmniPro Club\"",
        Payload: []
    },
    {
        Timestamp: "2025-08-28T20:45:23.939+02:00",
        SystemID: null,
        Type: "Command",
        Message: "LOGS=0,74724418,\"log LVL Error\"",
        Payload: [{ Device: [], Data: "", Code: "log" }]
    },
    {
        Timestamp: "2025-08-28T20:45:23.941+02:00",
        SystemID: null,
        Type: "Command",
        Message: "VERB=0 response RSLT=VERB,OK",
        Payload: []
    },
    {
        Timestamp: "2025-08-28T20:45:23.952+02:00",
        SystemID: null,
        Type: "Exception",
        Message: "Versions info, current: 1.004,1.004,10.4.0, latest: ,,"
    },
    {
        Timestamp: "2025-08-28T20:45:23.952+02:00",
        SystemID: "D074",
        Type: "Command",
        Message: "ABOU response RSLT=ABOU,MSG,\"D074 v1.004 v1.004\"",
        Payload: []
    }
];

const quickFilter = [
    {
        label: 'Pending buyers',
        key: 'PENDING',
        isActive: true
    },
    {
        label: 'Rejected/Blocked buyers',
        key: 'INACTIVE',
        isActive: false
    },
    {
        label: 'Dispute raised buyers',
        key: 'NOT_VERIFIED',
        isActive: false
    },
    {
        label: 'Newly signed-up buyers',
        key: 'ACTIVE',
        isActive: true
    },
]

const initialFilterData = {
    f_user_status: {
        operator: 'equals',
        value:'',
        type: 'checkbox'
    }
}

export default function ActivityLog() {
    // Right side panel tab label and key
    const [tabs, setTabs] = useState({
        'devices': {
            label: 'Devices/System Logs'
        },
        'app': {
            label: 'App/Exceptions Logs'
        },
    })

    const [activeTab, setActiveTab] = useState('devices')
    const [showFilterDropList, toggleFilterDropList] = useToggle()
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useToggle()
    const [isMobile, setIsMobile] = useState()

    
    const [devices, updateDevices] = useCollection('admin/devices', null, null)

        // Pass Filter params to the url
    const [
        currentFilterData,
        filterEnabled,
        getFilterSearchParams,
        onFilterInputChange,
        applyFilter,
        clearFilter,
        setFilterData 
    ] = useFilter(initialFilterData, updateDevices)

    // Search functionality
    const handleSearch = (qString, updateCollection) => {
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            searchParams.set('q', qString)

            return { searchParams }
        })
    }

        // Filter functionality
    const handleFilter = (key, value, updateCollection, checked) => {
        updateCollection(old => {
            let searchParams = new URLSearchParams(old.searchParams)
            if(checked) {
                searchParams.set(key, value)

            } else {
                searchParams.delete(key)
            }

            return { searchParams }
        })
        // updateQueryParam(key, value)
    }

    return <div className='page-container'>
        {isMobile
            ? (isMobileMenuOpen
                ? <div onClick={() => setIsMobileMenuOpen()} className='overlay'>
                    <Menubar/>
                </div>
                : null
            )
            : <div className='left-container'><Menubar/></div>
        }
        <div className='main-content'>
            <Header
                title='Activity Log'
            />
            <div className='main-content-body'>
                <Stats
                    title='Stats'
                    statValues={stats}
                    isDateDropList={false}
                    isDateInput={true}
                />
                <div className='activity-log-wrapper'>
                    <div className='activity-container'>

                        <div className='action-wrapper'>
                            <div className='left-content'>
                                <div className='label'>
                                    All Activities
                                </div>
                            </div>
                            <div className='right-content'>
                                <input
                                    id='search-input'
                                    type='text'
                                    className='search-input'
                                    placeholder='Search'
                                    onChange={e => handleSearch(e.target.value, updateDevices)}
                                />

                                {toggleFilterDropList && <div className='filter-btn-droplist-wrapper'>
                                    <button type='button'
                                        id='open-filters-form-button'
                                        className='filters-web'
                                        onClick={toggleFilterDropList}
                                    >
                                        Filters
                                    </button>
                                    {showFilterDropList &&
                                        <FilterDropList
                                            name='activity-log'
                                            quickFilter={quickFilter}
                                            toggleFilterDropList={toggleFilterDropList}
                                            showFilterDropList={showFilterDropList}
                                            isDateDropList={false}
                                            isDateInput={true}
                                            collection={devices}
                                            currentFilterData={currentFilterData}
                                            sliderFilter={handleFilter}
                                            updateCollection={updateDevices}
                                        />
                                    }
                                </div>}
                                
                            </div>
                        </div>
                        <div className='text-area-wrapper'>
                            <div className='text-area'>
                                <input type='text' placeholder='Add notes...' />
                                <div className='save-btn'>Save</div>
                            </div>
                        </div>
                        <div className='activity-wrapper'>
                            {activityLog.map(item =><div className='activity-details-wrapper'>
                                <hr className='vertical-line' />

                                <div className='point-icon'>

                                    <img src='/point.svg'/>
                                </div>
                                <div className='activity-details'>
                                    <div className='sub-label'>{formatDateTime(item.Timestamp)}</div>
                                    <div className='activity'>{item.Message}</div>
                                </div>
                            </div>)}
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
}