function getPlayers() {
    let inputs = document.getElementById("input")
    for (i = 0; i < inputs.length; i++) {
        let input = inputs[i];

        if (input.type === "radio" && input.name === "players") {
            return input.value;
        }
    }
}


function getDifficulty() {
    let inputs = document.getElementsByTagName("input");
    for (i = 0; i < inputs.length; i++) {
        let input = inputs[i];

        if (input.type === "radio" && input.checked) {
            return input.value;
        }
    }
}


class GameState {
    constructor(n_players, board, table, game_out) {
        this.m_players = n_players;
        this.board = board;
        this.table = table;
        this.game_out = game_out;
    }

    get board() {
        return this.board();
    }

    

}


function generateBoard(rows, cols) {
    const board = Array(rows).fill(0)

    for (i = 0; i < rows; i++) {
        board[i] = Array(cols).fill(0);
    }
    return board;
}


function placeBoardImage(board, row, col) {
    let img = document.createElement("img");
    img.height = "100";
    img.width = "100";
    if (board[row][col] === 2) {
        img.src = "static/conn4_black.gif";
    } else if (board[row][col] === 1) {
        img.src = "static/conn4_star.gif";
    } else {
        img.src = "static/1x1.png";
    }
    return img;
}


function buildTable(table, board) {
    for (let i = 0; i < board.length; i++) {
        let row = table.insertRow();
        for (let j = 0; j < board[i].length; j++) {
            let cell = row.insertCell();
            cell.appendChild(placeBoardImage(board, i, j));

            cell.addEventListener("click", () => onClickColumn(j, board, table));
        }
    }
}


function updateTable(table, board) {
    for (let i = 0; i < board.length; i++) {
        let row = table.rows[i];
        for (let j = 0; j < board[i].length; j++) {
            row.cells[j].firstChild.replaceWith(placeBoardImage(board, i, j));
        }
    }
}


function lowestEmptyRow(board, col) {
    for (let i = board.length - 1; i >= 0 ; i--) {
        if (board[i][col] === 0) {
            return i;
        }
    }

    return null;
}


function onClickColumn(col, board, table) {
    console.log("clicked col", col);

    row = lowestEmptyRow(board, col);

    if (row != null) {
        board[row][col] = player;
        placeBoardImage(board, row, col);
        updateTable(table, board);
        game_status = gameWon(board);
        if (game_status != null) {
            console.log(game_status);
        }

        if (game_status === RED) {
            game_out.innerHTML = "You won!";
        } else if (game_status === BLACK) {
            game.innerHTML = "You Lose!";
        }
    }
}


const RED = Symbol("red")
const BLACK = Symbol("black")


function gameWon(board) {
    // check for horizontal wins

    for (let i = 0; i < board.length; i++) {
        let row = board[i];
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

    for (j = 0; j < board[0].length; j++) {
        count = 0;
        cur_color = null;
        i = 0;

        while(count < 4 && i < board.length) {
            if (board[i][j] != 0 && cur_color === null) {
                cur_color = board[i][j];
                count++;
            } else if (board[i][j] != 0 && board[i][j] != cur_color && cur_color != null) {
                cur_color = board[i][j];
                count = 1;
            } else if (board[i][j] === cur_color && cur_color != null) {
                count++;
            } else if (cur_color != null && board[i][j] === 0) {
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
    return null;

    // check for diagional
}


function startGame() {

    var game_out = document.getElementById("game_out");
    var game_status = null;

    const board = generateBoard(6, 7);
    const table = document.getElementById("conn4_board");

    buildTable(table, board);

    const n_players = getPlayers();
    var player = 1;

    if (n_players === 1) {
        const difficulty = getDifficulty();

        game_out.innerHTML = difficulty.toString();
        
        console.log("difficulty" + difficulty.toString());
    } else if (n_players === 2) {
        multiPlayer(board, table);   
    }



}


function multiPlayer(board, table) {
    game_out.innerHTML = "Player1: Make your move.";


}
