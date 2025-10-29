## Resources for Intro to Programming
### Lab 8 - Pygame & functions
Some features to add to make a game addictive:<br>
    - Simple game design (visuals, goals)<br>
    - Low skill expected compared to performance (easy controls, or game interaction)<br>
    - Unpredictable reinforcement (randomness of difficulty, reward)<br>
    - Collecting items that do not pertain to goal<br>
    - Near-miss events or slowly increasing difficulty<br>
    - Culturally or socially relevants (somethingto talk about)

Lab 8 prompt for Claude: 

<code>Let's vibe code to make a step-by-step tutorial for building a simple, single level game in Python using pygame. Start with simple versions before adding complexity. Do not produce code examples until I expressly request it. Show syntax for coding concepts (such as loops and functions). Do not create objects or use OOP. Use comments in any example code to explain what each section of code does.
Do not include demonstration or code that 
   increase difficulty or frustration in the game
   add pause functionality
   collecting items outside of points to the game
   sound effects
   start or game over screens</code>
   
In the Lab 8 folder, you will find two files:
- **pygame_template.py** - shows the flow and organization for a pygame script. You can download this and give it to Claude to follow this organization, though it should match it pretty closly already.

    **The Flow**:<br>
    *Top Section*: Set up constants and initialize pygame <br>
    *Middle Sections*: Define your variables, classes, and functions <br>
    *Game Loop*: The heart of the game - runs 60 times per second<br>
    *Bottom*: Clean exit

- **function_example.py** - shows how to create functions with no parameter, one parameter and multiple parameters, then how to call each with respective arguments. Use this to help you create extensions for your game
