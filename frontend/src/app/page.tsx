'use client'

import { useRef, useEffect, useState, useLayoutEffect } from 'react'
import moment from 'moment';
import { useMemo } from 'react';  // You also use useMemo below
// import * as d3 from 'd3'
import useRequest from '@/hooks/useRequest';

import Menubar from '@/components/menuBar';
import { numFormat } from '@/helpers';

import useCollection from '@/hooks/useCollection';

export default function Home() {


    return <div className='page-container'>
        <div className='left-container'>
            {/* <Menubar/> */}
        </div>
        <div className='main-content'>
            <h1>Home</h1>
        </div>
    </div>
}


