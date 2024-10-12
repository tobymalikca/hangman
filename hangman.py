import pygame
import random

pygame.init()
pygame.font.init()
text = pygame.font.SysFont('Arial', 30)
screen = pygame.display.set_mode([1200, 800])
inputtedChars = ""
hiddenWord = ""
visibleWord = ""
lives = 10

# 370,100 words
# thanks for the dictionary tanducmai


def parseWord(chosenword): # there's a better way to do this but it works
  alphaonly = ""
  for i in chosenword:
    if i.isalpha():
      alphaonly += i
  return alphaonly


def loadWord():
    global hiddenWord
    with open('words_dictionary.json') as wordfile:
      chosenword = wordfile.readlines()[random.randrange(370100)+1]
    hiddenWord = parseWord(chosenword)
    # reject 11 char or longer words
    if len(hiddenWord) > 10:
      print("Rerolling " + hiddenWord + " - Too long")
      loadWord()

loadWord()


def drawLives():
  livesCount = "Lives: " + str(lives)
  if lives < 3:
    screen.blit(text.render(livesCount, True, (255, 0, 0)), (200, 100))
  elif lives < 6:
    screen.blit(text.render(livesCount, True, (255, 255, 0)), (200, 100))
  else:
    screen.blit(text.render(livesCount, True, (0, 255, 0)), (200, 100))


def drawKey(rowName, keyToDraw, offsetX, offsetY):
  startingOffsetX = 0
  if rowName == "mid":
    startingOffsetX -= 55
  elif rowName == "top":
    startingOffsetX -= 80
  # draw incorrect key red
  if keyToDraw.lower() in inputtedChars and keyToDraw.lower() not in hiddenWord:
    screen.blit(text.render (keyToDraw,
                            True, # anti-aliasing
                            (255, 0, 0)), # red
                            (offsetX * 76 + 280 + startingOffsetX, offsetY + 20, 80, 80)) # positioning
  # draw correct key green
  elif keyToDraw.lower() in inputtedChars and keyToDraw.lower() in hiddenWord:
    screen.blit(text.render (keyToDraw,
                            True, # anti-aliasing
                            (0, 255, 0)), # green
                            (offsetX * 76 + 280 + startingOffsetX, offsetY + 20, 80, 80)) # positioning
  # draw unknown key gray
  else:
    screen.blit(text.render (keyToDraw,
                            True, # anti-aliasing
                            (255, 255, 255)), # white
                            (offsetX * 76 + 280 + startingOffsetX, offsetY + 20, 80, 80)) # positioning
  # draw keyboard borders
  pygame.draw.rect(screen,
                  (150, 150, 150), # gray
                  (offsetX * 76 + 250 + startingOffsetX, offsetY, 80, 80), # positioning
                  5, 0, 0) # borders


def drawKeyboard():
  topkeys = "QWERTYUIOP"
  midkeys = "ASDFGHJKL"
  botkeys = "ZXCVBNM"
  for i in range(len(topkeys)):
    drawKey("top", topkeys[i], i, 550)
  for i in range(len(midkeys)):
    drawKey("mid", midkeys[i], i, 625)
  for i in range(len(botkeys)):
    drawKey("bot", botkeys[i], i, 700)


def drawTiles():
  for i in range(len(hiddenWord)):
    # TODO: make these lines scale with word length
    pygame.draw.rect(screen,
                     (255, 255, 255),
                     (100 * i + 100, 480, 80, 10),
                     0, 0, 0)
    screen.blit(text.render (visibleWord[i].upper(),
                            True, # anti-aliasing
                            (0, 255, 0)), # green
                            (100 * i + 125, 420)) # positioning


def readInput(char):
  global inputtedChars, visibleWord, lives
  # player pressed a repeat char
  if char in inputtedChars:
    return
  # no numbers or special chars
  if not char.isalpha():
    return
  inputtedChars += char
  # we found the char in the hidden word
  if char in hiddenWord:
    # find the indexes of the hidden word to update visibleWord with
    for i in range(len(hiddenWord)):
      if hiddenWord[i] == char:
        visibleWord = visibleWord[:i] + char + visibleWord[i + 1:]
  else:
    lives -= 1


def checkWinOrLoss():
  if hiddenWord == visibleWord:
    screen.blit(text.render ("You win",
                            True, # anti-aliasing
                            (0, 255, 0)), # green
                            (480, 300, 80, 80)) # positioning
    return True
  if lives <= 0:
    screen.blit(text.render ("You lose",
                            True, # anti-aliasing
                            (255, 0, 0)), # red
                            (480, 300, 80, 80)) # positioning
    return True
  return False


# fill visibleWord with spaces on initialization to match the length of hiddenWord
for i in range(len(hiddenWord)):
  visibleWord += " "

def main():
  running = True
  gameEnded = False
  # main loop
  while running:
    screen.fill((0, 0, 0))
    drawTiles()
    drawKeyboard()
    drawLives()
    if checkWinOrLoss():
      gameEnded = True

    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False
        elif not gameEnded:
          try:
            readInput(chr(event.key)) # converts the ascii code to string
          except:
            continue # player pressed shift or something which isn't a char
      if event.type == pygame.QUIT:
        running = False

    pygame.display.flip()

main()
pygame.quit()
