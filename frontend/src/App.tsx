import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Upload from './pages/Upload'
import Results from './pages/Results'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-dark-950">
        <Routes>
          <Route path="/" element={<Upload />} />
          <Route path="/results/:taskId" element={<Results />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

