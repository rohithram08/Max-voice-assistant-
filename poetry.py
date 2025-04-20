import pyttsx3
import random


engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_predefined_poem(theme):
    """Returns a predefined poem based on the theme."""
    poems = {
        "love": [
            "Your love is like a gentle breeze,\nSoftly blowing through the trees.\nA tender touch, a warm embrace,\nYour love fills up the empty space.",
            "In the garden of my heart,\nYou’re the rose, a work of art.\nWith every beat, you make me whole,\nYou are the music of my soul.",
            "Love is a whisper on a summer's night,\nA touch of warmth, a soft, sweet light.\nIt dances in the moon's soft glow,\nA feeling only true hearts know.",
            "Your eyes are stars that light my way,\nYour smile is the sun that brightens my day.\nIn your arms, I find my peace,\nIn your love, all worries cease.",
            "Love is a song that never ends,\nA melody that always mends.\nWith every note, our hearts entwine,\nIn this dance, forever we’ll shine.",
            "With you, my love, the world is bright,\nA canvas painted in pure delight.\nTogether we’ll embrace each dawn,\nOur love, a tale forever drawn.",
            "In your presence, time stands still,\nA love so deep, it’s always real.\nThrough every storm and sunny day,\nWith you, I’ll forever stay.",
            "Love is a journey we embark,\nGuided by a gentle spark.\nThrough every joy and every strife,\nYou are the love of my life.",
            "In the stillness of the night,\nYour love shines like a guiding light.\nA beacon bright, a tender care,\nIn your arms, nothing can compare.",
            "Love is a dance of hearts in tune,\nA serenade beneath the moon.\nWith every step and every sigh,\nWe’ll waltz beneath the starlit sky."
        ],
        "nature": [
            "The trees sway in the gentle breeze,\nLeaves rustle, whispering through the leaves.\nThe sun shines bright, the sky is clear,\nNature’s beauty is always near.",
            "Mountains rise, their peaks so high,\nKissing the clouds in the sky.\nRivers flow, so wild and free,\nNature's wonders for all to see.",
            "In the meadow, flowers bloom,\nBright colors chase away the gloom.\nButterflies dance from petal to petal,\nNature’s song, a sweet, soft kettle.",
            "The ocean waves crash on the shore,\nA symphony of nature’s roar.\nThe salty air, the seagulls' cry,\nNature’s grandeur, reaching the sky.",
            "The forest whispers secrets old,\nIn shades of green, the stories told.\nSunlight filters through the trees,\nNature’s poetry carried on the breeze.",
            "A rainbow arches in the sky,\nColors blend as clouds drift by.\nAfter rain, the world is new,\nNature’s promise, bright and true.",
            "The desert sands stretch far and wide,\nA tranquil place where secrets hide.\nThe sun sets low, the stars ignite,\nNature’s canvas painted bright.",
            "The river’s song flows soft and clear,\nA melody that all can hear.\nThrough valleys deep and forests grand,\nNature's voice, a guiding hand.",
            "The breeze that rustles through the leaves,\nThe chirping songs that morning weaves,\nIn every sound and sight so grand,\nNature’s beauty takes its stand.",
            "The mountain’s peak, the valley’s stream,\nNature’s wonders like a dream.\nIn every sight and every sound,\nNature’s magic can be found."
        ],
        "space": [
            "Stars twinkle in the velvet night,\nGalaxies swirl in cosmic flight.\nThe moon shines with a silver glow,\nSpace is a canvas we’ll never know.",
            "In the vast and endless sea,\nPlanets orbit gracefully.\nThe cosmos hums a silent song,\nA universe where we belong.",
            "The night sky holds a million lights,\nA tapestry of cosmic sights.\nNebulas bloom in colors bright,\nSpace’s wonders fill the night.",
            "The universe, a grand display,\nStars and planets in their ballet.\nA cosmic dance, a wondrous show,\nA mystery that we all know.",
            "Galaxies spiral in the dark,\nA celestial symphony leaves its mark.\nThe stars align in perfect grace,\nA cosmic journey through time and space.",
            "The Milky Way, a starry trail,\nAcross the heavens, bold and frail.\nA streak of light in the night’s embrace,\nA glimpse of the vast, infinite space.",
            "In the cosmos, stars are bright,\nGalaxies spin in the deep of night.\nThe universe, a grand expanse,\nA place of wonder and cosmic dance.",
            "The moon’s pale light, the stars' soft gleam,\nSpace is a realm where we can dream.\nThe planets dance in endless flight,\nA celestial ballet in the night.",
            "The cosmos whispers ancient tales,\nOf distant stars and comet trails.\nA universe vast and full of grace,\nA boundless sea of endless space.",
            "In the expanse where silence reigns,\nStars ignite and the cosmos strains.\nA universe of endless wonder,\nA cosmic realm where dreams can wander."
        ]
    }
    
    # Ensure the theme exists in the dictionary
    if theme not in poems:
        return "Invalid theme selected."

    return random.choice(poems[theme])

def handle_poetry_request():
    """Handles requests for poetry generation."""
    theme = random.choice(["love", "nature", "space"])
    poem = get_predefined_poem(theme)
    
    # Output the poem via both text-to-speech and print
    if "Invalid theme" not in poem:
        print(f"Here's a poem about {theme}:")
        print(poem)
        speak(f"Here's a poem about {theme}: {poem}")
    else:
        print(poem)
        speak(poem)
