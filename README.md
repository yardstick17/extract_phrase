![build-pass](https://travis-ci.org/yardstick17/extract_phrase.svg?branch=master)

#### How to get it:

[![Join the chat at https://gitter.im/yardstick17/extract_phrase](https://badges.gitter.im/yardstick17/extract_phrase.svg)](https://gitter.im/yardstick17/extract_phrase?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
> ###### git clone https://github.com/yardstick17/extract_phrase.git


##### Setup:
> cd to root directory
> ###### bash setup.sh


##### Command to use:
> ###### PYTHONPATH='.' python nlp/main.py --input_file test_input.txt --output_file=test_output.txt




``` shell
> [2017-07-07 08:34:19,275] INFO : Evaluating file: test_input.txt for extracting frequent tags
> [2017-07-07 08:34:19,473] INFO : Got total 87 frequent phrases.
> [2017-07-07 08:34:19,473] INFO : Frequent phrases:[('mushroom duplex', 4), ('bar exchange', 4), ('vapou bar grill', 3), ('list serving great food', 3), ('palak patta chaat', 3)]
> [2017-07-07 08:40:20,486] INFO : Output file: test_output.txt is written with most frequent phrases updated
```
