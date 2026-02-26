"""
Prompts user for input 
By Cato Cannizzo
02/2026
This file just contains a method for getting
user input cleanly with options as args
"""
def prompt_user(typed:type = None, 
               user_prompt: str = None, 
               aboveX:int = None,
               underY:int = None, 
               ynChoice: bool =False, 
               in_list=None, 
               not_list=None):
    """Returns value from prompted user, optional args to enforce certain traits, ynChoice return Bool"""


    while True:
        # Prints prompt if given
        if user_prompt:
            print(f"{user_prompt}")
        user_input = input()

        # Checks for type enforcement with error calls
        if typed is not None:
            try:
                user_input = typed(user_input)
            except ValueError:
                print("ValueError: value inputted"\
                      f" must be of {typed.__name__} type")
                continue 
            except Exception as e:
                print(f'Unknown Error: {type(e).__name__} - {e}')
                continue 

        #Checks which noun to use if future len checks fail
        if isinstance(user_input, int):
            len_input = user_input
            error_noun = "value"
        else:
            len_input = len(user_input)
            error_noun = "length"
            # length checks
            if aboveX is not None and not (len_input > aboveX):
                    print(f'ValueError: {error_noun} of'\
                          f' input must be greater than {aboveX}')
                    continue 
            if underY is not None and not (len_input < underY):
                print(f'ValueError: {error_noun} of input must be '\
                      f'less than {underY}')
                continue

        if isinstance(user_input, str):
            check = user_input.lower()

        if ynChoice:
            if  check not in ['y','n']:
                print(f'ValueError: value inputted must be y or n only.')
                continue
            if check =='y':
                    return True
            if check == 'n':
                    return False
                
        #must contain  
        if in_list:
            if check not in in_list:
                    print(f'ValueError: value inputted must one of {in_list}.')
                    continue  
        #can not contain
        if not_list:
            if check in not_list:
                    print(f'ValueError: value inputted can not contain one of {not_list}.')
                    continue   
        return user_input