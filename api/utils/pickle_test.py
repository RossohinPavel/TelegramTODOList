import pickle
import datetime
import sys


test_dct = {
    'func': 'check_user',
    'params': {
        'title': 'abcdefghijklmnopqrstvwuyzabcdefghijklmnopqrstvwuyz',
        'description': 'abcdefghijklmnopqrstvwuyzabcdefghijklmnopqrstvwuyz' * 500,
        'executed': True,
        'actual_on': datetime.datetime.now(datetime.UTC).timestamp(),
        'finish_by': datetime.datetime.now(datetime.UTC).timestamp()
    }
}




p = pickle.dumps(test_dct, pickle.HIGHEST_PROTOCOL)
n = 8192 * 4
nbytes = n.to_bytes(length=2)
print(len(nbytes))
print(nbytes)
print(sys.getsizeof(p))
print(int.from_bytes(nbytes))