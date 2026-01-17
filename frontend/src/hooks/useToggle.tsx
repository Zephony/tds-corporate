'use client'

import { useState } from 'react';

export default function useToggle(value = false) {
    const [isOn, setOn] = useState(value);

    function toggle() {
        // console.log('toggle', isOn);
        setOn(old => !old);
    }

    return [isOn, toggle, setOn];
}