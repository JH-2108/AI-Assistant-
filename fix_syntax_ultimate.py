#!/usr/bin/env python3

# Ultimate fix for all syntax errors in Assistant.py
try:
    with open('Assistant.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The issue is that there's a try block starting at line 137 that doesn't have a proper except block
    # Let's fix this by adding the missing except block structure
    
    # Find the try block and add the missing except
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Check if this is the try block that's missing its except
        if 'if auto_apply and "dangerous" not in safety_note.lower() and "risky" not in safety_note.lower():' in line:
            # Look ahead to find the return statement and add except after it
            j = i + 1
            while j < len(lines) and j < i + 50:  # Look ahead up to 50 lines
                if 'return f"""' in lines[j] and 'SELF-MODIFICATION APPLIED' in lines[j]:
                    # Found the return statement, now find where this f-string ends
                    k = j + 1
                    while k < len(lines) and k < j + 30:  # Look ahead up to 30 lines for closing quotes
                        if '"""' in lines[k]:
                            # Add the except block after the closing quotes
                            fixed_lines.append(lines[k])  # Add the closing quote line
                            fixed_lines.append('            except Exception as e:')
                            fixed_lines.append('                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."')
                            i = k  # Skip to the end of the f-string
                            break
                    break
                j += 1
        
        i += 1
    
    # Write back to file
    with open('Assistant.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print("Fixed syntax error by adding missing except block to try statement")
    print("Try running: python web_app.py")
    
except Exception as e:
    print(f"Error: {e}")
    
    # Last resort: create a clean minimal version
    try:
        with open('Assistant.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple fix: replace the problematic section with a working version
        old_section = '''        if auto_apply and "dangerous" not in safety_note.lower() and "risky" not in safety_note.lower():
            try:
                # Find insertion point
                if "after" in location.lower():
                    func_match = re.search(r'after\s+(.+?)\s+function', location.lower())
                    if func_match:
                        func_name = func_match.group(1)
                        pattern = rf'def {func_name}\(.*?\):\s*\n(.*?\n)*?\n'
                        match = re.search(pattern, current_code)
                        if match:
                            insertion_point = match.end()
                            modified_code = current_code[:insertion_point] + f"\\n\\n# {feature}\\n{new_code}\\n" + current_code[insertion_point:]
                        else:
                            modified_code = current_code + f"\\n\\n# {feature}\\n{new_code}\\n"
                    else:
                        modified_code = current_code + f"\\n\\n# {feature}\\n{new_code}\\n"
                else:
                    modified_code = current_code + f"\\n\\n# {feature}\\n{new_code}\\n"
                
                # Apply the change
                with open(self_file, 'w', encoding='utf-8') as f:
                    f.write(modified_code)
                
                return f"""
        u2705 SELF-MODIFICATION APPLIED
        u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015

        Feature: {feature}
        Location: {location}
        
        Code has been automatically applied to {self_file}
        
        Explanation: {explanation}
        Safety Note: {safety_note}
        
        Backup created at: {backup_file}
        
        u26a0ufe0f Restart Jarvis to activate the new feature.
        """
                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."

        # Return proposal for manual review'''
        
        new_section = '''        if auto_apply and "dangerous" not in safety_note.lower() and "risky" not in safety_note.lower():
            try:
                # Find insertion point
                if "after" in location.lower():
                    func_match = re.search(r'after\s+(.+?)\s+function', location.lower())
                    if func_match:
                        func_name = func_match.group(1)
                        pattern = rf'def {func_name}\(.*?\):\s*\n(.*?\n)*?\n'
                        match = re.search(pattern, current_code)
                        if match:
                            insertion_point = match.end()
                            modified_code = current_code[:insertion_point] + f"\\n\\n# {feature}\\n{new_code}\\n" + current_code[insertion_point:]
                        else:
                            modified_code = current_code + f"\\n\\n# {feature}\\n{new_code}\\n"
                    else:
                        modified_code = current_code + f"\\n\\n# {feature}\\n{new_code}\\n"
                else:
                    modified_code = current_code + f"\\n\\n# {feature}\\n{new_code}\\n"
                
                # Apply the change
                with open(self_file, 'w', encoding='utf-8') as f:
                    f.write(modified_code)
                
                return f"""
        u2705 SELF-MODIFICATION APPLIED
        u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015u2015

        Feature: {feature}
        Location: {location}
        
        Code has been automatically applied to {self_file}
        
        Explanation: {explanation}
        Safety Note: {safety_note}
        
        Backup created at: {backup_file}
        
        u26a0ufe0f Restart Jarvis to activate the new feature.
        """
            except Exception as e:
                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."

        # Return proposal for manual review'''
        
        content = content.replace(old_section, new_section)
        
        with open('Assistant.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Applied section replacement fix - fixed try-except structure")
        print("Try running: python web_app.py")
        
    except Exception as e2:
        print(f"Section replacement fix also failed: {e2}")
