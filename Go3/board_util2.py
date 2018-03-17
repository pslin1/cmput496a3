from board_util import GoBoardUtil

class GoBoardUtil2(GoBoardUtil):
    
    @staticmethod
    def generate_move_with_filter(board, use_pattern, check_selfatari):
        move = GoBoardUtil2.generate_atari_capture_moves(board, board.last_move)
        if move:
            return move
        move = GoBoardUtil2.generate_atari_defense_move(board, board.last_move, check_selfatari)
        if move:
            return move
        GoBoardUtil.generate_move_with_filter(board, use_pattern, check_selfatari)
        
    @staticmethod
    def generate_atari_defense_move(board, last_move, check_selfatari):
        moves = GoBoardUtil2.generate_all_atari_defense_moves(board, last_move)
        move = GoBoardUtil2.filter_moves_and_generate(board, moves, check_selfatari)   
        return move
    
    @staticmethod
    def generate_all_atari_defense_moves(board, last_move):
        return []
        
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
        if num_liberties == 1:
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
            atari_capture_list.append(atari_capture_point)
            atari_capture_list = GoBoardUtil2.filter_moves(board, atari_capture_list, check_selfatari)
            if atari_capture_list != None:
                return atari_capture_point, "Atari Capture"
            atari_defense_moves = GoBoardUtil2.generate_all_atari_defense_moves(board, last_move)
            atari_defense_moves = GoBoardUtil2.filter_moves(board, atart_defense_moves, check_selfatari)
            if len(atari_defense_moves) > 0:
                return atari_defense_moves, "AtariDefense"
        if pattern:
            pattern_moves = []
            pattern_moves = GoBoardUtil2.generate_pattern_moves(board)
            pattern_moves = GoBoardUtil2.filter_moves(board, pattern_moves, check_selfatari)
            if len(pattern_moves) > 0:
                return pattern_moves, "Pattern"
        return GoBoardUtil.generate_random_moves(board,True), "Random"