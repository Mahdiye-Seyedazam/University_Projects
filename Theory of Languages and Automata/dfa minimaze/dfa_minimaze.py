from DATA import input_lines_Data

class NFA_GNERATOR:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.numberStates = 0
        self.initial_states = 0
        self.entry_state = 0
        self.result = []
        self.accepting_states = []

    def ExportListData_to_Nfa(self, input_lines_Data):
        self.numberStates = int(input_lines_Data[0])
        # print(self.numberStates) "how many state" = 3
        
        self.states = list(range(self.numberStates))
        # print( self.states) "all of the state" = [0, 1, 2]
        
        self.alphabet = list(input_lines_Data[1])
        # print(self.alphabet) "alphabet" = ['a', 'b']

        accepting_states_line = input_lines_Data[2].split(" ")
        # print(accepting_states_line) "final state" = 1
        
        for index in range(len(accepting_states_line)):
            self.accepting_states.append(int(accepting_states_line[index]))
            # print(self.accepting_states)
            

        # self.initial_states = int(len(accepting_states_line))
        
        self.startState = int(input_lines_Data[3])
        # print(self.startState) ==> "start state is :" = 0

        for index in range(4, len(input_lines_Data)):
            every_line = input_lines_Data[index].split(" ")
            # print(every_line) ==> "Every index in automa"
            '''
                #? ['0', 'b', '0']
                #? ['0', 'a', '1']
                #? ['1', 'b', '1']
                #? ['1', 'a', '0']
                #? ['2', 'a', '1']
                #? ['2', 'b', '0']
            '''
            
            starting_state = int(every_line[0])
            # print(starting_state) 
            
            transition_symbol = every_line[1]
            # print(transition_symbol)
            
            ending_state = int(every_line[2])
            # print(ending_state)

            transition_function = (starting_state, transition_symbol, ending_state);
            self.result.append(transition_function)
            # print(self.result)
        """
            [(0, 'b', 0), (0, 'a', 1), (1, 'b', 1),
            (1, 'a', 0), (2, 'a', 1), (2, 'b', 0)]
        """
    
    def showNfa(self):
        print(self.numberStates)
        print(self.states)
        print(self.alphabet)
        print(self.initial_states)
        print(self.accepting_states)
        print(self.entry_state)
        print(self.result)


class DFA_GNERATOR:
    def __init__(self):
        self.Qstate= []
        self.numberStates = 0
        self.alphabet = []
        self.initial_states = 0
        self.entry_state = 0
        self.accepting_states = []
        self.result = []

    def nfaConvert(self, nfa):
        self.alphabet = nfa.alphabet
        # print(self.alphabet) 
        '''
            #! ['a', 'b']
        '''
        self.entry_state = nfa.entry_state
        nfa_passing_dict = {}
        dfa_passing_dict = {}


        for transition in nfa.result:
            starting_state = transition[0]
            transition_symbol = transition[1]
            ending_state = transition[2]

            if (starting_state, transition_symbol) in nfa_passing_dict:
                nfa_passing_dict[(starting_state, transition_symbol)].append(ending_state)        
                # print(nfa_passing_dict)
            else:
                nfa_passing_dict[(starting_state, transition_symbol)] = [ending_state]             
                # print(nfa_passing_dict)
        """
            #!{(0, 'b'): [0]}
            #!{(0, 'b'): [0], (0, 'a'): [1]}
            #!{(0, 'b'): [0], (0, 'a'): [1], (1, 'b'): [1]}
            #!{(0, 'b'): [0], (0, 'a'): [1], (1, 'b'): [1], (1, 'a'): [0]}
            #!{(0, 'b'): [0], (0, 'a'): [1], (1, 'b'): [1], (1, 'a'): [0], (2, 'a'): [1]}
            #?{(0, 'b'): [0], (0, 'a'): [1], (1, 'b'): [1], (1, 'a'): [0], (2, 'a'): [1], (2, 'b'): [0]}
        
        """

        self.Qstate.append((0,))
        #? Convert NFA transitions to DFA transitions
        for dfa_state in self.Qstate:
            for symbol in nfa.alphabet:
                if  (dfa_state, symbol) in nfa_passing_dict:                    
                    dfa_passing_dict[(dfa_state, symbol)] = nfa_passing_dict[(dfa_state, symbol)]
                    
                    if tuple(dfa_passing_dict[(dfa_state, symbol)]) not in self.Qstate:
                        self.Qstate.append(tuple(dfa_passing_dict[(dfa_state, symbol)]))
                        
                else:
                    destinations = []
                    final_destination = []
                 
                    for nfa_state in dfa_state: 
                        
                        if (nfa_state, symbol) in nfa_passing_dict and nfa_passing_dict[(nfa_state, symbol)] not in destinations:
                            destinations.append(nfa_passing_dict[(nfa_state, symbol)]) 
                            
                    if not destinations:
                        final_destination.append(None)
                    else:
                        # Create Final state
                        for destination in destinations:
                            for value in destination:
                                if value not in final_destination:
                                    final_destination.append(value)
                                    
                                    
                    dfa_passing_dict[(dfa_state, symbol)] = final_destination
                    
                    if tuple(final_destination) not in self.Qstate:
                        self.Qstate.append(tuple(final_destination))
                        
                        
        #? Convert NFA states to DFA states
        for key in dfa_passing_dict:
            self.result.append((self.Qstate.index(key[0]), key[1], self.Qstate.index(tuple(dfa_passing_dict[key]))))
            
        """ (0, 'a', 1)
            (0, 'b', 0)
            (1, 'a', 0)
            (1, 'b', 1)
        """
        
        for q_state in self.Qstate:
            for nfa_accepting_state in nfa.accepting_states:
                if nfa_accepting_state in q_state:
                    self.accepting_states.append(self.Qstate.index(q_state))
                    self.initial_states += 1

                    
    #! Print every think  you have in DFA  
    def showDfa(self):
        
        length_states = len(self.Qstate)
        print('States in machine : {0} '.format(length_states))
        
        print('Alphabet : {0}'.format("".join(self.alphabet)))
        
        print('Start state is : {0}'.format(self.entry_state))
        
        print('Final state is : {0}'.format(self.initial_states))
        
        
        for transition in sorted(self.result):
            print(f'δ{tuple(transition)[0:2]} = {tuple(transition)[2]}')
            


#? create object to discribe and call the nfa and dfa
object_nfa = NFA_GNERATOR()
object_dfa = DFA_GNERATOR()

object_nfa.ExportListData_to_Nfa(input_lines_Data)
object_dfa.nfaConvert(object_nfa)

object_dfa.showDfa()
# object_nfa.showNfa()