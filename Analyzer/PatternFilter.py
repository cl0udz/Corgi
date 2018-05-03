#!/usr/bin/env python
# encoding: utf-8

import re
from string import maketrans
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

#  This class is defined as an automatically filter
#  with given pattern template and keywords & special_keywords.
#
#   !!!ATTENTION!!!
#       Token word, keywords and special words should be strictly
#   in lower case, or you may get wrong results when calling
#   ChkRelation() with your new words.
#
#   How To Use:
#       First you should new a instance for FuncFilter:
#           The arguments are optional(keywords(list), special keywords(list), pattern_template(list of dict) and token_word(string))
#       1   ff = FuncFilter()
#
#       Then you just need to call ChkRelation() with your new word
#       2   if ff.ChkRelation('Test'):
#       3       return True
#       4   else:
#       5       return False
#
#       Whenever you want to replace the args with a new one, just call the corresponding method
#       6   newkeywords = ['apple', 'pear']
#       7   ff.SetKeywords(newkeywords)
#
#       Besides that, the token words in pattern template and in this class should be the same word,
#       which means that your should set a new token word when you set a new pattern template
#       For example:
#       8   newtemplate = [
#       9   {
#       10      "prefix": "[0-9]{",
#       11      "template": "NEWTOKEN",
#       12      "suffix": "}"
#       13      }
#       14  ]
#       15  ff.SetPatternTemplate(newtemplate)
#       16  ff.SetTokenWord("newtoken")

class PatternFilter():
    def __init__(self, keywords = [], special_keywords = [], pattern_template = [], token_word = "qwertyuiop"):
        self.filter_patterns = []
        self.token_word = token_word

        if len(keywords) == 0:
            self.keywords = [
                            'aes',
                            'des',
                            'rsa',
                            'cipher',
                            'key'
                        ]
        else:
            self.keywords = keywords
            
        if len(special_keywords) == 0:
            self.special_keywords = [
                                    'crypt',
                                    'password',
                                    'passwd'
                                ]
        else:
            self.special_keywords = special_keywords

        if len(pattern_template) == 0:
            self.pattern_template = [
                                    {
                                        "prefix":   "[a-zA-Z0-9]?",
                                        "template": "[q|Q]wertyuiop",
                                        "suffix":   "[A-Z:\s]"
                                    },
                                    {
                                        "prefix":   "[a-zA-Z0-9]?",
                                        "template": "QWERTYUIOP",
                                        "suffix":   "[A-Z:\s]"
                                    }
                                ]
        else:
            self.pattern_template = pattern_template

        return

    # The external method to execute the filter process
    def ChkRelation(self, word):
        for i in self.keywords:
            self.filter_patterns.append(self.__pattern_gen(i))

        return self.__filter(word)

    def SetKeywords(self, keywords):
        if type(keywords) == list:
            self.keywords = keywords
            return True
        else:
            return False

    def SetSpecialKeywords(self, special_keywords):
        if type(special_keywords) == list:
            self.special_keywords = special_keywords
            return True
        else:
            return False

    def SetPatternTemplate(self, pattern_template):
        if type(pattern_template) == list and type(pattern_template[0]) == dict:
            self.pattern_template = pattern_template
            return True
        else:
            return False

    def SetTokenWord(self, token_word):
        self.token_word = token_word
        return True

    # The internal method to execute the real filter process
    def __filter(self, word):
        result = False
        flag = False

        for i in self.special_keywords:
            if word.lower().find(i) != -1:
                result = True
                flag = True
                break
        
        if flag:
            return result

        for i in self.filter_patterns:
            for j in i:
                if(re.search(j, word)):
                    result = True
                    flag = True
                    break
        
            if flag:
                break

        return result


    #
    # In terms of a new keyword, apple for example:
    #                                a              pple
    # template1:    prefix          [t|T]           oken        suffix
    # pattern1:     prefix          [a|A]           pple        suffix
    #
    #                               apple
    # template2:    prefix          token       suffix
    # pattern2:     prefix          apple       suffix
    #
    #                               a       p   p       le
    # template3:    prefix          [t|T]   o   [k|K]   en      suffix
    # pattern3:     prefix          [a|A]   p   [p|P]   le      suffix
    #
    def __pattern_gen(self, word):
        patterns = []

        for i in self.pattern_template:
            temp = i
            pattern_core = temp['template']

            if len(self.token_word) > len(word):
                intab = self.token_word[:len(word)] + self.token_word[:len(word)].upper()
                outtab = word + word.upper()

                length_word = len(word)
                index = pattern_core.lower().find(self.token_word[length_word])
                pattern_core = pattern_core.replace(pattern_core[index:], "")

                transtab = maketrans(intab, outtab)
                pattern_core = pattern_core.translate(transtab)
            else:
                intab = self.token_word + self.token_word.upper()
                outtab = word[:len(self.token_word)] + word[:len(self.token_word)].upper()

                length_token = len(self.token_word)
                index = pattern_core.lower().find(self.token_word[-1])
                pattern_core = pattern_core + word[length_token:]

                transtab = maketrans(intab, outtab)
                pattern_core = pattern_core[:index + 1].translate(transtab) + pattern_core[index + 1:]

            new_pattern = temp['prefix'] + pattern_core + temp['suffix']
            patterns.append(new_pattern)

            #print new_pattern
            
        return patterns