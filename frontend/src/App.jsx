import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import StoryLoader from "./components/StoryLoader"
import StoryGenerator from "./components/StoryGenerator.jsx";

function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
          <h1>🎭 Interactive Story Generator</h1>
          <p>Create your own adventure with AI-powered storytelling</p>
        </header>
        <main>
          <Routes>
            <Route path={"/story/:id"} element={<StoryLoader />} />
            <Route path={"/"} element={<StoryGenerator />} />
          </Routes>
        </main>
        <footer>
          <div className="footer-content">
            <p className="made-by">
              Built with React & FastAPI by <strong>KRUSHNA</strong>
            </p>
            <a
              href="https://github.com/KrushnaSonawane24/FastAPI_Adventure-AI_Story_Generator"
              target="_blank"
              rel="noopener noreferrer"
              className="github-link"
            >
              <span>⭐</span>
              <span>View on GitHub</span>
            </a>
            <p className="copyright">© 2026 Interactive Story Generator</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App