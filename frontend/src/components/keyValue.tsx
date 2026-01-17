'use client'

interface KeyValueProps {
    displayKey?: any
    value?: any
    name?: any
    subValue?: any
}

export default function KeyValue(props: KeyValueProps) {
    const isLongText = props.name === 'long-text' || (typeof props.value === 'string' && props.value.length > 100)
    
    return <div className={`key-values-wrapper ${isLongText ? 'long-text-wrapper' : ''}`}>
        <div className={`key-value-label ${props.name}`}>
            {props.displayKey}
        </div>
        <div className={`key-value-value ${props.name} ${isLongText ? 'long-text-value' : ''}`}>
            <div className={`key-value-main-value ${isLongText ? 'long-text-content' : ''}`}>
                {isLongText ? (
                    <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word', fontFamily: 'inherit', margin: 0 }}>
                        {props.value}
                    </pre>
                ) : (
                    props.value
                )}
            </div>
            {props.subValue && (
                <div className='key-value-sub-value'>{props.subValue}</div>
            )}
        </div>
    </div>
}