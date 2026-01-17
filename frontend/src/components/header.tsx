interface HeaderProps {
    title?: string,
}
export default function Header(props: HeaderProps) {
    return <div className='header-wrapper'>
        <div className='header-title'>
            {props.title}
        </div>
    </div>
    
}