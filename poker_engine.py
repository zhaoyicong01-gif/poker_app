import random
from collections import Counter

class PokerEngine:
    def __init__(self):
        self.ranks = '23456789TJQKA'
        self.suits = 'shdc'
        self.rank_map = {r: i for i, r in enumerate(self.ranks, 2)}
        
    def evaluate_7_cards(self, cards):
        hand = sorted([(self.rank_map[c[0]], c[1]) for c in cards], reverse=True)
        suit_counts = Counter(c[1] for c in hand)
        flush_suit = next((s for s, count in suit_counts.items() if count >= 5), None)
        
        unique_ranks = sorted(list(set(c[0] for c in hand)), reverse=True)
        if 14 in unique_ranks: unique_ranks.append(1) # A-2-3-4-5 支持
        
        straight_high = -1
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                straight_high = unique_ranks[i]
                break

        if flush_suit:
            f_ranks = sorted([c[0] for c in hand if c[1] == flush_suit], reverse=True)
            if 14 in f_ranks: f_ranks.append(1)
            for i in range(len(f_ranks) - 4):
                if f_ranks[i] - f_ranks[i+4] == 4: return (9, f_ranks[i], "同花顺")
            return (6, f_ranks[0], "同花")

        if straight_high != -1: return (5, straight_high, "顺子")

        rank_counts = Counter(c[0] for c in hand).most_common()
        top_c, top_v = rank_counts[0][1], rank_counts[0][0]
        sec_c = rank_counts[1][1] if len(rank_counts) > 1 else 0
        
        if top_c == 4: return (8, top_v, "四条")
        if top_c == 3 and sec_c >= 2: return (7, top_v, "葫芦")
        if top_c == 3: return (4, top_v, "三条")
        if top_c == 2 and sec_c == 2: return (3, top_v, "两对")
        if top_c == 2: return (2, top_v, "对子")
        return (1, hand[0][0], "高牌")

    def run_simulation(self, my_hand, board, num_players, iterations=5000):
        deck = [r + s for r in self.ranks for s in self.suits]
        known = my_hand + board
        rem_deck = [c for c in deck if c not in known]
        
        wins = 0
        for _ in range(iterations):
            temp_deck = rem_deck[:]
            random.shuffle(temp_deck)
            sim_board = board + temp_deck[:5-len(board)]
            ptr = 5-len(board)
            
            my_score = self.evaluate_7_cards(my_hand + sim_board)
            is_win = True
            for _ in range(num_players - 1):
                opp = [temp_deck[ptr], temp_deck[ptr+1]]
                ptr += 2
                if self.evaluate_7_cards(opp + sim_board)[:2] > my_score[:2]:
                    is_win = False; break
            if is_win: wins += 1
        return wins / iterations
