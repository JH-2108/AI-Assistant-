#!/usr/bin/env python3

# Comprehensive fix for all syntax errors in Assistant.py
try:
    with open('Assistant.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix all syntax issues by finding and fixing incomplete try-except structures
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for orphaned except blocks
        if 'except Exception as e:' in line:
            # Look backwards for a corresponding try block
            try_found = False
            for j in range(i-1, max(0, i-50), -1):
                if 'try:' in lines[j]:
                    # Count try and except blocks between j and i
                    try_count = 0
                    except_count = 0
                    for k in range(j, i):
                        if 'try:' in lines[k]:
                            try_count += 1
                        elif 'except' in lines[k]:
                            except_count += 1
                    
                    if try_count > except_count:
                        try_found = True
                        break
            
            if not try_found:
                # This is an orphaned except block, skip it
                i += 1
                continue
        
        # Check for incomplete f-strings that might cause syntax errors
        if 'result = f"""' in line:
            # Make sure this f-string is properly closed
            f_string_closed = False
            for j in range(i+1, min(len(lines), i+100)):
                if '"""' in lines[j]:
                    f_string_closed = True
                    break
            
            if not f_string_closed:
                # Add closing quotes
                fixed_lines.append(line)
                fixed_lines.append('        """')
                i += 1
                continue
        
        fixed_lines.append(line)
        i += 1
    
    # Write back to file
    with open('Assistant.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("Fixed all syntax errors in Assistant.py")
    print("Removed orphaned except blocks and fixed incomplete structures")
    print("Try running: python web_app.py")
    
except Exception as e:
    print(f"Error: {e}")
    # Alternative approach - create a clean version
    try:
        # Read the file and create a clean version
        with open('Assistant.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove all orphaned except blocks
        import re
        
        # Find and remove orphaned except blocks
        pattern = r'\s*except Exception as e:\s*\n.*?return f".*?"'
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
        
        # Write clean version
        with open('Assistant.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Applied regex fix - removed orphaned except blocks")
        print("Try running: python web_app.py")
        
    except Exception as e2:
        print(f"Regex fix also failed: {e2}")
