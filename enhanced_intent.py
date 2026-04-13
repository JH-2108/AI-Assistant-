import re
from typing import Tuple, Dict, List, Optional
from rapidfuzz import fuzz

class EnhancedIntentDetector:
    def __init__(self):
        self.intent_patterns = self._load_intent_patterns()
        self.question_indicators = self._load_question_indicators()
        self.action_indicators = self._load_action_indicators()
        
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load comprehensive intent patterns"""
        return {
            "greeting": [
                r"^(hi|hello|hey|good morning|good afternoon|good evening|yo|what's up)",
                r"^(how are you|how do you do)",
                r"^(jarvis|assistant|ai)\s*$",
            ],
            "farewell": [
                r"^(bye|goodbye|see you|later|cya|farewell)",
                r"^(talk to you later|see you later)",
            ],
            "time": [
                r"\bwhat time is it\b",
                r"\bwhat is the time\b",
                r"\btell me the time\b",
                r"\bcurrent time\b",
                r"\bwhat's the time\b",
                r"\bwhat is today's date\b",
                r"\btoday's date\b",
                r"\bcurrent date\b",
                r"\bwhat is the date\b",
                r"^(time|date|clock)$",
            ],
            "weather": [
                r"\bweather\b",
                r"\btemperature\b",
                r"\brain\b",
                r"\bsnow\b",
                r"\bsunny\b",
                r"\bforecast\b",
            ],
            "music": [
                r"\bplay\s+(music|song|track)\b",
                r"\bspotify\b",
                r"\btune(s)?\b",
                r"\blisten to\s+(music|song)\b",
                r"\bput on\s+(music|song)\b",
            ],
            "video": [
                r"\bwatch\s+(video|movie|film)\b",
                r"\byoutube\b",
                r"\bnetflix\b",
                r"\bstream\b",
                r"\bplay\s+(video|movie)\b",
            ],
            "search": [
                r"\bsearch\b",
                r"\bgoogle\b",
                r"\blook up\b",
                r"\bfind\b",
                r"\bwhat is\b",
                r"\bwho is\b",
                r"\bwhere is\b",
            ],
            "open": [
                r"\bopen\s+",
                r"\blaunch\s+",
                r"\bstart\s+",
                r"\brun\s+",
                r"\bfind\s+(?:file|document)\s+",
                r"\bsearch\s+(?:for\s+)?(?:file|document)\s+",
                r"\bopen\s+file\s+",
                r"\blocate\s+(?:file|document)\s+",
            ],
            "create": [
                r"\bcreate\s+",
                r"\bmake\s+",
                r"\bdesign\s+",
                r"\bbuild\s+",
                r"\bgenerate\s+",
            ],
            "help": [
                r"\bhelp\b",
                r"\bhow to\b",
                r"\binstructions\b",
                r"\btutorial\b",
            ],
            "suggest": [
                r"\bsuggest\b",
                r"\brecommend\b",
                r"\bgive me\s+(suggestions|ideas|recommendations)\b",
                r"\bwhat\s+(should|could)\s+i\b",
                r"\bwhat\s+(kind|type)\s+of\b",
                r"\bany\s+(ideas|suggestions|recommendations)\b",
                r"\bcould\s+(you|one)\s+suggest\b",
                r"\bdo\s+you\s+(have|know)\s+(any|some)\s+(ideas|suggestions)\b",
                r"\bwhat\s+(are|is)\s+(good|best|popular)\b",
            ],
            "system": [
                r"\bshutdown\b",
                r"\brestart\b",
                r"\bsleep\b",
                r"\bhibernate\b",
                r"\block\b",
            ],
        }
    
    def _load_question_indicators(self) -> List[str]:
        """Load question detection patterns"""
        return [
            r"\?",
            r"^(what|who|why|how|when|where|which)\s+",
            r"^(can you|could you|would you|will you)\s+",
            r"^(do you|are you|is it|does it)\s+",
            r"^(tell me|explain|describe|discuss)\s+",
            r"\b(meaning|definition|explanation)\b",
            r"\babout\s+",
            r"\b(?:is|are|was|were|do|does|did)\s+",
        ]
    
    def _load_action_indicators(self) -> List[str]:
        """Load action command patterns"""
        return [
            r"\b(open|launch|start|run|play|watch|listen|create|make|design|build)\s+",
            r"\b(search|google|find|look up)\s+",
            r"\b(show|display|tell me)\s+",
            r"\b(help|assist)\s+",
            r"\b(shutdown|restart|sleep|lock)\s+",
        ]
    
    def is_question(self, text: str) -> bool:
        """Enhanced question detection"""
        text = text.lower().strip()
        
        # Check for explicit question mark
        if "?" in text:
            return True
        
        # Check for question patterns
        for pattern in self.question_indicators:
            if re.search(pattern, text):
                return True
        
        return False
    
    def is_action_command(self, text: str) -> bool:
        """Enhanced action command detection"""
        text = text.lower().strip()
        
        # Check for action patterns
        for pattern in self.action_indicators:
            if re.search(pattern, text):
                return True
        
        return False
    
    def extract_intent_and_content(self, text: str) -> Tuple[str, str, bool]:
        """
        Extract intent, content, and whether it's a question
        Returns: (intent, content, is_question)
        """
        text = text.lower().strip()
        original_text = text
        
        # Check if it's a question first
        is_q = self.is_question(text)
        
        # Check for explicit intents
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    # Extract content after the intent pattern
                    content = re.sub(pattern, "", text, count=1).strip()
                    if not content:
                        content = original_text
                    return intent, content, is_q
        
        # Fuzzy matching for remaining cases
        intent_scores = self._calculate_intent_scores(text)
        best_intent = max(intent_scores, key=intent_scores.get)
        
        if intent_scores[best_intent] > 70:  # Confidence threshold
            content = text
            return best_intent, content, is_q
        
        # Default to chat
        return "chat", text, is_q
    
    def _calculate_intent_scores(self, text: str) -> Dict[str, int]:
        """Calculate fuzzy matching scores for intents"""
        scores = {}
        
        # Intent keywords for fuzzy matching
        intent_keywords = {
            "greeting": ["hello", "hi", "hey", "morning", "afternoon", "evening"],
            "music": ["music", "song", "track", "spotify", "tune", "play"],
            "video": ["video", "movie", "film", "watch", "youtube", "netflix", "stream"],
            "search": ["search", "google", "find", "look up", "what", "who", "where"],
            "open": ["open", "launch", "start", "run", "find", "search", "locate", "file", "document"],
            "create": ["create", "make", "design", "build", "generate"],
            "help": ["help", "how", "assist", "instruction"],
            "suggest": ["suggest", "recommend", "ideas", "suggestions", "recommendations", "what", "should", "could", "kind", "type", "any", "good", "best", "popular"],
            "system": ["shutdown", "restart", "sleep", "lock"],
        }
        
        for intent, keywords in intent_keywords.items():
            max_score = 0
            for keyword in keywords:
                score = fuzz.partial_ratio(keyword, text)
                max_score = max(max_score, score)
            scores[intent] = max_score
        
        return scores
    
    def separate_question_from_action(self, text: str) -> Tuple[str, str]:
        """
        Separate question content from action intent
        Returns: (action_intent, question_content)
        """
        text = text.lower().strip()
        
        # Look for patterns like "how do I open X" or "what is Y about"
        action_patterns = [
            r"(how do i|how can i|what is best way to)\s+(open|launch|start|run|create|make|design|build)\s+",
            r"(what|which)\s+(.+\s+)?(to|for)\s+(open|launch|start|run|create|make|design|build)\s+",
        ]
        
        # Look for suggestion patterns like "suggest some games" or "what games should I make"
        suggestion_patterns = [
            r"(suggest|recommend|give me)\s+(some|any|good|popular)\s+(games|ideas|suggestions)\b",
            r"what\s+(games|ideas|suggestions|kinds)\s+(should|could|would)\s+i\s+(make|create|build|design)\b",
            r"(can|could)\s+you\s+suggest\s+(some|any|good)\s+(games|ideas)\b",
            r"do\s+you\s+have\s+(any|some)\s+(game|idea)\s+suggestions\b",
            r"what\s+(are|is)\s+(good|best|popular)\s+(games|ideas)\s+(to\s+)?(make|create|build)\b",
        ]
        
        for pattern in action_patterns:
            match = re.search(pattern, text)
            if match:
                action_part = match.group(2) if len(match.groups()) >= 2 else match.group(1)
                question_part = text.replace(match.group(0), "").strip()
                return action_part, question_part
        
        for pattern in suggestion_patterns:
            match = re.search(pattern, text)
            if match:
                return "suggest", text.strip()
        
        # If no clear separation, return as is
        return "", text

# Global enhanced intent detector
enhanced_detector = EnhancedIntentDetector()

def detect_enhanced_intent(text: str) -> Tuple[str, str, bool]:
    """Enhanced intent detection wrapper"""
    return enhanced_detector.extract_intent_and_content(text)

def separate_question_action(text: str) -> Tuple[str, str]:
    """Separate question from action wrapper"""
    return enhanced_detector.separate_question_from_action(text)
