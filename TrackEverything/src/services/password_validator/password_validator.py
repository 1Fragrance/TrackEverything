import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


# Parse every symbol
def get_tokens(inputString):
        tokens = []
        for i in inputString:
            tokens.append(i)
        return tokens

# Verctorizer
vectorizer = TfidfVectorizer(tokenizer=get_tokens)

# Logistic regression classifier
lgs = LogisticRegression(penalty='l2', multi_class='ovr')


class PasswordValidator():
    def teach(self):
        # TODO: Move to config
        filepath = "data_set.csv"
        data = pd.read_csv(filepath, ',', error_bad_lines=False)

        data = pd.DataFrame(data)
        data = data.dropna()

        passwords = np.array(data)

        # Shuffling passwords for increasing chance of predict
        random.shuffle(passwords)  

        # Labels
        y = [d[1] for d in passwords]  

        # Passwords
        allpasswords = [d[0] for d in passwords]  
      
        X = vectorizer.fit_transform(allpasswords)

        # Splitting
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
  
        # Training
        lgs.fit(X_train, y_train)

    def validate_password(self, password):
        raw_password=[password]
        password_vector = vectorizer.transform(raw_password)
        predict = lgs.predict(password_vector)
        print(predict)
        print(raw_password)

        if predict < 1:
            return False
        else: 
            return True
