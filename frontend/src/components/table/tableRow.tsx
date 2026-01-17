'use client'

import React from 'react'
import { useState } from 'react'
import { byString } from '@/helpers';

function TableRow(props) {
    var userReadableRow = { ...props.row }


    function getDisplayDataCells() {
        const dataCells = props.columns.map((col) => {
            // TODO Temporary patch until backend is changed to `id` for both sorting and
            // filtering columns (or some other consistent format)
            //Below code commented as columns are state in Sunassist project
            // if (col.id === 'id_') {
            //     col.id = 'id';
            // }
            // console.log('getDisplayDataCells',col.name, col.id, typeof col.render);
            // For retrieving values that are to be displayed that are nested
            var value;
            // console.log(col);
            if (col.id.includes('.')) {      // IE 11 beware of `includes`
                value = byString(userReadableRow, col.id);
                // console.log(value);
            } else {
                value = userReadableRow[col.id];
            }

            const isEditing = props.editIndex === props.row.id

            let content;
            if (col.render) {
                // Both row and customData are passed in case the custom render
                // function requires those data in order to render successfully
                // collection and updateCollection are passed to update row
                // value - courtesy to installment mapper - there may be a better
                // way of doing it
                content = col.render(
                    props.row,
                    props.customData,
                    props.collection,
                    props.updateCollection,
                    props.index,
                    isEditing
                );
            } else {
                content = value;
            }

            //Code added to enable preferred columns using CSS
            // console.log('Column', col);
            let className = `${col.dataClassName} table-body-data`;
            // if (!col.visible){
            // className += ` table-body-data-column-hidden`;
            // }
            var cell = (
                <td key={col.id}
                    className={className}
                >
                    {content}
                </td>
            );

            return cell;
        });
        let [selectedOption, setSelectedOption] = useState(null);

        return <tr key={userReadableRow.id}
            // className={`${props.className || ''} data-row table-body-row`}
            className={`${props.className || ''} ${selectedOption ? selectedOption.class : ''} ${props.selectedIndex === props.index ? 'selected-index' : ''} data-row table-body-row`}
            onClick={onClick}
            style={props.style}
            ref={props.reference}
        >
            {/* Select checkbox */}
            {props.selectableRows === -1 && <td className='table-body-data'>
                <Checkbox
                    onChange={props.onCheckboxClick
                        ? onCheckboxSelect
                        : onClick
                    }
                    checked={props.row._selected}
                />
            </td>}

            {props.controlColumns.map((col, index) => (
                <td key={index} className='table-body-data'>
                    <div className={col.className}
                        onClick={(e) => {
                            e.stopPropagation();
                            col.onClick(props.index);
                        }}
                        title={col.tooltip}
                    >
                        {col.content}
                    </div>
                </td>
            ))}

            {dataCells}

            {props.hoverOptions && <td key={1000} className='table-body-data row-options-wrapper'>
                {/*Element is hidden from user using combination of CSS and JS*/}
                {!selectedOption && <div className='row-options'>
                    {props.hoverOptions.map(option => {
                        return <div className='row-option'>
                            <button onClick={(e) => {
                                e.preventDefault();
                                //If confirmation is requried show the relevant UI
                                if (option.requiresConfirmation) {
                                    setSelectedOption(option);
                                } else {
                                    option.onClick(props.row);
                                }
                            }}>
                                {option.image && <Icon path={option.image} />}
                                {option.text}
                            </button>
                        </div>
                    })}
                </div>}

                {selectedOption && <div className='option-expanded'>
                    <div className='confirmation-wrapper'>
                        <div className='confirmation-message'>
                            {selectedOption.confirmMessage}
                        </div>
                        {selectedOption.confirmRender && <div className='confirm-render'>
                            {selectedOption.confirmRender(props.row, props.customData)}
                        </div>}
                        <div className='close-option-confirmation'>
                            <button onClick={() => setSelectedOption(null)}>
                                <Icon path='confirm-close-circle.svg' />
                            </button>
                        </div>
                    </div>
                    <div className='option-confirm'>
                        <button
                            className='option-confirm-button'
                            onClick={e => {
                                e.preventDefault();
                                selectedOption.onClick(props.row, props.customData);
                            }}
                        >
                            <Icon path={selectedOption.image} />
                        </button>
                    </div>
                </div>}
            </td>}
        </tr>
    }

    function onClick(e) {
        if (props.onClick) {
            props.onClick(e, props.index);
        }
    }

    if (props.row.display === false) {
        return null;
    } 
    // else if (isEditing) {
    //     return getEditDataCells();
    // } 
    else {
        return getDisplayDataCells();
    }
}

export default React.memo(TableRow, (prevProps?: any, nextProps?: any) => {
    return false
})

