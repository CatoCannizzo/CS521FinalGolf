def promptUser(typed:type = None, userPrompt: str = None, aboveX:int = False, ynChoice: bool =False):
    """Returns value from prompted user, optional arg to enforce type return of prompt, and to give specific prompt"""
    
    if userPrompt:
        print(f"{userPrompt}")
    userInput = input()

    if typed is not None:
        try:
            userInput = typed(userInput)
        except ValueError:
            print(f'ValueError: value inputted must be of {typed.__name__} type')
            return promptUser(typed, userPrompt, aboveX, ynChoice) 
        except Exception as e:
            print(f'Unknown Error: {typed(e).__name__} - {e}')
            return promptUser(typed, userPrompt, aboveX, ynChoice)   
        
        if aboveX:
            if not userInput > aboveX:
                print(f'ValueError: value inputted must be greater than {aboveX}')
                return promptUser(typed, userPrompt, aboveX, ynChoice) 
        if ynChoice:
            if  userInput.lower() not in ['y','n']:
                print(f'ValueError: value inputted must be y or n only.')
                return promptUser(typed, userPrompt, aboveX, ynChoice)
    return userInput

