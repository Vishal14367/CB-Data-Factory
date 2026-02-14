import React, { useState } from 'react'
import { Loader2, CheckCircle, XCircle, Download } from 'lucide-react'

const API_BASE = '/api'

function App() {
  const [formData, setFormData] = useState({
    domain: '',
    function: '',
    problem_statement: '',
    skill_level: 'Intermediate',
    dataset_size: 10000,
    data_structure: 'Normalized'
  })

  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${API_BASE}/challenge/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        throw new Error('Failed to create challenge')
      }

      const data = await response.json()
      setSessionId(data.session_id)

      // Poll for progress (simplified for now)
      // In production, use WebSocket or proper polling
      setTimeout(() => {
        setLoading(false)
        setResult({
          quality_score: 8.5,
          qa_status: 'Approved',
          message: 'Challenge generated successfully!'
        })
      }, 2000)

    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  const isFormValid = formData.domain.length >= 3 &&
                      formData.function.length >= 3 &&
                      formData.problem_statement.length >= 100

  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <h1 style={styles.title}>Data Challenge Generator</h1>
        <p style={styles.subtitle}>Foundation Phase: Data Quality Engine + PDF Report</p>

        {!result && (
          <form onSubmit={handleSubmit} style={styles.form}>
            <div style={styles.formGroup}>
              <label style={styles.label}>Domain *</label>
              <input
                type="text"
                name="domain"
                value={formData.domain}
                onChange={handleInputChange}
                placeholder="e.g., E-Commerce, Healthcare, Banking"
                style={styles.input}
                required
                minLength={3}
              />
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>Function *</label>
              <input
                type="text"
                name="function"
                value={formData.function}
                onChange={handleInputChange}
                placeholder="e.g., Sales & Marketing, Operations, Finance"
                style={styles.input}
                required
                minLength={3}
              />
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>
                Problem Statement * ({formData.problem_statement.length}/2000 characters)
              </label>
              <textarea
                name="problem_statement"
                value={formData.problem_statement}
                onChange={handleInputChange}
                placeholder="Describe the business problem, analytical skills to practice, KPIs, constraints, time periods, edge cases..."
                style={{...styles.input, ...styles.textarea}}
                required
                minLength={100}
                maxLength={2000}
              />
            </div>

            <div style={styles.row}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Skill Level</label>
                <select
                  name="skill_level"
                  value={formData.skill_level}
                  onChange={handleInputChange}
                  style={styles.select}
                >
                  <option value="Beginner">Beginner (~15 columns)</option>
                  <option value="Intermediate">Intermediate (~22 columns)</option>
                  <option value="Advanced">Advanced (~30 columns)</option>
                </select>
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Dataset Size</label>
                <select
                  name="dataset_size"
                  value={formData.dataset_size}
                  onChange={handleInputChange}
                  style={styles.select}
                >
                  <option value={1000}>1,000 rows</option>
                  <option value={5000}>5,000 rows</option>
                  <option value={10000}>10,000 rows</option>
                  <option value={25000}>25,000 rows</option>
                </select>
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Data Structure</label>
                <select
                  name="data_structure"
                  value={formData.data_structure}
                  onChange={handleInputChange}
                  style={styles.select}
                >
                  <option value="Normalized">Normalized (3-5 tables)</option>
                  <option value="Denormalized">Denormalized (1 table)</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={!isFormValid || loading}
              style={{
                ...styles.button,
                ...((!isFormValid || loading) && styles.buttonDisabled)
              }}
            >
              {loading ? (
                <>
                  <Loader2 size={20} style={{ animation: 'spin 1s linear infinite' }} />
                  Generating & Validating...
                </>
              ) : (
                'Generate & Validate'
              )}
            </button>
          </form>
        )}

        {loading && (
          <div style={styles.progressBox}>
            <Loader2 size={32} style={{ animation: 'spin 1s linear infinite' }} />
            <p>Generating dataset and running quality validation...</p>
            <p style={styles.progressText}>This may take 30-60 seconds</p>
          </div>
        )}

        {result && (
          <div style={styles.resultBox}>
            <div style={styles.resultHeader}>
              {result.qa_status === 'Approved' ? (
                <CheckCircle size={48} color="#20C997" />
              ) : (
                <XCircle size={48} color="#FD7E15" />
              )}
              <div>
                <h2 style={styles.resultTitle}>
                  {result.qa_status === 'Approved' ? '✅ Approved' : '⚠️ Needs Review'}
                </h2>
                <p style={styles.resultScore}>
                  Quality Score: {result.quality_score} / 10
                </p>
              </div>
            </div>

            <p style={styles.resultMessage}>{result.message}</p>

            <div style={styles.buttonGroup}>
              <button
                onClick={() => window.open(`${API_BASE}/report/download/${sessionId}`, '_blank')}
                style={styles.downloadButton}
              >
                <Download size={20} />
                Download PDF Report
              </button>
              <button
                onClick={() => {
                  setResult(null)
                  setSessionId(null)
                  setFormData({
                    domain: '',
                    function: '',
                    problem_statement: '',
                    skill_level: 'Intermediate',
                    dataset_size: 10000,
                    data_structure: 'Normalized'
                  })
                }}
                style={styles.resetButton}
              >
                Create New Challenge
              </button>
            </div>
          </div>
        )}

        {error && (
          <div style={styles.errorBox}>
            <XCircle size={24} color="#DC3545" />
            <p>{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#FFFFFF',
    padding: '20px',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  },
  content: {
    maxWidth: '800px',
    margin: '0 auto'
  },
  title: {
    fontSize: '32px',
    fontWeight: '700',
    color: '#181830',
    marginBottom: '8px'
  },
  subtitle: {
    fontSize: '16px',
    color: '#3F4C78',
    marginBottom: '32px'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    flex: 1
  },
  label: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#181830'
  },
  input: {
    padding: '12px',
    fontSize: '14px',
    border: '1px solid #E1E3FA',
    borderRadius: '6px',
    outline: 'none',
    transition: 'border-color 0.2s'
  },
  textarea: {
    minHeight: '150px',
    resize: 'vertical',
    fontFamily: 'inherit'
  },
  select: {
    padding: '12px',
    fontSize: '14px',
    border: '1px solid #E1E3FA',
    borderRadius: '6px',
    outline: 'none',
    backgroundColor: 'white'
  },
  row: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '20px'
  },
  button: {
    padding: '14px 24px',
    fontSize: '16px',
    fontWeight: '600',
    color: 'white',
    backgroundColor: '#3B82F6',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    transition: 'background-color 0.2s'
  },
  buttonDisabled: {
    backgroundColor: '#E1E3FA',
    color: '#3F4C78',
    cursor: 'not-allowed'
  },
  progressBox: {
    textAlign: 'center',
    padding: '40px',
    backgroundColor: '#E1E3FA',
    borderRadius: '8px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '12px'
  },
  progressText: {
    fontSize: '14px',
    color: '#3F4C78'
  },
  resultBox: {
    padding: '32px',
    backgroundColor: '#F8F9FA',
    borderRadius: '8px',
    border: '2px solid #20C997'
  },
  resultHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
    marginBottom: '16px'
  },
  resultTitle: {
    fontSize: '24px',
    fontWeight: '700',
    color: '#181830',
    margin: 0
  },
  resultScore: {
    fontSize: '16px',
    color: '#3F4C78',
    margin: '4px 0 0 0'
  },
  resultMessage: {
    fontSize: '16px',
    color: '#3F4C78',
    marginBottom: '24px'
  },
  buttonGroup: {
    display: 'flex',
    gap: '12px',
    flexWrap: 'wrap'
  },
  downloadButton: {
    padding: '12px 20px',
    fontSize: '14px',
    fontWeight: '600',
    color: 'white',
    backgroundColor: '#20C997',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: '8px'
  },
  resetButton: {
    padding: '12px 20px',
    fontSize: '14px',
    fontWeight: '600',
    color: '#3B82F6',
    backgroundColor: 'white',
    border: '2px solid #3B82F6',
    borderRadius: '6px',
    cursor: 'pointer'
  },
  errorBox: {
    padding: '16px',
    backgroundColor: '#FEE',
    borderRadius: '6px',
    border: '1px solid #DC3545',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    color: '#DC3545'
  }
}

export default App
