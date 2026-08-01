import { FiMoon, FiSun } from 'react-icons/fi'
import { useTheme } from '../../context/ThemeContext'

export default function ThemeToggle() { const { theme, toggleTheme } = useTheme(); return <button className="icon-button" type="button" onClick={toggleTheme} aria-label="Toggle color theme">{theme === 'light' ? <FiMoon /> : <FiSun />}</button> }
