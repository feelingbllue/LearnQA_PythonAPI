class TestPhraseLength:
    def get_phrase(self):
        phrase = input("Set a phrase: ")
        return phrase

    def test_phrase_length(self):
        phrase = self.get_phrase()
        assert len(phrase) < 15, "The phrase must be shorter than 15 characters"
