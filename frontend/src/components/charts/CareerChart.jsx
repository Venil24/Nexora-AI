import React from 'react'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const CareerChart = ({ topCareers = [] }) => {
  const isDark = document.documentElement.classList.contains('dark')

  const labels = topCareers.map((c) => c.career)
  const probabilities = topCareers.map((c) => c.probability)

  const data = {
    labels: labels.length > 0 ? labels : ['No Data'],
    datasets: [
      {
        data: probabilities.length > 0 ? probabilities : [0],
        backgroundColor: 'rgba(124, 58, 237, 0.85)',
        hoverBackgroundColor: 'rgba(124, 58, 237, 1)',
        borderRadius: 6,
        borderWidth: 0,
        barThickness: 16,
      },
    ],
  }

  const options = {
    indexAxis: 'y', // Makes it horizontal
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: isDark ? '#1F2937' : '#FFFFFF',
        titleColor: isDark ? '#F9FAFB' : '#111827',
        bodyColor: isDark ? '#D1D5DB' : '#374151',
        borderColor: isDark ? '#374151' : '#E5E7EB',
        borderWidth: 1,
        titleFont: { family: 'Inter', weight: 'bold' },
        bodyFont: { family: 'Inter' },
        displayColors: false,
        callbacks: {
          label: (context) => `Match Probability: ${context.parsed.x}%`,
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          color: isDark ? '#9CA3AF' : '#4B5563',
          font: { family: 'Inter', size: 10 },
          callback: (value) => `${value}%`,
        },
        min: 0,
        max: 100,
      },
      y: {
        grid: {
          display: false,
        },
        ticks: {
          color: isDark ? '#9CA3AF' : '#4B5563',
          font: { family: 'Inter', size: 11, weight: 'semibold' },
        },
      },
    },
  }

  return (
    <div className="h-64 w-full flex items-center justify-center">
      <Bar data={data} options={options} />
    </div>
  )
}

export default CareerChart
