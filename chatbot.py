"""
Rule-Based AI Chatbot - Core Engine
====================================
A deterministic, rule-based conversational AI engine built strictly using
explicit logic, hash-map/dictionary lookups, input sanitization, and control flow.

Zero Generative AI / Zero Machine Learning / 100% Deterministic & Transparent.
"""

import re
import datetime
from typing import Dict, Any, Optional, Tuple, List


class RuleBasedChatbot:
    """
    Deterministic Rule-Based AI Chatbot.
    
    Demonstrates:
    1. Input Handling
    2. Input Sanitization (lowercase, strip, punctuation normalization)
    3. Intent Matching (Exact Hash-map Lookup + Rule Pattern Matching)
    4. Deterministic Decision Making
    5. Dictionary / Hash-Map Knowledge Base
    6. Safe Fallback Response via .get()
    7. Clean Exit Command Strategy
    8. Continuous Interaction Loop
    """

    # Exit commands that cleanly terminate conversation
    EXIT_COMMANDS = {
        "bye",
        "goodbye",
        "exit",
        "quit",
        "close",
        "terminate",
        "stop",
        "end"
    }

    # Predefined Fallback Response when no rule matches
    FALLBACK_RESPONSE = "I don't understand that yet. Try asking for help."

    def __init__(self):
        # Initialize the knowledge base dictionary
        self.knowledge_base = self._build_knowledge_base()
        self.direct_lookup_map = self._build_direct_lookup_map()

    def _build_knowledge_base(self) -> Dict[str, Dict[str, Any]]:
        """
        Builds the structured multi-intent knowledge base.
        Each intent contains patterns, possible responses, and metadata.
        """
        return {
            "greeting": {
                "description": "Standard greetings and welcomes",
                "patterns": [
                    "hello", "hi", "hey", "good morning", "good afternoon",
                    "good evening", "greetings", "howdy", "sup", "hey there", "hola"
                ],
                "response": "Hello! How can I help you today?"
            },
            "name": {
                "description": "Inquiries regarding the bot's identity",
                "patterns": [
                    "what is your name", "who are you", "your name",
                    "tell me your name", "what are you called", "identify yourself", "whats your name"
                ],
                "response": "I am a Rule-Based AI Chatbot, built using deterministic logic and control flow."
            },
            "help": {
                "description": "Guidance and available capability inquiries",
                "patterns": [
                    "help", "what can you do", "commands", "instructions",
                    "how to use", "options", "menu", "assist me"
                ],
                "response": "I can respond to predefined commands such as greetings, identity, status, project info, help, and goodbye. Type 'intents' or click any quick prompt to explore."
            },
            "status": {
                "description": "Questions about the chatbot's current state or well-being",
                "patterns": [
                    "how are you", "how are you doing", "how are things",
                    "what's up", "whats up", "how do you do", "are you okay"
                ],
                "response": "I'm doing great! Everything in my rule engine is running smoothly. Thanks for asking!"
            },
            "thanks": {
                "description": "Expressions of gratitude",
                "patterns": [
                    "thank you", "thanks", "thank you so much", "thanks a lot",
                    "appreciate it", "thx", "ty", "many thanks"
                ],
                "response": "You're very welcome! I'm happy to assist you."
            },
            "about_project": {
                "description": "Information about this Industrial Training AI kit",
                "patterns": [
                    "what is this project", "about project", "project info",
                    "tell me about this project", "project details", "what is rule based ai"
                ],
                "response": "This is 'Industrial Training Kit - AI Project 1: Rule-Based AI Chatbot'. It uses deterministic logic, hash-map lookups, and control flow without external LLMs or generative models."
            },
            "time": {
                "description": "Current date and time request",
                "patterns": [
                    "what time is it", "time", "current time", "date",
                    "what is the date", "today's date", "todays date"
                ],
                "response": f"Current system time is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            },
            "creator": {
                "description": "Developer and architecture credit",
                "patterns": [
                    "who created you", "who made you", "who is your developer",
                    "author", "who built you"
                ],
                "response": "I was developed for the Industrial Training Kit on Rule-Based AI Systems using Python, Flask, HTML, CSS, and JavaScript."
            },
            "intents_list": {
                "description": "Displays all supported intent categories",
                "patterns": [
                    "intents", "list intents", "show intents", "categories", "topics"
                ],
                "response": "Supported Intents:\n• greeting (hello, hi, hey)\n• name (what is your name, who are you)\n• help (help, what can you do)\n• status (how are you, how are you doing)\n• thanks (thank you, thanks)\n• about_project (what is this project)\n• time (what time is it)\n• goodbye (bye, exit, quit)"
            },
            "goodbye": {
                "description": "Polite farewell",
                "patterns": [
                    "bye", "goodbye", "see you", "see ya", "farewell", "cya", "have a good day"
                ],
                "response": "Goodbye! Have a great day!"
            }
        }

    def _build_direct_lookup_map(self) -> Dict[str, Tuple[str, str]]:
        """
        Builds a flattened hash-map (Dictionary) mapping normalized pattern string -> (intent_name, response_text).
        Provides O(1) instantaneous direct lookup time complexity.
        """
        lookup = {}
        for intent_name, intent_data in self.knowledge_base.items():
            for pattern in intent_data["patterns"]:
                # Ensure pattern itself is normalized
                clean_pattern = self.sanitize_input(pattern)
                lookup[clean_pattern] = (intent_name, intent_data["response"])
        return lookup

    @staticmethod
    def sanitize_input(raw_input: Optional[str]) -> str:
        """
        Sanitizes and normalizes user input:
        1. Handles None or non-string input safely.
        2. Converts text to lowercase.
        3. Strips leading and trailing whitespaces.
        4. Removes trailing punctuation marks (. ? ! , ; :) for robust matching.
        5. Normalizes internal multiple whitespaces to a single space.
        
        Example:
            '   HELLO, WORLD!  ' -> 'hello, world'
            '  What is your NAME? ' -> 'what is your name'
        """
        if raw_input is None:
            return ""
        
        # 1. Convert to string, lowercase, and strip bounding whitespace
        cleaned = str(raw_input).lower().strip()
        
        if not cleaned:
            return ""
        
        # 2. Collapse internal repeated whitespace
        cleaned = re.sub(r"\s+", " ", cleaned)
        
        # 3. Strip trailing punctuation for intent resilience
        cleaned = cleaned.rstrip(".?!,;:")
        
        return cleaned.strip()

    def check_exit_command(self, sanitized_input: str) -> bool:
        """
        Checks if the sanitized input matches any recognized exit command.
        """
        return sanitized_input in self.EXIT_COMMANDS

    def get_response(self, raw_input: str) -> Dict[str, Any]:
        """
        Main decision-making pipeline:
        Raw Input -> Sanitization -> Exit Check -> Hash-map Lookup -> Fallback -> Output
        
        Returns a structured dictionary with complete execution trace (useful for Debug Mode).
        """
        # Step 1: Input Sanitization
        clean_input = self.sanitize_input(raw_input)

        # Step 2: Handle empty input
        if not clean_input:
            return {
                "raw_input": raw_input,
                "sanitized_input": clean_input,
                "matched_intent": "empty_input",
                "matched_rule": "Rule: Empty Input Handler",
                "response": "Please type something so I can assist you! Type 'help' for options.",
                "is_exit": False,
                "status": "warning",
                "lookup_type": "guard_rail"
            }

        # Step 3: Check for Exit Strategy
        if self.check_exit_command(clean_input):
            return {
                "raw_input": raw_input,
                "sanitized_input": clean_input,
                "matched_intent": "exit",
                "matched_rule": f"Rule: Exit Command Match ('{clean_input}' in EXIT_COMMANDS)",
                "response": "Goodbye! Have a great day! Session has been terminated.",
                "is_exit": True,
                "status": "exit",
                "lookup_type": "control_flow_exit"
            }

        # Step 4: Direct Dictionary / Hash-Map Lookup (O(1) time complexity)
        # Demonstrates direct dictionary lookup using .get()
        direct_match = self.direct_lookup_map.get(clean_input)

        if direct_match:
            intent_name, response_text = direct_match
            # For dynamic intents like time, refresh response if needed
            if intent_name == "time":
                response_text = f"Current system time is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            return {
                "raw_input": raw_input,
                "sanitized_input": clean_input,
                "matched_intent": intent_name,
                "matched_rule": f"Rule: Exact Hash-Map Match (key='{clean_input}')",
                "response": response_text,
                "is_exit": False,
                "status": "success",
                "lookup_type": "hash_map_direct"
            }

        # Step 5: Secondary Rule-Based Substring / Keyword Match
        # (Provides deterministic fallback rules for composite phrases)
        for intent_name, intent_data in self.knowledge_base.items():
            for pattern in intent_data["patterns"]:
                # If a key pattern is clearly contained as a whole word/phrase
                pattern_regex = r"\b" + re.escape(pattern) + r"\b"
                if re.search(pattern_regex, clean_input):
                    resp = intent_data["response"]
                    if intent_name == "time":
                        resp = f"Current system time is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    
                    is_exit_intent = (intent_name == "goodbye")
                    return {
                        "raw_input": raw_input,
                        "sanitized_input": clean_input,
                        "matched_intent": intent_name,
                        "matched_rule": f"Rule: Keyword Substring Match ('{pattern}' found in input)",
                        "response": resp,
                        "is_exit": is_exit_intent,
                        "status": "success",
                        "lookup_type": "rule_based_keyword"
                    }

        # Step 6: Safe Fallback Mechanism (Dictionary .get() equivalent)
        return {
            "raw_input": raw_input,
            "sanitized_input": clean_input,
            "matched_intent": "fallback",
            "matched_rule": "Rule: Default Fallback Mechanism (No rule matched)",
            "response": self.FALLBACK_RESPONSE,
            "is_exit": False,
            "status": "fallback",
            "lookup_type": "fallback_handler"
        }

    def run_cli(self):
        """
        Continuous Command-Line Interface (CLI) interaction loop.
        Fulfills the mandatory while-loop requirement for terminal execution.
        """
        print("=" * 60)
        print("  RULE-BASED AI CHATBOT (CLI Mode)")
        print("  Industrial Training Kit - Project 1")
        print("=" * 60)
        print("Bot: Hello! I am a Rule-Based AI Chatbot. How can I help you?")
        print("     (Type 'help' for options, or 'exit' / 'bye' to quit)\n")

        # CONTINUOUS CHAT LOOP (Mandatory Requirement)
        while True:
            try:
                user_input = input("User: ")
                result = self.get_response(user_input)
                print(f"Bot:  {result['response']}\n")

                if result["is_exit"]:
                    print("[Session Terminated Cleanly]")
                    break
            except (KeyboardInterrupt, EOFError):
                print("\nBot:  Goodbye! Session closed via interrupt.")
                break


# Allow standalone testing from command line
if __name__ == "__main__":
    bot = RuleBasedChatbot()
    bot.run_cli()
