import sys
import os

# اضافه کردن مسیر ریشه پروژه
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.core.app import App

if __name__ == "__main__":
    app = App()
    app.run()