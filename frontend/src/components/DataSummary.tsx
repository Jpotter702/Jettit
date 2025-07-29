import React from 'react'
import './DataSummary.css'

interface Submission {
  id: string
  title: string
  score: number
  upvote_ratio: number
  num_comments: number
  author?: string
  subreddit: string
  created_utc: string
  url?: string
}

interface DataSummaryProps {
  data: Submission[]
}

const DataSummary: React.FC<DataSummaryProps> = ({ data }) => {
  if (data.length === 0) return null

  const totalScore = data.reduce((sum, item) => sum + item.score, 0)
  const avgScore = Math.round(totalScore / data.length)
  const avgUpvoteRatio = data.reduce((sum, item) => sum + item.upvote_ratio, 0) / data.length
  const totalComments = data.reduce((sum, item) => sum + item.num_comments, 0)
  const avgComments = Math.round(totalComments / data.length)
  
  const topPost = data.reduce((max, item) => item.score > max.score ? item : max, data[0])
  const mostCommented = data.reduce((max, item) => item.num_comments > max.num_comments ? item : max, data[0])

  return (
    <div className="data-summary">
      <h3>Data Summary</h3>
      <div className="summary-grid">
        <div className="summary-item">
          <div className="summary-value">{data.length}</div>
          <div className="summary-label">Total Posts</div>
        </div>
        <div className="summary-item">
          <div className="summary-value">{avgScore}</div>
          <div className="summary-label">Avg Score</div>
        </div>
        <div className="summary-item">
          <div className="summary-value">{(avgUpvoteRatio * 100).toFixed(1)}%</div>
          <div className="summary-label">Avg Upvote Ratio</div>
        </div>
        <div className="summary-item">
          <div className="summary-value">{avgComments}</div>
          <div className="summary-label">Avg Comments</div>
        </div>
      </div>
      
      <div className="summary-highlights">
        <div className="highlight-item">
          <strong>Top Post:</strong> {topPost.title.substring(0, 50)}... (Score: {topPost.score})
        </div>
        <div className="highlight-item">
          <strong>Most Commented:</strong> {mostCommented.title.substring(0, 50)}... ({mostCommented.num_comments} comments)
        </div>
      </div>
    </div>
  )
}

export default DataSummary 