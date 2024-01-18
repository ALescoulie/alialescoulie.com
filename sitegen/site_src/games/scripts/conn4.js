function getDifficulty() {
    var inputs = document.getElementsByTagName("input");
    for (i = 0; i < inputs.length; i++) {
        var input = inputs[i];

        if (input.type === "radio" && input.checked) {
            return input.value;
        }
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
        board[row][col] = 1;
        placeBoardImage(board, row, col);
        updateTable(table, board);
    }
}


function startGame() {

    const game_out = document.getElementById("game_out");
    const difficulty = getDifficulty();

    game_out.innerHTML = difficulty.toString();
    
    console.log("difficulty" + difficulty.toString());

    const board = generateBoard(6, 7);

    const table = document.getElementById("conn4_board");
    
    buildTable(table, board);

    game_out.innerHTML = "Make your move.";

    
}

