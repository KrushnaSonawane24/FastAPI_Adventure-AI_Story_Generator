import { useState } from "react"

function ThemeInput({ onSubmit }) {
    const [theme, setTheme] = useState("");
    const [error, setError] = useState("")

    const exampleThemes = [
        "🏴‍☠️ Pirates",
        "🚀 Space Adventure",
        "🏰 Medieval Fantasy",
        "🧟 Zombie Survival",
        "🔮 Magic School",
        "🦖 Jurassic Park"
    ];

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!theme.trim()) {
            setError("Please enter a theme name");
            return
        }

        onSubmit(theme);
    }

    const handleExampleClick = (example) => {
        setTheme(example);
        setError("");
    }

    return <div className="theme-input-container">
        <h2>✨ Generate Your Adventure</h2>
        <p>Enter a theme for your interactive story</p>

        <form onSubmit={handleSubmit}>
            <div className="input-group">
                <input
                    type="text"
                    value={theme}
                    onChange={(e) => {
                        setTheme(e.target.value);
                        setError("");
                    }}
                    placeholder="e.g., Pirates, Space, Medieval..."
                    className={error ? 'error' : ''}
                />
                {error && <p className="error-text">{error}</p>}
            </div>
            <button type="submit" className='generate-btn'>
                🎬 Generate Story
            </button>
        </form>

        <div className="examples">
            <h3>💡 Try These Examples</h3>
            <ul>
                {exampleThemes.map((example, index) => (
                    <li key={index} onClick={() => handleExampleClick(example)}>
                        {example}
                    </li>
                ))}
            </ul>
        </div>
    </div>
}

export default ThemeInput;