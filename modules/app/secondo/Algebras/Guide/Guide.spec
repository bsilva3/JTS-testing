
# simple prefix operator having one argument
operator perimeter alias PERIMETER pattern op(_)

# infix operator
operator distN alias DISTN pattern _ infixop _

# postfix operator having a parameter in square brackets
operator countNumber alias COUNTNUMBER pattern _ op[_]

#simple prefix operator
operator getChars alias GETCHARS pattern op(_)

# operator having a function with implicit arguments
operator replaceElem alias REPLACEELEM pattern _ op[ fun ] 
         implicit parameter streamelem type STREAMELEM

# postfix operator with an parameter
operator startsWithS alias STARTSWITHS pattern _ op [_ ]

# postfix operator with an additional argument
operator attrIndex alias ATTRINDEX pattern _ op [_]

#postfix operator without parameters
operator createPAVL alias CREATEPAVL pattern _ op


# infix operator
operator contains alias CONTAINS pattern _ infixop _


# postfix operazor with two arguments
operator insert alias INSERT pattern _ _ op


# prefix operator
operator importObject alias IMPORTOBJECT pattern op(_)

# prefix operator
operator importObject2 alias IMPORTOBJECT2 pattern op(_)

# prefix operator
operator text2vstring alias TEXT2VSTRING pattern op(_)


#postfix operator
operator reverseStream alias REVERSESTREAM pattern _ op

