from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        if self.hit and self.miss:
            raise InvalidGuessAttempt()
    
    def is_hit(self):
        if self.hit:
            return self.hit
        return False

    def is_miss(self):
        if self.miss:
            return self.miss
        return False
    
    
    
class GuessWord(object):
    def __init__(self, word):
        self.answer = word
        self.masked = '*' * len(word)

        if not word:
            raise InvalidWordException()
            
    def uncover_word(self, guess):
         
        masked_list = list(self.masked)
        index_to_switch = []
        masked_string = self.masked
        answer_lower = self.answer.lower()
        if guess in answer_lower:
            for ind, letter in enumerate(answer_lower):
                if guess == letter:
                    index_to_switch.append(ind)
            for item in index_to_switch:
                masked_list[item] = guess
            masked_string = ''.join(masked_list)
        
        return masked_string
    
    def perform_attempt(self, guess):
        guess = guess.lower()
        if len(guess) > 1:
            raise InvalidGuessedLetterException()
        
        if guess in self.answer.lower():
            hit_or_miss = GuessAttempt(guess, hit = True)
            self.masked = self.uncover_word(guess)
        else:
            hit_or_miss = GuessAttempt(guess, miss = True)
        return hit_or_miss
    

    
    
    
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, words = None, number_of_guesses = 5):
        
        if words == None:
            words = self.WORD_LIST
            
        self.remaining_misses = number_of_guesses
        random_word = self.select_random_word(words)
        self.word = GuessWord(random_word)
        self.previous_guesses = []
    
    def is_won(self):
        return self.word.masked == self.word.answer

    def is_lost(self):
        return self.remaining_misses == 0

    def is_finished(self):
        return self.is_won() or self.is_lost()

    def guess(self, letter):
        letter = letter.lower()
        if letter in self.previous_guesses:
            raise InvalidGuessedLetterException()
        if self.is_finished():
            raise GameFinishedException()
            
        self.previous_guesses.append(letter.lower())
        guess_attempt = self.word.perform_attempt(letter)
        
        if guess_attempt.is_miss():
            self.remaining_misses -= 1
            
        if self.is_won():
            raise GameWonException()

        if self.is_lost():
            raise GameLostException()

        return guess_attempt
    

        

    @classmethod
    def select_random_word(cls, list):
        if not list:
            raise InvalidListOfWordsException()
        return random.choice(list)
        
        
