interface SliderButtonProps {
    index?: any,
    itemKey?: any
    currentFilterData?: any
    onClick?: any
    updateCollection?: any
}

export default function SliderButton(props: SliderButtonProps) {
    return <div className='filter-toggle'>
        {Object.entries(props.currentFilterData).map(([key, value]) => {
            if (value?.type === 'checkbox') {
                return <div className='toggle-btn'>
                    <label className='toggle-switch'>
                        <input 
                            name={`${key}.value`}
                            value={props.itemKey}
                            onChange={(e) => {
                                props.onClick(
                                    key, 
                                    props.itemKey,  
                                    props.updateCollection, 
                                    e.target.checked)
                            }}
                            type='checkbox'
                        />
                        <span className='slider'></span>
                    </label>
                </div>
            }
        })}
    </div>
}