#!/usr/bin/env python3

# Final fix for syntax error in Assistant.py
try:
    with open('Assistant.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the incomplete try-except structure
    # The issue is that there's an except block without a corresponding try block
    
    # Find the problematic section and fix it
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if 'except Exception as e:' in line and i > 0:
            # Check if this except block has a corresponding try block
            try_found = False
            for j in range(i-1, max(0, i-20), -1):
                if 'try:' in lines[j]:
                    # Check if this try block is still open (not closed by another except)
                    except_count = 0
                    try_count = 0
                    for k in range(j, i):
                        if 'try:' in lines[k]:
                            try_count += 1
                        elif 'except' in lines[k]:
                            except_count += 1
                    
                    if try_count > except_count:
                        try_found = True
                        break
            
            if not try_found:
                # This except block doesn't have a corresponding try block
                # Remove it since it's causing the syntax error
                continue
        
        fixed_lines.append(line)
    
    # Write back to file
    with open('Assistant.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("Fixed syntax error in Assistant.py")
    print("Removed problematic except block without corresponding try")
    print("Try running: python web_app.py")
    
except Exception as e:
    print(f"Error: {e}")
    # Alternative simple fix
    try:
        with open('Assistant.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple fix: remove the problematic except block
        content = content.replace(
            '        except Exception as e:\n            return f"Model upgrade failed: {str(e)}\\n\\nFor manual setup:\\n{get_ai_model_setup_guide()}"',
            ''
        )
        
        with open('Assistant.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Applied simple fix - removed problematic except block")
        print("Try running: python web_app.py")
        
    except Exception as e2:
        print(f"Simple fix also failed: {e2}")
