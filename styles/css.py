css = """
.character-card {
    border: 1px solid var(--border-color-primary) !important;
    border-radius: 8px;
    padding: 12px !important;
    background: var(--background-fill-secondary) !important;
    margin: 6px 0 !important;
    color: var(--body-text-color);
    box-shadow: var(--shadow-drop-lg);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px !important;
    margin-left: 12px;
}

.stat-item {
    font-size: 1em !important;
    padding: 6px 8px !important;
    background: var(--background-fill-primary);
    border-radius: 4px;
    border: 1px solid var(--border-color-primary);
}

.character-portrait {
    margin-bottom: 2px !important;
    border: 1px solid var(--border-color-primary) !important;
    border-radius: 6px !important;
    background: var(--background-fill-primary);
    max-width: 200px !important;
    height: auto !important;
    aspect-ratio: 1/1;
}
.name-container {
    margin: 8px 0 4px 0 !important;
}

.name-text {
    font-size: 1.2em !important;
    color: var(--body-text-color) !important;
    font-weight: 600;
    text-align: center;
}

.health-text {
    font-size: 1em !important;
    color: var(--error-text-color) !important;
    text-align: center;
    font-weight: 500;
}

.stats-header {
    font-size: 1.3em !important;
    color: var(--body-text-color) !important;
    margin-bottom: 12px !important;
    padding-bottom: 6px !important;
    border-bottom: 2px solid var(--border-color-primary);
}
.dice-button {
    width: 60px !important;
    height: 60px !important;
    border-radius: 10px !important;
    padding: 0 !important;
    font-size: 2em !important;
    display: flex !important;
    align-items: center;
    justify-content: center;
    border: 2px solid var(--border-color-primary) !important;
    transition: transform 0.1s;
}

.dice-button:hover {
    transform: scale(1.05);
}

@keyframes shake {
    0% { transform: rotate(0deg) translateX(0); }
    25% { transform: rotate(-15deg) translateX(-5px); }
    50% { transform: rotate(15deg) translateX(5px); }
    75% { transform: rotate(-10deg) translateX(-3px); }
    100% { transform: rotate(0deg) translateX(0); }
}

.shaking {
    animation: shake 0.4s ease-in-out;
}

.result-container {
    display: flex;
    align-items: center;
    margin: 15px 0;
}

.dice-result {
    font-size: 1.8em !important;
    font-weight: bold !important;
    color: var(--body-text-color) !important;
    padding: 8px 15px !important;
    background: var(--background-fill-primary);
    border-radius: 6px;
    border: 1px solid var(--border-color-primary);
    box-shadow: var(--shadow-drop-sm);
}
"""
js = """
function() {
    var btn = document.getElementById('dice-button');
    btn.classList.add('shaking');
    setTimeout(() => btn.classList.remove('shaking'), 400);
    return [];
}
"""