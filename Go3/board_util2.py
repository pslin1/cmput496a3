from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, FLOODFILL

class GoBoardUtil2(GoBoardUtil):
    
    @staticmethod
    def generate_move_with_filter(board, use_pattern, check_selfatari):
        if board.last_move:
            move = GoBoardUtil2.generate_atari_capture_move(board, board.last_move)
            if move:
                return move
            move = GoBoardUtil2.generate_atari_defense_move(board, board.last_move, check_selfatari)
            if move:
                return move
        return GoBoardUtil.generate_move_with_filter(board, use_pattern, check_selfatari)
        
    @staticmethod
    def generate_atari_defense_move(board, last_move, check_selfatari):
        moves = GoBoardUtil2.generate_all_atari_defense_moves(board, last_move)
        move = GoBoardUtil2.filter_moves_and_generate(board, moves, check_selfatari)   
        return move
    
    @staticmethod
    def generate_all_atari_defense_moves(board, last_move):
        all_defense_moves = []
        threatened_stones = [] 
        
        neighbors = board._neighbors(last_move)
        for n in neighbors:
            if board.board[n] == board.current_player and board._single_liberty(n, board.current_player) != None:
                threatened_stones.append(n)
        for p in threatened_stones:
            adjacent = board._neighbors(p)
            for s in adjacent:
                if s not in threatened_stones and board.board[s] == board.current_player:
                    threatened_stones.append(s)
        
        for stone in threatened_stones:
            run_away_move = GoBoardUtil2.generate_run_away_move(board, stone)
            capture_adjacent_stones_moves = GoBoardUtil2.generate_neighbour_captures(board, stone)
            if run_away_move:
                capture_adjacent_stones_moves.append(run_away_move)
            for move in capture_adjacent_stones_moves:
                if move not in all_defense_moves:
                    all_defense_moves.append(move)
        return all_defense_moves
    
    @staticmethod
    def generate_run_away_move(board, stone):
        for n in board.neighbors_dic[stone]:
            if board.board[n] == EMPTY:
                board_copy = board.copy()
                board_copy.move(n, board.current_player)
                num_liberties, atari_point = board._liberty_point(n, board.current_player)
                if num_liberties >= 2:
                    return n
        return None
    
    @staticmethod
    def generate_neighbour_captures(board, stone):
        # determine if the threatened stone's neighbours are the opponent colour
        # if they are, determine if that adjacent stone's block is in atari and which move will capture it
        capture_moves = []
        neighbours = board.neighbors_dic[stone]
        colour = board.current_player
        opponent = GoBoardUtil.opponent(colour)
        for n in neighbours:
            num_liberties, atari_point = board._liberty_point(n, opponent)
            if board.board[n] == opponent and num_liberties == 1:
                if atari_point not in capture_moves:
                    capture_moves.append(atari_point)
        return capture_moves
    
    @staticmethod
    def playGame(board, color, **kwargs):
        komi = kwargs.pop('komi', 0)
        limit = kwargs.pop('limit', 1000)
        random_simulation = kwargs.pop('random_simulation',True)
        use_pattern = kwargs.pop('use_pattern',True)
        check_selfatari = kwargs.pop('check_selfatari',True)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        for _ in range(limit):
            if random_simulation:
                move = GoBoardUtil2.generate_random_move(board,color,True)
            else:
                move = GoBoardUtil2.generate_move_with_filter(board,use_pattern,check_selfatari)
            isLegalMove = board.move(move,color)
            assert isLegalMove
            if board.end_of_game():
                break
            color = GoBoardUtil2.opponent(color)
        winner,_ = board.score(komi)  
        return winner    

    @staticmethod
    def generate_atari_capture_move(board, last_move):
        opponent = GoBoardUtil2.opponent(board.current_player)
        num_liberties, atari_point = board._liberty_point(last_move, opponent)
        if num_liberties == 1 and board.check_legal(atari_point, board.current_player):
            return atari_point
        else:
            return None

    @staticmethod
    def generate_all_policy_moves(board,pattern,check_selfatari):
        """
            generate a list of policy moves on board for board.current_player.
            Use in UI only. For playing, use generate_move_with_filter
            which is more efficient
        """
        last_move = board.last_move
        if last_move != None:
            atari_capture_list =[]
            atari_capture_point = GoBoardUtil2.generate_atari_capture_move(board, last_move)
            if atari_capture_point != None:
                atari_capture_list.append(atari_capture_point)
                atari_capture_list = GoBoardUtil2.filter_moves(board, atari_capture_list, check_selfatari)
                if len(atari_capture_list) > 0:
                    return atari_capture_list, "AtariCapture"
            atari_defense_moves = GoBoardUtil2.generate_all_atari_defense_moves(board, last_move)
            atari_defense_moves = GoBoardUtil2.filter_moves(board, atari_defense_moves, check_selfatari)
            if len(atari_defense_moves) > 0:
                return atari_defense_moves, "AtariDefense"
        return GoBoardUtil.generate_all_policy_moves(board, pattern, check_selfatari)

