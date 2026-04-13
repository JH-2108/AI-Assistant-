#!/usr/bin/env python3

# Fix indentation issue in Assistant.py
with open('Assistant.py', 'r') as f:
    lines = f.readlines()

# Find and fix the indentation issue
for i, line in enumerate(lines):
    if line.strip().startswith('def is_self_modification_query(c):'):
        # Remove the 4 spaces of indentation
        lines[i] = 'def is_self_modification_query(c):\n'
    elif line.strip().startswith('"""Check if user wants Jarvis to modify itself"""') and i > 0:
        # Fix docstring indentation
        lines[i] = '    """Check if user wants Jarvis to modify itself"""\n'
    elif i > 0 and lines[i-1].strip().startswith('def is_self_modification_query(c):') and line.strip().startswith('mod_phrases'):
        # Fix the list indentation
        lines[i] = '    mod_phrases = [\n'

# Write back to file
with open('Assistant.py', 'w') as f:
    f.writelines(lines)

print("Fixed indentation issue in Assistant.py")
print("The is_self_modification_query function is now properly indented")
