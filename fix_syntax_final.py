#!/usr/bin/env python3

# Final comprehensive fix for syntax errors in Assistant.py
try:
    with open('Assistant.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the specific syntax error at line 178
    # The issue is that there's a try block without a corresponding except block
    
    # Find the problematic try block and add the missing except
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_lines.append(line)
        
        # Check if this is the return statement that needs an except block
        if 'return f"""' in line and i > 0:
            # Look for the try block that this return belongs to
            try_found = False
            for j in range(i-1, max(0, i-50), -1):
                if 'try:' in lines[j]:
                    # Check if this try block already has an except
                    has_except = False
                    for k in range(j+1, i):
                        if 'except' in lines[k]:
                            has_except = True
                            break
                    
                    if not has_except:
                        # Add the missing except block after the return statement
                        fixed_lines.append('            except Exception as e:')
                        fixed_lines.append('                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."')
                        try_found = True
                        break
            
            if try_found:
                continue
    
    # Write back to file
    with open('Assistant.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("Fixed syntax error by adding missing except block")
    print("Try running: python web_app.py")
    
except Exception as e:
    print(f"Error: {e}")
    
    # Alternative approach: simple regex fix
    try:
        with open('Assistant.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add missing except block after the try block
        content = content.replace(
            'return f"""\n        u2705 SELF-MODIFICATION APPLIED',
            'return f"""\n        u2705 SELF-MODIFICATION APPLIED'
        )
        
        # Find and fix the incomplete try-except structure
        import re
        
        # Add except block after the try block that's missing it
        pattern = r'(if auto_apply and "dangerous" not in safety_note\.lower\(\) and "risky" not in safety_note\.lower\(\):\s*try:.*?return f"""[^"]*""")'
        
        def add_except_block(match):
            return match.group(0) + '\n            except Exception as e:\n                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."'
        
        content = re.sub(pattern, add_except_block, content, flags=re.DOTALL)
        
        with open('Assistant.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Applied regex fix - added missing except block")
        print("Try running: python web_app.py")
        
    except Exception as e2:
        print(f"Regex fix also failed: {e2}")
