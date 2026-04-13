# Simple script to fix f-string syntax
with open('Assistant.py', 'r') as f:
    lines = f.readlines()

# Find the problematic line
for i, line in enumerate(lines):
    if "1. INSTALL OLLAMA" in line:
        # Replace with fixed version
        lines[i] = "1. INSTALL OLLAMA\n   Download from: https://ollama.com/download\n   Purpose: Run AI models locally\n   Installation: \n   - Windows: Download .exe installer\n   - Mac: brew install ollama\n   - Linux: curl -fsSL https://ollama.com/install.sh | sh"
        break

# Write back
with open('Assistant.py', 'w') as f:
    f.writelines(lines)

print("Fixed f-string syntax error")
