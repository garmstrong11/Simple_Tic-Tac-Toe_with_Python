from enum import Enum, unique

@unique
class GameStatus(Enum):
    NOT_FINISHED = 0
    X_WIN = 1
    O_WIN = 2
    DRAW = 3
    IMPOSSIBLE = 4

    def __str__(self):
        match self:
            case GameStatus.NOT_FINISHED:
                return "Game not finished"
            case GameStatus.X_WIN:
                return "X wins"
            case GameStatus.O_WIN:
                return "O wins"
            case GameStatus.DRAW:
                return "Draw"
            case GameStatus.IMPOSSIBLE:
                return "Impossible"
            case _:
                return "Unknown status"


def get_candidate(state: str, char: str) -> set[int]:
    return set([i for i, n in enumerate(state) if n == char])


def get_blank_count(state: str) -> int:
    return len(get_candidate(state, ' '))


def evaluate_game_status(state: str) -> GameStatus:
    blank_count = get_blank_count(state)
    x_candidate = get_candidate(state, 'X')
    o_candidate = get_candidate(state, 'O')

    if abs(len(x_candidate) - len(o_candidate)) > 1:
        return GameStatus.IMPOSSIBLE

    x_win = check_win(x_candidate)
    o_win = check_win(o_candidate)

    if x_win and o_win:
        return GameStatus.IMPOSSIBLE
    elif x_win:
        return GameStatus.X_WIN
    elif o_win:
        return GameStatus.O_WIN

    if blank_count > 0:
        return GameStatus.NOT_FINISHED

    return GameStatus.DRAW


def check_win(candidate: set[int]) -> bool:
    """
    Check a candidate set of indices against
    a list of known sets of winning indices.
    :param candidate: Set of indices to check.
    :return: bool:
        Does this candidate set match a winning set??
    """
    winners = [
        {0, 1, 2},
        {3, 4, 5},
        {6, 7, 8},
        {0, 3, 6},
        {1, 4, 7},
        {2, 5, 8},
        {0, 4, 8},
        {2, 4, 6},
    ]
    # Is any winning set a subset of the candidate?
    return any(winner <= candidate for winner in winners)


def display_game_state(state: str) -> None:
    row_length = 3
    separator = "---------"

    chunks = [' '.join(state[i:i + row_length])
              for i in range(0, len(state), row_length)]

    print(separator)
    for chunk in chunks:
        print(f"| {chunk} |")
    print(separator)


def add_move(state: str, coords: tuple[int, int], char: str) -> str:
    """
    Adds an entry to the game state.
    Throws exceptions for invalid coordinates.
    :param char: The content to add, X or O.
    :param state: The existing string-based state of the game.
    :param coords: One-based coordinates at which to insert a new entry.
    :return: A string representation of the new game state.
    """
    index = flatten_coordinates(coords)
    updated_state = state[:index] + char + state[index + 1:]
    return updated_state


def validate_move(state: str, coords: tuple[str, str]) -> tuple[int, int]:
    row, col = coords
    legal_range = range(1, 4)
    valid_content = ['X', 'O']

    if not row.isdigit() or not col.isdigit():
        raise NonNumericError()

    new_coords = (int(row), int(col))

    if new_coords[0] not in legal_range or new_coords[1] not in legal_range:
        raise CoordinateError()

    index = flatten_coordinates(new_coords)
    if state[index] in valid_content:
        raise OccupiedCellError()

    return new_coords


def flatten_coordinates(coordinates: tuple[int, int]) -> int:
    """
    Transforms one-based coordinates into an integer index
    """
    zeroed = tuple(x - 1 for x in coordinates)
    row, col = zeroed
    return row * 3 + col


def get_player(state: str) -> str:
    play_count = len([x for x in state if x in 'XO'])
    return 'X' if play_count % 2 == 0 else 'O'

class OccupiedCellError(Exception):
    """Exception raised when a grid cell is already occupied"""
    # message = "This cell is occupied! Choose another one!"

    def __init__(self, message="This cell is occupied! Choose another one!"):
        self.message = message
        super().__init__(self.message)


class NonNumericError(TypeError):
    """Exception raised when a non-numeric cell is submitted"""
    # message = None

    def __init__(self, message = "You should enter numbers!"):
        self.message = message
        super().__init__(self.message)


class CoordinateError(ValueError):
    """Exception raised when a coordinate is out of range"""
    # message = None

    def __init__(self, message = "Coordinates should be from 1 to 3!"):
        self.message = message
        super().__init__(self.message)

def main():
    game_state: str = ' ' * 9
    game_status: GameStatus = GameStatus.NOT_FINISHED
    display_game_state(game_state)

    while game_status == GameStatus.NOT_FINISHED:
        try:
            player = get_player(game_state)
            move = input().split()
            move_coords = (move[0], move[1])
            checked_coords = validate_move(game_state, move_coords)
            game_state = add_move(game_state, checked_coords, player)
            display_game_state(game_state)
            game_status = evaluate_game_status(game_state)
        except NonNumericError as e:
            print (e.message)
        except CoordinateError as e:
            print(e.message)
        except OccupiedCellError as e:
            print(e.message)

    print(str(game_status))

if __name__ == '__main__':
    main()