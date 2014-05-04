import simplegui
import random


CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)

CANVAS_W = 800
CANVAS_H = 600

COLORS = ('trefle','pique','coeur','carreau')
RANKS = ('A','2','3','4','5','6','7','8','9','T', 'J','Q','K')
POINTS = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:

    def __init__(self):
        self.color = random.randrange( 0, 4 )
        self.rank = random.randrange( 0, 13 )
        self.image = ( self.rank , self.color  )
        

class Blackjack:

    def deal(self):
        self.is_playing = True
        self.turns = 0
        self.msg = 'Hit or Stand?'
        self.gamer_cards = []
        self.bank_cards = []
        for i in range(2):
            card = Card() ; self.gamer_cards.append(card)
            card = Card() ; self.bank_cards.append(card)
        self.check_scores() 
    def __init__(self):
        self.is_playing = False
        self.gamer_cards = []
        self.bank_cards = []
        self.build_game()
        print self.gamer_cards
        self.score1 = 0
        self.score2 = 0
        self.turns = 0
        
        self.deal()
    #
    def check_scores(self):
        ace = False
        s = 0
        for c in self.gamer_cards:
            if c.image[0] == 0:
                ace = True
            s += POINTS[RANKS[c.image[0]]]
        self.score1 = s
        if ace and self.score1+10 <= 21:
            self.score1 += 10
        ace = False
        s = 0
        for c in self.bank_cards:
            if c.image[0] == 0:
                ace = True
            s += POINTS[RANKS[c.image[0]]]
        self.score2 = s
        if ace and self.score2+10 <= 21:
            self.score2 += 10
        if self.score1 == 21:
            self.turns += 1
            self.msg = 'player 21!'
            self.is_playing = False
            return
        if self.score2 == 21:
            self.msg = 'bank 21!'
            self.is_playing = False
            return    
        if self.score1>21:
            self.msg = 'player bust!'
            self.is_playing = False
        if self.score2>21:
            self.msg = 'bank bust!'
            self.is_playing = False
        if not(self.is_playing) and self.score1<22 and self.score2<22:
            if self.score1 == self.score2:
                self.msg = 'equality'
                return
            if self.score1 > self.score2:
                self.msg = 'player wins!'
            else:
                self.msg = 'bank wins!'
    def bank_hit(self):
        self.turns += 1
        if (self.is_playing):
            if (self.score2 >= 21):
                self.is_playing = False
                return
            card = Card()
            self.bank_cards.append(card)
            
            self.check_scores()
        
        
    def hit(self):
        if (self.is_playing):
            if (self.score1 >= 21):
                self.is_playing = False
                return
            card = Card()
            self.gamer_cards.append(card)
            self.turns += 1
            self.check_scores()
        
    
    def stand(self):
        self.turns += 1
        if (self.is_playing):
            if (self.turns == 0):
                pass
            else:
                while self.score2 < 17:
                    self.bank_hit()
                
        self.is_playing = False
        
 
   # define draw handler
    def draw_handler(self,canvas):
        self.check_scores() 
        #global timer_count, stop_count, match_count
        canvas.draw_text(("BLACKJACK GAME"), [260,41], 36, "Yellow")
        canvas.draw_text(("BANK"), [26,161], 36, "Orange")
        canvas.draw_text(("PLAYER"), [10,541], 36, "Orange")
        canvas.draw_text(str(self.msg), [50,350], 36, "Orange")
        if not(self.is_playing):
            canvas.draw_text(("SCORES:  "+str(self.score1)+"/"+str(self.score2)), [320,91], 26, "Yellow")
        count = 0

        for c in self.bank_cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * c.image[0], CARD_CENTER[1] + CARD_SIZE[1] * c.image[1])
            if (count == 0 and self.turns == 0 and self.score2 <> 21):
                canvas.draw_image(self.card_back,
                                  CARD_BACK_CENTER,
                                  CARD_BACK_SIZE,
                                  [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]+ 2 * CARD_BACK_SIZE[1]+2],
                                  CARD_BACK_SIZE
 
            )
            else:
                canvas.draw_image(self.cards_url,
                      card_loc,
                      CARD_SIZE,
                      (CARD_CENTER[0] + count * CARD_SIZE[0], CARD_CENTER[1] + 2 * CARD_SIZE[1]),
                      CARD_SIZE
            )
            count += 1
        
        count = 0

        for c in self.gamer_cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * c.image[0], CARD_CENTER[1] + CARD_SIZE[1] * c.image[1])
            canvas.draw_image(self.cards_url,
                      card_loc,
                      CARD_SIZE,
                      (CARD_CENTER[0] + count * CARD_SIZE[0], CARD_CENTER[1] + 4 * CARD_SIZE[1]),
                      CARD_SIZE
            )
            count += 1
    
    def build_game(self):
        # create timer and frame
        self.frame = simplegui.create_frame("Blackjack", CANVAS_W, CANVAS_H)
        self.cards_url = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
        self.card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    
        # register event handlers
        self.frame.add_button(" Deal  ", self.deal, 100)
        self.frame.add_button("  Hit  ", self.hit, 100)
        self.frame.add_button(" Stand ", self.stand, 100)
        self.frame.set_draw_handler(self.draw_handler)
        self.frame.set_canvas_background("Green")
        # start frame
        self.frame.start()

# Create game
bljack = Blackjack()

