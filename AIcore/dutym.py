# model for duty

"""

method : build a master infrastructure to post missions to workers to solve it in different time
instruction are as folow:
1 goals : score 1 > score 2 > ...
2 constraints : F <var> & <var> & ...
3 out : action 1 & action 2 & ...

"""


class duty:
    def __init__(self):
        # rule = {'name':[[goals],[constrain]]}
        self.rules = {}
        # vars = {'name':value}
        self.vars = []
        self.actions = []

        self.turn = 1

        self.hp = [[14262,13179,14176],[80648],[160000,80000,]]
        self.npneed = [50,30,20]

        self.atk = []

        """
        input : 
            curturn
            hook[1,2,3]
            card[1,2,3,4,5]
            actor[1,2,3,4,5]
            
        output:
            skill[1,2,3,4,5...]
            card[1,2,3,4...]    
        
        """

    def get_card(self):
        pass

    def new_turn(self):
        self.turn += 1