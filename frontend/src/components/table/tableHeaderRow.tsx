'use client'

import React, { useState, useEffect, useRef } from 'react';

import useToggle from '@/hooks/useToggle';
import { copy } from '@/helpers';


export default function TableHeaderRow(props) {
    // For column reorder - used inside the Column component
    const [source, setSource] = useState();
    const [expandColumnPreference,
        toggleExpandColumnPreference,
        setExpandColumnPreference
    ] = useToggle(false);

    function onColumnSortClick(colID, sortable, e) {
        console.log('Handling sort click..', colID, sortable);
        var list = [...props.items];

        props.setClickCount(prev => prev >= 3 ? 1 : prev + 1)

        if (sortable === 'backend') {
            var urlSearchParams = new URLSearchParams(props.searchParams);
            console.log('##onColumnSortClick', props.items, props.searchParams);

            if (props.clickCount === 3) {
                // console.log(props.clickCount, 'clickcount')
                urlSearchParams.delete('sort_by');

                props.setSorting({
                    sortedColID: '',
                    reverseSorted: false,
                });
            } else if (props.sorting.sortedColID === colID) {
                // Already sorted column is sorted (toggled)
                if (props.sorting.reverseSorted) {
                    urlSearchParams.set('sort_by', colID);
                } else {
                    urlSearchParams.set('sort_by', `-${colID}`);
                }

                // 1. Send request and update query string of parent state
                // 2. Update table component's state to keep track of the sort details
                props.setSorting(sorting => ({
                    ...sorting,
                    reverseSorted: !sorting.reverseSorted,
                }));
            } else {
                // A fresh column is sorted
                urlSearchParams.set('sort_by', colID);

                // Update table component's state to keep track of the sort details
                props.setSorting({
                    sortedColID: colID,
                    reverseSorted: false,
                });
            }

            // Update the parent component's state to trigger re-rendering
            const url = `${props.urlPath}?${urlSearchParams}`;
            props.updateCollection({
                searchParams: urlSearchParams,
                loaded: false,
            });

            return;
        }

        props.updateCollection({ items: list })
    }

    function toggleAllRowsSelection(e) {
        let select = false;
        if (rowsSelectionState === 'none') {
            select = true;
        }

        let tempItems = copy(props.items);
        tempItems.map(item => {
            item._selected = select;
        });

        // console.log('Toggling everything..');
        props.updateCollection({
            items: tempItems
        });
    }

    function getRowsSelectionState() {
        // Returns: 'all'/'none'/'some'
        let selectedCount = 0;
        let unselectedCount = 0;
        props.items.map(item => {
            if (item._selected) {
                selectedCount += 1;
            } else {
                unselectedCount += 1;
            }
        });

        if (selectedCount === 0) {
            return 'none';
        } else if (unselectedCount === 0) {
            return 'all';
        } else {
            return 'some';
        }
    }

    const rowsSelectionState = getRowsSelectionState();

    return (
        <tr className={`table-header-row${props.className ? ' ' + props.className : ''}`}>
            {props.columns.map((col) => <Column
                key={col.id}
                column={col}
                customData={props.customData}
                sorting={props.sorting}
                onColumnSortClick={onColumnSortClick}

                // For column reordering
                columns={props.columns}
                setColumns={props.setColumns}
                source={source}
                setSource={setSource}
            />)}
        </tr>
    );
}

function Column(props) {
    return <th key={props.column.id}
        className={`data-header ${props.column.headerClassName || ''} table-header-data`}
    >
        <div className='draggable-header'
            id={props.column.id}
        >
            {props.column.renderHeader
                ? props.column.renderHeader(props.column, props.customData)
                : <span className='column-name'
                    onClick={props.column.sortable
                        ? () => props.onColumnSortClick(props.column.id, props.column.sortable)
                        : null
                    }
                >
                    {props.column.name}
                    {props.column.sortable &&
                        <img src={
                            props.column.id === props.sorting.sortedColID
                                ? props.sorting.reverseSorted
                                    ?'/ascending-sort-icon.svg'
                                    : '/descending-sort-icon.svg'
                                :'/sort-icon.svg'}
                        />
                    }           
                    
                    {/* {props.column.id === props.sorting.sortedColID
                        ? props.sorting.reverseSorted ? ' ↓' : ' ↑'
                        : ''
                    } */}
                </span>
            }
        </div>
    </th>
}