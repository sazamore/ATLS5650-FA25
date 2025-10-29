introduction = "Hello, I want to play a game." #introduction to the game, Jigsaw reference
print(introduction)

playAnswer = input("Are you ready? ").lower() #ask if player is ready, makes input not-case sensitive  
if playAnswer == 'yes':
    print("Good, then let's get started.")
elif playAnswer == 'sure':
    print("Good, then let's get started.")
elif playAnswer == 'no':
    print("That's too bad, but I'm afraid we're going to have to start anyway.")
else:
    print("I don't understand. Either way, we're starting now.")


playerName = input("What should I call you? ") #ask for the player's name
print("Hello, " + playerName + ". I'm pleased you're here.")

gameGuess = input("What kind of game do you think we're going to play? ").lower() #see if player can guess what game is going to be played
if gameGuess == "mad libs":
    print("Correct. Your correct guess bodes well.")
else:
    print("Wrong. This doesn't bode well, but I think you can redeem yourself with some MadLib wit.")


word1 = input("First give me an adjective. ") #inputs of all the words needed for the madlib, in order
word2 = input("Next give me a noun. ")
word3 = input("Next give me a plural noun. ")
word4 = input("Next give me an adjective. ") 
word5 = input("Next give me a verb that ends in a letter s. ")
word6 = input("Next give me a plural noun. ")
word7 = input("Next give me a plural noun. ")
word8 = input("Next give me a noun. ")
word9 = input("Next give me a plural noun. ")
word10 = input("Finally, give me a noun. ")

print("The lights flickered on to reveal a " + word1 + " room filled with puzzles, each locked behind " + word2 + " and " + word3 + "A " + word4 + " voice crackled through a speaker: To Leave, you must solve what " + word5 + "you world. " + playerName + " spotteda wall of " + word6 + " and used their " + word7 + " to sort them by type, revealing a " + word8 + ". The floor creaked open to a tunnel lit by " + word9 + " guiding them towards freedom. As they emerged into daylight, they found a note: You chose " + word10 + " over fear. Well done.")