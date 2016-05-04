import simplegui
import random
print "Adam and David Blackjack has loaded"
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    
in_play = False
outcome = ""
j = 100
score = 0
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
background_timer_interval = 900
text_timer_interval = 900# In milliseconds (1000 ms = 1 s)
Color_Rainbow = ["Red","Orange","Yellow","Green","Blue","Indigo","Violet"]
Current_Color_Background = ""
Color_Counter_Background_Background = 2
Current_Color_Text = ""
Color_Counter_Text = 0
Rainbow_Toggle = True
Rainbow_Button_Label = "Toggle Rainbow Effect"
frame = simplegui.create_frame("Blackjack", 600, 600)
def background_timer_handler():
    global Color_Counter_Background_Background;
    global Current_Color_Background;
    global Counter_Background;
    global Color_Rainbow;
    if Rainbow_Toggle == True:
        if Color_Counter_Background_Background < 6:
            Color_Counter_Background_Background = Color_Counter_Background_Background + 1
        else:
            Color_Counter_Background_Background = 0
    Current_Color_Background = Color_Rainbow[Color_Counter_Background_Background]
    frame.set_canvas_background(Current_Color_Background)
timer = simplegui.create_timer(background_timer_interval, background_timer_handler)
timer.start()
background_timer_handler()
def time_text_handler():
    global Color_Counter_Text;
    global Current_Color_Text;
    global Counter_Background;
    global Color_Rainbow;
    global Current_Color_Text
    global Color_Counter_Text
    if Rainbow_Toggle == True:
        if Color_Counter_Text < 6:
            Color_Counter_Text = Color_Counter_Text + 1
        else:
            Color_Counter_Text= 0
    Current_Color_Text = Color_Rainbow[Color_Counter_Text]
texttimer = simplegui.create_timer(text_timer_interval, time_text_handler)
texttimer.start()
time_text_handler()
def Rainbow_Toggler():
    global Rainbow_Toggle, Rainbow_Button_Label;
    if Rainbow_Toggle == True:
        Rainbow_Toggle = False
    elif Rainbow_Toggle == False:
        Rainbow_Toggle = True
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
    def __str__(self):
        return self.suit + self.rank
    def get_suit(self):
        return self.suit
    def get_rank(self):
        return self.rank
    def draw(self, canvas, pos):
        card_pos = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_pos, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
class Hand:
    def __init__(self):
        self.hand = []
    def __str__(self):
        handstr = ''
        for x in self.hand:
            handstr = handstr + str(x)
        return handstr
    def add_card(self, card):
        self.hand.append(card)
    def get_value(self):
        handvalue = 0
        aces = 0
        for x in self.hand:
            if x.get_rank() == 'A':
                aces += 1
            handvalue += VALUES.get(x.get_rank())
        if aces > 0 and (handvalue + 10) <= 21:
            handvalue += 10
        return handvalue
    def busted(self):
        global score,outcome,in_play
        if self.get_value() > 21:
            outcome = "You have busted. New deal?"
            
            in_play = False
            return True
        else:
            outcome = "Hit or stand?" 
    def draw(self, canvas, p):
        for z in self.hand:
            card_pos = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(z.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(z.suit))
            canvas.draw_image(card_images, card_pos, CARD_SIZE, [p[0] + CARD_CENTER[0] + 73 * self.hand.index(z), p[1] + CARD_CENTER[1]], CARD_SIZE)
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(str(suit),str(rank)))
    def shuffle(self):
        random.shuffle(self.deck)
    def deal_card(self):
        self.card = self.deck[0]
        self.deck.remove(self.card)
        return self.card
def deal():
    global outcome, score, in_play, player_hand, dealer_hand, my_deck
    player_hand = Hand()
    dealer_hand = Hand()
    my_deck = Deck()
    my_deck.shuffle()
    player_hand.add_card(my_deck.deal_card())
    player_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    dealer_hand.add_card(my_deck.deal_card())
    outcome = 'Hit or stand?'
    if in_play:
        score-=1
    in_play = True
def hit():
    global outcome, score, in_play
    
    if not player_hand.busted():
        player_hand.add_card(my_deck.deal_card())
        if player_hand.busted():
            score-=1
    return score, outcome, in_play    
def stand():
    global outcome, score, in_play
    in_play = False
    #dealer_hand.busted()
    if player_hand.get_value() < 21:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
        else:
            if dealer_hand.get_value() > 21:
                outcome = "Dealer busts, you win. New deal?"
                score += 1
            elif dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer wins. New deal?"
                score -= 1
            else:
                outcome = "You win. New deal?"
                score += 1
    return score, outcome, in_play
def reset():
    global score
    score = 0
def draw(canvas):
    dealer_hand.draw(canvas, [0, 100])    
    player_hand.draw(canvas, [0, 300])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [CARD_BACK_CENTER[0], j + CARD_BACK_CENTER[1]], CARD_SIZE)    
    canvas.draw_text("Score: "+str(score),[50,50],20,Current_Color_Text)
    canvas.draw_text("BlackJack",[250,50],35,Current_Color_Text)
    canvas.draw_text(outcome,[50,75],20,Current_Color_Text)
print(Current_Color_Background)
frame.set_canvas_background(Current_Color_Background)
frame.add_button("New Game", reset, 200)
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button(Rainbow_Button_Label, Rainbow_Toggler, 200)
frame.set_draw_handler(draw)
deal()
frame.start()
