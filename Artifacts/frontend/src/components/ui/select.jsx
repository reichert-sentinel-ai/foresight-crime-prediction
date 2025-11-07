import React, { useState, useRef, useEffect } from 'react';

// Define SelectItem first so it can be referenced
export const SelectItem = ({ value, children, onClick, isSelected, className = '' }) => (
  <div
    onClick={onClick}
    role="option"
    aria-selected={isSelected}
    className={`px-3 py-2 text-sm cursor-pointer hover:bg-gray-100 dark:hover:bg-[#2a2a2a] text-gray-900 dark:text-[#e5e5e5] ${isSelected ? 'bg-blue-50 dark:bg-blue-900/30' : ''} ${className}`}
    style={{ minHeight: '36px', display: 'flex', alignItems: 'center' }}
  >
    {children}
  </div>
);

export const SelectValue = ({ children }) => <span>{children}</span>;

export const SelectContent = ({ children, className = '' }) => (
  <div 
    className={`absolute z-[9999] w-full mt-1 bg-white dark:bg-[#1f1f1f] border-2 border-blue-400 dark:border-blue-500 rounded-md shadow-xl max-h-60 overflow-auto ${className}`} 
    style={{ 
      top: '100%',
      left: 0,
      right: 0,
      minWidth: '100%'
    }}
  >
    {children}
  </div>
);

export const SelectTrigger = ({ children, onClick, className = '', isOpen = false }) => (
  <button
    type="button"
    onClick={onClick}
    className={`flex items-center justify-between w-full px-3 py-2 text-sm border-2 border-gray-300 dark:border-[#2a2a2a] rounded-md bg-white dark:bg-[#1a1a1a] hover:bg-gray-50 dark:hover:bg-[#2a2a2a] focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 text-gray-900 dark:text-[#e5e5e5] ${isOpen ? 'border-blue-500 dark:border-blue-400' : ''} ${className}`}
  >
    {children}
    <svg 
      className={`w-4 h-4 ml-2 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
      fill="none" 
      stroke="currentColor" 
      viewBox="0 0 24 24"
    >
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
    </svg>
  </button>
);

export const Select = ({ value, onValueChange, children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const selectRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (selectRef.current && !selectRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Find SelectItem components recursively
  const findSelectItems = (children) => {
    const items = [];
    React.Children.forEach(children, (child) => {
      if (child?.type === SelectItem) {
        items.push(child);
      } else if (child?.props?.children) {
        items.push(...findSelectItems(child.props.children));
      }
    });
    return items;
  };

  const allItems = findSelectItems(children);
  const selectedItem = allItems.find(item => item?.props?.value === value);
  const selectedLabel = selectedItem?.props?.children || value || 'Select...';

  const handleItemClick = (itemValue) => {
    if (onValueChange) {
      onValueChange(itemValue);
    }
    setIsOpen(false);
  };

  return (
    <div ref={selectRef} className="relative w-full" style={{ overflow: 'visible' }}>
      {React.Children.map(children, child => {
        if (child?.type === SelectTrigger) {
          return React.cloneElement(child, {
            onClick: (e) => {
              e.stopPropagation();
              e.preventDefault();
              setIsOpen(!isOpen);
            },
            isOpen,
            children: React.Children.map(child.props.children, (grandChild) => {
              if (grandChild?.type === SelectValue) {
                return React.cloneElement(grandChild, { children: selectedLabel });
              }
              return grandChild;
            })
          });
        }
        if (child?.type === SelectContent) {
          return isOpen ? React.cloneElement(child, {
            children: React.Children.map(child.props.children, (grandChild) => {
              if (grandChild?.type === SelectItem) {
                return React.cloneElement(grandChild, {
                  onClick: (e) => {
                    e.stopPropagation();
                    handleItemClick(grandChild.props.value);
                  },
                  isSelected: grandChild.props.value === value
                });
              }
              return grandChild;
            })
          }) : null;
        }
        return child;
      })}
    </div>
  );
};

