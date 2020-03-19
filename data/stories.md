## path play with instructions
* greet
  - utter_greet
* affirm
  - utter_explain_rules
* affirm
  - utter_rules
  - utter_ready
* affirm
  - action_ask_question

## path play without instructions
* greet
  - utter_greet
* affirm
  - utter_explain_rules
* deny
  - utter_ready
* affirm
  - action_ask_question
* answer_question{"user_answer": "Bad"}
  - action_validate_answer
  - slot{"end": "False"}

## path ask question
* answer_question{"user_answer": "Bad"}
  - action_validate_answer
  - slot{"end": False}
  - action_ask_question

## path round over
* answer_question{"user_answer": "Bad"}
  - action_validate_answer
  - slot{"end": True}
  - utter_round_over

## path dont play
* greet
  - utter_greet
* deny
  - utter_goodbye
