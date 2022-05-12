import pyautogui

def automateAction(commnad):
    x,y = pyautogui.position()
    if 'double click' in commnad:
        pyautogui.click(clicks=2)
    elif 'click' in commnad:
        pyautogui.click()
    elif 'press' in commnad:
        action = commnad.replace('press', '')
        actionList =  action.split()
        if len(actionList)==1:
            pyautogui.hotkey(actionList[0])
        elif len(actionList)==2:
            pyautogui.hotkey(actionList[0],actionList[1])
        else:
            pyautogui.hotkey(actionList[0],actionList[1],actionList[2])
    elif 'scroll down' in commnad:
        pyautogui.press('pgdn')
    elif 'scroll up':
        pyautogui.press('pgup')
    elif 'type' in commnad:
        pyautogui.typewrite(commnad.replace('type',''))
    elif 'move right' in commnad:
        x+=10
        pyautogui.move(x,y,0.5)
    elif 'move left' in commnad:
        x-=10
        pyautogui.move(x,y,0.5) 
    elif 'move down' in commnad:
        y+=10
        pyautogui.move(x,y,0.5)
    elif 'move up' in commnad:
        y-=10
        pyautogui.move(x,y,0.5)
    else:
        return 'no command found'
    return 'command performed'