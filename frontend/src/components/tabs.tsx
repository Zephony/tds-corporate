import { useState } from 'react'

interface TabsProps {
    tabs?: any
    setTabs?: any
    activeTab?: any
    setActiveTab?: any
}

export default function Tabs(props:TabsProps) {
    return <div className='tabs-wrapper'>
        {Object.entries(props.tabs).map(([key, item]) => <div 
            key={key} 
            onClick={() => props.setActiveTab(key)} 
            className={`tab-item ${props.activeTab === key ? 'active' : ''}`}
        >
            {item.label}
        </div>
        )}
    </div>
}