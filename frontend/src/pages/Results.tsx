import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getJobStatus, getCollectedData } from '../services/api'
import ResultsTable from '../components/ResultsTable'
import ExportButtons from '../components/ExportButtons'
import LoadingSpinner from '../components/LoadingSpinner'
import DataSummary from '../components/DataSummary'
import './Results.css'

interface JobStatus {
  job_id: string
  status: string
  progress?: number
  total_posts?: number
  collected_posts?: number
  error_message?: string
}

const Results: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>()
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null)
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [dataLoading, setDataLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!jobId) return

    const fetchStatus = async () => {
      try {
        const status = await getJobStatus(jobId)
        setJobStatus(status)
        
        if (status.status === 'completed') {
          setDataLoading(true)
          try {
            const resultData = await getCollectedData({ job_id: jobId })
            setData(resultData.data || [])
          } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch data')
          } finally {
            setDataLoading(false)
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch status')
      } finally {
        setLoading(false)
      }
    }

    fetchStatus()
    
    // Poll for status updates if job is still running
    if (jobStatus?.status === 'running' || jobStatus?.status === 'queued') {
      const interval = setInterval(fetchStatus, 5000)
      return () => clearInterval(interval)
    }
  }, [jobId, jobStatus?.status])

  if (loading) {
    return (
      <div className="results">
        <div className="container">
          <LoadingSpinner size="large" message="Loading collection results..." />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="results">
        <div className="container">
          <div className="error-message">{error}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="results">
      <div className="container">
        <h2>Collection Results</h2>
        
        {jobStatus && (
          <div className="job-status">
            <h3>Job Status: {jobStatus.status}</h3>
            {jobStatus.progress !== undefined && (
              <div className="progress">
                <div 
                  className="progress-bar" 
                  style={{ width: `${jobStatus.progress}%` }}
                ></div>
                <span>{jobStatus.progress}%</span>
              </div>
            )}
            {jobStatus.total_posts && (
              <p>Collected {jobStatus.collected_posts} of {jobStatus.total_posts} posts</p>
            )}
            {jobStatus.error_message && (
              <div className="error-message">{jobStatus.error_message}</div>
            )}
          </div>
        )}

        {jobStatus?.status === 'completed' && (
          <>
            <ExportButtons jobId={jobId!} />
            {dataLoading ? (
              <LoadingSpinner size="medium" message="Loading data..." />
            ) : data.length > 0 ? (
              <>
                <DataSummary data={data} />
                <ResultsTable data={data} />
              </>
            ) : (
              <div className="no-data">
                <p>No data was collected for this job.</p>
              </div>
            )}
          </>
        )}


      </div>
    </div>
  )
}

export default Results 