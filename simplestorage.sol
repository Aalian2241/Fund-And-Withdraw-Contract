// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.0 <0.9.0;

//contract like a class
contract SimpleStorage{
    //public = anyone can call, even a variable
    //external = only an outside contract can call the value
    //internal = can only be called by other functions in same contract, derived contract
    //private = self contained inside the bracket only.


    //uint is unsigned integer, neither positive nor negative
    uint256 public favoriteNumber = 5;
    bool favoritebool = true;
    string favoritestring = "string here";
    
    struct People{
        uint256 id ;
        string name;
    }

    People[] public people;

    address favoriteaddress = 0xfEF88f0b6D464534060B3C5EE57810741805ac18;
    bytes32 favbyte = "cat";
    //mapping
    mapping(string => uint256) public nameTofavnumber;
    
    function addPerson (string memory _name, uint256 _id) public {
        people.push(People({id:_id,name:_name} ));
        nameTofavnumber[_name] = _id;
    }

    //function (param types) {internal|external} [pure|constant|view|payable] [returns (return types)] varName;
    function retrieve()public view returns (uint256){ 
        return favoriteNumber;
    }
    function store(uint256 _favnumber) public returns (uint256){
        favoriteNumber = _favnumber;
        return favoriteNumber;
    }


    function getStruct()public view returns (uint, string memory){   
        return (people[0].id, people[0].name);
    }

    
}