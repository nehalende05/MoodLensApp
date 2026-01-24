#!/usr/bin/env python
"""
MoodLens Launcher Script
Quick start for the application
"""

import os
import sys
import webbrowser
import subprocess
import time
from pathlib import Path

class MoodLensLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / 'backend'
        self.frontend_dir = self.project_root / 'frontend'
        self.server_process = None
        
    def print_banner(self):
        """Print welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    🧠 MOODLENS 🧠                            ║
║              AI Mental Wellness Companion                    ║
║                                                              ║
║  Where Computer Vision Meets Human Emotions                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8+ required")
            print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
            return False
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    
    def check_dependencies(self):
        """Check if required packages are installed"""
        required = ['flask', 'numpy', 'cv2']
        missing = []
        
        for package in required:
            try:
                __import__(package if package != 'cv2' else 'cv2')
                print(f"✓ {package} installed")
            except ImportError:
                missing.append(package)
                print(f"✗ {package} NOT installed")
        
        if missing:
            print("\n⚠️  Missing dependencies. Run:")
            print(f"   pip install -r {self.backend_dir}/requirements.txt")
            return False
        return True
    
    def start_flask_server(self):
        """Start the Flask backend server"""
        print("\n🚀 Starting Flask server...")
        
        try:
            # Change to backend directory
            os.chdir(self.backend_dir)
            
            # Start Flask app
            self.server_process = subprocess.Popen(
                [sys.executable, 'app.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(3)
            
            if self.server_process.poll() is None:
                print("✓ Flask server running on http://localhost:5000")
                return True
            else:
                print("✗ Failed to start Flask server")
                return False
                
        except Exception as e:
            print(f"✗ Error starting server: {e}")
            return False
    
    def open_browser(self):
        """Open the application in browser"""
        print("\n🌐 Opening browser...")
        time.sleep(1)
        
        try:
            webbrowser.open('http://localhost:5000')
            print("✓ Browser opened")
            return True
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print("   Please open http://localhost:5000 manually")
            return False
    
    def launch_demo_mode(self):
        """Launch in demo mode (without backend)"""
        print("\n🎬 Launching MoodLens in Demo Mode...")
        print("   (Emotion detection uses simulated data)")
        
        frontend_path = self.frontend_dir / 'index.html'
        
        try:
            webbrowser.open('file:///' + str(frontend_path).replace('\\', '/'))
            print(f"✓ Demo opened in browser")
            return True
        except Exception as e:
            print(f"✗ Error opening demo: {e}")
            return False
    
    def print_usage_info(self):
        """Print usage information"""
        info = """
╔══════════════════════════════════════════════════════════════╗
║                   📖 USAGE INFORMATION                        ║
╚══════════════════════════════════════════════════════════════╝

🎯 Getting Started:

1. DASHBOARD
   - View your current emotional state
   - See stress, fatigue, and mood metrics
   - Quick access to all features

2. MONITOR
   - Click "Start Monitoring" to begin
   - Webcam feed shows in real-time
   - Emotion breakdown chart updates live

3. RECOMMENDATIONS
   - AI suggests interventions automatically
   - Choose from multiple options
   - Start interventions with one click

4. INSIGHTS
   - View your emotional trends
   - See detected patterns
   - Track intervention effectiveness

📋 Tips:

✓ Grant camera/microphone permissions when prompted
✓ Position yourself in good lighting
✓ Face the webcam clearly
✓ Provide feedback for better recommendations
✓ Use regularly to build your emotional profile

⚙️  Settings:

- Emotion thresholds: backend/config.py
- UI customization: frontend/styles.css
- Agent behavior: backend/agent.py

📞 Support:

- Check README.md for detailed documentation
- See QUICKSTART.md for a quick guide
- Review troubleshooting section

═══════════════════════════════════════════════════════════════

🎉 Ready to start your mental wellness journey!
        """
        print(info)
    
    def cleanup(self):
        """Clean up on exit"""
        if self.server_process:
            print("\n🛑 Stopping Flask server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            print("✓ Server stopped")
    
    def run_full_mode(self):
        """Run MoodLens in full mode with backend"""
        print("\n📋 Starting MoodLens (Full Mode)...\n")
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Check dependencies
        print("\n🔍 Checking dependencies...\n")
        if not self.check_dependencies():
            return False
        
        # Start server
        if not self.start_flask_server():
            return False
        
        # Open browser
        self.open_browser()
        
        # Print usage info
        self.print_usage_info()
        
        # Keep running
        try:
            print("\n💡 Press Ctrl+C to stop the server\n")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()
            print("\n👋 Thank you for using MoodLens!")
            return True
    
    def run_demo_mode(self):
        """Run MoodLens in demo mode"""
        print("\n🎬 Starting MoodLens (Demo Mode)...\n")
        
        if not self.launch_demo_mode():
            return False
        
        self.print_usage_info()
        
        # Keep running
        try:
            print("\n💡 Press Ctrl+C to exit\n")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Thank you for using MoodLens!")
            return True
    
    def show_menu(self):
        """Show launch options menu"""
        menu = """
╔══════════════════════════════════════════════════════════════╗
║              🎯 SELECT LAUNCH MODE                           ║
╚══════════════════════════════════════════════════════════════╝

1. 🚀 FULL MODE
   - Flask backend server
   - Real webcam emotion detection
   - Full AI agent functionality
   - Requires: Python dependencies
   → For production / full features

2. 🎬 DEMO MODE
   - No backend required
   - Simulated emotion data
   - UI preview & testing
   - Requires: Modern web browser
   → For quick preview / development

3. 📖 View Documentation
   - README.md
   - QUICKSTART.md

4. ❌ Exit

───────────────────────────────────────────────────────────────
        """
        print(menu)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            return 'full'
        elif choice == '2':
            return 'demo'
        elif choice == '3':
            return 'docs'
        elif choice == '4':
            return 'exit'
        else:
            print("❌ Invalid choice. Please try again.")
            return self.show_menu()
    
    def show_docs(self):
        """Show documentation menu"""
        docs_menu = """
╔══════════════════════════════════════════════════════════════╗
║              📚 DOCUMENTATION                                ║
╚══════════════════════════════════════════════════════════════╝

1. README.md
   - Complete project overview
   - Architecture & design
   - Full API documentation
   - Technology stack

2. QUICKSTART.md
   - 5-minute setup guide
   - Basic usage instructions
   - Troubleshooting tips
   - Configuration examples

3. Back to Main Menu

───────────────────────────────────────────────────────────────
        """
        print(docs_menu)
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            readme = self.project_root / 'README.md'
            print(f"\n📖 {readme}\n")
            print("To read: Open the file in a text editor")
        elif choice == '2':
            quickstart = self.project_root / 'QUICKSTART.md'
            print(f"\n📖 {quickstart}\n")
            print("To read: Open the file in a text editor")
        elif choice == '3':
            return None
        
        return self.show_menu()
    
    def run(self):
        """Main launcher routine"""
        self.print_banner()
        
        while True:
            choice = self.show_menu()
            
            if choice == 'full':
                self.run_full_mode()
                break
            elif choice == 'demo':
                self.run_demo_mode()
                break
            elif choice == 'docs':
                choice = self.show_docs()
                if choice is None:
                    continue
            elif choice == 'exit':
                print("\n👋 Thank you for using MoodLens!")
                break

def main():
    """Entry point"""
    try:
        launcher = MoodLensLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n\n👋 MoodLens closed")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
