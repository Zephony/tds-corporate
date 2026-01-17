import useToggle from '@/hooks/useToggle'
import DropList from './dropList'

interface DropDownProps {
    title?: string
    collection?: any
}
export default function DropDown(props: DropDownProps) {
    console.log(props.collection, 'collection')
    const list = props.collection?.map(item => item?.company_details?.approval_status)
    const uniqueList = [...new Set(list)]
    const [showDropDown, toggleDropDown] = useToggle()
    return <div className='drop-down-wrapper'>
        <div className='drop-down' onClick={toggleDropDown}>
            <div className='drop-down-label'>{props.title}</div>
            <div className='drop-down-icon-wrapper'>
                <img className='drop-down-icon' src='/drop-down-arrow.svg'></img>
            </div>
        </div>
        {showDropDown && <div className='drop-down-items-list'>
            {uniqueList.map(item => <button className='drop-down-item-wrapper'>
                <div className='drop-down-item'>
                    {item}
                </div>
            </button>)}
        </div>}
    </div>
} 
