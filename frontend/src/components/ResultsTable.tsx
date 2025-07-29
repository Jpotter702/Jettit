import React, { useState, useEffect } from 'react'
import './ResultsTable.css'

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

interface ResultsTableProps {
  data: Submission[]
}

const ResultsTable: React.FC<ResultsTableProps> = ({ data }) => {
  const [sortBy, setSortBy] = useState<keyof Submission>('score')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const [filterKeyword, setFilterKeyword] = useState('')
  const [minScore, setMinScore] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage] = useState(20)

  const handleSort = (column: keyof Submission) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(column)
      setSortOrder('desc')
    }
  }

  const filteredAndSortedData = data
    .filter(item => {
      const matchesKeyword = filterKeyword === '' || 
        item.title.toLowerCase().includes(filterKeyword.toLowerCase())
      const matchesScore = minScore === '' || item.score >= parseInt(minScore)
      return matchesKeyword && matchesScore
    })
    .sort((a, b) => {
      const aVal = a[sortBy]
      const bVal = b[sortBy]
      
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return sortOrder === 'asc' 
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal)
      }
      
      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return sortOrder === 'asc' ? aVal - bVal : bVal - aVal
      }
      
      return 0
    })

  // Pagination logic
  const totalItems = filteredAndSortedData.length
  const totalPages = Math.ceil(totalItems / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentData = filteredAndSortedData.slice(startIndex, endIndex)

  // Reset to first page when filters change
  useEffect(() => {
    setCurrentPage(1)
  }, [filterKeyword, minScore])

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  return (
    <div className="results-table">
      <div className="filters">
        <div className="filter-group">
          <label>Search:</label>
          <input
            type="text"
            placeholder="Filter by title..."
            value={filterKeyword}
            onChange={(e) => setFilterKeyword(e.target.value)}
          />
        </div>
        <div className="filter-group">
          <label>Min Score:</label>
          <input
            type="number"
            placeholder="0"
            value={minScore}
            onChange={(e) => setMinScore(e.target.value)}
          />
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th onClick={() => handleSort('title')}>
              Title {sortBy === 'title' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('score')}>
              Score {sortBy === 'score' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('upvote_ratio')}>
              Upvote Ratio {sortBy === 'upvote_ratio' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('num_comments')}>
              Comments {sortBy === 'num_comments' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('author')}>
              Author {sortBy === 'author' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('created_utc')}>
              Created {sortBy === 'created_utc' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
          </tr>
        </thead>
        <tbody>
          {currentData.map((item) => (
            <tr key={item.id}>
              <td>
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.title}
                </a>
              </td>
              <td>{item.score}</td>
              <td>{(item.upvote_ratio * 100).toFixed(1)}%</td>
              <td>{item.num_comments}</td>
              <td>{item.author || 'Anonymous'}</td>
              <td>{new Date(item.created_utc).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="pagination">
          <div className="pagination-info">
            Showing {startIndex + 1}-{Math.min(endIndex, totalItems)} of {totalItems} results
          </div>
          <div className="pagination-controls">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="pagination-btn"
            >
              Previous
            </button>
            
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              let pageNum
              if (totalPages <= 5) {
                pageNum = i + 1
              } else if (currentPage <= 3) {
                pageNum = i + 1
              } else if (currentPage >= totalPages - 2) {
                pageNum = totalPages - 4 + i
              } else {
                pageNum = currentPage - 2 + i
              }
              
              return (
                <button
                  key={pageNum}
                  onClick={() => handlePageChange(pageNum)}
                  className={`pagination-btn ${currentPage === pageNum ? 'active' : ''}`}
                >
                  {pageNum}
                </button>
              )
            })}
            
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="pagination-btn"
            >
              Next
            </button>
          </div>
        </div>
      )}

      {filteredAndSortedData.length === 0 && (
        <div className="no-results">
          No results match your filters.
        </div>
      )}
    </div>
  )
}

export default ResultsTable
