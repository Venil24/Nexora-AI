import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { Mail, ArrowLeft, CheckCircle } from 'lucide-react'
import { motion } from 'framer-motion'
import authService from '../../services/authService'
import Button from '../../components/ui/Button'
import Input from '../../components/ui/Input'

const ForgotPassword = () => {
  const [sent, setSent] = useState(false)
  const [loading, setLoading] = useState(false)
  const [apiError, setApiError] = useState('')
  const { register, handleSubmit, formState: { errors }, watch } = useForm()
  const email = watch('email')

  const onSubmit = async (data) => {
    setLoading(true)
    setApiError('')
    try {
      await authService.forgotPassword(data.email)
      setSent(true)
    } catch (err) {
      setApiError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {sent ? (
        <div className="text-center">
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-600 dark:text-emerald-400 rounded-full">
              <CheckCircle className="h-10 w-10" />
            </div>
          </div>
          <h2 className="text-2xl font-extrabold text-gray-900 dark:text-gray-100 mb-2">
            Check your inbox
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
            We sent a password reset link to <strong className="text-gray-900 dark:text-gray-100">{email}</strong>.
            Check your spam folder if you don't see it.
          </p>
          <Link to="/login">
            <Button variant="outline" className="w-full">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Login
            </Button>
          </Link>
        </div>
      ) : (
        <>
          <div className="flex justify-center mb-5">
            <div className="p-3 bg-primary-50 dark:bg-primary-950/40 text-primary-600 dark:text-primary-400 rounded-xl">
              <Mail className="h-7 w-7" />
            </div>
          </div>
          <h2 className="text-2xl font-extrabold text-gray-900 dark:text-gray-100 mb-1 text-center">
            Forgot your password?
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-8 text-center">
            Enter your email and we'll send you a reset link
          </p>

          {apiError && (
            <div className="mb-4 p-3 bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/50 rounded-xl text-sm text-rose-700 dark:text-rose-400 font-medium">
              {apiError}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5" id="forgot-password-form">
            <Input
              id="forgot-email"
              label="Email Address"
              type="email"
              placeholder="you@example.com"
              error={errors.email?.message}
              {...register('email', {
                required: 'Email is required',
                pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: 'Invalid email' }
              })}
            />

            <Button
              type="submit"
              loading={loading}
              className="w-full"
              size="lg"
              id="send-reset-link"
            >
              Send Reset Link
            </Button>
          </form>

          <div className="mt-6 text-center">
            <Link
              to="/login"
              className="inline-flex items-center text-sm font-semibold text-primary-600 dark:text-primary-400 hover:underline"
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back to Login
            </Link>
          </div>
        </>
      )}
    </motion.div>
  )
}

export default ForgotPassword
