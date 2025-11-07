import React from 'react';

export const Label = ({ 
  children, 
  className = '',
  htmlFor,
  ...props 
}) => (
  <label
    htmlFor={htmlFor}
    className={`
      text-sm font-medium leading-none 
      text-gray-900 dark:text-[#e5e5e5]
      peer-disabled:cursor-not-allowed peer-disabled:opacity-70
      ${className}
    `}
    {...props}
  >
    {children}
  </label>
);

