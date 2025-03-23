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
}"""