from backend.trader import Trader, TraderAction, SellAction, TakeAction, TradeAction
from backend.market import MarketObservation
from backend.goods import GoodType
from typing import Optional, Callable
import time


class GoldcrusherAgent(Trader):
    def __init__(self, seed, name):
        super().__init__(seed, name)
        self.memory = []
        self.total_move_time = 0.0
        self.max_move_time = 0.0
        self.move_count = 0

        self.good_values = {
            GoodType.DIAMOND: 7,
            GoodType.GOLD: 6,
            GoodType.SILVER: 5,
            GoodType.FABRIC: 4,
            GoodType.SPICE: 4,
            GoodType.LEATHER: 3,
            GoodType.CAMEL: 1,
        }

        self.premiumgoods = {
            GoodType.DIAMOND,
            GoodType.GOLD,
            GoodType.SILVER,
        }
        
        self.expectedbonus = {
            3: 2.0,
            4: 5.0,
            5: 9.0,
        } #expected values

    def select_action(self, actions: list[TraderAction], observation: MarketObservation,simulate_action_fnc: Callable[[TraderAction], MarketObservation]) -> TraderAction:
        start_time = time.time()
        #similar to the smart agent
        sell_actions = [a for a in actions if isinstance(a, SellAction)]
        take_actions = [a for a in actions if isinstance(a, TakeAction)]
        trade_actions = [a for a in actions if isinstance(a, TradeAction)]
        
        #check for forced sells first meaning if we have a really good sell action we should take it immediately instead of risking it by taking or trading first
        forced_sell =self.select_forcedsell(sell_actions,observation) 
        if forced_sell is not None:
            elapsed = time.time()-start_time
            self.total_move_time+=elapsed
            self.move_count+=1
            if elapsed >self.max_move_time:
                self.max_move_time = elapsed
            return forced_sell

        best_action = actions[0]
        best_score = float("-inf")

        for action in sell_actions:
            score = self._evaluate_sell_action(action, observation)
            if score > best_score:
                best_score = score
                best_action = action

        for action in take_actions:
            score = self._evaluate_take_action(action, observation)
            if score > best_score:
                best_score = score
                best_action = action

        for action in trade_actions:
            score = self._evaluate_trade_action(action, observation)
            if score > best_score:
                best_score=score
                best_action=action
        elapsed = time.time()-start_time
        self.total_move_time+=elapsed
        self.move_count+= 1
        if elapsed >self.max_move_time:
            self.max_move_time = elapsed
        return best_action

    def calculate_reward(self, old_observation: MarketObservation, new_observation: MarketObservation, has_acted: bool, environment_reward: Optional[float]):
        #called after every turn so we can use it to update our internal state and learning signals
        try:
            self.memory.append((has_acted,environment_reward))
            if len(self.memory)>64:
                self.memory.pop(0)
        except Exception:
            pass 
    
    #select the forced actions which we want to do if they are available
    def select_forcedsell(self, sell_actions, observation):
        if not sell_actions:
            return None

        scored=[]
        for action in sell_actions:
            scored.append((self._evaluate_sell_action(action,observation), action))

        scored.sort(key=lambda x:x[0],reverse=True)
        best_score,best_action=scored[0]

        if best_action._count>= 5:
            return best_action
        if best_action._count>= 4:
            return best_action
        if best_action._count>= 3 and best_score>= 10:
            return best_action
        if best_action._sell in self.premiumgoods and best_action._count>= 2 and best_score>= 8:
            return best_action
        if self.handspace(observation)<=1 and best_score>= 6:
            return best_action
        if self.isendgame(observation) and best_score>= 5:
            return best_action

        return None


    def _evaluate_sell_action(self, action: SellAction, observation: MarketObservation) -> float:
        good_type = action._sell
        count = action._count
        
        available_coins = self.coins_for_goods(observation, good_type) #more robust
        if len(available_coins) < count:
            return -1000.0 # Can't sell if not enough coins  #made float for consistency

        coins_to_receive = available_coins[-count:]
        coin_value = sum(coins_to_receive)

        score =float(coin_value)

        #this prioritizes selling 5+ cards the most, then 4+, then 3+ by adding the 15, 8, and 4 respectively
        if count >= 5:
            score += self.expectedbonus[5]+15
        elif count == 4:
            score += self.expectedbonus[4]+8
        elif count == 3:
            score += self.expectedbonus[3]+4
        
        #also prioritizes selling premium goods more than non premium goods
        #which we want because their coin stacks are strong and can run out quickly
        #so for premium goods even selling 2 is valuable since that is the minimum legal sell
        if good_type in self.premiumgoods:
            score +=2*len(available_coins)
            if count==2:
                score+=5

        #for all other good, selling just 1 is usually weak unless our hand is crowded or we're near the end and just want to cash things out
        if good_type not in self.premiumgoods and count==1:
            score -=5
            if self.handspace(observation)<=1:
                score +=3
            if self.isendgame(observation):
                score +=4
        
        #in endgame, selling becomes even better bc future setup matters less than securing coins now
        if self.isendgame(observation):
            score += 2+count

        return score

    def _evaluate_take_action(self, action: TakeAction, observation: MarketObservation) -> float:
        good_type = action._take

        if good_type == GoodType.CAMEL:
            camel_count = self.goodcount(self.marketgoods(observation), GoodType.CAMEL)
            score=0.0
            score+=3.0*camel_count
            
            #taking only 1 camel is usually not that strong early on since using a whole turn for a single camel has low impact
            if camel_count==1 and not self.isendgame(observation): #
                score-= 4.0
            #camels are a bit more useful when our hand is tight since they do not take up hand space
            if self.handspace(observation)<=2:
                score+= 3.0
            score+= 0.5*max(0, self.opponent_camels(observation)-self.mycamels(observation)) #if opponent has more camels, we want to catch up
            #in endgame camel majority matters more bc of bonus
            if self.isendgame(observation):
                score+= 4.0

            return score

        #for non-camel goods consider the value of the good, how many we already have, and how many coins are available for that good
        hand_space = self.handspace(observation)
        if hand_space<=0:
            return -1000.0

        #careful about taking goods if we don't have hand space or if we already have a lot of that good
        actor_goods = self.actorgoods(observation)
        owned = self.goodcount(actor_goods, good_type)
        new_count = owned+ 1

        score=0.0
        score+=3.0*self.good_values.get(good_type, 0)

        #prioritize taking goods that help us reach sell thresholds (2+ for premium and others for the tockens) especially for premium goods
        if good_type in self.premiumgoods:
            if new_count ==2:
                score+=10
            elif new_count ==3:
                score+=8
            elif new_count ==4:
                score+=7
            elif new_count >=5:
                score+=6
        else:
            if new_count ==2:
                score+=3
            elif new_count ==3:
                score+=10
            elif new_count ==4:
                score+=12
            elif new_count >=5:
                score+=14
        
        # if premium coin values are still large, getting those goods is better
        available_coins = self.coins_for_goods(observation, good_type)
        if good_type in self.premiumgoods:
            score +=1.5*len(available_coins)
        
        #dont take good when handspace is less
        if hand_space==1:
            score-=6
        elif hand_space==2:
            score-=2
        
        # in endgame, only take goods if they likely to convert into a sell soon
        if self.isendgame(observation):
            if self.is_sell_ready(good_type, new_count):
                score+=3
            else:
                score-=6

        return score

    def _evaluate_trade_action(self, action: TradeAction, observation: MarketObservation) -> float:
        requested = action.requested_goods
        offered = action.offered_goods
        actor_goods = self.actorgoods(observation)

        value_gained=0.0
        value_lost=0.0
        set_bonus=0.0
        break_penalty=0.0
        #we want to evaluate trades based on the net value gained or lost
        #also consider how the trade affects our progress towards selling sets and whether it gives away camels
        for g in self.allgoods():
            req =self.goodcount(requested, g)
            off =self.goodcount(offered, g)
            value_gained +=self.good_values.get(g,0)*req
            value_lost +=self.good_values.get(g,0)*off

            if g == GoodType.CAMEL:
                continue

            old_count = self.goodcount(actor_goods, g)
            new_count = old_count-off+req
            
            #reward trades that give us tocken
            if not self.is_sell_ready(g,old_count) and self.is_sell_ready(g,new_count):
                set_bonus +=9
            if new_count >= 3 and old_count <3:
                set_bonus += 4
            if new_count >= 4 and old_count <4:
                set_bonus += 5
            if new_count >= 5 and old_count <5:
                set_bonus += 6
            
            #penalize breaking a set we could already sell
            if self.is_sell_ready(g, old_count) and not self.is_sell_ready(g, new_count):
                break_penalty+=12

        score=0.0
        score +=2.0*(value_gained-value_lost)
        camel_offered = self.goodcount(offered,GoodType.CAMEL) #camels aregood to give away first (use mainly for trades)
        non_camel_offered=0
        for g in self.allgoods():
            if g != GoodType.CAMEL:
                non_camel_offered += self.goodcount(offered,g)

        #calculate sample score in order to make decisions
        score+=2.5 *camel_offered
        score-=2.0 *non_camel_offered
        score +=set_bonus
        score -=break_penalty
        score-=2.0

        if self.isendgame(observation) and set_bonus<9:
            score -=8

        return score



    #helper functions to safely access observation data 
    #so agent doesnt crash if backend structure varies
    def actorgoods(self, observation: MarketObservation):
        return getattr(observation,"actor_goods", None)

    def marketgoods(self, observation: MarketObservation):
        return getattr(observation,"market_goods", None)

    def coins_for_goods(self, observation: MarketObservation, good_type):
        coins_map = getattr(observation,"market_goods_coins", None)
        if coins_map is None:
            return []

        try:
            return coins_map[good_type]
        except Exception:
            pass

        try:
            return getattr(coins_map, good_type.name)
        except Exception:
            pass

        return []

    def goodcount(self, goods_obj, good_type) -> int: #try multiple access patterns since goods may not be a dict
        if goods_obj is None:
            return 0

        try:
            return int(goods_obj[good_type])
        except Exception:
            pass

        try:
            return int(goods_obj[good_type.name])
        except Exception:
            pass

        try:
            return int(getattr(goods_obj, good_type.name))
        except Exception:
            pass

        try:
            return int(getattr(goods_obj, good_type.name.lower()))
        except Exception:
            pass

        return 0

    #premium goods need at least 2 to sell
    def is_sell_ready(self, good_type, count: int)->bool:
        if good_type in self.premiumgoods:
            return count>=2
        return count>=1
    
    #amount of handspace left
    def handspace(self, observation: MarketObservation)->int:
        if hasattr(observation,"max_player_goods_count") and hasattr(observation,"actor_non_camel_goods_count"):
            return observation.max_player_goods_count-observation.actor_non_camel_goods_count
        return 7

    #if fewer good left in the market, we are closer to endgame
    def isendgame(self, observation: MarketObservation)->bool:
        if hasattr(observation,"market_reserved_goods_count"):
            return observation.market_reserved_goods_count<=10
        return False

    def mycamels(self, observation: MarketObservation)->int:
        for attr in ("actor_camels","player_camels","camel_count"):
            if hasattr(observation, attr):
                return int(getattr(observation,attr))
        return 0

    def opponent_camels(self, observation: MarketObservation)->int:
        for attr in ("opponent_camels","rival_camels","other_camels"):
            if hasattr(observation, attr):
                return int(getattr(observation,attr))
        return 0

    def allgoods(self):
        return [
            GoodType.DIAMOND,
            GoodType.GOLD,
            GoodType.SILVER,
            GoodType.FABRIC,
            GoodType.SPICE,
            GoodType.LEATHER,
            GoodType.CAMEL,
        ]