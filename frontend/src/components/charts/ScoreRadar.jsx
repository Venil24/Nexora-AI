import React from 'react'
import { Radar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

const ScoreRadar = ({ scores, theme = 'light' }) => {
  const isDark = theme === 'dark' || document.documentElement.classList.contains('dark')

  const data = {
    labels: [
      'ATS Format',
      'Formatting',
      'Keywords',
      'Experience',
      'Education',
      'Projects',
    ],
    datasets: [
      {
        label: 'Resume Score Breakdown',
        data: [
          scores.ats_score ?? 0,
          scores.formatting_score ?? 0,
          scores.keyword_score ?? 0,
          scores.experience_score ?? 0,
          scores.education_score ?? 0,
          scores.projects_score ?? 0,
        ],
        backgroundColor: 'rgba(124, 58, 237, 0.2)',
        borderColor: 'rgba(124, 58, 237, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(124, 58, 237, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(124, 58, 237, 1)',
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      r: {
        angleLines: {
          color: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.05)',
        },
        grid: {
          color: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.05)',
        },
        pointLabels: {
          color: isDark ? '#9CA3AF' : '#4B5563',
          font: {
            family: 'Inter',
            size: 11,
            weight: 'semibold',
          },
        },
        ticks: {
          color: isDark ? '#9CA3AF' : '#4B5563',
          backdropColor: 'transparent',
          font: {
            size: 9,
          },
          stepSize: 20,
        },
        min: 0,
        max: 100,
      },
    },
  }

  return (
    <div className="h-64 md:h-80 w-full flex items-center justify-center">
      <Radar data={data} options={options} />
    </div>
  )
}

export default ScoreRadar
