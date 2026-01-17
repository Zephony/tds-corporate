interface DeleteModalProps {
    text?: any
    toggleDeleteModal?: any
    handleDelete?: any
    buyerByCompanyId?: any
    deleteBtn?: any
}
export default function DeleteModal(props: DeleteModalProps) {
    return <div className='delete-text-wrapper'>
        <div className='delete-text'>
            {props.text}
        </div>
        <div className='delete-action-btn'>
            <button 
                onClick={props.toggleDeleteModal}
                className='without-bg-btn'
            >
                Cancel
            </button>
            <button 
                onClick={(e) => {
                    props.handleDelete(e, props.buyerByCompanyId)
                    props.toggleDeleteModal()
                }}
                className='delete-btn'
            >
                {props.deleteBtn}
            </button>
        </div>
    </div>
}