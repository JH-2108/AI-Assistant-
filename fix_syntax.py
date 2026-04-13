#!/usr/bin/env python3

# Fix f-string syntax error in Assistant.py
with open('Assistant.py', 'r') as f:
    content = f.read()

# Find and fix the problematic f-string
lines = content.split('\n')
for i, line in enumerate(lines):
    if '1. INSTALL OLLAMA' in line and 'Download ollama.exe and run' in line:
        # Fix the f-string syntax by using string concatenation
        fixed_line = '''1. INSTALL OLLAMA
   Download from: https://ollama.com/download
   Purpose: Run AI models locally
   Installation: 
   - Windows: Download .exe installer
   - Mac: brew install ollama
   - Linux: curl -fsSL https://ollama.com/install.sh | sh'''
        lines[i] = fixed_line

# Write back to file
with open('Assistant.py', 'w') as f:
    f.write('\n'.join(lines))

print('Fixed f-string syntax error in get_ai_model_setup_guide function')
