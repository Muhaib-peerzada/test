#import streamlit as st
#import random
#import numpy as np
#from datetime import datetime
#import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="For My Bebe 💖 Made with Love",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling - simplified
st.markdown("""
<style>
    .main { background-color: #fff0f5; }
    .stButton > button {
        background-color: #ff6b88;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .love-title {
        color: #ff1493;
        text-align: center;
        font-size: 3em;
        font-family: 'Brush Script MT', cursive;
        margin-bottom: 20px;
    }
    .love-message {
        color: #ff1493;
        text-align: center;
        font-family: 'Comic Sans MS', cursive;
        padding: 20px;
        border-radius: 15px;
        background-color: rgba(255, 182, 193, 0.3);
        margin: 10px 0;
    }
    .game-section {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    .hearts {
        font-size: 24px;
        color: #ff1493;
        text-align: center;
        margin: 10px 0;
    }
    /* Improved Snake Game UI */
    .snake-grid {
        display: grid;
        grid-template-columns: repeat(10, 30px);
        grid-gap: 2px;
        margin: 0 auto;
        width: fit-content;
    }
    .snake-cell {
        width: 30px;
        height: 30px;
        border-radius: 4px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Define love messages
love_messages = [
    "My heart beats only for you, bebe! 💓",
    "Every moment with you feels like a beautiful dream! 💭",
    "Your smile lights up my entire world, bebe! ✨",
    "I fall in love with you more each day! 💘",
    "You're my sunshine on cloudy days! ☀️",
    "Loving you is as natural as breathing! 💖",
    "You're the sweetest chapter in my story! 📖",
    "I cherish every second we spend together! ⏱️",
    "Your love is the greatest gift I've ever received! 🎁",
    "My heart belongs to you, bebe! 💝"
]

# App title and header
st.markdown("<div class='love-title'>For My Bebe 💖</div>", unsafe_allow_html=True)
st.markdown("<div class='hearts'>💕 💖 💓 💗 💘 💝 💕</div>", unsafe_allow_html=True)

# Initialize session state
if 'tab' not in st.session_state:
    st.session_state.tab = "Love Messages"

# Initialize game states
if 'tic_tac_toe_board' not in st.session_state:
    st.session_state.tic_tac_toe_board = [' ' for _ in range(9)]
    st.session_state.tic_tac_toe_turn = 'X'
    st.session_state.tic_tac_toe_winner = None
    st.session_state.tic_tac_toe_game_over = False

if 'snake_game' not in st.session_state:
    st.session_state.snake_game = {
        'snake': [(5, 5)],
        'food': (7, 7),
        'direction': 'RIGHT',
        'score': 0,
        'game_over': False,
        'grid_size': 10
    }

if 'memory_game' not in st.session_state:
    emojis = ['❤️', '💕', '💖', '💗', '💓', '💘', '💝', '💞']
    memory_cards = emojis + emojis
    random.shuffle(memory_cards)
    st.session_state.memory_game = {
        'cards': memory_cards,
        'flipped': [False] * 16,
        'matched': [False] * 16,
        'first_card': None,
        'matches': 0,
        'moves': 0
    }

if 'word_to_guess' not in st.session_state:
    love_words = ["kisses", "cuddles", "forever", "soulmate", "darling", "treasure", "angel", "sweetheart"]
    st.session_state.word_to_guess = random.choice(love_words)
    st.session_state.guessed_letters = []
    st.session_state.attempts = 5

# Calculate days together
def days_together():
    # Placeholder date - replace with your actual anniversary date
    anniversary = datetime(2023, 1, 1)  # Year, Month, Day
    today = datetime.now()
    days = (today - anniversary).days
    return days

# Game logic functions
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] != ' ' and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    
    if ' ' not in board:
        return 'Tie'
    
    return None

def ai_move():
    empty_spots = [i for i, spot in enumerate(st.session_state.tic_tac_toe_board) if spot == ' ']
    if empty_spots:
        return random.choice(empty_spots)
    return None

def move_snake():
    head_x, head_y = st.session_state.snake_game['snake'][0]
    
    if st.session_state.snake_game['direction'] == 'UP':
        new_head = (head_x, head_y - 1)
    elif st.session_state.snake_game['direction'] == 'DOWN':
        new_head = (head_x, head_y + 1)
    elif st.session_state.snake_game['direction'] == 'LEFT':
        new_head = (head_x - 1, head_y)
    else:  # RIGHT
        new_head = (head_x + 1, head_y)
    
    # Check for collision
    grid_size = st.session_state.snake_game['grid_size']
    if (new_head[0] < 0 or new_head[0] >= grid_size or 
        new_head[1] < 0 or new_head[1] >= grid_size or
        new_head in st.session_state.snake_game['snake']):
        st.session_state.snake_game['game_over'] = True
        return
    
    # Check for food
    if new_head == st.session_state.snake_game['food']:
        st.session_state.snake_game['score'] += 1
        st.session_state.snake_game['snake'].insert(0, new_head)
        # Generate new food
        while True:
            food = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
            if food not in st.session_state.snake_game['snake']:
                st.session_state.snake_game['food'] = food
                break
    else:
        st.session_state.snake_game['snake'].insert(0, new_head)
        st.session_state.snake_game['snake'].pop()

# Navigation tabs using buttons for better UX
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Love Messages"):
        st.session_state.tab = "Love Messages"
with col2:
    if st.button("Mini Games"):
        st.session_state.tab = "Mini Games"
with col3:
    if st.button("2D Games"):
        st.session_state.tab = "2D Games"
with col4:
    if st.button("Special Moments"):
        st.session_state.tab = "Special Moments"
st.markdown("</div>", unsafe_allow_html=True)

# Content based on selected tab
if st.session_state.tab == "Love Messages":
    st.markdown("<h2 style='text-align: center; color: #ff1493;'>Love Notes from Mubashir</h2>", unsafe_allow_html=True)
    
    # Random love message generator
    st.markdown("<div class='game-section'>", unsafe_allow_html=True)
    st.subheader("Get a Love Note 💌")
    if st.button("Show me how much you love me!"):
        message = random.choice(love_messages)
        st.markdown(f"<div class='love-message'>{message}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Days together counter
    st.markdown("<div class='game-section'>", unsafe_allow_html=True)
    st.subheader("Our Journey Together 🗓️")
    st.markdown(f"<div class='love-message'>We've been in love for {days_together()} wonderful days, bebe!</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Custom message
    st.markdown("<div class='game-section'>", unsafe_allow_html=True)
    st.subheader("A Special Message For You Today 💫")
    st.markdown("<div class='love-message'>My beautiful bebe, you are the reason for my smile every day. Your love makes my life complete, and I promise to cherish you forever. - Mubashir</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.tab == "Mini Games":
    st.markdown("<h2 style='text-align: center; color: #ff1493;'>Fun & Games</h2>", unsafe_allow_html=True)
    
    # Love compatibility game
    st.markdown("<div class='game-section'>", unsafe_allow_html=True)
    st.subheader("Love Compatibility Test 💘")
    if st.button("Check our compatibility"):
        compatibility = random.randint(95, 100)
        st.markdown(f"<div class='love-message'> Our love compatibility: {compatibility}%! Perfect match! 💯</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Love fortune teller
    st.markdown("<div class='game-section'>", unsafe_allow_html=True)
    st.subheader("Love Fortune Teller 🔮")
    if st.button("Tell our fortune"):
        fortunes = [
            "You will Marry very soon!",
            "Your love will grow stronger with each passing day!",
            "A romantic surprise is coming your way!",
            "Your bond is unbreakable and will last forever!",
            "You'll create beautiful memories together this week!"
        ]
        fortune = random.choice(fortunes)
        st.markdown(f"<div class='love-message'>{fortune}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Guess the word game
    st.markdown("<div class='game-section'>", unsafe_allow_html=True)
    st.subheader("Guess the Love Word 💝")
    
    # Display current state of word
    display_word = ""
    for letter in st.session_state.word_to_guess:
        if letter in st.session_state.guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    
    st.markdown(f"<div class='love-message' style='font-size: 24px; letter-spacing: 3px;'>{display_word}</div>", unsafe_allow_html=True)
    st.write(f"Attempts left: {st.session_state.attempts}")
    
    # Input for guessing
    guess = st.text_input("Guess a letter:", max_chars=1).lower()
    
    if st.button("Submit Guess"):
        if guess:
            if guess in st.session_state.guessed_letters:
                st.warning("You already guessed that letter!")
            elif guess in st.session_state.word_to_guess:
                st.session_state.guessed_letters.append(guess)
                st.success("Good guess, bebe! 💕")
            else:
                st.session_state.guessed_letters.append(guess)
                st.session_state.attempts -= 1
                st.error("Try again, my love! 💋")
            
            # Check if won
            won = all(letter in st.session_state.guessed_letters for letter in st.session_state.word_to_guess)
            if won:
                st.balloons()
                st.markdown("<div class='love-message' style='font-size: 20px;'>You won, my clever bebe! I love you! 💖</div>", unsafe_allow_html=True)
            
            # Check if lost
            if st.session_state.attempts <= 0:
                st.markdown(f"<div class='love-message'>Game over! The word was '{st.session_state.word_to_guess}'. But you're still my winner! 💖</div>", unsafe_allow_html=True)
    
    if st.button("Reset Word Game"):
        st.session_state.word_to_guess = random.choice(love_words)
        st.session_state.guessed_letters = []
        st.session_state.attempts = 5
        st.experimental_rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.tab == "2D Games":
    st.markdown("<h2 style='text-align: center; color: #ff1493;'>2D Games</h2>", unsafe_allow_html=True)
    
    game_choice = st.selectbox("Choose a game to play with Naemah:", 
                               ["Tic Tac Toe ⭕❌", "Snake Game 🐍"])
    
    if game_choice == "Tic Tac Toe ⭕❌":
        st.markdown("<div class='game-section'>", unsafe_allow_html=True)
        st.subheader("Tic Tac Toe - Play with Bebe!")
        
        # Display the game board
        cols = st.columns(3)
        for i in range(3):
            for j in range(3):
                cell_index = i * 3 + j
                with cols[j]:
                    if st.session_state.tic_tac_toe_board[cell_index] == ' ' and not st.session_state.tic_tac_toe_game_over:
                        if st.button(f"   ", key=f"ttt_{cell_index}"):
                            if st.session_state.tic_tac_toe_turn == 'X':
                                st.session_state.tic_tac_toe_board[cell_index] = 'X'
                                st.session_state.tic_tac_toe_winner = check_winner(st.session_state.tic_tac_toe_board)
                                
                                if st.session_state.tic_tac_toe_winner is None:
                                    st.session_state.tic_tac_toe_turn = 'O'
                                    # AI move
                                    ai_cell = ai_move()
                                    if ai_cell is not None:
                                        st.session_state.tic_tac_toe_board[ai_cell] = 'O'
                                        st.session_state.tic_tac_toe_winner = check_winner(st.session_state.tic_tac_toe_board)
                                        st.session_state.tic_tac_toe_turn = 'X'
                            
                            st.experimental_rerun()
                    else:
                        st.button(f" {st.session_state.tic_tac_toe_board[cell_index]} ", key=f"ttt_display_{cell_index}", disabled=True)
        
        # Display game status
        if st.session_state.tic_tac_toe_winner == 'X':
            st.success("You won! Bebe loves a winner! 💕")
            st.session_state.tic_tac_toe_game_over = True
        elif st.session_state.tic_tac_toe_winner == 'O':
            st.error("Bebe won this time! Better luck next round! 💋")
            st.session_state.tic_tac_toe_game_over = True
        elif st.session_state.tic_tac_toe_winner == 'Tie':
            st.info("It's a tie! Your love is always balanced! ❤️")
            st.session_state.tic_tac_toe_game_over = True
        
        # Reset button
        if st.button("Reset Tic Tac Toe"):
            st.session_state.tic_tac_toe_board = [' ' for _ in range(9)]
            st.session_state.tic_tac_toe_turn = 'X'
            st.session_state.tic_tac_toe_winner = None
            st.session_state.tic_tac_toe_game_over = False
            st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif game_choice == "Snake Game 🐍":
        st.markdown("<div class='game-section'>", unsafe_allow_html=True)
        st.subheader("Snake Game - Collect Hearts!")
        
        # Improved game controls - using a single row
        cols = st.columns([1,1,1,1,1])
        with cols[1]:
            if st.button("⬆️", key="up"):
                if st.session_state.snake_game['direction'] != 'DOWN':
                    st.session_state.snake_game['direction'] = 'UP'
        with cols[0]:
            if st.button("⬅️", key="left"):
                if st.session_state.snake_game['direction'] != 'RIGHT':
                    st.session_state.snake_game['direction'] = 'LEFT'
        with cols[2]:
            if st.button("➡️", key="right"):
                if st.session_state.snake_game['direction'] != 'LEFT':
                    st.session_state.snake_game['direction'] = 'RIGHT'
        with cols[1]:
            if st.button("⬇️", key="down"):
                if st.session_state.snake_game['direction'] != 'UP':
                    st.session_state.snake_game['direction'] = 'DOWN'
        
        # Move snake
        if not st.session_state.snake_game['game_over']:
            move_snake()
        
        # Display game board with improved grid
        grid_size = st.session_state.snake_game['grid_size']
        
        # Create CSS grid
        st.markdown("<div class='snake-grid'>", unsafe_allow_html=True)
        for y in range(grid_size):
            for x in range(grid_size):
                cell = "⬜"  # Empty cell
                
                # Place food
                food_x, food_y = st.session_state.snake_game['food']
                if (x, y) == (food_x, food_y):
                    cell = "❤️"
                
                # Place snake
                for i, (snake_x, snake_y) in enumerate(st.session_state.snake_game['snake']):
                    if (x, y) == (snake_x, snake_y):
                        if i == 0:  # Head
                            cell = "🟢"
                        else:  # Body
                            cell = "🟩"
                
                st.markdown(f"<div class='snake-cell'>{cell}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display score
        st.write(f"Score: {st.session_state.snake_game['score']} hearts collected for Naemah!")
        
        # Game over state
        if st.session_state.snake_game['game_over']:
            st.error("Game Over! Your love was too strong! 💘")
            if st.button("Restart Snake Game"):
                st.session_state.snake_game = {
                    'snake': [(5, 5)],
                    'food': (7, 7),
                    'direction': 'RIGHT',
                    'score': 0,
                    'game_over': False,
                    'grid_size': 10
                }
                st.experimental_rerun()
        
        # Advance game button
        if st.button("Advance Game"):
            st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.tab == "Special Moments":
    st.markdown("<h2 style='text-align: center; color: #ff1493;'>Our Special Moments</h2>", unsafe_allow_html=True)
    
    # Favorite memories
    st.markdown("<div class='game-section'>", unsafe_allow_html=True)
    st.subheader("My Favorite Memories With You 💭")
    memories = [
        "Our first date when you looked so beautiful I could barely speak",
        "That time we stayed up all night just talking and laughing",
        "When you held my hand for the first time and my heart skipped a beat",
        "Our first kiss that felt like time stood still",
        "When we watched the sunset together and I knew I wanted to spend forever with you"
    ]
    
    for i, memory in enumerate(memories, 1):
        st.markdown(f"<div class='love-message'>{i}. {memory}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Love poem
    st.markdown("<div class='game-section'>", unsafe_allow_html=True)
    st.subheader("A Poem For My Bebe 📝")
    poem = """
    My dearest, my beautiful bebe,
    Your love is a treasure, the greatest gift to me.
    Your smile brightens my days, your touch calms my nights,
    In your eyes I find home, in your arms pure delight.
    
    No words can express how much you mean to me,
    You're my present, my future, my sweet destiny.
    Forever and always, I promise to be true,
    My heart belongs to you, bebe, I'll always love you.
    
    - Mubashir
    """
    st.markdown(f"<div class='love-message' style='white-space: pre-line;'>{poem}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='hearts'>💕 💖 💓 💗 💘 💝 💕</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff1493; margin-top: 30px;'>Made with love by Mubashir for his bebe 💖</p>", unsafe_allow_html=True)
