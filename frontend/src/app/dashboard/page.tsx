'use client'
import {useRef, useEffect, useState } from 'react'
import moment from 'moment';
import { useMemo } from 'react';  // You also use useMemo below
import * as d3 from 'd3';

export default function DashBoard(){

    const chartRef = useRef();
    const [ width, setWidth ] = useState();

    const [ chart, setChart ] = useState([]);
    return <div className='page-container'>
        <>
        {/* <div className='left-container'></div>
        <div className='main-content'>

                <div className='section chart-section board'
                    ref={chartRef}
                    style={{
                        // Since it extends more on left and right
                        // according to design
                        width: 'calc(100% + 200px)',
                        // width: '100%',
                    }}
                >
                    {width && chart && <BarChart
                        data={chart}
                        width={width}
                        height={400}
                    />}
                </div>
        </div> */}
        </>
    </div>
}

// function BarChart(props) {
//     const ref = useRef();

//     // console.log('****************', 'RENDERING CHART');

//     const balance = 1000;

//     const data1 = [
//         {
//             key: 'A',
//             value: 233,
//         },
//         {
//             key: 'B',
//             value: 343,
//         },
//         {
//             key: 'C',
//             value: -123,
//         },
//         {
//             key: 'D',
//             value: 423,
//         },
//         {
//             key: 'E',
//             value: 13,
//         },
//         {
//             key: 'F',
//             value: 400,
//         },
//         {
//             key: 'G',
//             value: 233,
//         },
//         {
//             key: 'H',
//             value: 343,
//         },
//         {
//             key: 'I',
//             value: -123,
//         },
//         {
//             key: 'J',
//             value: 423,
//         },
//         {
//             key: 'K',
//             value: 13,
//         },
//         {
//             key: 'L',
//             value: 400,
//         },
//     ];

//     // const data = props.data;
//     const data = props.data.map(item => {
//         return {
//             key: item.date,
//             value: item.amount,
//             balance: item.balance_amount
//         }
//     });

//     // const [ data, setData ] = useState([]);
//     // const [ xScale, setXScale ] = useState();
//     // const [ yScale, setYScale ] = useState();
//     // const [ xAxisDomain, setXAxisDomain ] = useState();

//     // useEffect(() => {
//     //     if (!props.data) {
//     //         return
//     //     }

//     //     const newData = props.data.map(item => {
//     //         return {
//     //             key: item.date,
//     //             value: item.amount,
//     //             balance: item.balance_amount
//     //         }
//     //     });

//     //     setData(newData);
//     // }, [ props.data ])

//     useEffect(() => {
//         console.log('Reference', ref);
//         const svgElement = d3.select(ref.current);
//         // svgElement.append('circle')
//         //     .attr('cx', 5)
//         //     .attr('cy', 5)
//         //     .attr('r', 5);
//     }, [ ref ]);

//     const width = props.width,
//         height = 350,
//         leftPadding = 75,
//         rightPadding = 75,
//         topPadding = 50,
//         bottomPadding = 50,
//         barWidth = 20;

//     let maxValue = Math.max.apply(Math, data.map(function(o){return Math.abs(o.value);})) || 100;
//     let maxBalance = Math.max.apply(Math, data.map(function(o){return Math.abs(o.balance);})) || 100;
//     const max = Math.max(maxValue, maxBalance);

//     const xAxisDomain  = data.map(item => item.key);
//     const xScale = d3.scaleLinear()
//         .domain([0, xAxisDomain.length - 1])
//         .range([0, width - leftPadding - rightPadding - 20]);

//     const yScale = d3.scaleLinear()
//         .domain([maxValue * 1.5, 0])
//         .range([0, height - topPadding - bottomPadding]);

//     const y1Scale = d3.scaleLinear()
//         .domain([maxBalance * 1.5, 0])
//         .range([0, height - topPadding - bottomPadding]);

//     const points = [];
//     data.map((item, index) => {
//         let x = (leftPadding + xScale(index)), // - (barWidth / 2),
//             y = (topPadding + y1Scale(item.balance));

//         if (item.balance < 0) {
//             y = topPadding + y1Scale(0);
//         }

//         if (index === data.length-1) {
//             x = x + barWidth;
//         }

//         points.push([x, y]);
//     });
//     // points[points.length - 1][0] += 30;

//     let zeroIndicatorVisible = false;
//     const bars = data.map((item, index) => {
//         const x = (leftPadding + xScale(index)), // - (barWidth / 2),
//             y = topPadding + yScale(Math.abs(item.value)),
//             // y = yScale(500),
//             barHeight = 300 - y;

//         const date = moment(item.key),
//             today = moment();

//         let showTodayLine = false;
//         if (date.month() == today.month() && date.year() == today.year()) {
//             showTodayLine = true;
//             {/* return <> */}
//             {/*     <path d={[ */}
//             {/*             'M', x, topPadding, */}
//             {/*             'V', height - bottomPadding, */}
//             {/*         ].join(' ')} */}
//             {/*         fill='red' */}
//             {/*         stroke='green' */}
//             {/*     /> */}
//             {/*     <path d={`M ${x-3} ${height - bottomPadding} a 1 2 0 1 1 6 0`} fill="green" /> */}
//             {/* </> */}
//         }

//         let showZeroLine = false;
//         if (!zeroIndicatorVisible && item.balance <= 0) {
//             // return <Line x1={x} y1={topPadding} x2={x} y2={height - topPadding - bottomPadding} />
//             zeroIndicatorVisible = true;
//             showZeroLine = true;
//         }

//         let color = item.value >= 0
//             ? date > today
//                 ? 'url(#positive-gradient-faded)'
//                 : 'url(#positive-gradient)'
//             : date > today
//                 ? 'url(#negative-gradient-faded)'
//                 : 'url(#negative-gradient)';

//         return <>
//             <defs>
//                 <linearGradient id='positive-gradient' x1='0%' y1='0%' x2='0%' y2='100%'>
//                     <stop offset='5%' stop-color='#80efcb' />
//                     <stop offset='95%' stop-color='#46b8ca' />
//                 </linearGradient>
//                 <linearGradient id='negative-gradient' x1='0%' y1='0%' x2='0%' y2='100%'>
//                     <stop offset='5%' stop-color='#a571f4' />
//                     <stop offset='95%' stop-color='#7d2ff0' />
//                 </linearGradient>
//                 <linearGradient id='positive-gradient-faded' x1='0%' y1='0%' x2='0%' y2='100%'>
//                     <stop offset='5%' stop-color='#bbf3f0' />
//                     <stop offset='95%' stop-color='#c2f4f1' />
//                 </linearGradient>
//                 <linearGradient id='negative-gradient-faded' x1='0%' y1='0%' x2='0%' y2='100%'>
//                     <stop offset='5%' stop-color='#e2d0fc' />
//                     <stop offset='95%' stop-color='#e4d4fc' />
//                 </linearGradient>
//             </defs>
//             <path
//                 // d={[
//                 //     'M', x, y,
//                 //     'H', x+barWidth,
//                 //     'q', 2, 0, 2, 2,
//                 //     'V', y+barHeight,
//                 //     'H', x,
//                 //     'Z'
//                 // ].join(' ')}
//                 // fill='#21BE89'
//                 // stroke='#21BE89'

//                 d={[
//                     'M', x, y+barHeight,
//                     'V', y,
//                     'q', 0, -2, 2, -2,
//                     'H', x+barWidth,
//                     'q', 2, 0, 2, 2,
//                     'V', y+barHeight,
//                     'Z'
//                 ].join(' ')}

//                 class={item.value >= 0
//                     ? 'bar-positive'
//                     : 'bar-negative'
//                 }
//                 x={x}
//                 y={y}
//                 width={barWidth}
//                 height={barHeight}
//                 rx={5}
//                 ry={5}
//                 // fill={item.value >= 0
//                 //     ? { date > today ? '#D4DBF5' : '#3285FF' }
//                 //     : { date > today ? '#F6E9D1' : '#F8AD1D' }
//                 // }
//                 // opacity={date > today ? 0.7 : 1}
//                 fill={color}
//                 // fill='url(#gradient)'
//                 onMouseOver={() => setTooltip({x:x+15, y:y, value: item.value, balance: item.balance})}
//                 onMouseOut={() => setTooltip(null)}
//                 style={{ borderRadius: '5px' }}
//             />
//             {showZeroLine && <g>
//                 <text key={x}
//                     x={x}
//                     y={topPadding}
//                     style={{
//                         fontSize: '10px',
//                         textAnchor: 'middle',
//                         transform: 'translateY(-10px)',
//                         fill: '#676478',
//                         'font-weight': 'bold'
//                     }}
//                 >$0</text>
//                 <path d={[
//                         'M', x, topPadding,
//                         'V', height - bottomPadding,
//                     ].join(' ')}
//                     // fill='#F66E5E'
//                     stroke='#F66E5E'
//                     stroke-width='2'
//                 />
//                 {/* <path d={`M ${x-3} ${height - bottomPadding} a 1 2 0 1 1 6 0`} fill="red" /> */}
//                 <path d={`M ${x-4} ${height - bottomPadding} L ${x} ${height - bottomPadding - 8} L ${x+4} ${height - bottomPadding}`} fill="#F66E5E" />
//             </g>}
//             {!showZeroLine && showTodayLine && <g>
//                 <text key={x}
//                     x={x}
//                     y={topPadding}
//                     style={{
//                         fontSize: '10px',
//                         textAnchor: 'middle',
//                         transform: 'translateY(-10px)',
//                         fill: '#676478',
//                         'font-weight': 'bold'
//                         // 'font-weight': `${month == 0 ? 'bold' : ''}`
//                     }}
//                 >Today</text>
//                 <path d={[
//                         'M', x, topPadding,
//                         'V', height - bottomPadding,
//                     ].join(' ')}
//                     fill='#30C4B8'
//                     stroke='#30C4B8'
//                     stroke-width='2'
//                 />
//                 {/* <path d={`M ${x-3} ${height - bottomPadding} a 2 3 0 1 1 6 0`} fill="green" /> */}
//                 <path d={`M ${x-4} ${height - bottomPadding} L ${x} ${height - bottomPadding - 8} L ${x+4} ${height - bottomPadding}`}
//                     fill='#30C4B8'
//                 />
//             </g>}
//         </>
//     });

//     const [ tooltip, setTooltip ] = useState(null);

//     useEffect(() => {
//         // console.log(tooltip);
//     }, [ tooltip ]);

//     return <>
//         <svg ref={ref}
//             width={width}
//             height={height}
//             style={{
//                 // backgroundColor: '#fcfcfd',
//             }}
//         >
//             <Axis domain={xAxisDomain} range={[0, width - leftPadding - rightPadding - barWidth]} transform={`translate(${leftPadding}, ${height - bottomPadding})`}/>
//             <YAxis width={width - leftPadding - rightPadding - barWidth} domain={[maxValue * 1.5, 0]} range={[0, height - topPadding - bottomPadding]} transform={`translate(${leftPadding}, ${topPadding})`}/>
//             <Y1Axis width={width - leftPadding - rightPadding - barWidth} domain={[maxBalance * 1.5, 0]} range={[0, height - topPadding - bottomPadding]} transform={`translate(${width - rightPadding}, ${topPadding})`}/>

//             {/* <rect x='100' y='100' width='20' height='100'></rect> */}
//             {bars}
//             {/* <path d="M 10 80 C 40 10, 65 10, 95 80 S 250 150, 380 80" stroke="black" fill="transparent"/> */}
//             <CurvedLine points={points}/>

//             {points.length > 0 && <>
//                 <circle cx={points[0][0]} cy={points[0][1]} r={3} stroke="#62CAF7" fill='white'></circle>
//                 <circle cx={points[points.length-1][0]} cy={points[points.length-1][1]} r={3} stroke="#62CAF7" fill='white'></circle>
//             </>}
//         </svg>

//         {tooltip && <div style={{
//             position: 'relative',
//             left: `${tooltip.x - 50}px`,
//             top: `-${height - tooltip.y + 75}px`,
//             // top: '-150px'
//             // 'z-index': 999
//             display: 'inline-block',
//             border: '1px solid #d0d6ef',
//             borderRadius: 3,
//         }}>
//             <div className='tooltip bar-tooltip'>
//                 <div className={`profit-loss ${tooltip.value < 0 ? 'negative' : 'positive'}`}>
//                     V: {`${numFormat(Math.abs(tooltip.value), 'USD', 0)}`}
//                 </div>
//                 <div className={`balance`}>
//                     B: {`${numFormat(tooltip.balance, 'USD', 0)}`}
//                 </div>

//                 <div className='arrow-down'>
//                     <div className='arrow-down-inner'></div>
//                 </div>
//             </div>
//         </div>}
//     </>
// }

// function CurvedLine(props) {
//     // The smoothing ratio
//     const smoothing = 0.2

//     // const points = [
//     //   [5, 10],
//     //   [10, 40],
//     //   [40, 30],
//     //   [60, 5],
//     //   [90, 45],
//     //   [120, 10],
//     //   [150, 45],
//     //   [200, 10]
//     // ]

//     // Properties of a line
//     // I:  - pointA (array) [x,y]: coordinates
//     //     - pointB (array) [x,y]: coordinates
//     // O:  - (object) { length: l, angle: a }: properties of the line
//     const line = (pointA, pointB) => {
//         const lengthX = pointB[0] - pointA[0]
//         const lengthY = pointB[1] - pointA[1]
//         return {
//         length: Math.sqrt(Math.pow(lengthX, 2) + Math.pow(lengthY, 2)),
//         angle: Math.atan2(lengthY, lengthX)
//         }
//     }

//     // Position of a control point
//     // I:  - current (array) [x, y]: current point coordinates
//     //     - previous (array) [x, y]: previous point coordinates
//     //     - next (array) [x, y]: next point coordinates
//     //     - reverse (boolean, optional): sets the direction
//     // O:  - (array) [x,y]: a tuple of coordinates
//     const controlPoint = (current, previous, next, reverse) => {
//         // When 'current' is the first or last point of the array
//         // 'previous' or 'next' don't exist.
//         // Replace with 'current'
//         const p = previous || current
//         const n = next || current

//         // Properties of the opposed-line
//         const o = line(p, n)

//         // If is end-control-point, add PI to the angle to go backward
//         const angle = o.angle + (reverse ? Math.PI : 0)
//         const length = o.length * smoothing

//         // The control point position is relative to the current point
//         const x = current[0] + Math.cos(angle) * length
//         const y = current[1] + Math.sin(angle) * length
//         return [x, y]
//     }

//     // Create the bezier curve command
//     // I:  - point (array) [x,y]: current point coordinates
//     //     - i (integer): index of 'point' in the array 'a'
//     //     - a (array): complete array of points coordinates
//     // O:  - (string) 'C x2,y2 x1,y1 x,y': SVG cubic bezier C command
//     const bezierCommand = (point, i, a) => {
//         // start control point
//         const cps = controlPoint(a[i - 1], a[i - 2], point)

//         // end control point
//         const cpe = controlPoint(point, a[i - 1], a[i + 1], true)
//         return `C ${cps[0]},${cps[1]} ${cpe[0]},${cpe[1]} ${point[0]},${point[1]}`
//     }

//     // Render the svg <path> element
//     // I:  - points (array): points coordinates
//     //     - command (function)
//     //       I:  - point (array) [x,y]: current point coordinates
//     //           - i (integer): index of 'point' in the array 'a'
//     //           - a (array): complete array of points coordinates
//     //       O:  - (string) a svg path command
//     // O:  - (string): a Svg <path> element
//     const svgPath = (points, command) => {
//         // build the d attributes by looping over the points
//         // console.log('sd---------------------')
//         const d = props.points.reduce((acc, point, i, a) => i === 0
//         ? `M ${point[0]},${point[1]}`
//         : `${acc} ${command(point, i, a)}`
//         , '')
//         // console.log(d, 'sd---------------------')
//         return <path d={d} fill="none" stroke="#62CAF7" strokeWidth={2}/>
//     }

//     // console.log(props.points)
//     // const svg = document.querySelector('.svg')

//     // svg.innerHTML = svgPath(points, bezierCommand)
//     return <>
//         {svgPath(props.points, bezierCommand)}
//     </>
// }

// function Axis(props) {
//     const ticks = useMemo(() => {
//         const xScale = d3.scaleLinear()
//             .domain([0, props.domain.length - 1])
//             .range(props.range);
//         const width = props.range[1] - props.range[0];
//         const pixelsPerTick = 20;
//         // let numberOfTicksTarget = Math.max(
//         //     1,
//         //     Math.floor(width / pixelsPerTick),
//         // );
//         // numberOfTicksTarget = 10;
//         // console.log(xScale('A'), xScale('B'), xScale('C'))
//         return props.domain.map((value, index) => ({
//             value,
//             xOffset: xScale(index),
//             index: index
//         }))
//     }, [ props.domain.join('-'), props.range.join('-') ]);

//     return <g transform={props.transform}>
//         <path d={[
//                 'M', 0, 0,
//                 'H', props.range[1] + 20,
//             ].join(' ')}
//             fill='#E6EAF9'
//             stroke='#E6EAF9'
//         />
//         {ticks.map(({ value, xOffset, index }) => {
//             let displayText = '';
//             let date = moment(value),
//                 month = date.month(),
//                 year = date.year(),
//                 textColor = '#676478';

//             if (ticks.length > 12 && month % 3 != 0) {
//                 return
//             } else {
//                 // console.log(month)
//                 if (month == 0) {
//                     displayText = year;
//                     textColor = '#241F3E';
//                 } else {
//                     displayText = date.format('MMM');
//                 }
//             }

//             return <g key={value}
//                 transform={`translate(${xOffset}, 0)`}
//             >
//                 <line y2='6' stroke='#D2DAF6' strokeWidth='2px'/>

//                 <text key={value}
//                     style={{
//                         fontSize: '10px',
//                         textAchor: 'middle',
//                         transform: 'translateY(20px)',
//                         fill: `${textColor}`,
//                         'font-weight': `${month == 0 ? 'bold' : ''}`,
//                     }}
//                 >
//                     {displayText}
//                 </text>
//             </g>
//         })}
//     </g>
// }

// function YAxis(props) {
//     const ticks = useMemo(() => {
//         const yScale = d3.scaleLinear()
//             .domain(props.domain)
//             .range(props.range);

//         const height = props.range[1] - props.range[0];
//         const pixelsPerTick = 30;
//         let numberOfTicksTarget = Math.max(
//             1,
//             Math.floor(height / pixelsPerTick),
//         );
//         // numberOfTicksTarget = 10;

//         return yScale.ticks(numberOfTicksTarget).map(value => {
//             return {
//                 value,
//                 yOffset: yScale(value),
//             }
//         })
//     }, [ props.domain.join('-'), props.range.join('-') ]);

//     return <g transform={props.transform}>
//         <path d={[
//                 'M', 0, 0,
//                 'v', props.range[1],
//             ].join(' ')}
//             fill='#E6EAF9'
//             stroke='#E6EAF9'
//         />

//         {ticks.map(({ value, yOffset }) => {
//             console.log(0, yOffset, props.width);
//             return <g key={value}
//                 transform={`translate(0, ${yOffset})`}
//             >
//                 { value != 0 && <line x2={props.width + 20} stroke-dasharray={`3, 8`} stroke='#B4BDE1' />}

//                 <text key={value}
//                     style={{
//                         fontSize: '10px',
//                         fill: '#676478',
//                         // textAnchor: 'middle',
//                         transform: 'translateX(-20px)',
//                         direction: 'rtl'
//                     }}
//                 >
//                     {/* {`${numFormat(value, 'USD', 0)}`} */}
//                     {(d3.format('.2s'))(value)}
//                 </text>
//             </g>
//         })}
//     </g>
// }

// function Y1Axis(props) {
//     const ticks = useMemo(() => {
//         const yScale = d3.scaleLinear()
//             .domain(props.domain)
//             .range(props.range);

//         const height = props.range[1] - props.range[0];
//         const pixelsPerTick = 30;
//         let numberOfTicksTarget = Math.max(
//             1,
//             Math.floor(height / pixelsPerTick),
//         );
//         // numberOfTicksTarget = 10;

//         return yScale.ticks(numberOfTicksTarget).map(value => {
//             return {
//                 value,
//                 yOffset: yScale(value),
//             }
//         })
//     }, [ props.domain.join('-'), props.range.join('-') ]);

//     return <g transform={props.transform}>
//         <path d={[
//                 'M', 0, 0,
//                 'v', props.range[1],
//             ].join(' ')}
//             fill='#E6EAF9'
//             stroke='#E6EAF9'
//         />

//         {ticks.map(({ value, yOffset }) => {
//             // console.log(0, yOffset);
//             return <g key={value}
//                 transform={`translate(0, ${yOffset})`}
//             >
//                 { value != 0 && <line x2={props.width + 30} />}

//                 <text key={value}
//                     style={{
//                         fontSize: '10px',
//                         fill: '#676478',
//                         // textAnchor: 'middle',
//                         transform: 'translateX(20px)',
//                         // direction: 'rtl'
//                     }}
//                 >
//                     {/* {`${numFormat(value, 'USD', 0)}`} */}
//                     {(d3.format('.2s'))(value)}
//                 </text>
//             </g>
//         })}
//     </g>
// }