THEMES = {
    "dark": {
        "app_theme": "dark",
        "background": "#2b2b2b",
        "nav_bar": "#282828",
        "text_color": "#ffffff",
        "alt_text_color": "#000000",
        "dropdown_hover_color": "#333333",
        "tomorrow_schedule": "#7df19a",
        "day_after_tomorrow_schedule": "#ffe680",
        "note_background": "#1f1d1d",
        "focus_mode": "#000000",
        "focus_mode_text": "#ffffff"
    },
    "light": {
        "app_theme": "light",
        "background": "#f0f0f0",
        "nav_bar": "#e0e0e0",
        "text_color": "#000000",
        "alt_text_color": "#000000",
        "dropdown_hover_color": "#d3d3d3",
        "tomorrow_schedule": "#7df19a",
        "day_after_tomorrow_schedule": "#ffe680",
        "note_background": "#ffffff",
        "focus_mode": "#000000",
        "focus_mode_text": "#ffffff"
    }
}

def get_theme(name="dark"):
    return THEMES.get(name, THEMES["dark"])