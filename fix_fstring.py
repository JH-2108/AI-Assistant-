#!/usr/bin/env python3

# Fix f-string syntax error in Assistant.py
with open('Assistant.py', 'r') as f:
    content = f.read()

# Find the problematic section and fix it
content = content.replace(
    "1. INSTALL OLLAMA\n   Download from: https://ollama.com/download\n   Purpose: Run AI models locally\n   Installation: \n   - Windows: Download .exe installer\n   - Mac: brew install ollama\n   - Linux: curl -fsSL https://ollama.com/install.sh | sh",
    """1. INSTALL OLLAMA
   Download from: https://ollama.com/download
   Purpose: Run AI models locally
   Installation: 
   - Windows: Download .exe installer
   - Mac: brew install ollama
   - Linux: curl -fsSL https://ollama.com/install.sh | sh"""
)

# Write back to file
with open('Assistant.py', 'w') as f:
    f.write(content)

print('Fixed f-string syntax error in get_ai_model_setup_guide function')
