"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls
Website is: http://deckofcardsapi.com

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
          self.response = response.json()
        else:
          print(f'Error: {response.status_code} - {self.url}')
          self.response = None

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self) -> None:
        print('Reshuffle Deck')
        t = Request_thread(f'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        t.start()
        t.join()


    def draw_card(self) -> str:
        t = Request_thread(f'https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=1')
        t.start()
        t.join()
        try:
            return t.response['cards'][0]['code']
        except:
            return 'Out of Cards'

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()

class BlackjackHand:
    def __init__(self) -> None:
        self.deck = Deck('0phxkqcabmnp')
        self.hand = []
        self.hand_value = 0
        self.game_over = False
    
    def draw_hand(self):
        self.hand = []
        for i in range(2):
            self.hand.append(self.deck.draw_endless())
        self.hand_value = self.hand_evaluation()
    
    def hit(self):
        self.hand.append(self.deck.draw_endless())
        self.hand_value = self.hand_evaluation()
    
    def stand(self):
        pass

    def hand_evaluation(self):
        hand_value = 0
        for card in self.hand:
            if card[0] == 'A':
                if hand_value + 11 > 21:
                    hand_value += 1
                else:
                    hand_value += 11
            elif card[0] == 'K':
                hand_value += 10
            elif card[0] == 'Q':
                hand_value += 10
            elif card[0] == 'J':
                hand_value += 10
            elif card[0] == '0':
                hand_value += 10
            else:
                hand_value += int(card[0])
        return hand_value
    
    def __str__(self) -> str:
        return f'{self.hand} - {self.hand_value}'


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = '0phxkqcabmnp'

    # # Testing Code >>>>>
    # deck = Deck(deck_id)
    # for i in range(55):
    #     card = deck.draw_endless()
    #     print(i, card, flush=True)
    # print()

    game = BlackjackHand()
    game.draw_hand()
    print(game, flush=True)
    
    while(game.game_over == False):
        inp = input('Will you hit? y/n: ')
        if inp == 'n':
            game.game_over = True
        else:
            game.hit()
        print(game, flush=True)
        if game.hand_value > 21:
            game.game_over = True
            print('You Lose')
    
    dealer_hand = BlackjackHand()
    print('Dealer Turn')
    dealer_hand.draw_hand()
    print(dealer_hand, flush=True)
    while(dealer_hand.hand_value < 17):
        dealer_hand.hit()
        print(dealer_hand, flush=True)

    if dealer_hand.hand_value > 21:
        print('Dealer Busts')
    elif dealer_hand.hand_value > game.hand_value:
        print('Dealer Wins')
    elif dealer_hand.hand_value == game.hand_value:
        print('Tie')
    else:
        print('You Win')

    # <<<<<<<<<<<<<<<<<<

