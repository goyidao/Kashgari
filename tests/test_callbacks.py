# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: test_utils.py
# time: 14:46
import os
import unittest
from kashgari import callbacks
from kashgari.tasks.classification import BLSTMModel
from kashgari.tasks.labeling import BiLSTM_Model as Labeling_BiLSTM_Model
from kashgari.corpus import ChineseDailyNerCorpus, SMP2018ECDTCorpus


class TestCallbacks(unittest.TestCase):

    def test_labeling_eval_callback(self):
        train_x, train_y = ChineseDailyNerCorpus.load_data()
        test_x, test_y = ChineseDailyNerCorpus.load_data('test')

        train_x = train_x[:1000]
        train_y = train_y[:1000]
        model = Labeling_BiLSTM_Model()
        eval_callback = callbacks.EvalCallBack(model, test_x, test_y, step=1)
        model.fit(train_x, train_y, callbacks=[eval_callback], epochs=1)

    def test_classification_eval_callback(self):
        train_x, train_y = SMP2018ECDTCorpus.load_data()
        test_x, test_y = SMP2018ECDTCorpus.load_data('test')

        train_x = train_x[:1000]
        train_y = train_y[:1000]
        model = BLSTMModel()
        eval_callback = callbacks.EvalCallBack(model, test_x, test_y, step=1)
        model.fit(train_x, train_y, callbacks=[eval_callback], epochs=1)

    def test_classification_checkpoint_callback(self):
        train_x, train_y = SMP2018ECDTCorpus.load_data()
        test_x, test_y = SMP2018ECDTCorpus.load_data('test')

        train_x = train_x[:1000]
        train_y = train_y[:1000]
        model = BLSTMModel()
        model_path = os.path.join('model_saved', 'test_classification_checkpoint')
        checkpoint = callbacks.KashgariModelCheckpoint(model_path,
                                                       verbose=1,
                                                       save_best_only=True,
                                                       save_weights_only=False,
                                                       kash_model=model)
        model.fit(train_x, train_y, test_x, test_y, epochs=2, callbacks=[checkpoint])
        model.evaluate(train_x, train_y, 64)

        # load and predict
        from kashgari import utils
        new_model = utils.load_model(model_path)
        print(new_model.predict(train_x[:10]))
        print(new_model.predict_top_k_class(train_x[:10]))

        # load and train
        new_model = utils.load_model(model_path)
        new_model.compile_model()
        checkpoint = callbacks.KashgariModelCheckpoint(model_path,
                                                       verbose=1,
                                                       save_best_only=True,
                                                       save_weights_only=False,
                                                       kash_model=new_model)
        new_model.fit(train_x, train_y, test_x, test_y, epochs=2, callbacks=[checkpoint])
        new_model.evaluate(train_x, train_y, 64)

    def test_labeling_checkpoint_callback(self):
        train_x, train_y = ChineseDailyNerCorpus.load_data()
        test_x, test_y = ChineseDailyNerCorpus.load_data('test')

        train_x = train_x[:1000]
        train_y = train_y[:1000]
        model_path = os.path.join('model_saved', 'test_labelling_checkpoint')
        model = Labeling_BiLSTM_Model()
        checkpoint = callbacks.KashgariModelCheckpoint(model_path,
                                                       verbose=1,
                                                       save_best_only=True,
                                                       save_weights_only=False,
                                                       kash_model=model)
        model.fit(train_x, train_y, test_x, test_y, epochs=2, callbacks=[checkpoint])
        model.evaluate(train_x, train_y, 64)

        # load and predict
        from kashgari import utils
        new_model = utils.load_model(model_path)
        print(new_model.predict(train_x[:10]))

        # load and train
        new_model = utils.load_model(model_path)
        new_model.compile_model()
        checkpoint = callbacks.KashgariModelCheckpoint(model_path,
                                                       verbose=1,
                                                       save_best_only=True,
                                                       save_weights_only=False,
                                                       kash_model=new_model)
        new_model.fit(train_x, train_y, test_x, test_y, epochs=2, callbacks=[checkpoint])
        new_model.evaluate(train_x, train_y, 64)


if __name__ == "__main__":
    print("hello, world")
