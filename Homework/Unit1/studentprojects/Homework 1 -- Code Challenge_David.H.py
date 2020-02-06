#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# # Challenge 1: Largest Palindrome
# 
# #### A palindromic number reads the same both ways. For example, 1234321 is a palindrome. The largest palindrome made from the product of two two-digit numbers is 9009 = 91 × 99. Find the largest palindrome made from the product of two three-digit numbers. Afterward, write a brief explanation walking through your code's logic in markdown.

# In[8]:


#Use two loops that multiplies all possible two 3 digit numbers together
#create two variables

a = 100
b = 100

largestPal = 0

#palindrome test function

def IsPalindrome(n):
    possiblePal = str(n)
    if possiblePal == possiblePal [::-1]:
        return 1
    else:
        return 0
    
#Calculations

for a in range(100, 1000):
    for b in range(100, 1000):
        if IsPalindrome(a*b) == 1 and (a*b) > largestPal:
            largestPal = (a*b)
#Result
print(largestPal)


# # Challenge 2: Summation of Primes
# 
# #### The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17. Find the sum of all the primes below 2,000. Afterward, write a brief explanation walking through your code's logic in markdown.

# In[9]:


def isPrime(n):
    if n < 2: return "Neither prime, nor composite"
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

sum = 0
for i in range(2, 2000):
    if isPrime(i):
        sum += i

print (sum)


# 

# In[14]:


import math


def check_prime(num):
    if num > 2 and num % 2 == 0:
        return False
    else:
        # I tried using a generator here,
        # but it is slower by a noticeable amount.
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
    return True


def find_sum(limit):
    sum = 0
    for i in range(2, limit):
        if check_prime(i):
            sum += i
    
    return sum


if __name__ == '__main__':

# Find the sum of all primes below two million

    print(find_sum(2000))

# confirm above is correct by solving example
# and verifying results are euqal to that presented
# by example

    print(find_sum(10))


# #### ^^^^^^^^^^^^^^^^^^^^^^ NOTE on Challenge 2 ^^^^^^^^^^^^^^^^^^^^^^
# 
# I'm not 100% sure of everything in the above examples but I did seek out two different methods to find the sum of primes under 2000, so as to confirm(verify) the correct outcome
# 
# **********************************************************************

# # Challenge 3: Multiples of 3 and 5
# 
# #### If we list all of the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6, and 9. The sum of these multiples is 23. Find the sum of all the multiples of 3 and 5 below 1,000. Afterward, write a brief explanation walking through your code's logic in markdown.

# In[15]:


sum = 0
for i in range(0,1000):
    if i % 3 == 0 or i % 5 == 0:
        sum = sum + i
print(sum)


# # Challenge 4: String Compressor
# 
# #### Implement a method to perform basic string compression using the counts of repeated characters. (This is called run-length encoding.) For example, the string "aabcccccaaa" would become a2b1c5a3. If the “compressed” string would not become smaller than the original string, your method should return the original string. You can assume the string has only uppercase and lowercase letters (a–z). Specify whether your solution is case sensitive or case insensitive and what you would need to change to make it the other. Afterward, write a brief explanation walking through your code's logic in markdown.

# In[27]:


def compress_string(string):
    char_count = 1
    compressed_string = ""
    for pos, char in enumerate(string):
        if pos + 1 < len(string) and char == string[pos + 1]:
            char_count += 1
        else:
            compressed_chars = char + str(char_count)
            compressed_string = compressed_string + compressed_chars
            char_count = 1
    if len(compressed_string) < len(string):
        return compressed_string
    else:
        return string

if __name__ == "__main__":
    input_string = input("Enter string to compress: ")
    print(compress_string(input_string))


# # BONUS Challenge: FizzBuzz
# 
# #### Write a program that prints all of the numbers from 1 to 100. For multiples of 3, instead of the number, print "Fizz;" for multiples of 5, print "Buzz." For numbers that are multiples of both 3 and 5, print "FizzBuzz." Afterward, write a brief explanation walking through your code's logic in markdown.

# In[30]:


#Python program to print Fizz Buzz 
#loop for 100 times i.e. range 

for fizzbuzz in range(100):  
  
    # number divisible by 3, print 'Fizz'  
    # in place of the number 
    
    if fizzbuzz % 15 == 0:  
        print("FizzBuzz")                                          
        continue
  
    # number divisible by 5, print 'Buzz' 
    # in place of the number 
    
    elif fizzbuzz % 3 == 0:      
        print("Fizz")                                          
        continue
  
    # number divisible by 15 (divisible  
    # by both 3 & 5), print 'FizzBuzz' in 
    # place of the number 
    
    elif fizzbuzz % 5 == 0:          
        print("Buzz")                                      
        continue
  
    # print numbers 
    
    print(fizzbuzz) 


# In[ ]:




