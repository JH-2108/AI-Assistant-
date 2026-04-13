import threading
import queue
import time
import os
import re
from typing import Optional
import pyttsx3
import pygame

class VoiceResponder:
    def __init__(self):
        self.engine = None
        self.voice_queue = queue.Queue()
        self.is_speaking = False
        self.voice_enabled = True
        self.voice_thread = None
        self.init_voice_engine()
        
    def init_voice_engine(self):
        """Initialize text-to-speech engine with SSML support"""
        try:
            self.engine = pyttsx3.init(driverName='sapi5')  # Use SAPI5 for better SSML support
            
            # Configure voice settings
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a good voice (prefer female or natural sounding)
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                    elif 'david' in voice.name.lower() or 'male' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
            
            # Enable SSML support for better prosody
            try:
                self.engine.setProperty('speech-xml', True)
            except:
                pass  # Fall back if not supported
            
            # Set initial speech rate and volume for faster delivery
            self.engine.setProperty('rate', 180)  # Words per minute (fast and enthusiastic)
            self.engine.setProperty('volume', 0.95)  # Volume (0.0 to 1.0)
            
            # Start voice processing thread
            self.voice_thread = threading.Thread(target=self._voice_worker, daemon=True)
            self.voice_thread.start()
            
        except Exception as e:
            print(f"Voice engine initialization failed: {e}")
            # Try fallback without SSML
            try:
                self.engine = pyttsx3.init()
                voices = self.engine.getProperty('voices')
                if voices:
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.engine.setProperty('voice', voice.id)
                            break
                self.engine.setProperty('rate', 155)
                self.engine.setProperty('volume', 0.95)
                self.voice_thread = threading.Thread(target=self._voice_worker, daemon=True)
                self.voice_thread.start()
            except Exception as e2:
                print(f"Fallback voice engine failed: {e2}")
                self.voice_enabled = False
    
    def _voice_worker(self):
        """Background thread for processing voice queue"""
        while True:
            try:
                if not self.voice_queue.empty() and not self.is_speaking:
                    text = self.voice_queue.get(timeout=1)
                    if text and self.voice_enabled:
                        self._speak_text(text)
                else:
                    time.sleep(0.1)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Voice worker error: {e}")
    
    def _speak_text(self, text: str):
        """Actually speak the text with enthusiastic delivery and prosody"""
        try:
            self.is_speaking = True
            
            # Clean up text for better speech
            clean_text = self._clean_text_for_speech(text)
            
            if clean_text:
                # Convert to SSML for better prosody control
                ssml_text = self._convert_to_ssml(clean_text)
                
                # Speak with SSML for expressive delivery
                self.engine.say(ssml_text)
                self.engine.runAndWait()
            
            self.is_speaking = False
            
        except Exception as e:
            print(f"Speech error: {e}")
            self.is_speaking = False
    
    def _convert_to_ssml(self, text: str) -> str:
        """Convert text to SSML for better prosody and intonation"""
        # Try simple text first if SSML fails
        try:
            # SSML wrapper for expressive speech
            ssml = '<speak>'
            
            # Split into sentences for individual processing
            sentences = re.split(r'[.!?]+', text)
            
            for i, sentence in enumerate(sentences):
                sentence = sentence.strip()
                if not sentence:
                    continue
                    
                # Add prosody based on content
                if any(word in sentence.lower() for word in ['awesome', 'great', 'cool', 'excellent', 'fantastic']):
                    # Excited words - higher pitch and faster rate
                    ssml += f'<prosody pitch="+20%" rate="+10%" volume="+10dB">{sentence}</prosody>'
                elif any(word in sentence.lower() for word in ['hello', 'hi', 'hey', 'greetings']):
                    # Greetings - friendly and welcoming
                    ssml += f'<prosody pitch="+10%" rate="medium" volume="medium">{sentence}</prosody>'
                elif any(word in sentence.lower() for word in ['important', 'remember', 'note', 'attention']):
                    # Important words - emphasis and slower
                    ssml += f'<prosody pitch="medium" rate="-10%" volume="+5dB"><emphasis level="strong">{sentence}</emphasis></prosody>'
                elif any(word in sentence.lower() for word in ['sorry', 'oops', 'error', 'problem']):
                    # Apologies - lower pitch, softer
                    ssml += f'<prosody pitch="-10%" rate="-10%" volume="-5dB">{sentence}</prosody>'
                elif sentence.endswith('?'):
                    # Questions - rising intonation
                    ssml += f'<prosody pitch="+15%" rate="medium">{sentence}</prosody>'
                else:
                    # Regular speech - varied intonation to avoid monotone
                    pitch_variation = "+10%" if i % 2 == 0 else "medium"
                    rate_variation = "+5%" if len(sentence) < 10 else "medium"
                    ssml += f'<prosody pitch="{pitch_variation}" rate="{rate_variation}" volume="medium">{sentence}</prosody>'
                
                # Add minimal pauses between sentences for faster delivery
                if i < len(sentences) - 1:
                    ssml += '<break time="100ms"/>'
            
            ssml += '</speak>'
            return ssml
            
        except Exception:
            # Fallback to simple text with emphasis
            return self._add_simple_emphasis(text)
    
    def _add_simple_emphasis(self, text: str) -> str:
        """Add simple emphasis when SSML fails"""
        # Add dramatic pauses and emphasis manually
        text = text.replace('!', '! ')
        text = re.sub(r'\b(awesome|great|cool|excellent|fantastic)\b', r'**\1**', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(hello|hi|hey)\b', r'*\1*', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(important|remember|note)\b', r'**\1**', text, flags=re.IGNORECASE)
        
        # Ensure enthusiastic ending
        if not text.endswith(('!', '?', '.')):
            text += '!'
        
        return text
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text to make it more natural for enthusiastic speech"""
        if not text:
            return ""
        
        # Remove markdown and code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'#+\s*', '', text)
        
        # Replace special characters with more enthusiastic alternatives
        text = text.replace('→', 'to')
        text = text.replace('←', 'from')
        text = text.replace('↑', 'up')
        text = text.replace('↓', 'down')
        
        # Add enthusiastic emphasis markers for TTS
        text = text.replace('!', '! ')  # Add pause after exclamations
        text = re.sub(r'\b(awesome|great|cool|excellent|perfect|wonderful|fantastic)\b', r'\1!', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(hello|hi|hey|greetings)\b', r'\1 there!', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(thank you|thanks|thanks|appreciate)\b', r'Thanks so much!', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(yes|sure|okay|got it|alright)\b', r'Absolutely!', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(no|sorry|apologies|oops)\b', r'Oh no!', text, flags=re.IGNORECASE)
        
        # Add emphasis to important words
        emphasis_words = ['important', 'remember', 'note', 'attention', 'critical', 'essential']
        for word in emphasis_words:
            text = re.sub(rf'\b{word}\b', rf'**{word}**', text, flags=re.IGNORECASE)
        
        # Handle emojis (remove them but add enthusiastic punctuation)
        text = re.sub(r'[^\w\s\.,!?;:()-]', '', text)
        
        # Ensure enthusiastic ending
        if not text.endswith(('!', '?', '.')):
            text += '!'
        
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Limit length for better performance
        if len(text) > 500:
            text = text[:497] + "!"
        
        return text
    
    def speak(self, text: str, priority: bool = False):
        """Add text to speech queue"""
        if not self.voice_enabled or not text:
            return
        
        try:
            if priority:
                # Clear queue and speak immediately
                while not self.voice_queue.empty():
                    try:
                        self.voice_queue.get_nowait()
                    except queue.Empty:
                        break
            
            self.voice_queue.put(text)
            
        except Exception as e:
            print(f"Queue error: {e}")
    
    def speak_immediately(self, text: str):
        """Speak text immediately (bypass queue)"""
        if not self.voice_enabled or not text:
            return
        
        try:
            # Stop current speech if any
            if self.engine:
                self.engine.stop()
            
            # Speak immediately
            clean_text = self._clean_text_for_speech(text)
            if clean_text:
                self.engine.say(clean_text)
                self.engine.runAndWait()
                
        except Exception as e:
            print(f"Immediate speech error: {e}")
    
    def toggle_voice(self):
        """Toggle voice on/off"""
        self.voice_enabled = not self.voice_enabled
        status = "enabled" if self.voice_enabled else "disabled"
        self.speak_immediately(f"Voice {status}")
        return self.voice_enabled
    
    def set_voice_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        if self.engine:
            self.engine.setProperty('rate', max(50, min(400, rate)))
    
    def set_voice_volume(self, volume: float):
        """Set voice volume (0.0 to 1.0)"""
        if self.engine:
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.engine:
            self.engine.stop()
        self.is_speaking = False
        
        # Clear queue
        while not self.voice_queue.empty():
            try:
                self.voice_queue.get_nowait()
            except queue.Empty:
                break

# Global voice responder instance
voice_responder = VoiceResponder()

def speak_response(text: str, priority: bool = False):
    """Convenience function to speak a response with enthusiastic delivery"""
    # Apply tone settings before speaking
    from tone_manager import get_tone_manager
    tone_mgr = get_tone_manager()
    voice_settings = tone_mgr.get_voice_settings()
    
    # Update voice settings for current tone with enthusiastic modulation
    if voice_responder.engine:
        voice_responder.set_voice_rate(voice_settings.get("rate", 165))
        voice_responder.set_voice_volume(voice_settings.get("volume", 0.9))
        
        # Apply pitch adjustment if available
        pitch_adj = voice_settings.get("pitch_adjustment", 8)
        if hasattr(voice_responder.engine, 'setProperty'):
            try:
                # Try to set pitch for more enthusiastic delivery
                voice_responder.engine.setProperty('pitch', pitch_adj)
            except:
                pass  # Fall back if not supported
    
    voice_responder.speak(text, priority)

def speak_immediate(text: str):
    """Convenience function to speak immediately"""
    voice_responder.speak_immediately(text)

def toggle_voice():
    """Toggle voice on/off"""
    return voice_responder.toggle_voice()

def is_voice_enabled():
    """Check if voice is enabled"""
    return voice_responder.voice_enabled
