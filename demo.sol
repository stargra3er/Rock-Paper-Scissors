// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RockPaperScissors {
    address public player1;
    address public player2;
    uint256 public betAmount;
    bytes32 public commitment1;
    bytes32 public commitment2;
    string public clearMove1;
    string public clearMove2;
    address public winner;
    uint256 public reward;
    uint256 constant public MIN_BET = 0.0001 ether;
    uint256 constant public REVEAL_TIMEOUT = 1 hours;

    constructor() {
        player1 = address(0);
        player2 = address(0);
        betAmount = 0;
    }

    function register() public payable {
        require(player1 == address(0) || player2 == address(0), "Both players are already registered.");
        require(msg.value >= MIN_BET, "Minimum bet not met.");

        if (player1 == address(0)) {
            player1 = msg.sender;
        } else {
            player2 = msg.sender;
            betAmount = msg.value;
        }
    }

    function play(bytes32 _commitment) public {
        require(msg.sender == player1 || msg.sender == player2, "You are not registered to play.");
        require(commitment1 == bytes32(0) || commitment2 == bytes32(0), "Both players have already played.");

        if (msg.sender == player1) {
            commitment1 = _commitment;
        } else {
            commitment2 = _commitment;
        }
    }

    function reveal(string memory _clearMove, string memory _password) public {
        require(msg.sender == player1 || msg.sender == player2, "You are not registered to reveal.");
        require(commitment1 != bytes32(0) && commitment2 != bytes32(0), "Both players have not played yet.");
        require(bytes(_clearMove).length > 0, "Invalid clear move.");

        if (msg.sender == player1) {
            require(keccak256(abi.encodePacked(_clearMove, _password)) == commitment1, "Invalid commitment.");
            clearMove1 = _clearMove;
        } else {
            require(keccak256(abi.encodePacked(_clearMove, _password)) == commitment2, "Invalid commitment.");
            clearMove2 = _clearMove;
        }

        if (bytes(clearMove1).length > 0 && bytes(clearMove2).length > 0) {
            determineWinner();
        }
    }

    function determineWinner() internal {
        require(bytes(clearMove1).length > 0 && bytes(clearMove2).length > 0, "Both players have not revealed yet.");

        if (keccak256(abi.encodePacked(clearMove1)) == keccak256(abi.encodePacked(clearMove2))) {
            // It's a draw
            winner = address(0);
            reward = betAmount;
        } else if (
            (keccak256(abi.encodePacked(clearMove1)) == keccak256(abi.encodePacked("rock")) && keccak256(abi.encodePacked(clearMove2)) == keccak256(abi.encodePacked("scissors"))) ||
            (keccak256(abi.encodePacked(clearMove1)) == keccak256(abi.encodePacked("scissors")) && keccak256(abi.encodePacked(clearMove2)) == keccak256(abi.encodePacked("paper"))) ||
            (keccak256(abi.encodePacked(clearMove1)) == keccak256(abi.encodePacked("paper")) && keccak256(abi.encodePacked(clearMove2)) == keccak256(abi.encodePacked("rock")))
        ) {
            // Player 1 wins
            winner = player1;
            reward = 2 * betAmount;
        } else {
            // Player 2 wins
            winner = player2;
            reward = 2 * betAmount;
        }
    }

    function getOutcome() public {
        require(winner != address(0), "The game is not over yet.");
        require(msg.sender == player1 || msg.sender == player2, "You are not part of the game.");
        require(msg.sender == winner, "You are not the winner.");

        payable(winner).transfer(reward);
        // Reset game state
        player1 = address(0);
        player2 = address(0);
        betAmount = 0;
        commitment1 = bytes32(0);
        commitment2 = bytes32(0);
        clearMove1 = "";
        clearMove2 = "";
        winner = address(0);
        reward = 0;
    }

    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function whoAmI() public view returns (uint256) {
        if (msg.sender == player1) {
            return 1;
        } else if (msg.sender == player2) {
            return 2;
        } else {
            return 0;
        }
    }

    function bothPlayed() public view returns (bool) {
        return commitment1 != bytes32(0) && commitment2 != bytes32(0);
    }

    function bothRevealed() public view returns (bool) {
        return bytes(clearMove1).length > 0 && bytes(clearMove2).length > 0;
    }

    function revealTimeLeft() public view returns (uint256) {
        if (bothPlayed()) {
            return 0;
        } else {
            return REVEAL_TIMEOUT;
        }
    }
}
