import React, { forwardRef } from 'react'

const Input = forwardRef(({
  label,
  type = 'text',
  error,
  className = '',
  id,
  placeholder,
  ...props
}, ref) => {
  return (
    <div className={`flex flex-col space-y-1.5 w-full ${className}`}>
      {label && (
        <label
          htmlFor={id}
          className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400"
        >
          {label}
        </label>
      )}
      <input
        id={id}
        type={type}
        ref={ref}
        placeholder={placeholder}
        className={`w-full px-4 py-2.5 rounded-lg border bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all duration-200 ${
          error
            ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20'
            : 'border-gray-200 dark:border-gray-800'
        }`}
        {...props}
      />
      {error && (
        <span className="text-xs text-red-500 font-medium">
          {error}
        </span>
      )}
    </div>
  )
})

Input.displayName = 'Input'

export default Input
