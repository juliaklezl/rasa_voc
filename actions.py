# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import random

QUESTIONS = [("What does 'kvinna' mean in English?", "Woman"),
             ("What is the opposite of 'god' in English?", "Bad")]

class ActionAskQuestion(Action):

    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
           domain:Dict[Text, Any]) -> List[Dict[text, Any]]:

    def helper_one_turn(self,turn_num, point_num, streak_num) 
        history = tracker.get_slot("history")
        if history:
            available = [i for i in range(len(QUESTIONS)) if i not in history]
        else:
            available = list(range(len(QUESTIONS)))
            history = []
        qix = random.choice(available)
        history.append(qix)
        dispatcher.utter_message(text=QUESTIONS[qix][0]
