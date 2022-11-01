"""
A target game:
    - A field of 9 letters is displayed
    - The user has to find words(>=4 chars) that consist of these letters
    - The amount of the same letter in the word mustn't be greater than
        the amount of the same letter in the field
    - The words must contain the middle letter(the fifth one)
"""
import random


def generate_grid() -> list[list[str]]:
    """
    Generate a 3x3 grid of random letters

    Returns
    -------
    list[list[str]]
        The generated grid
    """
    letters = "abcdefghijklmnopqrstuvwxyz"
    grid: list[list] = []
    for i in range(3):
        grid.append([])
        for _ in range(3):
            grid[i].append(random.choice(letters))
    return grid


def get_words(file: str, letters: list) -> tuple:
    """
    Get all possible  words that consist of these letters

    Parameters
    ----------
    file : str
        The file to read the words from
    letters : list
        The letters to use

    Returns
    -------
    list
        The words that consist of these letters
    """
    with open(file, encoding="utf-8") as dictionary:
        words = dictionary.read().splitlines()[3:]
        valid_words = set()
        letter_amounts = _get_letter_amounts(letters)
        middle_letter = letters[4]
        for word in words:
            if len(word) >= 4 and set(word).issubset([i[0] for i in letter_amounts]):
                if (
                    all(
                        word.count(i) <= _find_amount_by_letter(i, letter_amounts)
                        for i in word
                    )
                    and middle_letter in word
                ):
                    valid_words.add(word)
        return tuple(valid_words)


def _get_letter_amounts(letters: list) -> list[tuple]:
    """
    Get the amount of each letter in the letters list

    Parameters
    ----------
    letters : list
        The letters to get the amount of

    Returns
    -------
    list[tuple[]]
        The amount of each letter
    """
    letter_amounts: list[list] = []
    for letter in letters:
        i = 0
        found = False
        while i < len(letter_amounts):
            if letter in letter_amounts[i]:
                letter_amounts[i][1] += 1
                found = True
            i += 1
        if not found:
            letter_amounts.append([letter, 1])
    return [tuple(i) for i in letter_amounts]


def _find_amount_by_letter(letter: str, letter_list: list[tuple]) -> int:
    """
    Find the amount of a letter from a list of tuple

    Parameters
    ----------
    letter : str
        The letter to find the amount of
    letter_list : list[tuple[]]
        The list to find the letter amount in

    Returns
    -------
    int
        The amount of the letter taken from list
    """
    for i in letter_list:
        if i[0] == letter:
            return i[1]
    return 0


def get_user_words():
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish for *nix or Ctrl-Z+Enter
    for Windows.
    Note: the user presses the enter key after entering each word.

    Returns
    -------
    list
        The words entered by the user
    """
    user_words = []
    while True:
        try:
            user_words.append(input("Enter a word: "))
        except EOFError:
            return user_words


def get_pure_user_words(
    user_words: list[str], letters: list[str], words_from_dict: list[str]
) -> list[str]:
    """
    Checks user words with the rules and returns list of those words
    that are not in dictionary.

    Parameters
    ----------
    user_words : list[str]
        The words entered by the user
    letters : list[str]
        The letters to use
    words_from_dict : list[str]
        The words from the dictionary

    Returns
    -------
    list[str]
        The words entered by the user that are not in dictionary
    """
    letter_amounts = _get_letter_amounts(letters)
    middle_letter = letters[4]
    pure_user_words = []
    for word in user_words:
        if (
            len(word) >= 4
            and set(word).issubset([i[0] for i in letter_amounts])
            and all(
                word.count(i) <= _find_amount_by_letter(i, letter_amounts) for i in word
            )
            and middle_letter in word
            and word not in words_from_dict
        ):
            pure_user_words.append(word)
    return pure_user_words


def results(grid: list[list[str]], user_words: list[str], words_from_dict: list[str]) -> None:
    """
    Prints the results of the game

    Parameters
    ----------
    grid : list[list[str]]
        The grid of letters
    user_words : list[str]
        The words entered by the user
    words_from_dict : list[str]
        The words from the dictionary
    """
    print()
    print("Possible words:")
    for i in words_from_dict:
        print(f"  {i}")
    print("User words:")
    for i in user_words:
        print(f"  {i}")
    pure_user_words = get_pure_user_words(
        user_words, [i for j in grid for i in j], words_from_dict
    )
    print("Pure user words:")
    for i in pure_user_words:
        print(f"  {i}")
    print()
    print("Results")
    print("-------")
    print(f"Correct words: {sum(i in words_from_dict for i in user_words)}")
    print("Possible words:")
    for i in words_from_dict:
        print(f"  {i}")
    print("Forgotten words:")
    for i in words_from_dict:
        if i not in user_words:
            print(f"  {i}")
    print("Unknown user words:")
    for i in pure_user_words:
        print(f"  {i}")
