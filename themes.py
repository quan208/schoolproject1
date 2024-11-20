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
    },
    "vintage": {
        "app_theme": "light",
        "background": "#FDF7E4",
        "nav_bar": "#DED0B6",
        "text_color": "#000000",
        "alt_text_color": "#000000",
        "dropdown_hover_color": "#FAEED1",
        "tomorrow_schedule": "#7df19a",
        "day_after_tomorrow_schedule": "#ffe680",
        "note_background": "#FAEED1",
        "focus_mode": "#000000",
        "focus_mode_text": "#ffffff"
    },
    "pink heart": {
        "app_theme": "light",
        "background": "#FFE4E1",
        "nav_bar": "#FFC0CB",
        "text_color": "#000000",
        "alt_text_color": "#000000",
        "dropdown_hover_color": "#FFB6C1",
        "tomorrow_schedule": "#7df19a",
        "day_after_tomorrow_schedule": "#ffe680",
        "note_background": "#FFB6C1",
        "focus_mode": "#000000",
        "focus_mode_text": "#ffffff"
    },
    "blue sky": {
        "app_theme": "light",
        "background": "#E6E6FA",
        "nav_bar": "#ADD8E6",
        "text_color": "#000000",
        "alt_text_color": "#000000",
        "dropdown_hover_color": "#B0C4DE",
        "tomorrow_schedule": "#7df19a",
        "day_after_tomorrow_schedule": "#ffe680",
        "note_background": "#B0C4DE",
        "focus_mode": "#000000",
        "focus_mode_text": "#ffffff"
    }
}

def get_theme(name="dark"):
    return THEMES.get(name, THEMES["dark"])