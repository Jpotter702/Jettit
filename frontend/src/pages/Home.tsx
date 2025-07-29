import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { collectSubredditData } from '../services/api'
import './Home.css'

interface CollectionForm {
  subreddit: string
  sortType: 'hot' | 'new' | 'top'
  postLimit: number
  includeComments: boolean
  anonymizeUsers: boolean
}

const Home: React.FC = () => {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<CollectionForm>({
    defaultValues: {
      subreddit: '',
      sortType: 'hot',
      postLimit: 100,
      includeComments: true,
      anonymizeUsers: true
    }
  })

  const onSubmit = async (data: CollectionForm) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await collectSubredditData({
        subreddit: data.subreddit,
        sort_type: data.sortType,
        post_limit: data.postLimit,
        include_comments: data.includeComments,
        anonymize_users: data.anonymizeUsers
      })
      
      // Navigate to results page
      navigate(`/results/${response.job_id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="home">
      <div className="container">
        <h2>Collect Reddit Data</h2>
        <p>Enter a subreddit name to start collecting data</p>
        
        <form onSubmit={handleSubmit(onSubmit)} className="collection-form">
          <div className="form-group">
            <label htmlFor="subreddit">Subreddit Name</label>
            <input
              id="subreddit"
              type="text"
              placeholder="e.g., programming, askreddit"
              {...register('subreddit', { 
                required: 'Subreddit name is required',
                pattern: {
                  value: /^[a-zA-Z0-9_]+$/,
                  message: 'Invalid subreddit name format'
                }
              })}
            />
            {errors.subreddit && (
              <span className="error">{errors.subreddit.message}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="sortType">Sort Type</label>
            <select id="sortType" {...register('sortType')}>
              <option value="hot">Hot</option>
              <option value="new">New</option>
              <option value="top">Top</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="postLimit">Post Limit</label>
            <input
              id="postLimit"
              type="number"
              min="1"
              max="1000"
              {...register('postLimit', { 
                valueAsNumber: true,
                min: { value: 1, message: 'Minimum 1 post' },
                max: { value: 1000, message: 'Maximum 1000 posts' }
              })}
            />
            {errors.postLimit && (
              <span className="error">{errors.postLimit.message}</span>
            )}
          </div>

          <div className="form-group checkbox">
            <label>
              <input
                type="checkbox"
                {...register('includeComments')}
              />
              Include Comments
            </label>
          </div>

          <div className="form-group checkbox">
            <label>
              <input
                type="checkbox"
                {...register('anonymizeUsers')}
              />
              Anonymize Users
            </label>
          </div>

          <button 
            type="submit" 
            disabled={isLoading}
            className="submit-btn"
          >
            {isLoading ? 'Starting Collection...' : 'Start Collection'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}

export default Home 