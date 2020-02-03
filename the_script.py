# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 14:32:05 2019

@author: Jonat
"""

def enter_your_age(something):
    
    if something < 13:
        print("You are an adolescent")
    elif something >= 13 and something < 45:
        print("You are a young man")
    else:
        print("You are in your prime")