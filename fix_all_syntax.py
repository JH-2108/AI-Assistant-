#!/usr/bin/env python3

# Comprehensive fix for all syntax issues in Assistant.py
with open('Assistant.py', 'r') as f:
    content = f.read()

# Fix 1: Remove problematic f-string in get_ai_model_setup_guide
content = content.replace(
    '1. INSTALL OLLAMA\\n   Download from: https://ollama.com/download\\n   Purpose: Run AI models locally\\n   Installation: \\n   - Windows: Download .exe installer\\n   - Mac: brew install ollama\\n   - Linux: curl -fsSL https://ollama.com/install.sh | sh',
    '''1. INSTALL OLLAMA
   Download from: https://ollama.com/download
   Purpose: Run AI models locally
   Installation: 
   - Windows: Download .exe installer
   - Mac: brew install ollama
   - Linux: curl -fsSL https://ollama.com/install.sh | sh'''
)

# Fix 2: Fix incomplete except block around line 682
content = content.replace(
    '        except Exception as e:\n        return f"❌ Model upgrade failed: {str(e)}\\n\\nFor manual setup:\\n{get_ai_model_setup_guide()}"',
    '''        except Exception as e:\n            return f"❌ Model upgrade failed: {str(e)}\\n\\nFor manual setup:\\n{get_ai_model_setup_guide()}"'''
)

# Write back to file
with open('Assistant.py', 'w') as f:
    f.write(content)

print("✅ Fixed all syntax issues in Assistant.py")
print("🚀 Your AI should now run properly!")
print("📋 Try running: python web_app.py")
