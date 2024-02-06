function getPlayers() {
    let inputs = document.getElementsByTagName("input")
    for (i = 0; i < inputs.length; i++) {
        let input = inputs[i];

        if (input.type === "radio" && input.name === "players" && input.checked) {
            return input.value;
        }
    }
}


function getDifficulty() {
    let inputs = document.getElementsByTagName("input");
    for (i = 0; i < inputs.length; i++) {
        let input = inputs[i];

        if (input.type === "radio" && input.name === "difficulty" && input.checked) {
            return input.value;
        }
    }
}


const RED = Symbol("red")
const BLACK = Symbol("black")

const sym2str = new Map();

sym2str.set(RED, "Red");
sym2str.set(BLACK, "Black");


class GameState {
    #n_players;
    #board;
    #table = null;
    #game_out;
    #n_turn = 2;
    #game_over = false;

    constructor(n_players, board, game_out) {
        this.#n_players = n_players;
        this.#board = board;
        this.#game_out = game_out;
    }

    setTable(table) {
        this.#table = table;
    }

    get gameOver() {
        return this.#game_over;
    }

    get boardLen() {
        return this.#board.length;
    }

    get boardCols() {
        return this.#board[0].length;
    }

    get nPlayers() {
        return this.#n_players;
    }

    #updateTable() {
        for (let i = 0; i < this.#board.length; i++) {
            let row = this.#table.rows[i];
            for (let j = 0; j < this.#board[i].length; j++) {
                row.cells[j].firstChild.replaceWith(this.placeBoardImage(i, j));
            }
        }
    }

    #setGameOut(message) {
        this.#game_out.innerHTML = message;
    }

    #clearGameOut() {
        this.#game_out.innerHTML = "";
    }

    placeBoardImage( row, col) {
        let img = document.createElement("img");
        img.height = "100";
        img.width = "100";
        if (this.#board[row][col] === 2) {
            img.src = "static/conn4_black.gif";
        } else if (this.#board[row][col] === 1) {
            img.src = "static/conn4_star.gif";
        } else {
            img.src = "static/1x1.png";
        }
        return img
    }

    #checkGameWon() {
        // check for horizontal wins

        for (let i = 0; i < this.#board.length; i++) {
            let row = this.#board[i];
            let count = 0;
            let cur_color = null;
            let j = 0;

            while (count < 4 && j < row.length) {
                if (row[j] != 0 && cur_color === null) {
                    cur_color = row[j]
                    count++;
                } else if (cur_color != null && row[j] === cur_color) {
                    count++;
                } else if (cur_color != null && row[j] != cur_color && row[j] != 0) {
                    cur_color = row[j];
                    count = 1;
                } else if (cur_color != null && row[j] != cur_color && row[j] === 0) {
                    cur_color = null;
                    count = 0;
                }
                j++;
            }

            if (count === 4 && cur_color === 1) {
                return RED;
            } else if (count === 4 && cur_color === 2) {
                return BLACK;
            }
        }

        // check for verticle wins

        for (let j = 0; j < this.#board[0].length; j++) {
            let count = 0;
            let cur_color = null;
            let i = 0;

            while(count < 4 && i < this.#board.length) {
                if (this.#board[i][j] != 0 && cur_color === null) {
                    cur_color = this.#board[i][j];
                    count++;
                } else if (this.#board[i][j] != 0 && this.#board[i][j] != cur_color && cur_color != null) {
                    cur_color = this.#board[i][j];
                    count = 1;
                } else if (this.#board[i][j] === cur_color && cur_color != null) {
                    count++;
                } else if (cur_color != null && this.#board[i][j] === 0) {
                    cur_color = null;
                    count = 0;
                }
                i++;
            }

            if (count === 4 && cur_color === 1) {
                return RED;
            } else if (count === 4 && cur_color === 2) {
                return BLACK;
            }
            
        }

        // check for diagional
        // get all valid possible sets of diagionals first

        function getDiagionals(board) {
            let diagionals = Array();
            
            // top row to bottom left diagionals
            
            let top_row = board[0];

            for (let k = 0; k < top_row.length; k++) {
                let cur_diag = Array();
                let i = 0;
                let j = k;
                while (board.length > i && board[0].length > j) {
                    cur_diag.push(board[i][j]);
                    i++;
                    j++;
                }

                diagionals.push(cur_diag);
            }

            // first col down diagionals
            
            for (let k = 1; k < board[0].length; k++) {
                let cur_diag = Array();
                let i = k;
                let j = 0;
                while (board.length > i && board[0].length > j) {
                    cur_diag.push(board[i][j]);
                    i++;
                    j++;
                }

                diagionals.push(cur_diag);
            }
            
            // bottom row up diagionals

            for (let k = 0; k < board[0].length; k++) {
                let cur_diag = Array();
                let i = board.length - 1;
                let j = k;
                while (i >= 0 && board[0].length > j) {
                    cur_diag.push(board[i][j]);
                    i--;
                    j++;
                }

                diagionals.push(cur_diag);
            }

            // last col up diagionals
            
            for (let k = board[0].length - 1; k >= 0; k--) {
                let cur_diag = Array();
                let i = k;
                let j = board[0].length - 1;
                while (board.length > i && j >= 0) {
                    cur_diag.push(board[i][j]);
                    i++;
                    j--;
                }

                cur_diag.push(cur_diag);
            }

            return diagionals;
        }

        let diagionals = getDiagionals(this.#board);

        for (let i = 0; i < diagionals.length; i++) {
            let row = diagionals[i]
            let count = 0;
            let cur_color = null;
            let j = 0;

            while (count < 4 && j < row.length && row.length >= 4) {
                if (row[j] != 0 && cur_color === null) {
                    cur_color = row[j]
                    count++;
                } else if (cur_color != null && row[j] === cur_color) {
                    count++;
                } else if (cur_color != null && row[j] != cur_color && row[j] != 0) {
                    cur_color = row[j];
                    count = 1;
                } else if (cur_color != null && row[j] != cur_color && row[j] === 0) {
                    cur_color = null;
                    count = 0;
                }
                j++;
            }

            if (count === 4 && cur_color === 1) {
                return RED;
            } else if (count === 4 && cur_color === 2) {
                return BLACK;
            }
        }

        return null;
    }

    setBoardCell(row, col) {
        let player = 0;
        this.#clearGameOut();

        if (this.n_players === 1) {
            player = 1;
        } else {
            player = (this.#n_turn % 2) + 1;
        }

        this.#board[row][col] = player;
        this.#updateTable();
        let game_status = this.#checkGameWon();

        if (game_status === null) {
            this.#n_turn++;
            return;
        } else {
            console.log(game_status.toString() + "won the game.");
            this.#game_over = true;
            this.finishGame(game_status);

        }
    }

    lowestEmptyRow(col) {
        for (let i = this.boardLen - 1; i >= 0 ; i--) {
            if (this.#board[i][col] === 0) {
                return i;
            }
        }

        return null;
    }

    finishGame(winner) {
        this.#setGameOut(sym2str.get(winner) + " Wins!\nPress 'Start' button to play again.");
    }
     
}


function generateBoard(rows, cols) {
    const board = Array(rows).fill(0)

    for (i = 0; i < rows; i++) {
        board[i] = Array(cols).fill(0);
    }
    return board;
}


function buildTable(table, game) {
    for (let i = 0; i < game.boardLen; i++) {
        let row = table.insertRow();
        for (let j = 0; j < game.boardCols; j++) {
            let cell = row.insertCell();
            cell.appendChild(game.placeBoardImage(i, j));

            cell.addEventListener("click", () => onClickColumn(game, j));
        }
    }
}


function onClickColumn(game, col) {
    if (game.gameOver) {
        return null;
    }
    console.log("clicked col", col);

    row = game.lowestEmptyRow(col);

    if (row != null) {
        game.setBoardCell(row, col)
    }
}

function setupGame(board_rows, board_cols) {

    const game_out = document.getElementById("game_out");

    const n_players = getPlayers();

    const board = generateBoard(board_rows, board_cols);


    game = new GameState(n_players, board, game_out);
    
    console.log("building table");

    const table = document.getElementById("conn4_board");
    table.innerHTML = "";
    buildTable(table, game);
    game.setTable(table);
    
    return game;
}


function startGame() {
    console.log("starting game");
    game = setupGame(6, 7);

    if (game.nPlayers === 1) {
        const difficulty = getDifficulty();

        game_out.innerHTML = difficulty.toString();
        
        console.log("difficulty" + difficulty.toString());
    } else if (game.nPlayers === 2) {
        console.log("2 player game");
    }

}



