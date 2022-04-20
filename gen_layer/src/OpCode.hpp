#ifndef OPCODE_HPP_INCLUDED
#define OPCODE_HPP_INCLUDED

#include <map>

enum OpCodeFeedInfo
{
    VALUE_FEED = 1, //When a value is used
    MULT_VALUES_FEED = 2, //When multiples values are used
    ASSIGN_FEED = 3, //When a value is assigned to the list of values
    TYPE_FEED = 4, // When the value is a type
    BLOCK_FEED = 5, //When the value is a block id
    DATA_64BITS = 6, //When there is 64 bits of data
    DATA_32BITS = 7, //When there is 32 bits of data
    DATA_STR = 8, //When there is a string data
};


std::map<int,std::vector<OpCodeFeedInfo>> OpCodesInfo =
{
    {1,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {2,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {3,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {4,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {5,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {6,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {7,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {8,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {9,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {10,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {11,{VALUE_FEED, ASSIGN_FEED}},
    {12,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {13,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {14,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {15,{VALUE_FEED, ASSIGN_FEED}},
    {16,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {17,{VALUE_FEED, ASSIGN_FEED}},
    {100,{VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {101,{VALUE_FEED, ASSIGN_FEED}},
    {150,{BLOCK_FEED}},
    {151,{VALUE_FEED, BLOCK_FEED,BLOCK_FEED}},
    {152,{VALUE_FEED, VALUE_FEED, VALUE_FEED, ASSIGN_FEED}},
    {153,{TYPE_FEED,VALUE_FEED, MULT_VALUES_FEED, ASSIGN_FEED}},
    {170,{DATA_32BITS, MULT_VALUES_FEED, ASSIGN_FEED}},
    {171,{VALUE_FEED, DATA_32BITS, MULT_VALUES_FEED, ASSIGN_FEED}},
    {1000,{DATA_64BITS,ASSIGN_FEED}},
    {1000,{DATA_64BITS,ASSIGN_FEED}},
    {1001,{DATA_32BITS,ASSIGN_FEED}},
    {1002,{DATA_32BITS,ASSIGN_FEED}},
    {1003,{DATA_32BITS,ASSIGN_FEED}},
    {1004,{DATA_32BITS,ASSIGN_FEED}},
    {1005,{DATA_64BITS,ASSIGN_FEED}},
    {1007,{DATA_32BITS,ASSIGN_FEED}},
    {1006,{TYPE_FEED, ASSIGN_FEED}},
    {1010,{VALUE_FEED,TYPE_FEED,ASSIGN_FEED}},
    {1011,{VALUE_FEED,TYPE_FEED,ASSIGN_FEED}},
    {1012,{VALUE_FEED,TYPE_FEED,ASSIGN_FEED}},
    {1013,{VALUE_FEED,TYPE_FEED,ASSIGN_FEED}},
    {1014,{VALUE_FEED,TYPE_FEED,ASSIGN_FEED}},
    {1015,{VALUE_FEED,TYPE_FEED,ASSIGN_FEED}},
    {1050,{TYPE_FEED,ASSIGN_FEED}},
    {2000,{VALUE_FEED}},
    {2001,{}},
    {2002,{}},
    {3000,{DATA_32BITS,ASSIGN_FEED}},
    {3001,{DATA_STR,ASSIGN_FEED}},
    {3002,{DATA_32BITS,ASSIGN_FEED}},
    {9998,{TYPE_FEED,ASSIGN_FEED}},
    {9999,{TYPE_FEED,ASSIGN_FEED}},
    {10000,{VALUE_FEED}},
    {10001,{}},
    {10002,{}},

};


#endif // OPCODE_HPP_INCLUDED
