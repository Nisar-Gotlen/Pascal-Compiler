from enum import Enum


class LexemesList(Enum):
    KAssignment = "Assignment"
    kIdentifier = "Identifier"
    kIntNumber = "Integer"
    kRelNumber = "Real"
    kRelDegreeNumber = "Real number degree form"
    kRelFloatNumber = "Real number float form"
    kRelNumber_e = "Real exponential form"
    kString = "String"
    kOperator = "Operator"
    kUnaryOperator = "Unary operator"
    kRelationOperator = "Relation operator"
    kAddOperator = "Addition operator"
    kMulOperator = "Multiple operator"
    kReserved = "Reserved Word"
    kDelimiter = "Delimiter"
    KComment = "Comment"
    kConstant = "Constant Identifier"
    kType = "Type Identifier"
    kFunction = "Function Identifier"
    kProcedure = "Procedure Identifier"
    kDirective = "Directive"
    kError = "Error"
