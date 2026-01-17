import useToggle from '@/hooks/useToggle'

import { replaceUnderScoreWithSpace } from '@/helpers'
import KeyValue from './keyValue'
import DropList from './dropList'

interface ExpandCollapseSectionProps {
    item?: any
    disputesKeyValue?: any
    subTextLabel?: any
    mainLabelText?: any
    status?: any
    summaryView?: any
    showFileSummary?: any
    toggleFileSummary?: any
    records?: any
}

export default function ExpandCollapseSection(props: ExpandCollapseSectionProps) {
    const [showExpandedSection, toggleExpandedSection] = useToggle()

    return <div className='expand-collapse-container'>
        <div 
            className='collapse-section'
            onClick={(e) => {
                e.stopPropagation()
                toggleExpandedSection()
            }}    
        >
            <div className='expand-collapse-left'>
                <div className='expand-collapse-wrapper'>
                    <img
                        src={showExpandedSection
                            ? '/collapse-up.svg'
                            : '/expand-down.svg'
                        }
                        className='expand-collapse-icon'
                    />
                </div>

                <div className='expand-collapse-middle-section'>
                    <div className='main-label'>
                        {props.mainLabelText}
                    </div>
                    <div className='sub-label-wrapper'>
                        <div className='sub-label-text'>
                            {replaceUnderScoreWithSpace(props.subTextLabel)}
                        </div>
                        {props.summaryView && <>
                            <div className='dot'>.</div>
                            <div className='record-button-droplist-wrapper'>
                                <button 
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        props.toggleFileSummary()
                                    }} 
                                    className='sub-label-btn'
                                >
                                        View file summary
                                </button>
                                {props.showFileSummary && <DropList
                                    title='Records Uploaded'
                                    showDropList={props.showFileSummary}
                                    toggleDropList={props.toggleFileSummary}
                                    name='link'
                                >
                                    {props.records.map((item, index) => <div className='record-item'>
                                        <div className='record-label'>{item.name}</div>
                                        <div className='record-value'>{item.value}</div>
                                    </div>)}

                                    <hr className='light-line'/>
                                    <div className='total-value-wrapper'>
                                        <div className='bold-text'>Total</div>
                                        <div className='bold-text'>288,607</div>
                                    </div>
                                </DropList>}
                            </div>
                        </>}
                    </div>
                </div>
            </div>
            <div className='expand-collapse-right'>
                <div className={`status ${
                    props.status == 'IN_PROGRESS' || props.status === 'ESCALATED' || props.status === 'PENDING'
                        ? 'yellow' 
                    : props.status === 'RESOLVED' || 
                        props.status === 'REFUNDED' || 
                        props.status === 'COMPLETED'||
                        props.status === 'ACTIVE'
                            ? 'green'
                        : props.status === 'DISPUTED' || props.item.status === 'CLOSED'
                                ? 'red'
                                : props.status === 'INACTIVE'
                                ? 'grey'
                                : ''
                }`}>
                    {replaceUnderScoreWithSpace(props.status)}
                </div>
                {false && 
                    <div className='sub-details'></div>
                }
            </div>
        </div>
        <div className={`expand-section ${showExpandedSection ? 'expanded' : ''}`}>
            <div className='key-value-section'>
                {showExpandedSection && props?.disputesKeyValue.map(item =>
                    <KeyValue
                        displayKey={item.displayKey}
                        value={item.value}
                    />
                )}
            </div>
        </div>
    </div>
}