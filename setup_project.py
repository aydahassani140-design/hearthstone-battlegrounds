import os

# ساختار استاندارد پروژه
structure = {
    "assets": ["minions", "heroes", "fonts", "icons"],
    "common": [],
    "data": [],
    "services": [],
    "ui": ["core", "components", "screens"],
}

files = {
    "common": ["__init__.py", "models.py"],
    "data": ["__init__.py", "minions_data.py"],
    "services": ["__init__.py", "engine.py", "drag_manager.py"],
    "ui/core": ["__init__.py", "app.py", "config.py", "event_bus.py"],
    "ui/components": ["__init__.py", "card_slot.py", "log_panel.py"],
    "ui/screens": ["__init__.py", "recruit_screen.py"],
    "": ["main.py", "requirements.txt"]
}

def create_structure():
    base_path = os.getcwd()
    print(f"🏗️  Building project in: {base_path}")

    # ساخت پوشه‌ها
    for folder, subfolders in structure.items():
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)
        for sub in subfolders:
            os.makedirs(os.path.join(base_path, folder, sub), exist_ok=True)
            # فایل __init__ برای پکیج شدن
            with open(os.path.join(base_path, folder, sub, "__init__.py"), 'w') as f: pass

    # ساخت فایل‌ها
    for path, filenames in files.items():
        target_dir = os.path.join(base_path, path) if path else base_path
        os.makedirs(target_dir, exist_ok=True)
        for fname in filenames:
            full_path = os.path.join(target_dir, fname)
            if not os.path.exists(full_path):
                with open(full_path, 'w') as f:
                    if fname.endswith(".py"):
                        f.write(f"# {fname}\n# Hearthstone Clone Project\n\n")
    
    print("✅ Project structure ready!")

if __name__ == "__main__":
    create_structure()