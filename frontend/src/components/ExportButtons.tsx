import React, { useState } from 'react'
import { exportData } from '../services/api'
import './ExportButtons.css'

interface ExportButtonsProps {
  jobId: string
}

const ExportButtons: React.FC<ExportButtonsProps> = ({ jobId }) => {
  const [exporting, setExporting] = useState<string | null>(null)

  const handleExport = async (format: 'csv' | 'json' | 'jsonl') => {
    setExporting(format)
    try {
      await exportData(jobId, format)
    } catch (error) {
      console.error('Export failed:', error)
      alert('Export failed. Please try again.')
    } finally {
      setExporting(null)
    }
  }

  return (
    <div className="export-buttons">
      <h3>Export Data</h3>
      <div className="button-group">
        <button
          onClick={() => handleExport('csv')}
          disabled={exporting !== null}
          className="export-btn csv"
        >
          {exporting === 'csv' ? 'Exporting...' : 'Export as CSV'}
        </button>
        <button
          onClick={() => handleExport('json')}
          disabled={exporting !== null}
          className="export-btn json"
        >
          {exporting === 'json' ? 'Exporting...' : 'Export as JSON'}
        </button>
        <button
          onClick={() => handleExport('jsonl')}
          disabled={exporting !== null}
          className="export-btn jsonl"
        >
          {exporting === 'jsonl' ? 'Exporting...' : 'Export as JSONL'}
        </button>
      </div>
    </div>
  )
}

export default ExportButtons 