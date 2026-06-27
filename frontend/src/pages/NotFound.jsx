import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FileText, Home } from 'lucide-react'
import Button from '../components/ui/Button'

const NotFound = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 px-4">
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="text-center max-w-md"
    >
      <div className="flex justify-center mb-6">
        <div className="p-4 bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400 rounded-2xl">
          <FileText className="h-12 w-12" />
        </div>
      </div>
      <h1 className="text-7xl font-extrabold gradient-text mb-4">404</h1>
      <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">Page not found</h2>
      <p className="text-gray-500 dark:text-gray-400 mb-8 text-sm">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Link to="/dashboard">
        <Button size="lg">
          <Home className="h-5 w-5 mr-2" />
          Back to Dashboard
        </Button>
      </Link>
    </motion.div>
  </div>
)

export default NotFound
