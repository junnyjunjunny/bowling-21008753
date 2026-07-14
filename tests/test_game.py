from src.game import Game


def test_all_gutters_scores_zero():
    game = Game()

    for _ in range(20):
        game.roll(0)

    assert game.score() == 0


def test_all_ones_scores_twenty():
    game = Game()

    for _ in range(20):
        game.roll(1)

    assert game.score() == 20


def test_one_spare_adds_next_roll_as_bonus():
    game = Game()

    game.roll(3)
    game.roll(7)  # 1프레임: 스페어 (3+7=10)
    game.roll(4)  # 보너스 투구 + 2프레임의 첫 투구
    game.roll(0)  # 2프레임의 두 번째 투구

    for _ in range(16):  # 3~10프레임: 전부 거터
        game.roll(0)

    assert game.score() == 18


def test_one_strike_adds_next_two_rolls_as_bonus():
    game = Game()

    game.roll(10)  # 1프레임: 스트라이크
    game.roll(3)   # 2프레임 첫 투구
    game.roll(4)   # 2프레임 두 번째 투구

    for _ in range(16):  # 3~10프레임: 전부 거터
        game.roll(0)

    assert game.score() == 24


def test_perfect_game_scores_three_hundred():
    game = Game()

    for _ in range(12):
        game.roll(10)

    assert game.score() == 300


def test_tenth_frame_spare_gets_one_bonus_roll():
    game = Game()

    for _ in range(18):  # 1~9프레임: 전부 거터
        game.roll(0)

    game.roll(5)
    game.roll(5)  # 10프레임: 스페어
    game.roll(1)  # 보너스 투구 1회

    assert game.score() == 11


def test_tenth_frame_strike_gets_two_bonus_rolls():
    game = Game()

    for _ in range(18):  # 1~9프레임: 전부 거터
        game.roll(0)

    game.roll(10)  # 10프레임: 스트라이크
    game.roll(5)
    game.roll(3)   # 보너스 투구 2회

    assert game.score() == 18
