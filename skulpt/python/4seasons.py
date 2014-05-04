import simplegui
import random

#Images
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
 
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

SUITS = ('C', 'S', 'H', 'D')
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13}

position_list = [[50, 248],[375, 150],[297, 248],[375, 248],[453, 248],[375, 346],[297, 150],[453, 150],[297, 346],[453, 346],[173, 248]]
selected_card = [True and False for i in range(len(position_list))]

corner_base = 0

class Card:
    
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Error:", suit, rank, " is an invalid card."
  
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def get_value(self): 
        return VALUES[self.get_rank]
    
    def draw(self, canvas, pos):
        canvas.draw_image(card_images, (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                          CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit)),
                          CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)

class Deck:

    def __init__(self):
        self.deck = []
        for r in RANKS:
            a = r
            for s in SUITS:
                b = s
                card = Card(b, a)
                self.deck.append(card)

    def __repr__(self):
        return 'Deck'

    def shuffle(self):
        random.shuffle(self.deck)            

    def pop_card(self):
        return self.deck.pop()        
    
    def get_suit(self):
        return self.deck[-1].get_suit()

    def get_rank(self):
        return self.deck[-1].get_rank()

    def draw(self, canvas, pos):
        if self.deck == []:
            pass
        else:
            self.deck[-1].draw(canvas, pos)
        
class Cross:

    def __init__(self):
        self.cross = []

    def __repr__(self):
        return 'Cross'

    def add_card(self, card):
        self.cross.append(card)

    def pop_card(self):
        return self.cross.pop()        

    def get_suit(self):
        if self.cross == []:
            pass
        else:
            return self.cross[-1].get_suit()

    def get_rank(self):
        if self.cross == []:
            pass
        else:
            return self.cross[-1].get_rank()

    def check(self, location, card2rank, cross_pos): 
        if VALUES[card2rank] == corner_base:
            pass
        elif location == 'Cross':
            if self.get_rank() == None:
                self.add_card(cross[cross_pos].pop_card())
            elif VALUES[self.get_rank()] - VALUES[card2rank] % 13 == 1:
                self.add_card(cross[cross_pos].pop_card())
        elif location == 'Deck':
            if self.get_rank() == None:
                self.add_card(deck.pop_card())
            elif VALUES[self.get_rank()] - VALUES[card2rank] % 13 == 1:
                self.add_card(deck.pop_card())
           
        elif location == 'Discard':
            if self.get_rank() == None:
                self.add_card(discard.pop_card())
            elif card2rank == None:
                pass
            elif VALUES[self.get_rank()] - VALUES[card2rank] % 13 == 1:
                self.add_card(discard.pop_card())
 
    def draw(self, canvas, pos):
        if not self.cross:
            pass
        else:
            self.cross[-1].draw(canvas, pos)
        
class Corner:

    def __init__(self):
        self.corner = []

    def __repr__(self):
        return 'Corner'

    def add_card(self, card):
        self.corner.append(card)

    def pop_card(self):
        return self.corner.pop(-1)  

    def get_suit(self):
        if self.corner == []:
            pass
        else:
            return self.corner[-1].get_suit()

    def get_rank(self):
        if self.corner == []:
            pass
        else:
            return self.corner[-1].get_rank()

    def get_value(self):
        if self.corner == []:
            pass
        else:
            return VALUES[self.corner[-1].get_rank()]
        
    def check(self, location, card2rank, card2suit, cross_pos):
        if location == 'Deck':
            if self.corner == []:
                if VALUES[card2rank] == corner_base:
                    self.add_card(deck.pop_card())
            elif VALUES[card2rank] % 13 == (self.get_value() + 1) % 13 and self.get_suit() == card2suit:
                self.add_card(deck.pop_card())
        elif location == 'Cross':
            if self.corner == []:
                if card2rank == None:
                    pass
                elif VALUES[card2rank] == corner_base:
                    self.add_card(cross[cross_pos].pop_card())
            elif VALUES[card2rank] % 13 == (self.get_value() + 1) % 13 and card2suit == self.get_suit():
                self.add_card(cross[cross_pos].pop_card())     
        elif location == 'Discard':
            if card2rank == None:
                pass   
            elif self.corner == []:
                if VALUES[card2rank] == corner_base:
                    self.add_card(discard.pop_card())
            elif VALUES[card2rank] % 13 == self.get_value() + 1 % 13 and card2suit == self.get_suit():
                self.add_card(discard.pop_card())

    def draw(self, canvas, pos):
        if self.corner == []:
            pass
        else:
            self.corner[-1].draw(canvas, pos)   
        
class Discard:   

    def __init__(self):
        self.discard = []

    def __repr__(self):
        return 'Discard'

    def add_card(self, card):
        self.discard.append(card)

    def pop_card(self):
        return self.discard.pop()  

    def get_suit(sef):
        return card.get_suit(self.discard[-1])

    def get_rank(self):
        if self.discard == []:
            pass
        else:
            return self.discard[-1].get_rank()

    def check(self, location, card2rank):
        if VALUES[card2rank] == corner_base:
            pass
        elif location == 'Deck':
            self.add_card(deck.pop_card())

    def draw(self, canvas, pos):
        if self.discard == []:
            pass
        else:
            self.discard[-1].draw(canvas, pos)        
  
#Setup
deck = Deck()
cross = [Cross(), Cross(), Cross(), Cross(), Cross()]
corner = [Corner(), Corner(), Corner(), Corner()]
discard = Discard()

def deal():
    global deck, cross, corner_base, corner, discard
    deck = Deck()
    cross = [Cross(), Cross(), Cross(), Cross(), Cross()]
    corner = [Corner(), Corner(), Corner(), Corner()]
    discard = Discard()
    deck.shuffle()
    for card in cross:
        card.add_card(deck.pop_card())
    corner[0].add_card(deck.pop_card())
    corner_base = VALUES.get(corner[0].get_rank())
 
firstcard = 0
def mouseclick_handler(pos):
    global position_list, selected_card, loop, firstcard
    loop = -1
    list_check = 0
    list_check = selected_card.count(True)
    for card in position_list:
        loop +=1
        if pos[0] > card[0] and pos[0] < card[0]+CARD_SIZE[0] and pos[1] > card[1] and pos[1] < card[1] + CARD_SIZE[1]:
            if list_check == 0:
                firstcard = position_list.index(card) - 1
                selected_card[loop] = True
            elif list_check == 1:
                secondcard = position_list.index(card) - 1
                selected_card = [False, False, False, False, False, False, False, False, False, False, False]
                #DECK AND CROSS
                if  firstcard == -1 and 0 <= secondcard < 5:
                    cross[secondcard].check('Deck', deck.get_rank(), firstcard)
                #CROSS AND CROSS
                elif 0 <= firstcard <= 4 and 0 <= secondcard <= 4:
                    cross[secondcard].check('Cross', cross[firstcard].get_rank(), firstcard)
                #DECK AND CORNER
                elif firstcard == -1 and 5 <= secondcard <= 8:
                    #(Change) (used to be secondcard - 5)
                    corner[secondcard - 5].check('Deck', deck.get_rank(), deck.get_suit(), firstcard)
                #CROSS AND CORNER
                elif 0 <= firstcard < 5 and 5 <= secondcard <= 8:
                    #(Change) (used to be secondcard - 5)
                    corner[secondcard - 5].check('Cross', cross[firstcard].get_rank(), cross[firstcard].get_suit(), firstcard)
                #DECK AND DISCARD
                elif firstcard == -1 and secondcard == 9:
                    discard.check('Deck', deck.get_rank())          
                #DISCARD AND CORNER
                elif firstcard == 9 and 5 <= secondcard <= 8:
                    secondcard = secondcard - 5            
                    corner[secondcard].check('Discard', discard.get_rank(), corner[secondcard].get_suit(), firstcard)
                #DISCARD AND CROSS
                elif firstcard == 9 and 0 <= secondcard <=4:
                    cross[secondcard].check('Discard', discard.get_rank(), firstcard)
     
    list_check = selected_card.count(True)
    
def draw(canvas):
    global cross1pos, selected_card
    canvas.draw_text('Four Seasons', (300, 70), 50, 'Red')
    canvas.draw_text('Base Card value = ' + str(corner_base), (580, 300), 20, 'White')
    canvas.draw_text('INSTRUCTIONS:', (50, 500), 18, 'White')
    canvas.draw_text('[x] To move cards, click the card you want to move, then click its destination.', (50, 530), 18, 'White')
    canvas.draw_text('[*] Cross (Central 5 cards): The only rule is that cards must descend in RANK.', (50, 560), 18, 'White')
    canvas.draw_text('[*] Corners: Base card RANK must match the initial top-left. Cards must be of the same SUIT, ascend in RANK.', (50, 580), 18, 'White')
   
    canvas.draw_text('[*] If you can\'t play the card from the deck, discard. You may only use the top card of the discard pile.', (50, 600), 18, 'White')     
   
    canvas.draw_text('[X] The aim is to build four full sets of each suit in ascending order. Good luck!', (50, 630), 18, 'White')
    
    #Draw grid
    for i in position_list:
        canvas.draw_polygon([i, (i[0], i[1] + CARD_SIZE[1]), (i[0] + CARD_SIZE[0], i[1] + CARD_SIZE[1]), (i[0] + CARD_SIZE[0], i[1])], 2, 'black')
   
    #Draw cards
    deck.draw(canvas, [50, 150+ CARD_SIZE[1]])
    cross[0].draw(canvas, position_list[1])
    cross[1].draw(canvas, [370 - CARD_SIZE[0], 150+CARD_SIZE[1]])
    cross[2].draw(canvas, [375, 150+CARD_SIZE[1]])
    cross[3].draw(canvas, [380 + CARD_SIZE[0], 150+CARD_SIZE[1]])
    cross[4].draw(canvas, [375, 150+(CARD_SIZE[1]*2)])
    corner[0].draw(canvas, [370 - CARD_SIZE[0], 150])
    corner[1].draw(canvas, [380 + CARD_SIZE[0], 150])
    corner[2].draw(canvas, [370 - CARD_SIZE[0], 150+CARD_SIZE[1]*2])
    corner[3].draw(canvas, [380 + CARD_SIZE[0], 150+CARD_SIZE[1]*2])
    discard.draw(canvas, [100+CARD_SIZE[0],150+ CARD_SIZE[1]])
    
    #Draw selected card
    if any(selected_card):
        if selected_card.count(True) == 2:
            pass
        else: 
            canvas.draw_text('[X]', [position_list[selected_card.index(True)][0] + CARD_SIZE[0] / 3 ,
                             position_list[selected_card.index(True)][1] + CARD_SIZE[1] / 2],
                             20, 'Aqua')

#Frame
frame = simplegui.create_frame("Four Seasons", 900, 700)
frame.set_canvas_background("Green")
frame.add_button('Deal', deal)
#Register event handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick_handler)

#Initalize
frame.start()
deal()
