"""
Prompts user for input 
By Cato Cannizzo
02/2026
This file just contains a method for getting
user input cleanly with options as args
"""
def promptUser(typed:type = None, 
               userPrompt: str = None, 
               aboveX:int = None,
               underY:int = None, 
               ynChoice: bool =False, 
               inList=[], 
               notList=[]):
    """Returns value from prompted user, optional args to enforce certain traits, ynChoice return Bool"""

    while True:
        # Prints prompt if given
        if userPrompt:
            print(f"{userPrompt}")
        userInput = input()
        # Checks for type enforcement with error calls
        if typed is not None:
            try:
                userInput = typed(userInput)
            except ValueError:
                print(f'ValueError: "\
                      "value inputted must be of {typed.__name__} type')
                continue 
            except Exception as e:
                print(f'Unknown Error: {type(e).__name__} - {e}')
                continue 
        #Checks which noun to use if future len checks fail
        if isinstance(userInput, int):
            lenInput = userInput
            errorNoun = "value"
        else:
            lenInput = len(userInput)
            errorNoun = "length"
            # length checks
            if aboveX is not None and not (lenInput > aboveX):
                    print(f'ValueError: {errorNoun} of'\
                          ' input must be greater than {aboveX}')
                    continue 
            if underY is not None and not (lenInput < underY):
                print(f'ValueError: {errorNoun} of input must be '\
                      'less than {underY}')
                continue
            if ynChoice:
                if  userInput.lower() not in ['y','n']:
                    print(f'ValueError: value inputted must be y or n only.')
                    if userInput.lower() =='y':
                         return True
                    if userInput.lower() == 'n':
                         return False
        #must contain  
        if inList:
            if userInput.lower() not in inList:
                    print(f'ValueError: value inputted must one of {inList}.')
                    continue  
        #can not contain
        if notList:
            if userInput.lower() in notList:
                    print(f'ValueError: value inputted can not contain one of {notList}.')
                    continue   
        return userInput

