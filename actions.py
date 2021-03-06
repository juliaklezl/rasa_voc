# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa.core.slots import Slot

import random

QUESTIONS = [("What does 'kvinna' mean in English?", "woman"),
             ("What is the opposite of 'god' in English?", "bad"),
             ("What does 'bord' mean in English?", "table"),
             ("What does 'dricka' mean in English?", "drink"),
             ("What does 'pojke' mean in English?", "boy"),
             ("What does 'flicka' mean in English?", "girl"),
             ("What does 'bra' mean in English?", "good"),
             ("What does 'vit' mean in English?", "white"),
             ("What does 'grön' mean in English?", "green"),
             ("What does 'moln' mean in English?", "cloud"),
             ("What does 'skola' mean in English?", "school"),
             ("What does 'djur' mean in English?", "animal"),
             ("What is the opposite of 'kallt' in English?", "warm"),
             ("What is the opposite of 'aldrig' in English?", "always"),
             ("What is the opposite of 'vän' in English?", "enemy"),
             ("What is the opposite of 'ung' in English?", "old"),
             ("What is the opposite of 'full' in English?", "empty"),
             ("What is the opposite of 'älska' in English?", "hate"),
             ("What is the opposite of 'vänster' in English?", "right"),
             ("What is the opposite of 'ner' in English?", "up")]

class ActionAskQuestion(Action):

    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            history = tracker.get_slot("history")
            question_count = int(tracker.get_slot("question_count"))
            points = int(tracker.get_slot("points"))
            streak_count = int(tracker.get_slot("streak_count"))
            if question_count > 9:
                question_count = 0
                points = 0
                streak_count = 0
            if history:
                available = [i for i in range(len(QUESTIONS)) if i not in history]
            else:
                available = list(range(len(QUESTIONS)))
                history=[]
            if available == []:
                dispatcher.utter_message(text="Sorry, you have answered all available questions")
                return []
            qix = random.choice(available)
            history.append(qix)
            question_count += 1
            dispatcher.utter_message(text=QUESTIONS[qix][0])
            return [SlotSet("qix", qix), SlotSet("history", history), SlotSet("question_count", question_count), SlotSet("points", points), SlotSet("streak_count", streak_count)]

class ActionValidateAnswer(Action):

    def name(self) -> Text:
        return "action_validate_answer"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        qix = int(tracker.get_slot("qix"))
        user_answer=tracker.get_slot("user_answer")
        points=int(tracker.get_slot("points"))
        streak_count = int(tracker.get_slot("streak_count"))
        question_count = int(tracker.get_slot("question_count"))
        if question_count > 9:
            end = "True"
        else:
            end = "False"
        if user_answer.lower() == QUESTIONS[qix][1]:
            if streak_count == 4:
                points += 2
                streak_count = 1
                dispatcher.utter_message(template="utter_correct")
            else:
                points += 1
                streak_count += 1
                dispatcher.utter_message(template="utter_correct")
        else:
            streak_count = 0
            dispatcher.utter_message(template="utter_wrong")
        return [SlotSet("points", points), SlotSet("streak_count", streak_count), SlotSet("end", end)]


class ActionGiveHint(Action):

    def name(self) -> Text:
        return "action_give_hint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        qix = int(tracker.get_slot("qix"))
        hint = "The first letter is " + QUESTIONS[qix][1][0]
        dispatcher.utter_message(text=hint)
        return []
