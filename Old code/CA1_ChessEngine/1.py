import chess
import chess.polyglot
import time
import os

class TurochampLike:
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 200000000000000
        }
        self.position_values = {
            chess.PAWN: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 5, 5, 5, 5, 5, 5, 5,
                1, 1, 2, 3, 3, 2, 1, 1,
                0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
                0, 0, 0, 2, 2, 0, 0, 0,
                0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
                0.5, 1, 1, -2, -2, 1, 1, 0.5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.KNIGHT: [
                -5, -4, -3, -3, -3, -3, -4, -5,
                -4, -2, 0, 0, 0, 0, -2, -4,
                -3, 0, 1, 1.5, 1.5, 1, 0, -3,
                -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
                -3, 0, 1.5, 2, 2, 1.5, 0, -3,
                -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
                -4, -2, 0, 0.5, 0.5, 0, -2, -4,
                -5, -4, -3, -3, -3, -3, -4, -5
            ],
            chess.BISHOP: [
                -2, -1, -1, -1, -1, -1, -1, -2,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -1, 0, 0.5, 1, 1, 0.5, 0, -1,
                -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
                -1, 0, 1, 1, 1, 1, 0, -1,
                -1, 1, 1, 1, 1, 1, 1, -1,
                -1, 0.5, 0, 0, 0, 0, 0.5, -1,
                -2, -1, -1, -1, -1, -1, -1, -2
            ],
            chess.ROOK: [
                0, 0, 0, 0, 0, 0, 0, 0,
                0.5, 1, 1, 1, 1, 1, 1, 0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                -0.5, 0, 0, 0, 0, 0, 0, -0.5,
                0, 0, 0, 0.5, 0.5, 0, 0, 0
            ],
            chess.QUEEN: [
                -2, -1, -1, -0.5, -0.5, -1, -1, -2,
                -1, 0, 0, 0, 0, 0, 0, -1,
                -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
                -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
                0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
                -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,
                -1, 0, 0.5, 0, 0, 0, 0, -1,
                -2, -1, -1, -0.5, -0.5, -1, -1, -2
            ],
            chess.KING: [
                -3, -4, -4, -5, -5, -4, -4, -3,
                -3, -4, -4, -5, -5, -4, -4, -3,
                -3, -4, -4, -5, -5, -4, -4, -3,
                -3, -4, -4, -5, -5, -4, -4, -3,
                -2, -3, -3, -4, -4, -3, -3, -2,
                -1, -2, -2, -2, -2, -2, -2, -1,
                2, 2, 0, 0, 0, 0, 2, 2,
                2, 3, 1, 0, 0, 1, 3, 2
            ]
        }
        self.depth = 4
        self.transposition_table = {}
        self.nodes_evaluated = 0
        self.time_limit = 5  # Time limit in seconds
        
        # Try to open the opening book, but continue without it if not found
        try:
            self.opening_book = chess.polyglot.open_reader("book.bin")
            print("Opening book loaded successfully.")
        except FileNotFoundError:
            print("Opening book 'book.bin' not found. Continuing without opening book.")
            self.opening_book = None

    def evaluate_board(self, board):
        if board.is_checkmate():
            return -9999 if board.turn else 9999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.piece_values[piece.piece_type]
                position_value = self.position_values[piece.piece_type][square]
                if piece.color == chess.WHITE:
                    score += value + position_value
                else:
                    score -= value + position_value

        # Bonus for controlling the center
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        for square in center_squares:
            if board.is_attacked_by(chess.WHITE, square):
                score += 0.1
            if board.is_attacked_by(chess.BLACK, square):
                score -= 0.1

        # Penalty for exposed king
        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)
        score += self.king_safety(board, white_king_square, chess.WHITE)
        score -= self.king_safety(board, black_king_square, chess.BLACK)

        return score

    def king_safety(self, board, king_square, color):
        safety_score = 0
        for square in chess.SQUARES:
            if chess.square_distance(king_square, square) <= 2:
                if board.is_attacked_by(not color, square):
                    safety_score -= 0.1
        return safety_score

    def get_best_move(self, board):
        # Check opening book first, if available
        if self.opening_book:
            try:
                return self.opening_book.weighted_choice(board).move
            except IndexError:
                pass  # Not in opening book, continue with normal search

        self.nodes_evaluated = 0
        start_time = time.time()
        best_move = None
        
        for depth in range(1, self.depth + 1):
            best_move = self.iterative_deepening(board, depth, start_time)
            if time.time() - start_time > self.time_limit * 0.8:  # Use 80% of time limit for search
                break

        print(f"Depth reached: {depth}, Nodes evaluated: {self.nodes_evaluated}")
        return best_move

    def iterative_deepening(self, board, depth, start_time):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        moves = list(board.legal_moves)
        moves.sort(key=lambda move: self.move_value(board, move), reverse=True)

        for move in moves:
            board.push(move)
            eval = -self.alpha_beta(board, depth - 1, -beta, -alpha, False, start_time)
            board.pop()

            if time.time() - start_time > self.time_limit:
                return best_move

            if eval > alpha:
                alpha = eval
                best_move = move

        return best_move

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player, start_time):
        self.nodes_evaluated += 1

        if time.time() - start_time > self.time_limit:
            return 0

        if depth == 0:
            return self.quiescence(board, alpha, beta)

        if board.is_game_over():
            return self.evaluate_board(board)

        moves = list(board.legal_moves)
        moves.sort(key=lambda move: self.move_value(board, move), reverse=True)

        if maximizing_player:
            for move in moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, False, start_time)
                board.pop()
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return alpha
        else:
            for move in moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, True, start_time)
                board.pop()
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return beta

    def quiescence(self, board, alpha, beta):
        stand_pat = self.evaluate_board(board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -self.quiescence(board, -beta, -alpha)
                board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    def move_value(self, board, move):
        if board.is_capture(move):
            return 10
        elif board.gives_check(move):
            return 5
        elif move.promotion:
            return 15  # Increased value for promotions
        elif board.is_castling(move):
            return 3  # Value for castling
        else:
            return 0

def play_game():
    board = chess.Board()
    engine = TurochampLike()

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            # Human's turn (White)
            print(board)
            while True:
                try:
                    move = input("Enter your move (e.g., e2e4): ")
                    move = chess.Move.from_uci(move)
                    if move in board.legal_moves:
                        board.push(move)
                        break
                    else:
                        print("Illegal move. Try again.")
                except ValueError:
                    print("Invalid input. Please use UCI format (e.g., e2e4)")
        else:
            # Computer's turn (Black)
            move = engine.get_best_move(board)
            print(f"Computer's move: {move}")
            board.push(move)

    print(board)
    print("Game Over")
    print(f"Result: {board.result()}")

if __name__ == "__main__":
    play_game()