class Model:
    def __init__(self):
        print('Model init')

class ExtendedModel(Model):
    def __init__(self):
        print('ExtendedModel init')
        super(ExtendedModel, self).__init__()

exxx = ExtendedModel()
