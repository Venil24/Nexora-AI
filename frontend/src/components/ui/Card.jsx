import React from 'react'

const Card = ({
  children,
  className = '',
  hoverEffect = true,
  glass = false,
  ...props
}) => {
  return (
    <div
      className={`rounded-2xl border ${
        glass
          ? 'bg-white/80 dark:bg-gray-950/80 backdrop-blur-md border-white/20'
          : 'bg-white dark:bg-gray-950 border-gray-100 dark:border-gray-900'
      } ${
        hoverEffect
          ? 'shadow-premium hover:shadow-premium-hover transition-all duration-300 hover:-translate-y-[2px]'
          : 'shadow-premium'
      } p-6 ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}

export default Card
