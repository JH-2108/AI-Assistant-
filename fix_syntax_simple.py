#!/usr/bin/env python3

# Fix indentation issue in Assistant.py
try:
    with open('Assistant.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the indentation issue by replacing the incorrectly indented function
    content = content.replace(
        '    def is_self_modification_query(c):\n    """Check if user wants Jarvis to modify itself"""',
        'def is_self_modification_query(c):\n    """Check if user wants Jarvis to modify itself"""'
    )
    
    with open('Assistant.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed indentation issue in Assistant.py")
    print("The is_self_modification_query function is now properly indented")
    print("Try running: python web_app.py")
    
except Exception as e:
    print(f"Error: {e}")
