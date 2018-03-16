from board_util import GoBoardUtil

class GoBoardUtil2(GoBoardUtil):
    
    @staticmethod
    def generate_move_with_filter(board, use_pattern, check_selfatari, last_move):
        # last_move is the single point representation of the last move taken
        # needs to be converted to x,y or formatted if necessary
        move = None
        if use_pattern:
            # implement our filters here
            pass
        GoBoardUtil.generate_move_with_filter(board, use_pattern, check_selfatari)
        
    @staticmethod
    def playGame(board, color, **kwargs):
        komi = kwargs.pop('komi', 0)
        limit = kwargs.pop('limit', 1000)
        random_simulation = kwargs.pop('random_simulation',True)
        use_pattern = kwargs.pop('use_pattern',True)
        check_selfatari = kwargs.pop('check_selfatari',True)
        last_move = kwargs.pop('last_move', None)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        for _ in range(limit):
            if random_simulation:
                move = GoBoardUtil2.generate_random_move(board,color,True)
            else:
                move = GoBoardUtil2.generate_move_with_filter(board,use_pattern,check_selfatari,last_move)
            isLegalMove = board.move(move,color)
            assert isLegalMove
            if board.end_of_game():
                break
            color = GoBoardUtil2.opponent(color)
        winner,_ = board.score(komi)  
        return winner    