import React from 'react'
import { SelectField } from './form'
import Checklist from './checklist'

interface ProductEditViewProps {
    updateData: any
    updateOnChange: any
    details?: any
}

const productDetails = [
    {
      label: "Privacy Policy Alignment",
      status: "error",
      keyWord: [],
      action: () => console.log("Add keywords for Privacy Policy Alignment"),
    },
    {
      label: "Third Party Opt-in",
      status: "error",
      keyWord: [],
      action: () => console.log("Add keywords for Third Party Opt-in"),
    },
    {
      label: "Data Collection Practices",
      status: "success",
      keyWord: ["user data", "cookies", "tracking"],
    },
    {
      label: "Purposes of Data Processing",
      status: "success",
      keyWord: ["marketing", "analytics", "personalization"],
    },
    {
      label: "Data Sharing and Disclosure",
      status: "success",
      keyWord: ["third-party", "consent"],
    },
    {
      label: "User Rights and Controls",
      status: "success",
      keyWord: ["opt-out", "access", "deletion"],
    },
    {
      label: "Data Security Measures",
      status: "error",
      keyWord: [],
      action: () => console.log("Add keywords for Data Security Measures"),
    },
    {
      label: "Data Retention",
      status: "success",
      keyWord: ["90 days", "policy retention", "data lifecycle"],
    },
];

const statusOptions = [
    { name: 'Approved', value: 'APPROVED' },
    { name: 'Pending Approval', value: 'PENDING_APPROVAL' },
    { name: 'Not Verified', value: 'NOT_VERIFIED' },
    { name: 'Rejected', value: 'REJECTED' },
];

export default function ProductEditView(props: ProductEditViewProps) {
    return <div className='product-edit-container'>
        <hr className='hr-line' />

        {/* Status Select Field */}
        <div className='edit-status'>
            <SelectField
                label='Status'
                name='status'
                value={props?.updateData['status']}
                onChange={props.updateOnChange}
                className='input-wrapper'
                options={statusOptions}
            />
        </div>
        
        <hr className='hr-line' />

        {/* Checklist Component */}
        <Checklist
            title='Policy Compliance'
            subtitle='Uploaded Date'
            text='Last Updated'
            subtitleText='Date Info'
            items={productDetails}
        />

    </div>
}