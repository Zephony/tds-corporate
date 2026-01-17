'use client'
import React, { useState, useEffect } from 'react';

// import { copy, byString, getTime, getMap } from '';
import { copy , byString, getTime, getMap } from '@/helpers'

import moment from 'moment'

const selectEventTypes = [
    'select-option', 'remove-value',
    'clear', 'pop-value', 'set-value',
];

function useForm(initialData) {
    // initialData - Initial JSON structure
    // Make sure to remove all empty fields (lead update - exception) before submitting

    const [data, setData] = useState(initialData);
    const [errors, setErrors] = useState({});
    const [errorMessage, setErrorMessage] = useState();

    function setErrorsMap(error) {
        setErrors(getMap(error, 'field', false, key => key, 'description'));
    }

    function onSubmit(e) {
        e.preventDefault();     // To not submit the form by reloading the page
        afterSubmit();
    }

    function onInputChange(e, selectEvent = null, compositeValueInArray = true) {
        // selectEvent: react-select returns the selected option as the first value
        // and selectEvent as the second with extra info about the event

        let name, value;
        // console.log('Inside onChange', e);

        if (selectEvent !== null && selectEventTypes.includes(selectEvent.action)) {
            // React-Select
            name = selectEvent.name;
            value = getEventValue(e, selectEvent);
            console.log(name, value, selectEvent, 'name and value')
        } else if (e.target.closest('.select-option') !== null) {
            // Select field
            console.log(e.target.closest('.select-field'), 'target closest');

            name = e.target.closest('.select-field').getAttribute('name');
            value = getEventValue(e);
            console.log('ddddddd', name, value, e.target.closest('.select-field'));
        } else if (e.target && e.target.type === 'checkbox') {
            // Checkbox
            name = e.target.name;
            value = getEventValue(e);
        } else if (e.target && e.target.type === 'radio') {
            // Checkbox
            name = e.target.name;
            value = getEventValue(e);
        } else if (e.target && e.target.closest('.composite-text-field') !== null) {
            // Composite Text Field
            const compositeFieldElement = e.target.closest('.composite-text-field');
            name = compositeFieldElement.getAttribute('name');
            value = getEventValue(e, selectEvent, compositeValueInArray);
        } else if (e.target.closest('.date-field') !== null) {
            // Date field
            const dateFieldElement = e.target.closest('.date-field');
            name = dateFieldElement.querySelector('.date-text-input').name;
            value = getEventValue(e);
        } else if (e.target.closest('.option') !== null) {
            //Code for multi-select component
            name = e.target.closest('.option').dataset.name;
            value = getEventValue(e);
            let tempArray = [];

            if (e.target.closest('.option').dataset.valuearray) {
                tempArray = e.target.closest('.option').dataset.valuearray.split(',');
            }

            let index = tempArray
                .map(element => element).indexOf(value);
            if (index === -1) {
                tempArray = [...tempArray, value];
            } else {
                // console.log('Inside remove');
                tempArray.splice(index, 1);
            }
            value = tempArray;
        } else {
            // TextField, TextArea, etc.
            name = e.target.name;
            value = getEventValue(e);
            console.log('Value: nnn', value);
        }

        console.log('New value:', value, 'Field:', name, 'Data:', data);

        setData(old => {
            let new_ = copy(old);
            byString(new_, name, value);
            // console.log('aaa', old, new_);
            return new_;
        });
    }

    return [data, setData, onInputChange, errors, setErrorsMap, errorMessage, setErrorMessage];
}


function getEventValue(e, selectEvent = null, compositeValueInArray = true) {
    // If compositeValueInArray is true, it's value is put in an array - it's
    // a hack used in lead filters

    let value;

    if (selectEvent !== null && selectEventTypes.includes(selectEvent.action)) {
        // React-Select
        if (selectEvent.action === 'clear') {
            // User cleared the field value (by clicking on the 'x' icon)
            value = null;
        } else if (Array.isArray(e)) {
            // Multiselect field
            value = e.map(option => option.value)
        } else {
            // Single option select
            value = e.value;
        }
    } else if (e.target.closest('.select-option') !== null) {
        // Select field
        value = e.target.closest('.select-option').dataset.value;

        // For select options where value is the id of the item
        if (e.target.closest('.select-option').dataset.type == 'number') {
            value = Number(value);
        }
    } else if (e.target && e.target.type === 'checkbox') {
        // Checkbox
        value = e.target.checked;
        console.log('(((())))', value);
    } else if (e.target && e.target.closest('.composite-text-field') !== null) {
        // Composite Text Field
        const compositeFieldElement = e.target.closest('.composite-text-field');
        const selectedItemElement = compositeFieldElement.querySelector('.selected-item');
        const inputElement = compositeFieldElement.querySelector('.input');
        // console.log('{{{{{{{{}}}}}}}}', e.target.text[0]);

        let dropdownValue;
        if (e.target.classList.contains('dropdown-item')) {
            dropdownValue = e.target.dataset.value;
        } else {
            dropdownValue = selectedItemElement.dataset.value;
        }

        let textValue;
        if (e.target.value) {
            textValue = e.target.value;
        } else if (inputElement.value) {
            textValue = inputElement.value
        } else {
            textValue = '';
        }

        value = {
            [compositeFieldElement.dataset.operatorName]: dropdownValue,
            [compositeFieldElement.dataset.valueName]: textValue, // Returns 0 for some reason
        }

        // Hack to put the composite value inside an array (for lead filters search)
        if (compositeValueInArray) {
            value[compositeFieldElement.dataset.valueName] = [textValue];
        }
    } else if (e.target.closest('.date-field') !== null) {
        // Date field
        const dateFieldElement = e.target.closest('.date-field');
        const dateInputElement = dateFieldElement.querySelector('.calendar')
            .querySelector('.date-input');
        const timeInputElement = dateFieldElement.querySelector('.calendar')
            .querySelector('.time-input');

        // Check if user is clearing or setting the date
        if (e.target.classList.contains('clear-button')) {
            // User just cleared the date
            value = null;
            // console.log('Cleared date..');
        } else if (timeInputElement) {
            // User just set the date and it has a time input field
            let userInputDate = dateInputElement.value;
            let userInputTime = timeInputElement.value;
            value = moment(userInputDate, 'DD/MM/YYYY').format('YYYY-MM-DD')
                + 'T'
                + getTime(userInputTime);
        } else {
            // User just set the date and it has NO time input field
            let userInputDate = dateInputElement.value;
            value = moment(userInputDate, 'DD/MM/YYYY').format('YYYY-MM-DD');
        }
    } else if (e.target.closest('.option')) {
        value = e.target.closest('.option').dataset.value;
    } else {
        // console.log(e.target.type, e.target.value);
        // TextField, TextArea, etc.
        if (e.target.type === 'number') {
            if (e.target.step) {
                // Float
                value = parseFloat(e.target.value);
            } else {
                // Integer
                value = parseInt(e.target.value);
            }
        } else if (e.target.type === 'radio') {
            // Standard radio button - return the value as is
            value = e.target.value;
        } else {
            value = e.target.value
        }
    }

    return value;
}

export {
    useForm,
    getEventValue,
}