def promptUser(typed:type = None, userPrompt: str = None, aboveX:int = False, lowered:bool = False, ynChoice: bool =False):
    """Returns value from prompted user, optional arg to enforce type return of prompt, and to give specific prompt"""
    
    if userPrompt:
        print(f"{userPrompt}")
    userInput = input()

    if typed is not None:
        try:
            userInput = typed(userInput)
        except ValueError:
            print(f'ValueError: value inputted must be of {typed.__name__} type')
            return promptUser(typed, userInput, aboveX, lowered, ynChoice) 
        except Exception as e:
            print(f'Unknown Error: {typed(e).__name__} - {e}')
            return promptUser(typed, userInput, aboveX, lowered, ynChoice)   
        
        if aboveX:
            if not userInput > aboveX:
                print(f'ValueError: value inputted must be greater than {aboveX}')
                return promptUser(typed, userInput, aboveX, lowered, ynChoice) 
        if typed == str:
            if lowered:
                userInput = userInput.lower()
        if ynChoice:
            if not userInput.lower() == 'y' | 'n':
                return promptUser(typed, userInput, aboveX, lowered, ynChoice)
    return userInput