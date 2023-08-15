// SPDX-License-Identifier: UNLICENSED
pragma solidity =0.8.0;


// Betting smartcontract by gensx-x1
// git: https://github.com/gensx-x1
// tg: @gensx1

import "./SafeMath.sol";
import {ERC20} from "./teamToken.sol";


contract MuskvsZuckBet {

    using SafeMath for uint;

    address _vault;
    address _owner;
    ERC20 teamElon;
    ERC20 teamMark;
    address MarkToken;
    address ElonToken;
    bool beforeFight = false;
    bool afterFight = false;
    uint fightBlock;
    uint winner = 0;
    uint betMusk = 0;
    uint betZuck = 0;
    struct Bets{
        address better;
        uint256 betAmount;
        uint side;  // 1 = Musk , 2 = Zuckerberg
    }
    Bets[] betList;

    constructor() {
        _vault = msg.sender;
        _owner = msg.sender;
        teamElon = new ERC20('teamElon', 'ELON');
        teamMark = new ERC20('teamMark', 'MARK');
        ElonToken = address(teamElon);
        MarkToken = address(teamMark);
    }

    receive() external payable {}

    // CONTROL FUNCTIONS
    function setWinner(uint side) public {
        require(msg.sender == _owner, "need owner");
        winner = side;
    }

    function setBeforeFight(bool set) public {
        require(msg.sender == _owner, "need owner");
        beforeFight = set;
    }

    function setAfterFight(bool set) public {
        require(msg.sender == _owner, "need owner");
        afterFight = set;
    }

    function setFightBlock(uint _fightBlock) public {
        require(msg.sender == _owner, "need owner");
        fightBlock = _fightBlock;

    }

    // VIEW PUBLIC FUNCIONS
    function owner() public view returns (address){
        return _owner;
    }

    function vault() public view returns (address){
        return _vault;
    }

    function totalBets() public view returns (uint256 Musk, uint256 Zuckerberg){
        return (betMusk, betZuck);
    }

    function checkBet() public view returns(uint256 betAmount, string memory side){
        for (uint i; i < betList.length; i++){
            if (betList[i].better == msg.sender){
                string memory pickedSide;
                if (betList[i].side == 1){
                    pickedSide = "Musk";
                }
                if (betList[i].side == 2){
                    pickedSide = "Zuckerberg";
                }
                return (betList[i].betAmount, pickedSide);
            }
            
        }
    }

    function teamElonToken() public view returns(address _teamElon) {
        return address(teamElon);
    }

    function teamMarkToken() public view returns(address _teamMark) {
        return address(teamMark);
    }

    // VIEW INTERNAL FUNCTIONS
    function checkIfEnter(address who) internal view returns(bool entered, uint _id){
        for (uint i; i < betList.length; i++){
            if (betList[i].better == who){
                return (true, i);
            }        
        }
    }

    // PAYABLE FUNCTIONS
    function placeBet(uint betSide) external payable {
        require(beforeFight == false, "lock before fight");
        require(afterFight == false, "fight is over");
        require(betSide == 1|| betSide == 2, "pick side");
        (bool alreadyEnter, uint id) = checkIfEnter(msg.sender);
        uint256 fees = msg.value*20000/1000000;
        uint256 betAmount = msg.value-fees;
        if (alreadyEnter == false){
            betList.push(Bets(msg.sender, betAmount, betSide));
        }
        if (alreadyEnter == true){
            betList[id].betAmount += betAmount;
            betList[id].side = betSide;
            }
        if (betSide == 1){
            betMusk += betAmount;
            teamElon.mint(msg.sender);
        }
        if (betSide == 2){
            betZuck += betAmount;
            teamMark.mint(msg.sender);
        }
        payable(_vault).transfer(fees);
    }

    function withdrawBet() public {
        require(beforeFight == false, "lock before fight");
        require(afterFight == false, "fight is over");
        (bool alreadyEnter, uint id) = checkIfEnter(msg.sender);
        if (alreadyEnter == false){
            return;
        }
        if (alreadyEnter == true){
            uint256 amount = betList[id].betAmount;
            // replace this with funcion, maybe
            if (betList[id].side == 1){
                betMusk -= amount;
            }
            if (betList[id].side == 2){
                betZuck -= amount;
            }
            delete betList[id];
            payable(msg.sender).transfer(amount);
        }
    }

    function claim() public {
        require(afterFight == true, "fight is not over");
        ( , uint playerId) = checkIfEnter(msg.sender);
        require(betList[playerId].side == 1|| betList[playerId].side == 2, "no bet");
        require(winner == 1||winner == 2, "no winner set yet");
        if (betList[playerId].side == winner){
            if (winner == 1){
                uint256 percentAmount = (betList[playerId].betAmount.mul(1000000)).div(betMusk);
                uint payout = ((betZuck).mul(percentAmount).div(1000000).add(betList[playerId].betAmount));
                delete betList[playerId];
                payable(msg.sender).transfer(payout);
                return;
            }
            if (winner == 2){
                uint percentAmount = (betList[playerId].betAmount.mul(1000000)).div(betZuck);
                uint payout = ((betMusk*percentAmount).div(1000000)).add(betList[playerId].betAmount);
                delete betList[playerId];
                payable(msg.sender).transfer(payout);
                return;
            } 
        }

    }

}
