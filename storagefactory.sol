// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.6.0 < 0.9.0;
import "simplestorage.sol";

//to inherit functions of another contract, use IS
contract storagefactory  is SimpleStorage{
    SimpleStorage[] public simpleStorageArray;
    function createSimpleStorageContract()public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function sfstore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).store(_simpleStorageNumber);
        //SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        //simpleStorage.store(_simpleStorageNumber);
    }

    function sfGet(uint256 _simpleStorageIndex) public view returns (uint256){
        return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve();
        
        //SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        //return simpleStorage.retrieve();
    }

}