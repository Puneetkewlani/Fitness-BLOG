import re

with open('exercise.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix border-left- (135deg
text = text.replace('style="border-left- (135deg', 'style="background: linear-gradient(135deg')

# Fix (135deg
text = text.replace('style="(135deg', 'style="background: linear-gradient(135deg')

# Fix border-left-
text = text.replace('style="border-left-"', '')

with open('exercise.html', 'w', encoding='utf-8') as f:
    f.write(text)
