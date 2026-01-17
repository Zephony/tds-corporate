interface StatusTextProps {
    text?: any,
    status?: any
    setApiResponse?: any
}


export default function StatusText(props: StatusTextProps) {
    return <div className='message-wrapper'>
        {props.text.map((item) => 
            <div className={`message ${item.status}`}>
                <div className='response-text'>
                    {item.text}
                </div>
                <img onClick={() => props.setApiResponse(false)} className='close-icon' src='/close-icon.svg' />
            </div>
        )}
    </div>
}