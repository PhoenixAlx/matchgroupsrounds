
# -*- coding: utf-8 -*-
#
#  matchgroupsrounds.py
#  
#  Copyright 2017 álex bueno <francisco.manuel.alexander@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 

import random
import itertools

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ElementsError(Error):
    """Exception raised for numbers elements different to 20.

    Attributes:
        len_elements -- number of elements
        message -- explanation of the error
    """
    def __init__(self, len_elements):
        super(Error, self).__init__()
        self.message = "There is %i  in elements parameter, it must have 20 elements"%(len_elements)
class NumberRoundsError(Error):
    """Exception raised for numbers rounds >5.

    Attributes:
        number_rounds -- number of rounds
        message -- explanation of the error
    """
    def __init__(self, number_rounds):
        super(Error, self).__init__()
        self.message = "There is %i  rounds, it must have 5 or less rounds"%(number_rounds)
class NumberElementsByGroupError(Error):
    """Exception raised for numbers elements by group ==4.

    Attributes:
        elements_by_group -- number of elements by group
        message -- explanation of the error
    """
    def __init__(self, elements_by_group):
        super(Error, self).__init__()
        self.message = "There is %i  elements by group, it must have 4 elements by group"%(elements_by_group)
class NumberElementsByGroupError(Error):
    """Exception raised for pairs repeat.

    Attributes:
        elements_by_group -- number of elements by group
        message -- explanation of the error
    """
    def __init__(self, pair,round):
        super(Error, self).__init__()
        self.message = "There pair %s is repeated in round %i"%(pair,round)
        
class MatchGroups():
    '''match elements in groups for different rounds where two elements do not repeat group in different rounds.
        elements is a list with 20 elements, for example:
        elements=["A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
        num_rounds is a number of rounds . More of 5 does that the elements repeat pairs
        elements_by_group is a number elements in a group. This algoritm is though to 4 elements_by_group
    '''
    def __init__(self, elements,num_rounds,elements_by_group):
        self.elements=elements;
        self.num_rounds=num_rounds;
        self.elements_by_group=elements_by_group;
        self.list_rounds=None;
        try:
            self.test_parameters();
            self.match_group();
            self.test_chek_number_pairs();
        except Error as e:
            print (e.message)
            #raise error
        
    def test_parameters(self):
        '''test for parameters'''
        if (len(self.elements)!=20):
            raise ElementsError(len(self.elements));
        if (self.num_rounds>5):
            raise NumberRoundsError(self.num_rounds);
        if (self.elements_by_group !=4):
            raise NumberElementsByGroupError(self.elements_by_group)
        
    def __sum_each_elements(self):
        '''function to calculate how much move each element'''
        candidates_sum=[0];
        num_elements=len(self.elements);
        k=self.elements_by_group;
        num_groups=num_elements//k
        for i in range(0,100000):
            i_is_candiate=True;
            if (i in candidates_sum):
                i_is_candiate=False;
            for r in range(1,num_groups):
                if (r*i%5==0):
                   i_is_candiate=False;
            if (len(candidates_sum)>1):
                for c in candidates_sum:
                    if (c!=i):
                        if ((c-i)%num_groups==0):
                            i_is_candiate=False;
            if (i_is_candiate):
                if (len(candidates_sum)<k):
                    candidates_sum.append(i);
        return candidates_sum;
        
    def match_group(self):
        '''match elements in groups for different rounds where two elements do not repeat group in different rounds.
            elements is a list with 20 elements, for example:
            elements=["A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
        '''
        elements=self.elements;
        k=self.elements_by_group
        num_rounds=self.num_rounds;
        num_elements=len(elements);
        random.shuffle(elements);
        list_rounds=[[[] for g in range(0,num_elements//self.elements_by_group )] for r in range(0,num_rounds)];
        #first round
        sum_player_position={}
        group_of_player={};
        p_i=0;
        groups=list_rounds[0];
        sum_each_elements=self.__sum_each_elements()
        #calculate how much move each element
        for g_i in range(0,len(groups)):
            g=groups[g_i];
            for p_g in sum_each_elements:
                if (len(g)<k) :
                    g.append(elements[p_i]);
                    sum_player_position[elements[p_i]]=p_g;
                    group_of_player[elements[p_i]]=g_i;
                    p_i=p_i+1;
        #for each rounds replace elements
        for r in range (1,len(list_rounds)):
            round_now=list_rounds[r];
            round_before=list_rounds[r-1];
            for p in elements:
                group_before=group_of_player[p];
                group_new=(group_before+sum_player_position[p])%(num_elements//k);
                group_of_player[p]=group_new;
                round_now[group_new].append(p);

        self.list_rounds=random.sample(list_rounds,len(list_rounds));
        
        
    def test_chek_number_pairs(self):
        '''test numbers pairs repeat is zero '''
        list_rounds=self.list_rounds;
        #chek number pairs
        list_pairs={};
        for r in range (0,len(list_rounds)):
            round_now=list_rounds[r];
            for g in round_now:
                list_pairs_in_group=[list(t) for t in itertools.combinations(g, 2)];
                for pair in list_pairs_in_group:
                    key_pair_reverse=pair[1]+"_"+pair[0];
                    key_pair=pair[0]+"_"+pair[1];
                    if (key_pair in list_pairs.keys() or key_pair_reverse in list_pairs.keys()):
                        list_pairs[key_pair]=list_pairs[key_pair]+1;
                        if (list_pairs[key_pair]>1):
                            raise NumberElementsByGroupError(key_pair,r+1)
                        
                              
                    else:
                       list_pairs[key_pair]=1;

            return list_pairs;
def test_main():        
    #elements=["A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"]
    elements=["A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
    #elements=["A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X"]

    num_rounds=5;
    k=4
    mg=MatchGroups(elements,num_rounds,k)
    print(mg.list_rounds)
    print (mg.test_chek_number_pairs())
if __name__ == "__main__":
    test_main();
