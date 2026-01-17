'use client'

import React, { useState, useEffect, useRef } from 'react';

// import { MeContext } from 'src/contexts';
import Calendar from '@/components/calendar';
import { Icon } from '@/components/icon';
import {
    equal,
    getDayLabel,
    getOptions,
    toLower
} from '@/helpers';
import useCollection from '@/hooks/useCollection';
import useToggle from '@/hooks/useToggle';
import moment from 'moment'

// NOTE: Memoing fields don't rerender them if a prop function uses a prop
// inside the parent component and that prop changes
// Already faced the issue with toggleAllRowSelection checkbox

const DateField = React.memo(props => {
    // If `props.time` is set to true, the field is assumed to be a
    // datetime field and the time input is taken into account for handling
    //

    /*
        * MeContext is used to fetch preferred date time format.
        *The ideal way to do this would have been to pass a date format
        *as a prop to the DateField component.
    */
    // const { me } = useContext(MeContext);
    const [selectedDate, setSelectedDate] = useState(props.value || null);

    console.log(selectedDate, 'selectedDate')
    // Note: Passing a function as an argument to useState gets executed without
    // having to call the function: https://github.com/facebook/react/issues/15209
    const [enteredDate, setEnteredDate] = useState(() => {
        let date = moment(props.value);
        if (date.isValid()) {
            return date.format('DD/MM/YYYY');
        }
        return moment().add(1, 'days').format('DD/MM/YYYY')
    });
    const [enteredTime, setEnteredTime] = useState(() => {
        let time = moment(props.value);
        if (time.isValid()) {
            return time.format('HH:mm A');
        }
        return '10:00 AM';
    });
    const [calendarVisible, setCalendarVisible] = useState(false);

    // To close calendar when clicking outside
    useEffect(() => {
        document.addEventListener('click', onClick);

        return () => document.removeEventListener('click', onClick);
    }, []);

    let errorClass = props.errorMessage ? 'error' : '';

    function toggleCalendar() {
        setCalendarVisible(old => {
            if (old) {
                return false;
            }
            return true;
        });
        // calendarVisible ? setCalendarVisible(false) : setCalendarVisible(true);
    }

    function onClick(e) {
        let calendarElement = document.querySelector('.calendar');
        let calendarInputElement = dateFieldNode.current;

        if (calendarElement && !calendarElement.contains(e.target)
            && !calendarInputElement.contains(e.target)) {
            setCalendarVisible(false);
            console.log('**Inside calendar input', calendarElement, e.target);
        }
    }

    let className = `date-field ${props.className || ''}`;
    if (props.disabled) {
        className += ' disabled'
    }

    let classNameDateInput = 'date-label';
    const dateFieldNode = useRef();

    //Logic to manipulate states based on viewMode
    let displayElement;
    if (!props.viewMode || props.viewMode === 'edit') {
        // Display logic for edit
        displayElement = <div
            className={`date-input-btn ${props.component}`}
            onClick={e => {
                props.disabled || toggleCalendar();
            }}
        >
            {props.label && <label className={`from-to${props.error ? ' error-label' : ''}`}>
                {props.label || selectedDate}
                {props.required && <span className='required'> *</span>}
            </label>}

            <div className={`date-input ${props.error && 'error'}`}>
                <div className={classNameDateInput || ''}
                    
                    disabled={props.disabled}
                >
                    {props.value
                        ? <span className='readable-date input-display-text'>
                            {props.datetime
                                && moment(props.value).format('MMMM Do, YYYY, h:mm a')
                                || moment(props.value).format('MMM D, YYYY')
                            }
                        </span>
                        : <span className='placeholder'>
                            {props.placeholder ? props.placeholder : ''}
                        </span>
                    }

                    <img
                        className='calender-icon'
                        src='/calender.svg'
                    />
                </div>

                {calendarVisible && <Calendar className='calendar'
                    value={props.value}
                    selectedDate={selectedDate}
                    setSelectedDate={setSelectedDate}
                    enteredDate={enteredDate}
                    setEnteredDate={setEnteredDate}
                    enteredTime={enteredTime}
                    setEnteredTime={setEnteredTime}
                    onChange={props.onChange}
                    setCalendarVisible={setCalendarVisible}
                    datetime={props.datetime}   // Whether to get the time along with the date or not
                    disableBefore={props.disableBefore}
                    disableAfter={props.disableAfter}
                />}

                <input type='text' autoComplete='off'
                    style={{ display: 'none' }}
                    className={`date-text-input`}
                    name={props.name}
                    value={props.value || ''}
                    onChange={() => props.onChange}
                // onFocus={showCalendar}
                />
            </div>

            {props.error && <span className='error-message'>
                {props.error}
            </span>}

            {props.success && <span className='succes-message'>
                {props.success}
            </span>}
        </div>
    } else {
        // Dispaly logic for read state
        displayElement = <>
            {props.label && <label className='read-state-label'>
                {props.label}
                {props.required && <span className='required'> *</span>}
            </label>}
            <div className='read-state-value'>
                {props.value
                    ? getDayLabel(
                        moment(props.value, 'YYYY-MM-DD'),
                        me.preferred_date_format
                    )
                    : '-'
                }
            </div>
        </>
    }

    return <div className={className} ref={dateFieldNode}>
        {displayElement}
    </div>
}, equal);

const Input = React.memo(props => {
    const textAreaRef = useRef();
    const hiddenDivRef = useRef();
    let displayElement;

    useEffect(() => {
        if (props.autoResize) {
            let textArea = textAreaRef.current;
            let hiddenDiv = hiddenDivRef.current;

            // textArea.style.resize = 'none';
            textArea.style.overflow = 'hidden';

            // Add the same content to the hidden div
            let value = props.value || '';
            hiddenDiv.innerHTML = value || 'a';
            if (value[value.length - 1] == '\n') {
                hiddenDiv.innerHTML = value + 'a';
            }

            // Briefly make the hidden div block but invisible
            // This is in order to read the height
            hiddenDiv.style.visibility = 'hidden';
            hiddenDiv.style.display = 'block';
            // console.log(
            // 'Hidden Div height:',
            // hiddenDiv.offsetHeight,
            // );
            textArea.style.height = hiddenDiv.offsetHeight + 'px';

            // Make the hidden div display:none again
            hiddenDiv.style.visibility = 'visible';
            hiddenDiv.style.display = 'none';
        }
    }, [props.value]);

    let inputElement;
    if (props.type === 'textarea') {
        inputElement = <>
            <textarea {...props}
                ref={textAreaRef}
                className={`input-element input-display-text ${props.error && 'error'}`}
                name={props.name}
                value={props.value}
                onChange={props.onChange}
            >
                {props.value}
            </textarea>

            {/* Used for textarea autoresize
                - https://www.impressivewebs.com/textarea-auto-resize/ */}
            {props.autoResize && <div ref={hiddenDivRef}
                className='hidden-div'
            />}
        </>
    } else {
        let searchStr;
        let options = props.options || [];
        let className = 'input-element-wrapper';
        if (props.error) {
            className += ' error';
        }
        if (props.disabled) {
            className += ' disabled';
        }

        inputElement = <div className={className}>
            {props.prefixIconPath && <Icon path={props.prefixIconPath}
                className='prefix'
                size={15}
            />}

            <input {...props}
                type={props.type}
                className={`input ${props.className} ${props.error && 'error'}`}
                name={props.name}
                value={props.value}
                onChange={props.onChange}
                disabled={!!props.disabled}
            />

            {props.suggest && props.value && <div className='suggestions'>
                {options.map(option => <button
                    type='button'
                    className='cobb suggestion'
                    onClick={e => props.onOptionSelect(e, option)}
                >
                    {(searchStr = toLower(String(props.value)).split('')) && ''}
                    {option.name.split('').map((letter, index) => {
                        let className = 'suggestion-character';
                        if (searchStr.length > 0 && searchStr[0] === toLower(letter)) {
                            className += ' match';
                            searchStr.splice(0, 1);
                        }

                        return <span className={className}>{letter}</span>
                    })}
                </button>)}
            </div>}

            {props.postfixText && <span className='input-inside-right'>
                {props.postfixText}
            </span>}

            {props.postfixIconPath && <Icon path={props.postfixIconPath}
                onClick={props.onPostfixClick}
                className='postfix'
                size={12}
            />}
        </div>
    }

    let className = 'input';
    if (props.className) {
        className += ' ' + props.className;
    }
    if (props.type === 'textarea') {
        className += ' textarea';
    }

    if (!props.viewMode || props.viewMode === 'edit') {
        //Display logic for edit
        displayElement = <>
            {props.label && <label className={`input-label${props.error ? ' error-label' : ''}`}>
                {props.label}
                {props.required && <span className='required'> *</span>}
            </label>}

            {inputElement}

            {!props.pure && <span className='error-message'>
                {props.error}
            </span>}
            {!props.pure && <span className='success-message'>
                {props.success}
            </span>}
        </>
    } else {
        //Dispaly logic for read state
        displayElement = <>
            {props.label && <label className='read-state-label'>
                {props.label}
                {props.required && <span className='required'> *</span>}
            </label>}
            <div className='read-state-value'>
                {props.value ? props.value : '-'}
            </div>
        </>
    }

    return <div className={className}>
        {displayElement}
    </div>
}, equal);

const SelectField = React.memo(props => {
    const [isOn, toggle, setOn] = useToggle(false);
    const [optionC, updateOptionC] = useCollection(null , null);
    // const selectedDropdownValue = useRef();
    const scrollRef = useRef(null); // Reference to scroll to the selected option

    let displayElement;
    let options = props.enableLazyLoadOptions
        ? (optionC.loaded ? getOptions(optionC.items, 'name', 'id') : [])
        : (props.options || [])
        ;

    // To close the options when clicking outside
    useEffect(() => {
        document.addEventListener('click', onClick);

        return () => document.removeEventListener('click', onClick);
    }, []);

    function onClick(e) {
        let optionsElement = document.querySelector('.select-options');
        let selectInputElement = selectFieldNode.current;

        if (optionsElement && !optionsElement.contains(e.target)
            && !selectInputElement.contains(e.target)) {
            setOn(false);
        }
    }

    if (props.enableNoneOption) {
        options = [{
            name: '-----',
            value: 'clear',
        }, ...options];
    }

    let selectedOption;
    if (props.value !== null && props.value !== undefined) {
        selectedOption = options.find(option => option.value === props.value);

        if (props.enableLazyLoadOptions && selectedOption === undefined) {
            request.get(`${props.optionsURL}/${props.value}`)
                .then(([status_, response]) => {
                    let newItems = copy(optionC.items);
                    newItems.push(response.data);
                    updateOptionC({
                        items: newItems,
                    });
                })
                ;
        }
    }


    const [filterText, setFilterText] = useState('');

    // Frontend search: New custom search matches if all words in box
    // are found anywhere in the option.label, case in-sensitive
    function customFilter(option, rawInput) {
        const words = rawInput.split(' ');

        if (option.data.searchString) {
            return words.reduce(
                (acc, cur) =>
                    acc &&
                    option.data.searchString
                        .toLowerCase()
                        .includes(cur.toLowerCase()),
                true
            );
        }

        if (typeof option.label === 'string') {
            return words.reduce(
                (acc, cur) =>
                    acc && option.label.toLowerCase().includes(cur.toLowerCase()),
                true
            );
        }

        if (!rawInput) {
            return true;
        }

        return false;
    }

    const selectFieldNode = useRef();

    const ref = useRef(null);

    const onDropdownArrowClick = () => {
        ref.current.focus();
    };

    //To scroll into view when option is selected
    //Added as seperate useEffect as the options are not strictly rendered on
    //dropdown click
    // useEffect(() => {
    //
    //     if(isOn) {
    //         const parent = selectFieldNode.current;
    //         const selectedElement = selectFieldNode.current.querySelector('.selected');
    //
    //         if(parent && selectedElement) {
    //             parent.scrollTop = selectedElement.offsetTop - parent.offsetTop;
    //         }
    //     }
    // }, [isOn])

    let inputClassName = 'select-box-left input-display-text';
    if (filterText) {
        inputClassName += ' filter-text';
    }

    if (selectedOption) {
        inputClassName += ' option-selected';
    }

    // console.log('SelectField', props);
    console.log(filterText, 'filterText')

    if (!props.viewMode || props.viewMode === 'edit') {
        //Display logic for edit
        displayElement = <>
            {props.label && <label className={`input-label${props.error ? ' error-label' : ''}`}>
                {props.label}
                {props.required && <span className='required'> *</span>}
            </label>}

            <div className='select-field-inner'>
                <div className={`select-box ${props.error && 'error'}`}
                    onClick={!props.disabled ? toggle : null}
                >
                    <input
                        ref={ref}
                        {...props}
                        type='text'
                        className={inputClassName}
                        data-test='dropdown-searchable-text-input'
                        value={filterText}
                        onChange={e => {
                            setFilterText(e.target.value);
                            setOn(true);
                        }}
                        placeholder={(selectedOption && selectedOption.name)
                            || props.placeholder
                            || 'Select a value'
                        }
                        autoComplete='off'
                        disabled={props.disabled}
                    />
                    <div className='select-box-right' onClick={onDropdownArrowClick}>
                        <img className='drop-down-icon' src='/drop-down-arrow.svg' />
                    </div>
                </div>

                {isOn && <div className='select-options'>
                    {options.length > 0 && options.map((selectOption, index) => {
                        console.log(selectOption, 'selectedOption')
                        const isSelected = selectOption.value === props.value;
                        let itemMatches = true;
                        let optionNameCharacters = selectOption.name
                            ? selectOption.name.toString().split('')
                            : [];
                        let filterTextRemainingChars = toLower(filterText).split('');
                        let buttonText = optionNameCharacters.map((character, index) => {
                            let className = 'suggestion-character';
                            // console.log(filterTextChars, filterTextChars[0], character);
                            if (filterTextRemainingChars.length > 0
                                && filterTextRemainingChars[0] === toLower(character)) {
                                className += ' match';
                                filterTextRemainingChars.splice(0, 1);
                            }

                            if (index === optionNameCharacters.length - 1
                                && filterTextRemainingChars.length > 0) {
                                itemMatches = false;
                            }

                            // if(isSelected) {
                            //     className += ' selected';
                            // }

                            if (character === ' ') {
                                return <span className={className}>
                                    &nbsp;
                                </span>
                            }
                            return <span className={className}>
                                {character}
                            </span>
                        });

                        if (!itemMatches) {
                            return null;
                        }

                        return <button type='button'
                            className={`select-option ${isSelected ? 'selected' : ''}`}
                            data-value={selectOption.value}
                            // Since HTML attributes cannot store type, we
                            // have to explicity specify the type here
                            // for useForm to get the value in the proper type
                            data-type={typeof selectOption.value}
                            onClick={e => {
                                e.stopPropagation()
                                props.onChange(e);
                                setOn(false);
                                setFilterText('');
                            }}
                            key={index}
                            ref={isSelected ? scrollRef : null}
                        >
                            {buttonText}
                        </button>
                    })}
                    {options.length === 0 && <div className='select-options-no-data'>
                        No options available
                    </div>}
                </div>}
            </div>

            {!props.pure && <>
                <span className='error-message'>{props.error}</span>
                <span className='success-message'>{props.success}</span>
            </>}
        </>
    } else {
        const selectedValue = options.find(option => option.value === props.value);
        //Dispaly logic for read state
        displayElement = <>
            {props.label && <label className='read-state-label'>
                {props.label}
                {props.required && <span className='required'> *</span>}
            </label>}
            <div className='read-state-value'>
                {selectedValue?.name ?? '-'}
            </div>
        </>
    }

    useEffect(() => {
        if (props.enableLazyLoadOptions) {
            console.log('$$Inside SelectField lazy load');
            updateOptionC({
                url: props.optionsURL,
                queryString: `${props.optionsURLParams ? props.optionsURLParams + '&' : ''}page_size=10&q=${filterText}`,
            });
        }
    }, [props.enableLazyLoadOptions, filterText]);

    return <div
        className={`select-field ${props.className || ''}${props.disabled && props.viewMode === 'edit' ? 'select-field-disabled' : ''}`}
        name={props.name}
        ref={selectFieldNode}
    >
        {displayElement}
    </div>
}, equal);

const Checkbox = React.memo(props => {
    let displayElement;
    if (!props.viewMode || props.viewMode === 'edit') {
        //Display logic for edit
        displayElement = <>
            {props.label && <label className='label'>
                {props.label}
            </label>}

            <label className='checkbox-inner'>
                <input type='checkbox'
                    name={props.name}
                    checked={props.checked}
                    onChange={props.onChange}
                    // ref={props.inputRef}
                    data-value={props.value} //To add support CheckboxGroup
                    disabled={props.disabled}
                />

                {/* For custom radio button */}
                <span className='checkmark'>
                    <span className='checkmark-inner'></span>
                </span>

                {props.labelText && <div className='label-text'>
                    <span>{props.labelText}</span>
                </div> }
            </label>

            {props.errorMessage && <span className='error-message'>{props.errorMessage}</span>}
            {props.successMessage && <span className='succes-message'>{props.successMessage}</span>}
        </>
    } else {
        //Dispaly logic for read state
        displayElement = <>
            {props.label && <label className='read-state-label'>
                {props.label}
                {props.required && <span className='required'> *</span>}
            </label>}
            <label className='checkbox-inner checkbox-inner-read-state'>
                <input type='checkbox'
                    name={props.name}
                    checked={props.checked}
                    // ref={props.inputRef}
                    data-value={props.value} //To add support CheckboxGroup
                />

                {/* For custom radio button */}
                <span className='checkmark'>
                    <span className='checkmark-inner'></span>
                </span>

                {props.labelText && <div className='label-text'>
                    <span>{props.labelText}</span>
                </div> }
            </label>
        </>
    }

    return <div className={`checkbox-field ${props.className || ''}`} >
        {displayElement}
    </div>
}, equal);

export {
    DateField,
    Input,
    SelectField,
    Checkbox,
}
