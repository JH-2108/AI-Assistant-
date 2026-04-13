import sys

with open('Assistant.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Lines 159-178
# The string part contains an injected except block, and the real except block is missing at the end.
old_str_1 = '''                return f"""
            except Exception as e:
                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."
'''
new_str_1 = '''                return f"""
'''
content = content.replace(old_str_1, new_str_1)

old_str_2 = '''        """
                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."
'''
new_str_2 = '''        """
            except Exception as e:
                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."
'''
content = content.replace(old_str_2, new_str_2)

# Fix 2: Lines 208-212
old_str_3 = '''        
        return result
        
        return f"Error during self-modification: {str(e)}\\n\\nFor safety, I cannot proceed without understanding the error."'''
new_str_3 = '''        
        return result
        
    except Exception as e:
        return f"Error during self-modification: {str(e)}\\n\\nFor safety, I cannot proceed without understanding the error."'''
content = content.replace(old_str_3, new_str_3)

# Fix 3: Lines 251-255
old_str_4 = '''        
        return analysis
        
        return f"Self-analysis failed: {str(e)}"'''
new_str_4 = '''        
        return analysis
        
    except Exception as e:
        return f"Self-analysis failed: {str(e)}"'''
content = content.replace(old_str_4, new_str_4)

# Fix 4: Lines 359-363
old_str_5 = '''        """
        
        return f"Autonomous improvement failed: {str(e)}"'''
new_str_5 = '''        """
        
    except Exception as e:
        return f"Autonomous improvement failed: {str(e)}"'''
content = content.replace(old_str_5, new_str_5)

# Fix 5: Lines 441-446
old_str_6 = '''            time.sleep(IMPROVEMENT_INTERVAL)
            
            print(f"Continuous improvement error: {e}")'''
new_str_6 = '''            time.sleep(IMPROVEMENT_INTERVAL)
            
        except Exception as e:
            print(f"Continuous improvement error: {e}")'''
content = content.replace(old_str_6, new_str_6)

# Fix 6: Lines 655-678
old_str_7 = '''                return f"""
            except Exception as e:
                return f"Failed to auto-apply change: {str(e)}\\n\\nManual application required."
🚀 AI MODEL UPGRADED SUCCESSFULLY'''
new_str_7 = '''                return f"""
🚀 AI MODEL UPGRADED SUCCESSFULLY'''
content = content.replace(old_str_7, new_str_7)

old_str_8 = '''            else:
                return f"❌ Failed to download {new_model}: {result.stderr}"
        
            return f"❌ Model upgrade failed: {str(e)}\\n\\nFor manual setup:\\n{get_ai_model_setup_guide()}"'''
new_str_8 = '''            else:
                return f"❌ Failed to download {new_model}: {result.stderr}"
        
        except Exception as e:
            return f"❌ Model upgrade failed: {str(e)}\\n\\nFor manual setup:\\n{get_ai_model_setup_guide()}"'''
content = content.replace(old_str_8, new_str_8)

with open('Assistant.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax errors in Assistant.py")
